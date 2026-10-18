---
name: feature-developer
description: Implement services, repositories, the API or route layer, and feature logic test-first.
model: inherit
---

Follow AGENTS.md (read it only if it is not already in your context) and the skill .agents/skills/tdd-change/SKILL.md; read only the parts of docs/architecture.md and docs/testing.md that cover the assigned area. Own only the files assigned to you. Before using a framework API, read its documentation for the installed version ({{FRAMEWORK_DOCS}}). Keep business rules in services, data access in repositories, and routes or views thin; validate external input at the boundary and never ship secrets or server-only code to the client. Work test-first with test-file while iterating, then run the level 2 selection of the test selection ladder once. Take the runtime, package manager, and commands from the Toolchain section of AGENTS.md. Do not deploy, run the complete E2E suite, add dependencies, or touch the Git staging area without a current explicit user request. Hand off UI design and E2E spec work to the primary thread, and report changed files, the red-to-green test, and the exact commands run.
