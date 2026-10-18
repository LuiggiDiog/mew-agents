---
name: mobile-ux
description: Use to audit and improve the mobile and responsive experience of existing screens or flows (touch targets, layout and reflow, mobile forms, navigation and overlays, perceived performance), mobile-first and then at desktop widths. Skip for service-only work; for a new component without a mobile concern, use ui-accessibility.
---

# Mobile UX workflow

1. `AGENTS.md` is normally already in context; read it only if it is not. Commands named below are defined in its Toolchain section. Read `DESIGN.md` (Layout, Responsive behavior, Responsive verification, Shapes) and, when writing a mobile spec, the Mobile checks section of `docs/e2e-playbook.md`. Read the framework documentation for the installed version ({{FRAMEWORK_DOCS}}) before changing framework behavior (viewport metadata, layouts, images, fonts).
2. In the requirement round, agree the screens or flows in scope and the widths. Use the widths in `DESIGN.md` Responsive verification; if it lists none, use 320, 375, 768, 1024, and 1440 CSS pixels and propose them there in the same change.
3. Audit mobile-first: each screen at the smallest width, then up to desktop, against the checklist below. Inspect the code (viewport metadata, styles, components) and, when a browser is available, the rendered screen with touch emulation. Record each finding with file and line, checklist item, width, and priority.
4. Fix in priority order within the agreed scope, using the existing tokens in `{{STYLE_TOKENS_FILE}}` and existing components. Write base styles for small screens and enhance with `min-width` media queries. When a fix sets a reusable rule (target size, breakpoint behavior, sheet versus dialog), record it in `DESIGN.md` together with the stylesheet. Findings outside the scope or needing a product decision become follow-ups.
5. Test first where a check can prove the fix: a behavior change gets a component test (`tdd-change`); horizontal overflow and undersized targets get a focused `*.mobile.spec.ts` that fails before the fix, using the helpers in `docs/e2e-playbook.md`. A visual adjustment with no deterministic check is validated by inspection at each width, and the report says so.
6. Validate with the changed spec (`e2e --project=mobile <spec>` while iterating, then once as the level 2 run per Validation in `AGENTS.md`), then `lint-files` and `typecheck` once, then re-inspect each screen at every agreed width.
7. Report findings by priority with their status (fixed or follow-up), the widths and emulated devices checked, the commands run, and what was not verified (real devices, iOS Safari when only Chromium ran, screen readers).

## Checklist

**Critical: touch and access**

- Targets are at least 24×24 CSS px or spaced so they do not overlap (WCAG 2.2 AA); primary and frequent actions are 44×44.
- Nothing depends on hover: hover-revealed actions and tooltips have a tap and keyboard path. Hover-only styling goes inside `@media (hover: hover)`.
- Swipe, drag, pinch, and long-press have a visible single-tap alternative.
- Zoom is never blocked: viewport is `width=device-width, initial-scale=1`, without `user-scalable=no` or `maximum-scale=1`.
- Focus is visible, and sticky headers or bottom bars never cover the focused element (`scroll-padding` equal to the bar height).

**High: layout and reflow**

- No page-level horizontal scroll at 320 px (WCAG 1.4.10). Wide content (tables, code, carousels) scrolls inside its own container, or tables stack as cards. Never mask overflow with `overflow-x: hidden` on `html` or `body`.
- Long text wraps (`overflow-wrap: anywhere` for URLs and IDs); flex children that truncate have `min-width: 0`.
- Full-height layouts use `dvh` or `svh`, not `100vh`. Fixed and full-bleed elements respect `env(safe-area-inset-*)` (with `viewport-fit=cover`).
- Primary actions sit in thumb reach on mobile: bottom of the screen, or a sticky bottom CTA that does not cover content.
- Portrait and landscape both work; orientation is never locked.
- Body text is at least 16 px with a line height near 1.5, and survives 200% text resize.

**High: navigation and overlays**

- Mobile navigation is reachable and labeled: a bottom bar with at most 5 items, or a menu button with an accessible name and `aria-expanded`.
- Browser back returns to the previous meaningful state; tabs, filters, pagination, and steps live in the URL.
- On mobile, dialogs become full-screen or bottom sheets: they scroll internally (`overscroll-behavior: contain`), keep focus inside, close with a visible button, and return focus on close.
- Destructive actions ask for confirmation or offer undo.

**Medium: mobile forms**

- Inputs have the right `type`, `inputmode`, `autocomplete`, and `enterkeyhint`, and a visible label (never placeholder-only).
- Input font size is at least 16 px, so iOS Safari does not zoom on focus.
- The virtual keyboard never hides the focused field or the submit button. Errors appear as text next to the field, and focus moves to the first error on submit.
- Paste is never blocked; no `autofocus` on mobile.

**Medium: perceived performance and motion**

- Images set `width` and `height` (or `aspect-ratio`), responsive `srcset` and `sizes`, and `loading="lazy"` below the fold, so layout shift stays under 0.1 CLS.
- Every tap gets feedback within about 100 ms (pressed state, spinner, or skeleton); submit buttons disable while pending to prevent double submission.
- Custom interactive elements set `touch-action: manipulation`; `-webkit-tap-highlight-color` is changed only when a visible pressed state replaces it.
- Animations use only `transform` and `opacity`, never `transition: all`, and respect `prefers-reduced-motion`.
