# How to apply this template to a project

This file is the procedure an AI coding agent (Claude Code, Codex, or any other) follows to apply the template. Give the agent this repository and the target project, for example:

> Apply the agent-rules template at `<path-to-this-repo>` to this project, following `APPLY.md`. Ask me only what you cannot infer.

The agent must read this whole file before touching the target project. It makes no commits and does not modify the Git staging area.

## 1. Discover the target project

Read, without changing anything:

- `package.json` (scripts, dependencies, `packageManager`, `engines`), the lockfile, `.nvmrc` or `.node-version`.
- Package manager in use: the `packageManager` field first, then the lockfile (see the table in step 3; `.yarnrc.yml` marks Yarn Berry). Note conflicts: several lockfiles, or `packageManager` disagreeing with the lockfile. If neither exists, nothing is detected.
- Framework and build config: `next.config.*`, `vite.config.*`, `angular.json`, `tsconfig*.json`.
- Existing test config: `vitest.config.*`, `jest.config.*`, `karma.conf.js`, `playwright.config.ts` (root or under `e2e/`).
- Existing `AGENTS.md`, `CLAUDE.md`, `DESIGN.md`, `README.md`, `docs/`, `.agents/`, `.claude/`, `.codex/`.
- Source layout: where routes/pages, components, services, and styles live; where the global stylesheet with tokens is.
- Git state: `git status --short`. Note uncommitted work; never revert or absorb it.

Pick the stack file from `stacks/` that matches: `nextjs`, `vite-react`, or `angular`. If none matches, use the closest one and say so in the report; do not invent framework rules.

## 2. Ask only what cannot be inferred

Ask these in one message, with the inferred defaults shown:

1. Response language for the agent (default: Spanish).
2. Package manager for the project: npm, pnpm, Yarn, Bun, or another (default: the one detected in step 1; `pnpm` when nothing is detected). Mention any conflict found in step 1. If the choice differs from the detected one, the template is written for the choice and the migration is left as a follow-up (see step 4).
3. Tools in use: Claude Code, Codex, or both (default: both).
4. Whether to install and configure the test tooling now (unit runner and Playwright) when the project lacks it, or only write the docs that describe the setup (default: write docs only; installation is a separate, explicitly requested step).
5. Any project-specific rules to keep (domain terminology, safety invariants, environment URLs). Existing `AGENTS.md` content outside the template markers is kept automatically.

Do not ask about anything that step 1 already answered.

## 3. Fill the variables

Every template file uses `{{VARIABLE}}` placeholders. Replace all of them; a leftover `{{` is an error. The stack file's `### profile-defaults` section gives typical values.

| Variable | Meaning | Example (Next.js, pnpm) |
| --- | --- | --- |
| `{{TEMPLATE_VERSION}}` | Version from `CHANGELOG.md` of this repo | `1.0.0` |
| `{{PROJECT_NAME}}` | `name` from `package.json` or the folder name | `california-anime` |
| `{{RESPONSE_LANGUAGE}}` | Language the agent answers in | `Spanish` |
| `{{NODE_VERSION}}` | Runtime, as in `.nvmrc` plus the major | `` `lts/krypton` (Node 24 LTS) `` |
| `{{PM}}`, `{{PM_LOCKFILE}}`, `{{PM_INSTALL}}`, `{{PM_ADD}}`, `{{PM_ADD_DEV}}` | Package manager chosen in step 2 and its commands (see "Package manager forms" below) | `pnpm`, `pnpm-lock.yaml`, `pnpm install`, `pnpm add`, `pnpm add -D` |
| `{{STACK}}` | Stack file used | `nextjs` |
| `{{FRAMEWORK_DOCS}}` | Where the framework docs for the installed version are | `` `node_modules/next/dist/docs/` `` |
| `{{SOURCE_DIR}}` | Where application code lives | `` `app/` and `modules/` `` |
| `{{STYLE_TOKENS_FILE}}` | Global stylesheet holding design tokens | `app/globals.css` |
| `{{E2E_DIR}}` | Folder with Playwright specs | `tests/e2e` |
| `{{E2E_CONFIG}}` | Playwright config path | `playwright.config.ts` |
| `{{CMD_DEV}}` | Start the dev server | `pnpm run dev` |
| `{{CMD_BUILD}}` | Production build | `pnpm run build` |
| `{{CMD_LINT}}` | Lint | `pnpm run lint` |
| `{{CMD_TYPECHECK}}` | Type check (write `n/a` if the project has none) | `pnpm run typecheck` |
| `{{CMD_TEST}}` | Unit tests, single run | `pnpm run test` |
| `{{CMD_TEST_WATCH}}` | Unit tests in watch mode | `pnpm run test:watch` |
| `{{CMD_TEST_FILE}}` | Run one unit test file | `pnpm run test <file>` |
| `{{CMD_TEST_RELATED}}` | Run the unit tests that cover the given source files | `pnpm exec vitest related --run <files>` |
| `{{CMD_TEST_LIST_CHANGED}}` | List, without running, the unit test files related to the changes since `<base>` (`n/a` when the runner cannot) | `pnpm exec vitest list --filesOnly --changed=<base>` |
| `{{CMD_LINT_FILES}}` | Lint only the given files, with cache | `pnpm exec eslint --cache <files>` |
| `{{CMD_E2E}}` | Playwright base command, including config if not at the root | `pnpm exec playwright test` |

`{{CMD_*}}` values come from the stack file's `### profile-defaults`, written as package-manager forms; compose them with the chosen package manager and check each script name against `package.json`.

### Package manager forms

Template and stack files never name a package manager. Besides the `{{PM*}}` variables, they use three forms, which are resolved with the column of the package manager chosen in step 2:

- `{{RUN:<script> [args]}}` runs a `package.json` script, with or without arguments.
- `{{EXEC:<bin> [args]}}` runs a binary installed in the project.
- `{{DLX:<package> [args]}}` runs a package without adding it to the project.

| | npm | pnpm | Yarn Berry (2+) | Yarn Classic (1.x) | Bun |
| --- | --- | --- | --- | --- | --- |
| `{{PM}}` | `npm` | `pnpm` | `yarn` | `yarn` | `bun` |
| `{{PM_LOCKFILE}}` | `package-lock.json` | `pnpm-lock.yaml` | `yarn.lock` | `yarn.lock` | `bun.lock` |
| `{{PM_INSTALL}}` | `npm install` | `pnpm install` | `yarn install` | `yarn install` | `bun install` |
| `{{PM_ADD}}` | `npm install` | `pnpm add` | `yarn add` | `yarn add` | `bun add` |
| `{{PM_ADD_DEV}}` | `npm install -D` | `pnpm add -D` | `yarn add -D` | `yarn add -D` | `bun add --dev` |
| `{{RUN:s}}` | `npm run s` | `pnpm run s` | `yarn run s` | `yarn run s` | `bun run s` |
| `{{RUN:s args}}` | `npm run s -- args` | `pnpm run s args` | `yarn run s args` | `yarn run s args` | `bun run s args` |
| `{{EXEC:bin args}}` | `npx bin args` | `pnpm exec bin args` | `yarn bin args` | `yarn bin args` | `bunx bin args` |
| `{{DLX:pkg args}}` | `npx --yes pkg args` | `pnpm dlx pkg args` | `yarn dlx pkg args` | `npx --yes pkg args` | `bunx pkg args` |

Notes:

- npm is the only one that needs `--` before script arguments; without it npm consumes flags such as `--watch=false` itself.
- Yarn Classic has no `dlx`; one-off packages run through `npx`, which never touches the project's dependencies or lockfile.
- Bun before 1.2 writes `bun.lockb`; use whichever lockfile the project has.
- For a package manager not in the table, add a column with its equivalents in this file and say so in the report.

Stack snippets: every `{{STACK:<name>}}` marker is replaced by the body of the `### <name>` section of the chosen stack file (without the heading). Markers used: `toolchain`, `architecture`, `ui-rules`, `performance`, `lighthouse-collect`, `test-layers`, `testing-setup`, `testing-map`, `layout`, `e2e-gotchas`. The stack file's header explains how to adapt `lighthouse-collect`.

## 4. Write the files

Copy from `template/` into the project root, after filling variables and snippets:

| File | New project | Existing file in the project |
| --- | --- | --- |
| `AGENTS.md` | Write it | **Merge** (see step 5) |
| `CLAUDE.md` | Write `@AGENTS.md` | Keep if it already loads `AGENTS.md`; if it only links to it, replace with `@AGENTS.md` and say why (a link does not load the content) |
| `DESIGN.md` | Write the skeleton | **Never overwrite.** Keep as is |
| `.agents/skills/*/` | Write all six, with their `scripts/` | Replace a skill with the same name; keep other skills |
| `.agents/scripts/affected-tests.mjs` | Write it (the `affected` command) | Replace |
| `.claude/skills` | Symlink to `../.agents/skills` | Keep; if `.claude/skills` is a real folder, move its skills to `.agents/skills/` and ask before replacing it with the symlink |
| `.claude/agents/*.md`, `.codex/agents/*.toml` | Write all five in each format the user uses | Replace profiles with the same name; keep others |
| `.claude/settings.json` | Write it (turns off commit and PR attribution) | Keep every existing key; set only `attribution` to the template's value and say so |
| `.codex/config.toml` | Write it | Keep the existing one |
| `docs/testing.md`, `docs/e2e-playbook.md`, `docs/agent-workflows.md` | Write them | Replace, after moving any project-specific content into `docs/context/` or the preserved area and saying so |
| `lighthouserc.json` | Write it, with the key routes (1–5 public, representative URLs inferred from the router; ask only if none is obvious) | Keep; report thresholds or budgets lower than the template's, and a missing `aggregationMethod: median` |
| `@lhci/cli` dev dependency (the `lighthouse` command) | Add it with `{{PM_ADD_DEV}} @lhci/cli` only when the user chose to install tooling in step 2; otherwise list it as a follow-up | Keep |
| `.gitignore` | Add `.lighthouseci/` if missing | Same |
| `docs/architecture.md` | Write the skeleton | **Never overwrite.** Keep as is |
| `docs/context/` | Do not create | Keep |
| `.nvmrc`, `package.json` `engines` | Add only if missing and the Node version is known | Keep |

If the package manager chosen in step 2 differs from the detected one, write every file for the chosen one, but do not delete or create lockfiles, reinstall dependencies, or edit `packageManager`. Report the migration as a follow-up: remove the old lockfile, run `{{PM_INSTALL}}` with the chosen package manager, set `packageManager` in `package.json`, and update any CI or config that calls the old one.

Other `.md` files at the project root (except `README.md`) are moved into `docs/` with a kebab-case name, and references to them updated, unless the user says otherwise.

The Next.js `<!-- BEGIN:nextjs-agent-rules -->` block is generated by `next dev`; leave it wherever it is.

## 5. Merge an existing `AGENTS.md`

1. If the file has no `agent-rules` markers: keep every existing section whose topic is not covered by a template block, move it below the final "Project-specific rules" comment, and insert the template blocks above. When an existing section overlaps a template block (for example its own TDD policy), the template block wins and any extra project rule from the old section moves to the project-specific area. List each moved or dropped paragraph in the report.
2. If the file already has markers: replace each `BEGIN:agent-rules:<id>` … `END:agent-rules:<id>` block with the new version, insert the blocks the file does not have yet in template order, remove blocks whose id the template no longer has (for example `planning`, merged into `tdd` in 1.5.0), keep everything outside the markers verbatim, and update the version in the `profile` block. Since 1.7.0 the `e2e-prod` command is `e2e-build` and its switch `E2E_BUILD`: update `E2E_PROD` in the project's Playwright config and scripts, and say so.
3. Never merge domain invariants, safety rules, terminology, or environment values into template blocks; they stay in the project-specific area.

## 6. Verify

Run only what exists; do not install anything unless the user chose that in step 2:

- `grep -rn "{{" AGENTS.md DESIGN.md docs .agents .claude .codex` returns nothing.
- `AGENTS.md` markers are balanced: every `BEGIN` has one `END` with the same id.
- No package manager is named outside the Toolchain block of `AGENTS.md`: `grep -rnwE 'npm|npx|pnpm|yarn|bun|bunx' .agents .claude/agents .codex/agents DESIGN.md docs/agent-workflows.md docs/e2e-playbook.md docs/architecture.md` returns nothing. The only expected matches elsewhere are config code that runs a command, such as `webServer.command` in the setup section of `docs/testing.md`. A preserved `DESIGN.md` or `docs/architecture.md` from an older template version may still name one; report it instead of rewriting those files.
- The `design-lint` command from the Toolchain block reports no errors (the empty skeleton passes).
- Symlink: `ls -la .claude/skills` points to `../.agents/skills`.
- Every `.codex/agents/*.toml` parses (balanced `"""`, quoted strings), and `lighthouserc.json` and `.claude/settings.json` parse as JSON.
- If Playwright is configured: the `e2e` command with `--list` lists specs without starting the server. Report specs without a module tag (`@<module>`) as a follow-up; do not tag them during the apply.
- If a unit runner is configured: run one existing test file with the `test-file` command.
- If Playwright or a unit runner is configured: the `affected` command runs from the project root and prints its sections (with no changes, every section is empty and no command is proposed).
- If a type check exists: the `typecheck` command.
- Optional, Claude Code 2.1.283 or later: `/doctor prompt-audit` reports contradictions and stale rules across `AGENTS.md`, rules, skills, and profiles. Report what it finds; do not edit template blocks to resolve it.

Do not run the full E2E suite, a production build, or E2E against any deployed environment during the apply.

## 7. Report

In the response language, state:

- Template version applied, stack file used, and package manager chosen, noting whether it differs from the detected one.
- Files written, replaced, merged, and left untouched, with the reason for each exception.
- Paragraphs moved to the project-specific area or `docs/context/`, and anything dropped.
- Checks run with their outcome, and checks skipped with the reason.
- Follow-ups the user may want: migrate the package manager when the choice differs from the detected one (step 4), install test tooling (see the stack file's `testing-setup`) and `@lhci/cli`, run `lighthouse` once for a baseline of the key routes, fill `DESIGN.md`, fill `docs/architecture.md`, open a new agent session so the new skills and profiles load.
