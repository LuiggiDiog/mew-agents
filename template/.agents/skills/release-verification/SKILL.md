---
name: release-verification
description: Use for regression review, release readiness, verifying a finished change, an explicitly requested full test run, or an explicitly requested deployment. Skip for routine feature implementation.
---

# Verification and release workflow

1. `AGENTS.md` is normally already in context; read it only if it is not. Commands named below are defined in its Toolchain section. Inspect the current diff (`git status`, `git diff`) and list the touched source files, specs, and modules.
2. Select checks with the test selection ladder from level 2: run `affected` (with the base branch when the work is committed) and execute the unit and E2E commands it prints (`e2e-build` instead of `e2e` when production can differ), then `lint-files` and `typecheck`. Use `build` only when integration or production behavior matters. Never run E2E against a production environment. If a script or test layer does not exist yet, say so instead of inventing a substitute.
3. Run level 4 (the complete unit suite or E2E suite) only when the current user request explicitly asks for it, or for unit tests when test config or dependencies changed. Never use real secrets or paid providers in tests.
4. If deployment is explicitly requested for the current work, confirm the production build passes, required environment variables are documented in `.env.example`, and no local secrets or tooling files ship. Deploy only after those checks, then verify the deployed URL and the changed routes.
5. Before attributing a failure to the current change, check whether it also fails without it. Report the exact commands, the ladder level reached, outcomes, failure locations, skipped checks, and the practical limits of what was verified. Do not stage or commit anything.
