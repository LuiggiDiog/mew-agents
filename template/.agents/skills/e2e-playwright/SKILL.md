---
name: e2e-playwright
description: Use to design, write, debug, or stabilize Playwright end-to-end specs, page objects, and helpers under {{E2E_DIR}}, or to verify a user-visible flow in a real browser. Skip for unit-testable logic.
---

# E2E workflow

1. Read `AGENTS.md` (E2E policy) and `docs/e2e-playbook.md`, including its stack-specific gotchas. Configuration is in `{{E2E_CONFIG}}`. Commands named below (`test-file`, `e2e`, ...) are defined in the Toolchain section of `AGENTS.md`.
2. Write the flow map first: routes, user actions, expected destination URLs, state each step creates, and external dependencies. Decide real vs mock per step with the playbook's matrix, and respect what `page.route()` can and cannot intercept in this stack.
3. Reuse or create one page object per page in `{{E2E_DIR}}/pages/` with `assertLoaded()`. Put shared waits and setup in `{{E2E_DIR}}/helpers/`. Prefer isolated tests; use `test.describe.serial` only for true dependent journeys.
4. For a new behavior, write the spec first and run it to see it fail on the missing behavior, then hand off or implement the minimum change. Locate by role and accessible name, then label, then test ID. Assert exact URLs and readiness (visible value, enabled CTA). Never synchronize with `waitForTimeout`. Generate unique data at runtime; retry only known conflicts, bounded to 3–5 attempts.
5. Validate with the `e2e` command and `--list`, then only the changed spec or `--grep` title. Do not run the complete suite unless the current user request explicitly asks for it.
6. For flaky or failing specs, open the trace first. Identify the root cause (overlay, strict-mode match, weak success condition, stack-specific causes from the playbook's failure table) before raising any timeout.
7. Update flow documentation in the same change. Report the specs run, results, trace findings, and anything left unverified.
