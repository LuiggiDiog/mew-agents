# How to apply this template to a project

This file is the procedure an AI coding agent (Claude Code, Codex, or any other) follows to apply the template. Give the agent this repository and the target project, for example:

> Apply the agent-rules template at `<path-to-this-repo>` to this project, following `APPLY.md`. Ask me only what you cannot infer.

The agent must read this whole file before touching the target project. It makes no commits and does not modify the Git staging area.

## 1. Discover the target project

Read, without changing anything:

- `package.json` (scripts, dependencies, `packageManager`, `engines`), the lockfile, `.nvmrc` or `.node-version`.
- Framework and build config: `next.config.*`, `vite.config.*`, `angular.json`, `tsconfig*.json`.
- Existing test config: `vitest.config.*`, `jest.config.*`, `karma.conf.js`, `playwright.config.ts` (root or under `e2e/`).
- Existing `AGENTS.md`, `CLAUDE.md`, `DESIGN.md`, `README.md`, `docs/`, `.agents/`, `.claude/`, `.codex/`.
- Source layout: where routes/pages, components, services, and styles live; where the global stylesheet with tokens is.
- Git state: `git status --short`. Note uncommitted work; never revert or absorb it.

Pick the stack file from `stacks/` that matches: `nextjs`, `vite-react`, or `angular`. If none matches, use the closest one and say so in the report; do not invent framework rules.

## 2. Ask only what cannot be inferred

Ask these in one message, with the inferred defaults shown:

1. Response language for the agent (default: Spanish).
2. Tools in use: Claude Code, Codex, or both (default: both).
3. Whether to install and configure the test tooling now (unit runner and Playwright) when the project lacks it, or only write the docs that describe the setup (default: write docs only; installation is a separate, explicitly requested step).
4. Any project-specific rules to keep (domain terminology, safety invariants, environment URLs). Existing `AGENTS.md` content outside the template markers is kept automatically.

Do not ask about anything that step 1 already answered.

## 3. Fill the variables

Every template file uses `{{VARIABLE}}` placeholders. Replace all of them; a leftover `{{` is an error. The stack file's `### profile-defaults` section gives typical values.

| Variable | Meaning | Example (Next.js + pnpm) |
| --- | --- | --- |
| `{{TEMPLATE_VERSION}}` | Version from `CHANGELOG.md` of this repo | `1.0.0` |
| `{{PROJECT_NAME}}` | `name` from `package.json` or the folder name | `california-anime` |
| `{{RESPONSE_LANGUAGE}}` | Language the agent answers in | `Spanish` |
| `{{NODE_VERSION}}` | Runtime, as in `.nvmrc` plus the major | `` `lts/krypton` (Node 24 LTS) `` |
| `{{PM}}` | Package manager name | `pnpm` |
| `{{PM_EXEC}}` | Prefix to run a local binary | `pnpm exec` (`yarn`, `npx`) |
| `{{STACK}}` | Stack file used | `nextjs` |
| `{{FRAMEWORK_DOCS}}` | Where the framework docs for the installed version are | `` `node_modules/next/dist/docs/` `` |
| `{{SOURCE_DIR}}` | Where application code lives | `` `app/` and `modules/` `` |
| `{{STYLE_TOKENS_FILE}}` | Global stylesheet holding design tokens | `app/globals.css` |
| `{{E2E_DIR}}` | Folder with Playwright specs | `tests/e2e` |
| `{{E2E_CONFIG}}` | Playwright config path | `playwright.config.ts` |
| `{{CMD_DEV}}` | Start the dev server | `pnpm dev` |
| `{{CMD_BUILD}}` | Production build | `pnpm build` |
| `{{CMD_LINT}}` | Lint | `pnpm lint` |
| `{{CMD_TYPECHECK}}` | Type check (write `n/a` if the project has none) | `pnpm typecheck` |
| `{{CMD_TEST}}` | Unit tests, single run | `pnpm test` |
| `{{CMD_TEST_WATCH}}` | Unit tests in watch mode | `pnpm test:watch` |
| `{{CMD_TEST_FILE}}` | Run one unit test file | `pnpm test <file>` |
| `{{CMD_E2E}}` | Playwright base command, including config if not at the root | `pnpm exec playwright test` |

Stack snippets: every `{{STACK:<name>}}` marker is replaced by the body of the `### <name>` section of the chosen stack file (without the heading). Markers used: `toolchain`, `architecture`, `ui-rules`, `test-layers`, `testing-setup`, `testing-map`, `layout`, `e2e-gotchas`.

## 4. Write the files

Copy from `template/` into the project root, after filling variables and snippets:

| File | New project | Existing file in the project |
| --- | --- | --- |
| `AGENTS.md` | Write it | **Merge** (see step 5) |
| `CLAUDE.md` | Write `@AGENTS.md` | Keep if it already loads `AGENTS.md`; if it only links to it, replace with `@AGENTS.md` and say why (a link does not load the content) |
| `DESIGN.md` | Write the skeleton | **Never overwrite.** Keep as is |
| `.agents/skills/*/SKILL.md` | Write all four | Replace a skill with the same name; keep other skills |
| `.claude/skills` | Symlink to `../.agents/skills` | Keep; if `.claude/skills` is a real folder, move its skills to `.agents/skills/` and ask before replacing it with the symlink |
| `.claude/agents/*.md`, `.codex/agents/*.toml` | Write all five in each format the user uses | Replace profiles with the same name; keep others |
| `.codex/config.toml` | Write it | Keep the existing one |
| `docs/testing.md`, `docs/e2e-playbook.md`, `docs/agent-workflows.md` | Write them | Replace, after moving any project-specific content into `docs/context/` or the preserved area and saying so |
| `docs/architecture.md` | Write the skeleton | **Never overwrite.** Keep as is |
| `docs/context/` | Do not create | Keep |
| `.nvmrc`, `package.json` `engines` | Add only if missing and the Node version is known | Keep |

Other `.md` files at the project root (except `README.md`) are moved into `docs/` with a kebab-case name, and references to them updated, unless the user says otherwise.

The Next.js `<!-- BEGIN:nextjs-agent-rules -->` block is generated by `next dev`; leave it wherever it is.

## 5. Merge an existing `AGENTS.md`

1. If the file has no `agent-rules` markers: keep every existing section whose topic is not covered by a template block, move it below the final "Project-specific rules" comment, and insert the template blocks above. When an existing section overlaps a template block (for example its own TDD policy), the template block wins and any extra project rule from the old section moves to the project-specific area. List each moved or dropped paragraph in the report.
2. If the file already has markers: replace each `BEGIN:agent-rules:<id>` … `END:agent-rules:<id>` block with the new version, insert the blocks the file does not have yet in template order, keep everything outside the markers verbatim, and update the version in the `profile` block.
3. Never merge domain invariants, safety rules, terminology, or environment values into template blocks; they stay in the project-specific area.

## 6. Verify

Run only what exists; do not install anything unless the user chose that in step 2:

- `grep -rn "{{" AGENTS.md DESIGN.md docs .agents .claude .codex` returns nothing.
- `AGENTS.md` markers are balanced: every `BEGIN` has one `END` with the same id.
- `npx @google/design.md lint DESIGN.md` reports no errors (the empty skeleton passes).
- Symlink: `ls -la .claude/skills` points to `../.agents/skills`.
- Every `.codex/agents/*.toml` parses (balanced `"""`, quoted strings).
- If Playwright is configured: `{{CMD_E2E}} --list` lists specs without starting the server.
- If a unit runner is configured: run one existing test file with `{{CMD_TEST_FILE}}`.
- If a type check exists: `{{CMD_TYPECHECK}}`.

Do not run the full E2E suite or a production build during the apply.

## 7. Report

In the response language, state:

- Template version applied and stack file used.
- Files written, replaced, merged, and left untouched, with the reason for each exception.
- Paragraphs moved to the project-specific area or `docs/context/`, and anything dropped.
- Checks run with their outcome, and checks skipped with the reason.
- Follow-ups the user may want: install test tooling (see the stack file's `testing-setup`), fill `DESIGN.md`, fill `docs/architecture.md`, open a new agent session so the new skills and profiles load.
