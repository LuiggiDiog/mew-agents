---
name: tdd-change
description: Use for any behavior change, bug fix, or new feature in services, components, routes, or API handlers. Drives the test-first loop. Skip for docs-only, formatting-only, or initial configuration work.
---

# Test-first change workflow

1. `AGENTS.md` is normally already in context; read it only if it is not. Commands named below are defined in its Toolchain section. Read only the parts of `docs/architecture.md` and `docs/testing.md` that cover the area you change. Trace the behavior from the route or component through the service to the data access layer. Before using a framework API, read its documentation for the installed version ({{FRAMEWORK_DOCS}}).
2. State the expected behavior in one or two observable sentences. Pick the lowest test layer that proves it, using the table in `docs/testing.md`: unit test on a service, component test, or E2E only for behavior lower layers cannot prove.
3. Red: write or update the smallest test that expresses the behavior. For a bug, reproduce it. Run only that test with `test-file` and confirm it fails for the expected reason.
4. Green: implement the minimum change in the right layer. Keep business rules in services, data access in repositories, and routes or views thin. Re-run only the focused test while iterating.
5. Refactor with the test green, without adding behavior. When all tasks are green, climb the test selection ladder from level 2 (`test-related` with the touched files), and run `lint-files` and `typecheck` once.
6. Update `docs/architecture.md` when a module or layer is added, `docs/testing.md` when test configuration or scripts change, and add a note in `docs/context/` when a bug's root cause was not obvious.
7. Report the behavior, the test that went red then green, the files changed, the exact commands run, and the ladder level reached. If TDD was skipped, say why and what validated the change instead.
