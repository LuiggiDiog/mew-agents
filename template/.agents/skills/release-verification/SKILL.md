---
name: release-verification
description: Use for regression review, release readiness, verifying a finished change, an explicitly requested full test run, or an explicitly requested deployment. Skip for routine feature implementation.
---

# Verification and release workflow

1. Read `AGENTS.md` and `docs/testing.md`, then inspect the current diff (`git status`, `git diff`). Select checks from the changed files: focused unit test files (`{{CMD_TEST_FILE}}`), focused Playwright specs (`{{CMD_E2E}} <spec>`), `{{CMD_TYPECHECK}}`, `{{CMD_LINT}}`, and `{{CMD_BUILD}}` only when integration or production behavior matters.
2. Run checks with Node {{NODE_VERSION}} and `{{PM}}`. If a script or test layer does not exist yet, say so instead of inventing a substitute.
3. Run the complete E2E suite only when the current user request explicitly asks for it. Never use real secrets or paid providers in tests.
4. If deployment is explicitly requested for the current work, confirm the production build passes, required environment variables are documented in `.env.example`, and no local secrets or tooling files ship. Deploy only after those checks, then verify the deployed URL and the changed routes.
5. Before attributing a failure to the current change, check whether it also fails without it. Report the exact commands, outcomes, failure locations, skipped checks, and the practical limits of what was verified. Do not stage or commit anything.
