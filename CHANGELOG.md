# Changelog

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
