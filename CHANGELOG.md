# Changelog

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
