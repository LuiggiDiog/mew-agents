---
version: alpha
name: "{{PROJECT_NAME}}"
description: "Design standards for {{PROJECT_NAME}}. Sections that say 'Not defined yet' carry no rule."
# Tokens are normative; the prose below explains how to apply them.
# Reference other tokens with {path.to.token}, for example {colors.primary}.
colors: {}
  # primary: '#0D7665'
  # on-primary: '#FFFFFF'
  # surface: '#FFFFFF'
  # on-surface: '#24343E'
  # error: '#BA4949'
typography: {}
  # body-md:
  #   fontFamily: 'system-ui'
  #   fontSize: 16px
  #   fontWeight: 400
  #   lineHeight: 1.5
spacing: {}
  # xs: 4px
  # sm: 8px
  # md: 16px
rounded: {}
  # sm: 6px
  # md: 10px
  # full: 9999px
components: {}
  # button-primary:
  #   backgroundColor: '{colors.primary}'
  #   textColor: '{colors.on-primary}'
  #   typography: '{typography.label-md}'
  #   rounded: '{rounded.md}'
---

# {{PROJECT_NAME}} design system

## Overview

This file is the design source of truth for UI work in this repository. It follows the [Google Labs DESIGN.md format](https://github.com/google-labs-code/design.md): the YAML frontmatter holds exact tokens, and the `##` sections below, in the order the format fixes, explain how to apply them. Tokens are implemented in `{{STYLE_TOKENS_FILE}}`; update this file and the stylesheet together. Validate edits with `npx @google/design.md lint DESIGN.md`; export tokens with `npx @google/design.md export --format css-tailwind DESIGN.md` when the stylesheet should be generated from them.

How agents use this file:

- Read it before any UI change (see the Design section in `AGENTS.md`).
- A section that says "Not defined yet" has no rule. Follow the existing UI and propose the rule here in the same change; do not invent a parallel convention.
- When no specific rule or token applies, this Overview is the foundational context for style decisions, so fill it first.
- A section that deliberately does not apply goes in the `omitted` frontmatter list with a reason, instead of staying empty.
- When a change adds a reusable token, component rule, or accessibility check, record it here.

Describe in one paragraph what the product is, who uses it, and how the interface should feel (calm, dense, playful, editorial, ...). Not defined yet.

## Colors

Palette and roles. Define at least `primary`; the conventional order is primary, secondary, tertiary, neutral, and the recommended names are `primary`, `secondary`, `tertiary`, `neutral`, `surface`, `on-surface`, `error`, with `on-*` pairs for text over a colored surface. State the allowed foreground/background pairings and the contrast rule for new pairs (WCAG 2.2: 4.5:1 for normal text, 3:1 for large text and essential UI; the linter checks `contrast-ratio`). Color is never the only carrier of meaning. Not defined yet.

## Typography

Type scale, usually 9 to 15 levels across headline, display, body, label, and caption, with the recommended names `headline-display`, `headline-lg`, `headline-md`, `body-lg`, `body-md`, `body-sm`, `label-lg`, `label-md`, `label-sm`. Each token sets `fontFamily`, `fontSize`, `fontWeight`, `lineHeight` (unitless preferred), and `letterSpacing` when needed. State the base reading size, the minimum supporting size, and the 200% text-resize expectation. Not defined yet.

## Layout

Grid model and spacing strategy; tokens map to `spacing` (`xs`, `sm`, `md`, `lg`, `xl`). State container widths and the reflow expectation (no page-level horizontal scroll at 320 CSS pixels). Not defined yet.

### Responsive behavior

Breakpoints and what changes at each one (navigation, columns, floating controls, tables). Not defined yet.

### Responsive verification

The viewport widths, zoom levels, and screens to check after a layout change, and what must remain visible and operable. Not defined yet.

## Elevation & Depth

How hierarchy is expressed: shadows (spread, blur, color) or, for flat designs, borders and color contrast. State what a shadow may never be the sole boundary for. Not defined yet.

## Shapes

Corner radius and shape language; tokens map to `rounded` (`none`, `sm`, `md`, `lg`, `xl`, `full`). Also the minimum interactive target size and the focus-ring style (token, width, offset, shape) as project rules. Not defined yet.

## Components

Rules per component atom (buttons, inputs, chips, lists, tooltips, checkboxes, radio buttons, dialogs, toasts, tables, empty/loading/error states). Tokens map to `components`, each a map of `backgroundColor`, `textColor`, `typography`, `rounded`, `padding`, `size`, `height`, `width` with token references, and variants as sibling keys (`button-primary`, `button-primary-hover`). Each rule names the states that must be distinguishable without color alone. Not defined yet.

## Do's and Don'ts

Short paired rules that prevent recurring mistakes, added as they are found. Not defined yet.
