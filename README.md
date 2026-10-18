# agent-rules-template

Reusable instructions for AI coding agents (Claude Code and Codex): working rules, Angular-style commits, TDD-first planning, Playwright E2E policy, a design contract (`DESIGN.md`), documentation layout, skills, and agent profiles. One template, adapted per project through variables and per-stack snippets.

## Layout

```txt
APPLY.md                 # procedure an agent follows to apply the template
CHANGELOG.md             # template versions
template/                # files copied into a project, with {{VARIABLES}} and {{STACK:...}} markers
  AGENTS.md              # rules, split into BEGIN/END marked blocks
  CLAUDE.md              # @AGENTS.md
  DESIGN.md              # design standards skeleton (Google Labs DESIGN.md format)
  lighthouserc.json      # Lighthouse CI: key routes, minimum scores, metric budgets (median of 3 runs)
  .agents/skills/        # tdd-change, e2e-playwright, ui-accessibility, mobile-ux, web-performance, release-verification
  .agents/scripts/       # affected-tests.mjs: the `affected` command (tests and specs that cover the touched files)
  .agents/hooks/         # guard.mjs: PreToolUse guard for both tools (no full suites without FULL_SUITE=1, no E2E outside test environments)
  .claude/agents/        # Claude Code profiles (.md); .claude/skills -> ../.agents/skills
  .claude/settings.json  # Claude Code settings: no AI attribution in commits or PRs, guard hook
  .codex/agents/         # Codex profiles (.toml) + .codex/config.toml
  docs/                  # testing, e2e-playbook, agent-workflows, architecture skeleton
bench/                   # behavioral benchmark: same tasks per template version (see bench/README.md)
stacks/
  nextjs.md              # Next.js App Router + Vitest + Playwright
  vite-react.md          # Vite + React + Vitest + Playwright
  angular.md             # Angular CLI + Karma/Jasmine + Playwright
```

## Apply to a project

Open an agent session in the target project and paste:

> Apply the agent-rules template at `<path-to-this-repo>` to this project, following `APPLY.md`. Ask me only what you cannot infer.

The agent discovers the stack, fills the variables, copies or merges the files, verifies, and reports. Existing `DESIGN.md`, `docs/architecture.md`, `docs/context/`, and any `AGENTS.md` content outside the template markers are preserved.

## Update projects after changing the template

1. Edit `template/` or `stacks/`, add an entry to `CHANGELOG.md`, bump the version, and tag it (`git tag v1.1.0`).
2. In each project, run the same apply prompt. Marked blocks in `AGENTS.md` are replaced; everything else is kept.
3. Each project's `AGENTS.md` records the applied version in its first comment, so outdated projects are easy to spot.

## Conventions

- Template files are in English; the response language is a variable.
- Package-manager agnostic: template and stack files never name a package manager. They use the `{{PM*}}` variables and the `{{RUN:…}}`, `{{EXEC:…}}`, `{{DLX:…}}` forms defined in `APPLY.md`, and in each project only the Toolchain block of `AGENTS.md` holds the resolved commands.
- Invariant rules live in `template/`; anything that depends on the framework lives in `stacks/` under `### <snippet>` headings that `APPLY.md` maps to `{{STACK:<snippet>}}` markers.
- Efficiency without losing quality: each rule lives in one place, agents read only what the task needs, tests climb a selection ladder instead of running full suites, and extra agents are used only when they finish the work sooner.
- `AGENTS.md` stays short (about 130 content lines once rendered): binding rules only, with checklists and procedures in skills and docs that load on demand. E2E runs only against local or test environments, never production.
- The benchmark in `bench/` runs only when the maintainer explicitly asks for it. Agents never run it on their own, as a validation step, or as part of a release.
- Never put domain rules in the template. They belong to each project's own area in `AGENTS.md` and `docs/context/`.

## Release checklist

1. `python3 bench/render.py <version> <dir>` for every version in `bench/versions.json` renders without leftovers, and the rendered `lighthouserc.json` and `.claude/settings.json` parse.
2. The verify step of `APPLY.md` passes on the rendered working tree (markers balanced, no package manager named outside the Toolchain, every command name in skills and profiles exists in the Commands table, Claude Code and Codex profiles identical).
3. `node --check` on the three scripts, and the guard denies `npm test` with exit code 2.
4. `/doctor prompt-audit` in a Claude Code session on the rendered tree reports no contradictions.
5. `CHANGELOG.md` has the entry, with a **Breaking** lead when a command, variable, or file name changed.
6. The benchmark runs only when the maintainer asks; when it does, the new version must keep quality and not lose speed (see `bench/README.md`).

## Deferred

Decided but not applied yet. Each item names what would trigger it.

- **Cheaper models for the read-only profiles.** `quality-reviewer` and `verification-runner` only run checks, read output, and list findings, so a faster model at medium effort would likely do the same work sooner and cheaper. Codex already runs `verification_runner` on `gpt-6-luna` at medium effort; Claude Code runs `verification-runner` on `sonnet` with no `effort`, and `quality-reviewer` inherits the session model in Claude Code and uses `gpt-6-sol` at high effort in Codex. The change: `model: sonnet` and `effort: medium` on both Claude Code profiles, and `gpt-6-luna` on `quality_reviewer` in Codex, so both formats say the same. The profiles that write code keep the session model. Trigger: a benchmark task large enough to justify delegation, so a cheaper reviewer that misses bugs would show up in the hidden tests before the change ships.
