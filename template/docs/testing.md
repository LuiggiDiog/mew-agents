# Testing and TDD

`AGENTS.md` holds the binding TDD policy and the test selection ladder, and the `tdd-change` skill holds the step-by-step loop. This file covers what is specific to this repository: the test layers, their configuration, and which command to use for each goal.

## Choosing the layer

{{STACK:testing-map}}

Prefer the lowest layer that proves the behavior. Add an E2E spec only for user-visible flows that lower layers cannot prove.

## Conventions for unit and component tests

- Co-locate tests with the code they cover, following the project's existing placement and naming.
- Name tests by behavior: `it('rejects an empty title')`, not `it('works')`.
- Use fakes at external boundaries (HTTP clients, repositories, clocks, randomness). Do not mock the unit under test or its internal collaborators.
- No network, real providers, or shared mutable state in unit tests.

## Setup and configuration

{{STACK:testing-setup}}

## Commands

The exact commands are defined once, in the Toolchain section of `AGENTS.md`. This table says which one to use for each goal.

| Goal | Command |
| --- | --- |
| One unit test file | `test-file` |
| TDD loop | `test-watch` |
| Unit tests that cover the touched files | `test-related` with the files |
| All unit and component tests | `test` |
| Lint touched files, type check | `lint-files` with the files, `typecheck` |
| Discover E2E specs without starting the server | `e2e` with `--list` |
| One E2E spec | `e2e` with `{{E2E_DIR}}/<flow>.spec.ts` |
| One E2E test by title | `e2e` with `--grep "<title>"` |
| Specs with uncommitted changes, or whose page objects and helpers changed | `e2e` with `--only-changed` (`--only-changed=<base>` once committed) |
| Specs of a touched module | `e2e` with `--grep "@<module>"` |
| Only the specs that failed last run | `e2e` with `--last-failed` |
| Level 2 run against a production build | `e2e-prod` with the level 2 selection |
| Lighthouse scores of the key routes | `lighthouse` after a production build, then `node .agents/skills/web-performance/scripts/lighthouse-audits.mjs` |
| One mobile spec | `e2e` with `--project=mobile {{E2E_DIR}}/<flow>.mobile.spec.ts` |
| Debug an E2E spec | `e2e` with `--debug {{E2E_DIR}}/<flow>.spec.ts` |
| Open a failure trace | `e2e-trace` with `<test-results>/<run>/trace.zip` |

Run the complete E2E suite (the `e2e` command with no filter) only when the user explicitly asks for it.
