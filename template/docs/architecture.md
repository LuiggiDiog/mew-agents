# Architecture

This file maps the project structure and its boundaries. Update it in the same change whenever a module, layer, or route group is added.

## Current state

Describe what exists today in two or three sentences: entry points, feature modules, data sources, and which test layers are configured.

## Stack

| Concern | Choice |
| --- | --- |
| Runtime | Node.js {{NODE_VERSION}} |
| Package manager | `{{PM}}` |
| Framework | {{STACK}} (docs: {{FRAMEWORK_DOCS}}) |
| Source | {{SOURCE_DIR}} |
| Design tokens | `{{STYLE_TOKENS_FILE}}` (see `DESIGN.md`) |
| Unit tests | see `docs/testing.md` |
| E2E tests | Playwright, `{{E2E_DIR}}` (see `docs/e2e-playbook.md`) |

## Target layout

Create folders only when a feature needs them.

{{STACK:layout}}

## Boundaries

- Routes and views compose; they do not hold business rules.
- Components render data and emit user intent. They never call a repository or external API directly.
- Services own business rules and are the main unit-test target. They depend on repository or API-client interfaces, so tests inject fakes.
- Validate all external input at the boundary.
- Secrets and server-only code stay on the server.

## Testing map

{{STACK:testing-map}}
