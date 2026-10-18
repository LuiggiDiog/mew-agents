# Changelog

## 1.7.0 — 2026-10-18

Driven by the six-version benchmark (`bench/results/20261018-1500`): 1.6.1 kept quality but was 30% slower than 1.4.0, because Lighthouse ran for small UI changes and level 2 E2E paid a production build for text and service changes; the ambiguous task was asked about in 3 of 5 runs against 5 of 5 on 1.3.0 and 1.4.0 with the same rule, in a file 30% longer.

- `validation`: level 2 E2E runs against the dev server; the production build is paid only when the change can behave differently in production (routes or lazy chunks, build configuration, dependencies, assets, environment variables, server rendering). `lighthouse` runs only when the change can move a score (routes, `index.html` or the document head, assets, client dependencies, build configuration, first-screen layout), never for a text, control, component, service, test, or documentation change.
- `e2e` and all docs: E2E runs only against local or test environments (local, dev, staging), never against production. The `e2e-prod` command is now `e2e-build` and its switch `E2E_BUILD`, to say what it is: a local production build that Playwright builds and serves.
- `lighthouse` runs the installed `@lhci/cli` (`{{EXEC:lhci autorun}}`) instead of downloading it on every run through `dlx`; `APPLY.md` adds the dev dependency when tooling is installed, or lists it as a follow-up. The `web-performance` skill falls back to `dlx` once when it is missing.
- `requirements`: a question is open only when the answer changes what the user sees or the scope; details that patterns or an obvious default settle are assumed and stated in the report.
- `tdd`: the failing test runs before any source file is touched, also when the edit is a `sed` or a script that writes tests and source together.
- `AGENTS.md` trimmed from 272 to about 215 rendered lines (3568 to about 3330 words): the Lighthouse checklist and `{{STACK:performance}}` moved to the `web-performance` skill, E2E detail stays in `docs/e2e-playbook.md`, the package-manager table became one line, and `architecture`, `working-style`, `documentation`, `tdd`, and `orchestration` say the same in fewer lines. Path-scoped rules were considered and not adopted: Codex loads nested `AGENTS.md` by working directory, not by touched file, so a split would leave Codex without the rules.
- New command guard (`.agents/hooks/guard.mjs`), run as a `PreToolUse` hook on shell commands by Claude Code (`hooks` in `.claude/settings.json`) and Codex (`[[hooks.PreToolUse]]` in `.codex/config.toml`), which share the hook JSON and the exit-code-2 deny. It blocks a full unit or E2E suite unless the command carries `FULL_SUITE=1`, so an explicit request leaves a visible mark, and an E2E base URL whose host is not local, dev, staging, test, QA, preview, or sandbox. Heredoc bodies are ignored. Following Anthropic's guidance that instructions are not guardrails and a real guardrail is deterministic; `AGENTS.md` keeps the rules, the hook enforces two of them.
- New `affected` command (`.agents/scripts/affected-tests.mjs`): lists the unit tests the runner relates to the change (new `{{CMD_TEST_LIST_CHANGED}}`, `vitest list --filesOnly --changed=<base>`; `n/a` for Karma), the specs Playwright relates to it (`--only-changed`), the specs tagged with each touched module, the source files whose module has no tag, and the level 2 commands to run. `validation` now says to run it instead of describing the union by hand; the mechanics stay in `docs/e2e-playbook.md`. Following the TDAD finding that surfacing which tests cover the change beats prescribing the procedure.
- `lighthouserc.json`: every assertion now aggregates with `median`; without it Lighthouse CI defaults to `optimistic`, the run most likely to pass, so the 3 runs did not give the median the docs promised. Numeric budgets added next to the category scores: LCP 2500 ms, CLS 0.1, TBT 200 ms (the lab proxy for INP). The `performance` block and the `web-performance` skill state them, and `lighthouse-audits.mjs` prints the three metrics per route.
- `APPLY.md`: optional `/doctor prompt-audit` in the verify step (Claude Code 2.1.283 or later); the apply never runs E2E against a deployed environment; re-apply updates `E2E_PROD` to `E2E_BUILD`.
- Benchmark: two trajectory metrics from the transcripts, next to repeated reads: failed tool calls (tool results flagged as errors) and files edited more than twice. `bench/results/20261018-1500` is rescored with them. Cheaper models for the read-only profiles are documented as deferred in `README.md`.
- Benchmark: `versions.json` registers 1.0.0, 1.2.0, 1.3.0, 1.4.0, 1.5.0, 1.6.1, and 1.7.0; the runner refuses to start below Node 22 (Vitest 5 runs no tests on Node 20 and every unit result read as failed), saves each quality check's output, counts repeated file reads, and compares 1.4.0 (the best measured version) with the working tree by default. The fixture installs `@lhci/cli`.

## 1.6.1 — 2026-10-18

- `commits`: never add AI or tool attribution to commits or pull requests (`Co-Authored-By` naming an AI, "Generated with" lines, tool links, robot emoji), overriding tool defaults; human co-authors only on request.
- New `.claude/settings.json` that turns off Claude Code's commit and PR attribution (`attribution.commit` and `attribution.pr` empty, `sessionUrl` false; this form also works on versions before 2.1.281). `APPLY.md` merges only that key into an existing file.

## 1.6.0 — 2026-10-17

- Lighthouse: every key route meets Performance, Best Practices, and SEO 90 and Accessibility 95 on the mobile profile. New `performance` block in `AGENTS.md` with the binding rules and a `{{STACK:performance}}` snippet per stack (Next.js `next/image`, `next/font`, Metadata API, `next/script`; Vite lazy routes and chunk checks; Angular `NgOptimizedImage`, lazy routes, `@defer`, budgets).
- New `lighthouserc.json` (Lighthouse CI: 3 runs per URL, median, assertions, local reports in `.lighthouseci/`, never uploaded) and `lighthouse` command run through the package manager's `dlx`, with no new dependency. `{{STACK:lighthouse-collect}}` serves the build: `next start` for Next.js, the static `dist` with SPA fallback for Vite and Angular.
- `validation`: `lighthouse` runs once per task, after level 2, only when the change touches UI, routes, assets, dependencies, or build configuration, reusing the production build `e2e-prod` made.
- New skill `web-performance` (measure, prioritize, fix, re-measure, report before and after) with `scripts/lighthouse-audits.mjs`, which prints median scores and the audits that cost points.

## 1.5.2 — 2026-10-17

- `requirements`: back to the 1.2.0 rule, where every task starts by defining the requirement and asks everything open in one message, with a proposed default for each question. The 1.5.0 size tiers let the agent skip questions it should have asked: in the benchmark it named the ambiguity as an assumption, did not ask, and failed the hidden tests of the ambiguous task 3 out of 3 times (`bench/results/20261017-1649`). `working-style` goes back to its matching line.

## 1.5.1 — 2026-10-17

- `validation`: an empty E2E selection is never green; `--only-changed=<base>` once the work is committed; untagged modules fall back to finding specs by route, page object, or visible text. Restores the rule to prefer automated checks over manual verification.
- E2E level 2 is the union of changed specs and module-tagged specs, passed as explicit files: `--only-changed` and `--grep` in one command intersect, which would under-select.
- E2E level 2 runs once with `e2e-prod` instead of on the dev server and then again on a production build; level 3 re-runs the command that failed with `--last-failed`.
- `orchestration`: delegated agents work from the agreed requirement (restored).
- Fixed the level 2 row of the test selection table in `validation` (a missing column separator).
- New `bench/`: behavioral benchmark that runs the same tasks on a fixture project with each template version and compares speed and quality.
- Skills read `AGENTS.md` only when it is not already in context, which covers subagents that do not load it. `e2e-prod` documents the PowerShell form.

## 1.5.0 — 2026-10-17

- `AGENTS.md` `requirements`: the question round scales with the task (trivial: act; small: state the requirement and proceed; medium or ambiguous: one round of questions).
- `AGENTS.md` `validation`: test selection ladder (focused → related → failed → full). Related unit tests follow the import graph (`test-related`); related E2E specs come from `--only-changed` plus a `@<module>` tag per spec; `--last-failed` after fixes; full suites only on request. Lint and typecheck once per task, with cache.
- E2E iterates against the dev server; the final run and CI use a production build (`e2e-prod`, driven by `E2E_PROD` or `CI` in `webServer`).
- `AGENTS.md` `orchestration`: multi-agent policy. The primary thread works alone by default and delegates only when the parts are independent, large enough to save time, and quick to integrate; at most 3 agents at once, with self-contained briefs.
- `planning` and `tdd` merged into one `tdd` block ("Planning and TDD"); re-applying removes the old `planning` block. `docs/testing.md` and `docs/agent-workflows.md` no longer repeat rules from `AGENTS.md`.
- Skills and profiles do not re-read `AGENTS.md` and read only the doc sections the task needs.
- New commands and variables: `test-related` (`{{CMD_TEST_RELATED}}`), `lint-files` (`{{CMD_LINT_FILES}}`), `e2e-prod`. Stacks: incremental typecheck, `.eslintcache` and `*.tsbuildinfo` ignored, dev/production `webServer` switch.

## 1.4.0 — 2026-10-17

- New skill `mobile-ux`: audits and improves the mobile and responsive experience of existing screens, mobile-first, with a prioritized checklist (touch and access, layout and reflow, navigation and overlays, mobile forms, perceived performance). Reusable rules go to `DESIGN.md`.
- `docs/e2e-playbook.md`: Mobile checks section with a `mobile` Playwright project for `*.mobile.spec.ts` and helpers for horizontal overflow and touch-target size; new failure signatures and checklist item.
- `ui-accessibility`, the `product-ui` profiles, `docs/agent-workflows.md`, `docs/testing.md`, and `DESIGN.md` point to the new skill and the mobile spec command.

## 1.3.0 — 2026-10-17

- Package-manager agnostic: the `toolchain` block of `AGENTS.md` is the only place that names the runtime, the package manager, and the exact commands (new Package manager and Commands tables). Skills, agent profiles, `DESIGN.md`, and docs refer to commands by name (`test-file`, `e2e`, `design-lint`, ...).
- `APPLY.md`: asks which package manager to use (default: the detected one, `pnpm` when none is detected); new `{{RUN:…}}`, `{{EXEC:…}}`, `{{DLX:…}}` forms with a table for npm, pnpm, Yarn Berry, Yarn Classic, and Bun; a different choice from the detected one is reported as a migration follow-up, never performed; new check that no package manager is named outside the toolchain block.
- Variables: `{{PM_EXEC}}` removed; `{{PM_LOCKFILE}}`, `{{PM_INSTALL}}`, `{{PM_ADD}}`, `{{PM_ADD_DEV}}` added.
- Stacks: `profile-defaults`, `testing-setup`, and Playwright `webServer.command` use the package-manager forms instead of a fixed npm, pnpm, or Yarn.

## 1.2.0 — 2026-10-14

- `AGENTS.md` `planning`: every request is broken into small tasks, one per observable behavior, each with a defined check (a red-to-green test or a named alternative for test-ineligible work).

## 1.1.0 — 2026-10-12

- `AGENTS.md`: new `requirements` block. Every task starts with one round of questions that defines the requirement; no questions during execution. `working-style`, `planning`, and `orchestration` updated to match.
- `APPLY.md`: when re-applying, blocks the project does not have yet are inserted in template order.

## 1.0.0 — 2026-10-11

Initial extraction from `california-anime`, with rules consolidated from `doctor`, `selfservice-web`, and `MutuusCoreWeb`.

- `AGENTS.md` with marked blocks: communication, working style (including Git safety rules), Angular commit convention, documentation layout, design contract, toolchain, architecture, UI rules, planning, TDD policy, E2E policy, validation, orchestration.
- `DESIGN.md` skeleton in the Google Labs DESIGN.md format (`version: alpha`, fixed section order, recommended token names, linter and export commands).
- Skills: `tdd-change`, `e2e-playwright`, `ui-accessibility`, `release-verification`.
- Agent profiles in Claude Code and Codex formats: `feature-developer`, `product-ui`, `e2e-engineer`, `quality-reviewer`, `verification-runner`.
- Docs: `testing.md`, `e2e-playbook.md`, `agent-workflows.md`, `architecture.md` skeleton.
- Stacks: `nextjs`, `vite-react`, `angular`.
