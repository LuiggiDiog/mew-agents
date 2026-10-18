---
name: e2e-playwright
description: Use to design, write, debug, or stabilize Playwright end-to-end specs, page objects, and helpers under {{E2E_DIR}}, or to verify a user-visible flow in a real browser. Skip for unit-testable logic.
---

# E2E workflow

1. `AGENTS.md` is normally already in context; read it only if it is not. Commands named below are defined in its Toolchain section. Read the sections of `docs/e2e-playbook.md` the task needs, always including its stack-specific gotchas. Configuration is in `{{E2E_CONFIG}}`.
2. Write the flow map first: routes, user actions, expected destination URLs, state each step creates, and external dependencies. Decide real vs mock per step with the playbook's matrix, and respect what `page.route()` can and cannot intercept in this stack.
3. Reuse or create one page object per page in `{{E2E_DIR}}/pages/` with `assertLoaded()`, and shared waits and setup in `{{E2E_DIR}}/helpers/`. Tag each spec with the module it covers (`@<module>`).
4. For a new behavior, write the spec first and run it to see it fail on the missing behavior, then hand off or implement the minimum change. Apply the E2E policy in `AGENTS.md` (locators, deterministic waits, exact URLs, readiness, unique data, bounded retries).
5. Validate with `e2e --list` after structural edits, then follow the test selection ladder: the changed spec with `-x` on the dev server while iterating, then the level 2 selection that `affected` prints, once, on the dev server (`e2e-build` only when production can differ, see Validation in `AGENTS.md`; never accepting an empty selection), and `--last-failed` after a fix. E2E runs only against local or test environments, never production. Never run the complete suite unless the current user request explicitly asks for it.
6. For flaky or failing specs, open the trace first. Identify the root cause (overlay, strict-mode match, weak success condition, stack-specific causes from the playbook's failure table) before raising any timeout.
7. Update flow documentation in the same change. Report the specs run, the ladder level reached, results, trace findings, and anything left unverified.
