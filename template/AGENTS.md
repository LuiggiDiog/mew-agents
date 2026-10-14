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
- Questions go at the start of the task (see Requirements). While executing, do not stop to ask: infer the most reasonable option from the agreed requirement, the repository structure, and existing patterns, and state the assumption in the report.
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
- `docs/testing.md` — TDD loop, test layers, setup, and commands.
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
- `DESIGN.md` follows the Google Labs DESIGN.md format: normative tokens in the YAML frontmatter, prose in fixed `##` sections. After editing it, run `npx @google/design.md lint DESIGN.md` and fix every error. Tokens can be exported with `npx @google/design.md export --format css-tailwind DESIGN.md`.
<!-- END:agent-rules:design -->

<!-- BEGIN:agent-rules:toolchain -->
## Toolchain

- Runtime: Node.js {{NODE_VERSION}}, pinned in `.nvmrc`. Use that version for installs, scripts, and tests.
- Package manager: `{{PM}}` (see `packageManager` in `package.json` and the lockfile). Never use another package manager, and never commit another lockfile.
{{STACK:toolchain}}
- Do not deploy unless the user explicitly asks for a deployment of the current work.
- Never commit secrets. `.env*` files are git-ignored; document required variables in `.env.example`.
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

Every task starts by defining the requirement with the user, so the rest of the task runs without further input.

1. Read the request and the relevant code first, so the questions cover only what the repository cannot answer.
2. Ask everything that is open in one message, before planning or editing: scope, expected behavior, edge cases, acceptance criteria, constraints. Propose an inferred default for each question so the user can confirm quickly. If nothing is open, state the requirement as understood and proceed.
3. Record the agreed requirement as a short list of observable behaviors. It is the input to step 1 of Planning.
4. After that, do not ask again. Resolve new doubts from the agreed requirement and the repository patterns, and state each assumption in the report. Anything that would need a new decision from the user (a deployment, a new dependency, a destructive action, a change of scope) is left out of the change and reported as a follow-up.
<!-- END:agent-rules:requirements -->

<!-- BEGIN:agent-rules:planning -->
## Planning

Break every request into small tasks before implementing. Derive them from the agreed requirement (see Requirements): one task per observable behavior, in dependency order. Each task has a defined check that proves it is done: a test that goes from red to green, or, for a test-ineligible task (see TDD policy), a named alternative such as typecheck, lint, `--list`, or inspection. If a task has no check, split or merge it until it has one; do not split further than that.

Each task with a behavior change follows TDD. Its plan is:

1. Define the expected behavior, from the agreed requirement (see Requirements).
2. Add or update a failing test.
3. Implement the minimum change that makes it pass.
4. Run the relevant tests.
5. Refactor only if needed, then re-run them.

A plan must not jump straight to implementation unless the task is test-ineligible, and then it says why. Keep plans short, concrete, and low-risk.
<!-- END:agent-rules:planning -->

<!-- BEGIN:agent-rules:tdd -->
## TDD policy

TDD is mandatory for every behavior change, bug fix, or new feature:

1. Write a new failing test, or update an existing one so it fails against current behavior. Run it and confirm it fails for the expected reason.
2. Implement the smallest change that makes it pass.
3. Refactor only after it passes.
4. Re-run the relevant test scope to confirm the final result.

Do not implement first and add tests later. "Include tests when possible" is not enough; the default is test-first.

For bug fixes, the failing test reproduces the bug first.

Test-ineligible tasks:

- Purely mechanical renames with no behavior change
- Comment-only or documentation-only edits
- Formatting-only changes
- Initial configuration or infrastructure where no automated test layer exists yet

When TDD is skipped, state why it was not feasible and what alternative validation was used (inspection, typecheck, lint, manual run).

### Test layers

{{STACK:test-layers}}
Setup, configuration, and commands are in `docs/testing.md`.
<!-- END:agent-rules:tdd -->

<!-- BEGIN:agent-rules:e2e -->
## E2E policy (Playwright)

Patterns and diagnosis are in `docs/e2e-playbook.md`; these rules are binding.

- Test user-visible behavior, not implementation details.
- Do not run the complete E2E suite unless the user explicitly requests it. Run only the specs relevant to the change.
- Prefer isolated, independent tests. Use `test.describe.serial` only for true journeys where each step depends on the previous step's state.
- Do not add a test that only asserts a transient route hop when the next functional test already covers that transition.
- Locator priority: `getByRole` with accessible name → `getByLabel` → `getByTestId` → scoped CSS as last resort. Avoid selectors that match multiple elements in strict mode.
- Use deterministic waits (`expect(...)` auto-retrying assertions, `waitForURL`, explicit state checks). Never use `waitForTimeout` for synchronization.
- Assert destination URLs exactly. Validate readiness, not just presence: the expected value is visible and the CTA is enabled before acting.
- Real app behavior first. Mock only external, non-deterministic boundaries (third-party providers, payments, email) for a concrete technical reason, never as a replacement for core product behavior.
- To assert a specific error state, walk the real path that produces it instead of sending synthetic invalid input that fails at a different layer.
- Generate unique test data at runtime (timestamp/random suffix); keep static fixtures only for non-unique values. Retry only known recoverable conflicts, bounded to 3–5 attempts, and fail with the current URL and reason.
- Let Playwright own the app server (`webServer` in `{{E2E_CONFIG}}`) on a dedicated port with `reuseExistingServer: false`, so a stale server is never tested. Use test-only environment values and fake providers; see `docs/testing.md` for this stack's command.
- Keep traces and screenshots on failure (`trace: 'retain-on-failure'`, `screenshot: 'only-on-failure'`). Diagnose with the trace viewer first.
- Put shared helpers in `{{E2E_DIR}}/helpers/` and page objects (one per page, with an `assertLoaded` method) in `{{E2E_DIR}}/pages/`. Extract a config detail into a helper once it repeats in three or more specs.
- When a flow changes, update the spec, its page objects/helpers, and any flow documentation in the same change.

E2E validation order:

1. `{{CMD_E2E}} --list` after structural edits.
2. The changed spec or step: `{{CMD_E2E}} {{E2E_DIR}}/<flow>.spec.ts` or `--grep "<title>"`.
3. The full flow or suite only when coupling risk exists and the user asked for it.
<!-- END:agent-rules:e2e -->

<!-- BEGIN:agent-rules:validation -->
## Validation

- Always validate the change, using the smallest relevant scope.
- Priority: relevant automated tests → focused typecheck/lint of touched code → manual verification only when necessary.
- Do not run unrelated checks. Do not run `{{CMD_BUILD}}` by default; use it only when the user asks, or when integration or production behavior cannot be validated otherwise.
- If a command cannot be run, say so and state what should be run manually.
<!-- END:agent-rules:validation -->

<!-- BEGIN:agent-rules:orchestration -->
## Agent orchestration

Profiles and skills are described in `docs/agent-workflows.md`. Skills live in `.agents/skills/` (shared with Claude Code through the `.claude/skills` symlink); profiles live in `.claude/agents/` and `.codex/agents/` and must stay in sync.

- The primary thread owns the full user request, the constraints in this file, integration, validation, and the final report.
- Delegate only bounded, independent work when it improves the result. Prefer parallel read-only searches or reviews; assign one owner per edited file.
- Delegated agents follow this file and never override the user's instructions on deployment or running the full E2E suite.
- Delegated agents do not ask the user. They work from the agreed requirement and return open questions to the primary thread.
<!-- END:agent-rules:orchestration -->

<!-- Project-specific rules go below this line (domain invariants, terminology, environments, safety rules). They are preserved when the template is re-applied. -->
