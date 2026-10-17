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
  .agents/skills/        # tdd-change, e2e-playwright, ui-accessibility, mobile-ux, release-verification
  .claude/agents/        # Claude Code profiles (.md); .claude/skills -> ../.agents/skills
  .codex/agents/         # Codex profiles (.toml) + .codex/config.toml
  docs/                  # testing, e2e-playbook, agent-workflows, architecture skeleton
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
- Never put domain rules in the template. They belong to each project's own area in `AGENTS.md` and `docs/context/`.
