# Testing and TDD

`AGENTS.md` holds the binding TDD policy. This file explains how to apply it in this repository: the test layers, their configuration, and the commands.

## TDD loop

1. **Define the behavior** in one or two sentences, in terms a user or caller can observe.
2. **Red:** write or update the smallest test that expresses it. Run only that test and confirm it fails for the expected reason (an assertion, not a typo or a missing import).
3. **Green:** implement the minimum change that makes it pass.
4. **Refactor** with the test green. Do not add behavior during this step.
5. **Re-run** the focused scope, then typecheck the touched code.

For bug fixes, the red step reproduces the bug. Keep the test after the fix.

If a task is test-ineligible (docs, formatting, mechanical rename, initial configuration), say so in the report and name the alternative validation.

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
| All unit and component tests | `test` |
| Type check and lint | `typecheck`, `lint` |
| Discover E2E specs without starting the server | `e2e` with `--list` |
| One E2E spec | `e2e` with `{{E2E_DIR}}/<flow>.spec.ts` |
| One E2E test by title | `e2e` with `--grep "<title>"` |
| Debug an E2E spec | `e2e` with `--debug {{E2E_DIR}}/<flow>.spec.ts` |
| Open a failure trace | `e2e-trace` with `<test-results>/<run>/trace.zip` |

Run the complete E2E suite (the `e2e` command with no filter) only when the user explicitly asks for it.
