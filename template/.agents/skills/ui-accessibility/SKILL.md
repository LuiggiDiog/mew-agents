---
name: ui-accessibility
description: Use for interface, layout, responsive design, form, copy, styling, or accessibility changes in components and views. Skip for service-only or data-only work.
---

# Interface workflow

1. `AGENTS.md` is already in context; do not re-read it. Commands named below are defined in its Toolchain section. Read `DESIGN.md` and the parts of `docs/architecture.md` that cover the screen. Inspect the component, its route, adjacent screens, and the existing tokens in `{{STYLE_TOKENS_FILE}}`. Read the framework documentation for the installed version ({{FRAMEWORK_DOCS}}) before changing framework behavior (layouts, images, fonts, metadata, navigation).
2. Apply `DESIGN.md`. If it has no rule for the case, follow the existing UI and propose the missing rule in `DESIGN.md` in the same change; do not invent a parallel convention. When adding a reusable token or rule, update `DESIGN.md` and the stylesheet together, and validate with `design-lint`.
3. Follow the UI rules in `AGENTS.md`: one component per file or folder, typed inputs, focused responsibilities, logic extracted when a component grows.
4. Use semantic HTML and native controls first. Every control has an accessible name, visible focus, and a sufficient target size. Do not convey meaning by color alone. Give loading, empty, error, and success states visible text.
5. Keep layouts responsive from mobile up, and support the themes the project defines. Reuse existing tokens; add a new one only when it will be reused.
6. Test behavior changes first with the component test layer, querying by role and accessible name. For cross-route behavior or widgets the unit layer cannot render, use a focused Playwright spec (`e2e-playwright` skill). Style-only changes run no unit tests; they are inspected.
7. When layout changes, inspect the affected screen at the widths `DESIGN.md` lists (or representative mobile and desktop widths if it lists none). To audit or improve the mobile experience of existing screens, use the `mobile-ux` skill. Report the accessibility checks actually performed and anything not verified.
