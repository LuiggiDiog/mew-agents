---
name: tdd-change
description: Use for any behavior change, bug fix, or new feature in services, components, routes, or API handlers. Drives the test-first loop. Skip for docs-only, formatting-only, or initial configuration work.
---

# Test-first change workflow

1. Read `AGENTS.md`, `docs/architecture.md`, and `docs/testing.md`. Trace the behavior from the route or component through the service to the data access layer. Before using a framework API, read its documentation for the installed version ({{FRAMEWORK_DOCS}}). Commands named below (`test-file`, `e2e`, ...) are defined in the Toolchain section of `AGENTS.md`.
2. State the expected behavior in one or two observable sentences. Pick the lowest test layer that proves it, using the table in `docs/testing.md`: unit test on a service, component test, or E2E only for behavior lower layers cannot prove.
3. Red: write or update the smallest test that expresses the behavior. For a bug, reproduce it. Run only that test with the `test-file` command and confirm it fails for the expected reason.
4. Green: implement the minimum change in the right layer. Keep business rules in services, data access in repositories, and routes or views thin.
5. Refactor with the test green, without adding behavior. Re-run the focused test, then the `typecheck` and `lint` commands on touched files if types or imports changed.
6. Update `docs/architecture.md` when a module or layer is added, `docs/testing.md` when test configuration or scripts change, and add a note in `docs/context/` when a bug's root cause was not obvious.
7. Report the behavior, the test that went red then green, the files changed, and the exact commands run. If TDD was skipped, say why and what validated the change instead.
