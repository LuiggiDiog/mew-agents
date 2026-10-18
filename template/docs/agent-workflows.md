# Agent workflows

This repository works with both Claude Code and Codex. Both read the same rules (`AGENTS.md`), the same docs (`docs/`), and the same skills. Only the agent profile format differs.

The primary thread (the session you talk to) is the **orchestrator**. It owns the complete user request, the constraints in `AGENTS.md`, task breakdown, integration, validation, and the final report. Specialists are optional: use them for bounded, independent work.

## Where things live

| What            | Claude Code                         | Codex                           |
| --------------- | ----------------------------------- | ------------------------------- |
| Project rules   | `CLAUDE.md` → imports `AGENTS.md`   | `AGENTS.md`                     |
| Skills          | `.claude/skills/` (symlink)         | `.agents/skills/`               |
| Agent profiles  | `.claude/agents/*.md`               | `.codex/agents/*.toml`          |
| Session config  | `.claude/settings.json`             | `.codex/config.toml`            |

`.claude/skills` is a symlink to `.agents/skills`, so each skill is written once. Agent profiles exist in both formats with the same instructions; when you change one, change its counterpart in the same commit.

## Agent profiles

| Claude Code           | Codex                 | Model (Claude / Codex)   | Use it for                                                                  |
| --------------------- | --------------------- | ------------------------ | --------------------------------------------------------------------------- |
| `feature-developer`   | `feature_developer`   | inherit / GPT-6 Sol high | Services, repositories, API/route logic, data access, test-first.   |
| `product-ui`          | `product_ui`          | Sonnet / GPT-6 Luna high | Bounded React components, layout, styling, copy, accessibility.             |
| `e2e-engineer`        | `e2e_engineer`        | inherit / GPT-6 Sol high | Playwright specs, page objects, helpers; debugging and de-flaking.          |
| `quality-reviewer`    | `quality_reviewer`    | inherit / GPT-6 Sol high | Read-only diff review: bugs, boundaries, accessibility, missing tests.      |
| `verification-runner` | `verification_runner` | Sonnet / GPT-6 Luna med. | Focused tests, typecheck, and lint, with clear failure reports.             |

The stronger model goes to work with coupled correctness constraints (business logic, flaky E2E diagnosis, review). The economical model fits bounded UI work and mechanical verification.

## Skills by task

| Skill                  | Apply when                                                                                       |
| ---------------------- | ------------------------------------------------------------------------------------------------ |
| `tdd-change`           | Any behavior change, bug fix, or new feature.                                                    |
| `e2e-playwright`       | Writing, debugging, or stabilizing E2E specs, or verifying a flow in a browser.                  |
| `ui-accessibility`     | Changing screens, components, layout, styling, copy, or accessibility.                           |
| `mobile-ux`            | Auditing and improving the mobile and responsive experience of existing screens or flows.        |
| `web-performance`      | Measuring and improving Lighthouse scores, or changes that risk them.                            |
| `release-verification` | Reviewing regressions, verifying a finished change, or an explicitly requested full run/deploy.  |

## Orchestration rules

The binding policy is the Agent orchestration section of `AGENTS.md`: the primary thread works alone by default and delegates only when parallel work finishes sooner and integrates quickly. How that plays out:

- Small task (a few edits, one layer): the primary thread does it alone. No profile is used.
- Broad investigation across separate areas: up to 3 read-only searches in parallel, then the primary thread decides.
- Large feature across layers: the primary thread first fixes the contract (types, route, props). Then `feature-developer` (service) and `product-ui` (component) work in parallel on disjoint files, and `e2e-engineer` joins only if the flow needs a spec. The primary thread integrates and runs the level 2 test selection once.
- Review of a finished diff: `quality-reviewer` and `verification-runner` in parallel, both read-only on product source.
- Profiles and skills never override the user's current instructions, especially on deployment, running the complete E2E suite, adding dependencies, or using paid providers.

## Context for every agent

- `AGENTS.md`: binding rules (communication, toolchain, architecture, TDD, E2E, validation). Its Toolchain section is the only source for the runtime, the package manager, and the exact commands that skills and profiles name.
- `docs/architecture.md`: structure, layers, and boundaries.
- `docs/testing.md`: test layers, setup, and which command to use for each goal.
- `docs/e2e-playbook.md`: Playwright patterns, anti-flake rules, and failure signatures.
- `DESIGN.md`: design tokens, component rules, and accessibility checks for UI work.
- {{FRAMEWORK_DOCS}}: the framework documentation for the installed version. Read before using a framework API.

## How to request work

Describe the outcome to the primary thread from the repository root. Name a specialist only when you want to steer the assignment. For example:

- "Add a search filter to the list page; use the feature developer for the service and the UI specialist for the form, test-first, then run focused checks."
- "Write an E2E spec for the sign-up flow with the E2E engineer and run only that spec."
- "Review the current diff for boundary violations and missing tests without changing files."

Skills can also be invoked by name (`/tdd-change` in Claude Code; by name in Codex). Start a new session after adding or changing profiles or skills if the current one does not show them.
