# Behavioral benchmark

Measures whether a template version makes an agent faster without losing quality. It runs the same tasks on the same project with each version and compares the results.

**Run it only when the maintainer explicitly asks for it.** It spends model usage and takes minutes, so agents never start it on their own, as a validation step, or as part of a release.

## How it works

- **Fixture** (`fixture/`): a small Vite + React + TypeScript shop with Vitest (9 tests), Playwright (18 tests tagged `@catalog` and `@cart`), ESLint, and `@lhci/cli`, installed with pnpm from a committed lockfile. The production build carries a fixed 8 s cost, so runs that pay for a build cost what they would in a real project. Problems are seeded for the tasks: a UI typo, a cart total that ignores quantity, no way to remove items, and a price formatter shared across modules.
- **Tasks** (`tasks/<id>/task.json`): each has a prompt, a canned answer used if the agent asks questions, and hidden acceptance tests the agent never sees.
  - `t1-typo` (trivial): fix a UI typo that existing tests also contain.
  - `t2-total` (small): fix a bug test-first.
  - `t3-remove` (medium, ambiguous): the canned answer contradicts the natural default, so an agent that does not ask fails the hidden test.
  - `t4-currency` (small, scope trap): the formatter lives in `cart` but `catalog` uses it, so `@catalog` specs break without any catalog file changing. Selecting E2E specs only by the touched module's tag misses them.
- **Rendering** (`render.py`): fills the template at a git ref (or the working tree) deterministically, with the values in `versions.json`. A benchmark therefore measures the rules, not the variance of an agent applying them. Each version also gets the Playwright config its stack file prescribes (`variants/`).
- **Running** (`run.py`): the versions of each (task, repetition) are submitted together and pairs run concurrently (`--jobs`, default 6), on APFS clones of one installed fixture, so CPU contention is symmetric between versions. Each run calls `claude -p` headless with the same model, no MCP servers, and no user settings. If the agent finishes without changing files, it asked something: the runner answers with the canned answer (up to 2 rounds) and counts the round trip.
- **Quality**: after the agent finishes, the runner (not the agent) adds the hidden tests and runs, in parallel, one Vitest pass, one Playwright pass against a production build (JSON reporters split visible from hidden results), typecheck, and lint.
- **Report** (`report.py`): writes `results/<stamp>/REPORT.md` with a summary per version and a table by task and version.

## Metrics

| Metric | Source | Better |
| --- | --- | --- |
| Hidden acceptance tests passed | Runner, after the agent | Higher |
| All suites green (unit, E2E, typecheck, lint) | Runner | Higher |
| Test-first, and red test seen before the fix | Transcript order: test file edited, a test run, then source edited | Higher |
| Wall time, cost, turns, tokens | `claude -p` result events and the runner clock | Lower |
| Time inside checks | Each event is timestamped on arrival; a check lasts from its tool call to its result | Lower |
| Unit and E2E tests executed | Vitest and Playwright summaries in the tool output | Lower, with quality unchanged |
| Question rounds | Runs that ended without changes and needed the canned answer | Lower, unless the task is ambiguous |
| Focused versus full unit and E2E runs, production builds paid | Shell commands in the transcript | Fewer full runs and builds |
| Full E2E suite runs | Same | 0: every version forbids it without a request |
| Repeated file reads with no edit in between | `Read` calls and `cat`/`head`/`tail`/`sed -n` in the transcript | Lower |
| Failed tool calls | Tool results flagged as errors in the transcript, excluding test runs (a red test is expected) | Lower |
| Files edited more than twice | Edits per file in the transcript | Lower: churn means the agent is iterating on the same file instead of landing the change |

A version is better only if speed improves and quality stays equal or better. Faster with lower quality is a regression.

## Run it

```bash
python3 bench/run.py                          # all tasks, v1.4.0 vs v1.7.0 (working tree), 5 repetitions, Sonnet, 6 runs at a time
python3 bench/run.py --reps 5 --model opus    # more repetitions for less noise
python3 bench/run.py --tasks t2-total --versions 1.7.0
python3 bench/run.py --rescore bench/results/<stamp>   # recompute metrics from saved transcripts
python3 bench/report.py                       # rebuild the latest REPORT.md
```

Requirements: `claude` CLI logged in, pnpm, Node 24 (the runner refuses to start on an older Node, because Vitest 5 then runs no tests and every unit result reads as failed), and Playwright's Chromium installed. Runs execute with `--dangerously-skip-permissions` inside throwaway workspaces under the system temp directory (`--workdir` to change it). Each run also leaves a session in `~/.claude/projects/`.

To add a version, add it to `versions.json` with its git ref (or `WORKTREE`), its Playwright variant, and the variables it introduced.

## Limits

- Agent runs vary: with 5 repetitions, a difference under about 20% in time or cost is noise. Before calling a quality regression confirmed on `t3-remove` or `t4-currency`, run those tasks with `--reps 8`.
- One stack (Vite + React) and four tasks. Next.js server-side behavior, Angular, Codex, and the multi-agent policy (no task is large enough to justify delegation) are not exercised yet.
- Test-first detection reads the order of edits and test runs in the transcript, including `sed -i` and heredoc scripts that write files; an edit made some other way can be missed.
