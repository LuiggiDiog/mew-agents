<!-- BEGIN:agent-rules:profile -->
<!-- agent-rules template v{{TEMPLATE_VERSION}}. Sections between BEGIN/END markers come from the template and are replaced when it is re-applied. Anything outside the markers belongs to this project and is preserved. -->

# Project instructions

These are the default instructions for AI coding agents in this repository. Apply them before making changes.
If a direct user request conflicts with this file, follow the user request.
A more specific `AGENTS.md` in a subdirectory takes precedence for its scope.
<!-- END:agent-rules:profile -->

<!-- BEGIN:agent-rules:communication -->
## Communication

- Always respond to the user in {{RESPONSE_LANGUAGE}}.
- Keep code, identifiers, filenames, folder names, comments, commit messages, and repository documentation in English.
- Be concise, practical, and direct. Skip unnecessary explanations.
- When reporting work, state what changed, why, and how it was validated. Report what was actually run; list skipped checks and why.
<!-- END:agent-rules:communication -->

<!-- BEGIN:agent-rules:working-style -->
## Working style

- Read relevant files before proposing or applying changes. Understand the root cause before editing.
- Make the smallest correct change. Touch only files relevant to the task.
- Do not rewrite, rename, move, or reformat unrelated code.
- Preserve existing patterns and style; prefer repository conventions over personal preference.
- Prefer simple, maintainable solutions over clever ones. No speculative refactors or broad refactors unless requested.
- Questions, when the task needs them, go at the start (see Requirements). While executing, do not stop to ask: infer the most reasonable option from the requirement, the repository structure, and existing patterns, and state the assumption in the report.
- Do not re-read a file that is already in context, and read only the sections of a doc that the task needs.
- Do not introduce dependencies without a concrete, justified need.
- Treat existing uncommitted changes as the user's work. Do not revert, absorb, or rewrite them unless told to.
- Do not stage, unstage, commit, or otherwise modify the Git staging area unless the user explicitly asks.
- Keep generated output (reports, videos, screenshots, traces, test artifacts, logs) out of source changes unless the user explicitly asks for them.
<!-- END:agent-rules:working-style -->

<!-- BEGIN:agent-rules:commits -->
## Commits

Follow the Angular commit convention. Commit messages are short, clear, and direct: a single header line.

```txt
<type>(<scope>): <summary>
```

- `type`: `feat`, `fix`, `refactor`, `perf`, `test`, `docs`, `build`, `ci`.
- `scope`: the feature or module touched (for example `auth`, `catalog`, `e2e`, `deps`). Omit it for cross-cutting changes.
- `summary`: imperative mood, lowercase, no trailing period, at most 72 characters. One logical change per commit.
- No body and no bullet lists of changed files; the diff already shows them. The only exception is a breaking change, which adds a `BREAKING CHANGE:` footer.

Examples: `feat(catalog): add genre filter to the list`, `fix(auth): keep session after token refresh`, `test(e2e): cover sign-in redirect`, `docs: describe the TDD loop`.
<!-- END:agent-rules:commits -->

<!-- BEGIN:agent-rules:documentation -->
## Documentation

All project documentation lives in `docs/`. Only `AGENTS.md`, `CLAUDE.md`, `DESIGN.md`, and `README.md` stay at the root.

- `docs/architecture.md` — structure, layers, boundaries, and which test layer covers what.
- `docs/testing.md` — test layers, setup, and which command to use for each goal.
- `docs/e2e-playbook.md` — Playwright patterns, anti-flake rules, failure signatures, spec checklist.
- `docs/agent-workflows.md` — agent profiles and skills for Claude Code and Codex.
- `docs/context/` — short notes on feature decisions and non-obvious bug causes (problem, cause, decision, expected behavior), each starting with its date and scope. Create the folder with the first note.

Read the relevant doc before changing that area, and update it in the same change when behavior, structure, or commands change. New docs go in `docs/` with a kebab-case name.
<!-- END:agent-rules:documentation -->

<!-- BEGIN:agent-rules:design -->
## Design

- `DESIGN.md` at the repo root is the design source of truth: tokens, typography, color and contrast, layout and responsive rules, component rules, and accessibility checks. Read it before any UI change and keep it aligned with `{{STYLE_TOKENS_FILE}}`.
- While `DESIGN.md` is empty or has no rule for the case at hand, follow the existing UI and propose the missing rule in `DESIGN.md` in the same change. Do not invent a parallel convention.
- When a change introduces a reusable visual rule or token, update `DESIGN.md` and the stylesheet together.
- `DESIGN.md` follows the Google Labs DESIGN.md format: normative tokens in the YAML frontmatter, prose in fixed `##` sections. After editing it, run the `design-lint` command and fix every error. Tokens can be exported with the `design-export` command.
<!-- END:agent-rules:design -->

<!-- BEGIN:agent-rules:toolchain -->
## Toolchain

This section is the only place that names the runtime, the package manager, and the exact commands. Skills, agent profiles, and docs refer to commands by the names in the Commands table (for example "the `test-file` command"); resolve them here. To change the package manager or a command, edit only this section, plus any config code that runs a command (such as Playwright's `webServer.command`).

- Runtime: Node.js {{NODE_VERSION}}, pinned in `.nvmrc`. Use that version for installs, scripts, and tests.
- Package manager: `{{PM}}`, lockfile `{{PM_LOCKFILE}}`. Use only `{{PM}}` to install, add, run scripts, and run binaries. Never use another package manager, and never commit another lockfile.
{{STACK:toolchain}}
- Do not deploy unless the user explicitly asks for a deployment of the current work.
- Never commit secrets. `.env*` files are git-ignored; document required variables in `.env.example`.

### Package manager

| Action | Command |
| --- | --- |
| Install dependencies | `{{PM_INSTALL}}` |
| Add a dependency | `{{PM_ADD}} <package>` |
| Add a dev dependency | `{{PM_ADD_DEV}} <package>` |
| Run a `package.json` script | `{{RUN:<script>}}` |
| Run a script with arguments | `{{RUN:<script> <args>}}` |
| Run a locally installed binary | `{{EXEC:<bin> <args>}}` |
| Run a package without installing it | `{{DLX:<package> <args>}}` |

Adding a dependency still needs a justified need (see Working style).

### Commands

| Name | Command | Runs |
| --- | --- | --- |
| `dev` | `{{CMD_DEV}}` | Development server |
| `build` | `{{CMD_BUILD}}` | Production build |
| `lint` | `{{CMD_LINT}}` | Lint |
| `typecheck` | `{{CMD_TYPECHECK}}` | Type check |
| `test` | `{{CMD_TEST}}` | Unit and component tests, single run |
| `test-watch` | `{{CMD_TEST_WATCH}}` | Unit tests in watch mode (TDD loop) |
| `test-file` | `{{CMD_TEST_FILE}}` | One unit test file |
| `test-related` | `{{CMD_TEST_RELATED}}` | Unit tests that cover the given source files |
| `lint-files` | `{{CMD_LINT_FILES}}` | Lint only the given files, with cache |
| `e2e` | `{{CMD_E2E}}` | Playwright against the dev server; append a spec path, `--list`, `--grep "<title or @tag>"`, `--only-changed`, `--last-failed`, `-x`, or `--debug` |
| `e2e-prod` | `E2E_PROD=1 {{CMD_E2E}}` | Playwright against a production build: final validation and CI (CI sets it through `CI`) |
| `e2e-install` | `{{EXEC:playwright install chromium}}` | Playwright browser, once per machine |
| `e2e-trace` | `{{EXEC:playwright show-trace <trace.zip>}}` | Open a Playwright trace |
| `design-lint` | `{{DLX:@google/design.md lint DESIGN.md}}` | Validate `DESIGN.md` |
| `design-export` | `{{DLX:@google/design.md export --format css-tailwind DESIGN.md}}` | Export `DESIGN.md` tokens as CSS |

Arguments appended to a command (a spec path, `--list`) go after it unchanged, except when the command is a script: then use the "Run a script with arguments" form.
<!-- END:agent-rules:toolchain -->

<!-- BEGIN:agent-rules:architecture -->
## Architecture

See `docs/architecture.md` for the target layout and boundary diagram.

- Organize by feature/domain. Keep module-specific logic inside its module; share code only when it is genuinely reusable.
- Keep clear boundaries between UI, business logic, and data access. UI components must not call data sources directly.
{{STACK:architecture}}
- Keep secrets and server-only code on the server.

Recommended module structure, created only when needed:

- `components/` — UI pieces
- `services/` — business logic and orchestration
- `repositories/` — data access
- `types/` — local types
- `mocks/` — test mocks

Optional, only when clearly justified: `hooks/`, `utils/`, `constants/`, `schemas/`, `adapters/`, `config/`. Do not create folders just in case.

Index files: do not add barrel files by default. Use one `index.ts` at a module boundary only when it clearly improves imports; avoid hiding boundaries behind re-exports.
<!-- END:agent-rules:architecture -->

<!-- BEGIN:agent-rules:ui -->
## UI rules

{{STACK:ui-rules}}
<!-- END:agent-rules:ui -->

<!-- BEGIN:agent-rules:requirements -->
## Requirements

Size the requirement round to the task, so the rest of it runs without further input. When unsure between two sizes, take the larger.

- **Trivial** (a typo, a copy edit, a one-file fix with an obvious expected result): do it without asking.
- **Small** (a clear request with one reasonable interpretation): state the requirement and any assumption in one or two lines, then proceed without waiting.
- **Medium or ambiguous** (several behaviors, more than one reasonable interpretation, or a change to public behavior): read the request and the relevant code first, then ask everything open in one message (scope, expected behavior, edge cases, acceptance criteria, constraints), each with a proposed default.

The requirement is a short list of observable behaviors and the input to planning. After it, do not ask again: resolve doubts from the requirement and the repository patterns, and state each assumption in the report. Anything that needs a new decision from the user (a deployment, a new dependency, a destructive action, a change of scope) stays out of the change and is reported as a follow-up.
<!-- END:agent-rules:requirements -->


<!-- BEGIN:agent-rules:tdd -->
## Planning and TDD

Break the requirement into small tasks, one per observable behavior, in dependency order. Each task has one check that proves it is done: a test that goes from red to green or, for a test-ineligible task, a named alternative (typecheck, lint, `--list`, inspection). Split or merge tasks until each has a check, and no further. A trivial task is a single task and needs no written plan.

TDD is mandatory for every behavior change, bug fix, or new feature. Implementing first and adding tests later is not allowed:

1. Write a failing test, or update one so it fails against current behavior; for a bug, the test reproduces it. Run it and confirm it fails for the expected reason.
2. Implement the smallest change that makes it pass.
3. Refactor only with the test green.
4. Confirm through the test selection ladder (see Validation).

Test-ineligible: mechanical renames with no behavior change, comment-only or documentation-only edits, formatting-only changes, and initial configuration where no automated test layer exists yet. When TDD is skipped, state why and what validated the change instead.

### Test layers

{{STACK:test-layers}}
Setup and configuration are in `docs/testing.md`; the step-by-step loop is the `tdd-change` skill.
<!-- END:agent-rules:tdd -->

<!-- BEGIN:agent-rules:e2e -->
## E2E policy (Playwright)

These rules are binding; patterns, examples, and diagnosis are in `docs/e2e-playbook.md`.

- Test user-visible behavior with isolated tests. Use `test.describe.serial` only for true journeys where each step depends on the previous one. Do not add a test that only asserts a transient route hop the next test already covers.
- Locators: `getByRole` with accessible name → `getByLabel` → `getByTestId` → scoped CSS as last resort. No locator may match several elements in strict mode.
- Use deterministic waits only (auto-retrying `expect`, `waitForURL`, explicit state checks); never `waitForTimeout`. Assert exact destination URLs and readiness (expected value visible, CTA enabled) before acting.
- Real app behavior first. Mock only external, non-deterministic boundaries (third-party providers, payments, email) for a concrete reason. Reach a specific error state through the real path that produces it.
- Generate unique test data at runtime. Retry only known recoverable conflicts, 3–5 attempts, failing with the current URL and reason.
- Playwright owns the app server (`webServer` in `{{E2E_CONFIG}}`, dedicated port, `reuseExistingServer: false`): the dev server while iterating, a production build through `e2e-prod` for the final run and CI. Use test-only environment values and fake providers, never real secrets.
- Every spec is tagged with the module it covers (`{ tag: '@<module>' }`, where the module is the feature folder name), so a changed source file maps to its specs without a lookup table.
- Keep traces and screenshots on failure, and diagnose from the trace before touching a timeout.
- Page objects (one per page, with `assertLoaded()`) live in `{{E2E_DIR}}/pages/` and shared helpers in `{{E2E_DIR}}/helpers/`. A changed flow updates its spec, page objects, helpers, and flow docs in the same change.
- Never run the complete E2E suite unless the user explicitly asks for it. Select specs with the ladder in Validation.
<!-- END:agent-rules:e2e -->

<!-- BEGIN:agent-rules:validation -->
## Validation and test selection

Validate every change with the smallest scope that proves it. Climb one level only when the previous one is green, and stop at the first level that covers the change.

| Level | When | Unit | E2E |
| --- | --- | --- | --- |
| 1. Focused | While iterating on a task | `test-file` with the test being written | `e2e` with the spec, `--grep "<title>"`, and `-x` |
| 2. Related | Once the tasks are green, before reporting | `test-related` with the touched source files | `e2e --only-changed` (changed specs, page objects, helpers) plus `--grep "@<module>"` for each touched module |
| 3. Failed | After fixing failures found at level 2 | the failing test files | `e2e --last-failed` |
| 4. Full | Only on explicit request; for unit tests also when test config, dependencies, or a module imported almost everywhere changed | `test` | the complete `e2e`, only on explicit request |

- E2E levels 1–3 run against the dev server. The last E2E run before reporting repeats the level 2 selection with `e2e-prod`.
- Skip what the change cannot affect: documentation-only changes run no tests; style-only changes run no unit tests and are inspected instead; a test-only change runs only that test.
- Run `lint-files` on the touched files and `typecheck` once per task, not after every edit. Do not re-run a green check unless the code it covers changed since.
- Do not run the `build` command unless the user asks, or production behavior cannot be validated otherwise (`e2e-prod` already covers E2E).
- If a command cannot be run, say so and state what should be run manually. Report the level reached and why higher levels were not needed.
<!-- END:agent-rules:validation -->

<!-- BEGIN:agent-rules:orchestration -->
## Agent orchestration

Profiles and skills are described in `docs/agent-workflows.md`. Skills live in `.agents/skills/` (shared with Claude Code through the `.claude/skills` symlink); profiles live in `.claude/agents/` and `.codex/agents/` and must stay in sync.

The primary thread owns the full request, the constraints in this file, integration, validation, and the final report, and works alone by default. Extra agents exist only to finish sooner: spending more tokens is acceptable when it shortens the time to a validated result, never otherwise.

Delegate only when all three hold:

1. The work splits into parts with no shared files and no ordering dependency (for example, read-only exploration of separate areas, or a service and its UI once the contract between them is fixed).
2. Each part is large enough that running in parallel saves more time than briefing and integrating it costs. Work the primary thread can finish in a few edits is never delegated.
3. Integrating and validating the results is quick: disjoint files, an interface agreed before splitting, and a focused check per part.

- Use the fewest agents that cover the independent parts, at most 3 at once, launched together.
- Each brief is self-contained: goal, files owned, the agreed contract, the checks to run, what not to touch, and what to return (changed files, commands run, results, open questions).
- Do not delegate sequential steps, edits to the same file, decisions the other parts depend on (settle those first in the primary thread), or work that needs the user.
- Delegated agents follow this file, never override the user's instructions on deployment or the full E2E suite, do not ask the user, and return open questions to the primary thread.
- After integrating, the primary thread runs the level 2 selection (see Validation) once on the combined diff.
<!-- END:agent-rules:orchestration -->

<!-- Project-specific rules go below this line (domain invariants, terminology, environments, safety rules). They are preserved when the template is re-applied. -->
