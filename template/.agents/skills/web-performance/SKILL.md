---
name: web-performance
description: Use to measure and improve the Lighthouse scores (performance, accessibility, best practices, SEO) of key routes, or when a change risks them (images, fonts, third-party scripts, new client dependencies, routing, build configuration). Skip for service-only or test-only work.
---

# Web performance workflow

1. `AGENTS.md` is normally already in context; read it only if it is not. Commands named below are defined in its Toolchain section. Read `lighthouserc.json` (key routes and thresholds) and, before changing framework behavior, the framework documentation for the installed version ({{FRAMEWORK_DOCS}}).
2. Measure first. Run `build` unless `e2e-build` already wrote a production build to disk for this code (see the stack note in `docs/testing.md`); then run `lighthouse` and summarize with `node .agents/skills/web-performance/scripts/lighthouse-audits.mjs`, which prints per route the median scores and the audits that cost points. `lighthouse` uses the installed Chrome; without one, set `CHROME_PATH` to Playwright's Chromium (`node -e "console.log(require('@playwright/test').chromium.executablePath())"`). `lighthouse` needs `@lhci/cli` as a dev dependency; if it is missing, run `@lhci/cli autorun` once through the one-off package form in the Toolchain section of `AGENTS.md` and report the missing dependency as a follow-up instead of adding it.
3. Prioritize: categories below their threshold first, then budgets over their limit (LCP 2.5 s, CLS 0.1, TBT 200 ms); within Performance, the metric with the largest gap (usually LCP, then TBT, then CLS). Every assertion uses the median of the 3 runs, so a single slow run does not fail or pass it. INP cannot be measured in the lab: TBT is its proxy, and field data (CrUX or the `web-vitals` library) is the only real INP source. Accessibility fixes follow the `ui-accessibility` skill.
4. Fix one cause at a time with the smallest change, following the Performance rules in `AGENTS.md`, the checklist, and the stack rules below. A fix that changes behavior (lazy loading a component, deferring a script) keeps its tests green, and gets a test first when it adds behavior.
5. Re-measure the affected routes and compare medians; Lighthouse varies between runs, so a change under 3 points is noise. Then run the level 2 test selection once.
6. Never lower a threshold or budget, remove a route, or disable an audit to pass, and never remove a feature for score. If a threshold cannot be met (for example, a required third-party script), report the audit, its cost, and the options.
7. Report a before-and-after table per route and category, the causes fixed, the commands run, and what remains below threshold.

## Checklist

**Performance**

- LCP: the LCP image is in the initial HTML, never lazy-loaded, with `fetchpriority="high"`, explicit dimensions, and AVIF or WebP at the rendered size. No render-blocking CSS or font loads ahead of it.
- TBT: code split per route, no long tasks during load, heavy work deferred or moved off the main thread, third-party scripts loaded after the page.
- CLS: dimensions or `aspect-ratio` on media and embeds, space reserved for late content, fonts with `font-display: swap` and a metric-matched fallback.
- Network: text compressed (gzip or brotli), hashed static assets with long cache lifetimes, `preconnect` to required origins, no unused JavaScript or CSS shipped on the route.

**Accessibility** (see `ui-accessibility`): names on controls and links, contrast, `lang`, heading order, `alt`, form labels.

**Best practices**: HTTPS resources only, no console errors, no deprecated APIs, images at their natural aspect ratio and sufficient resolution.

**SEO**: unique `<title>` and meta description per page, viewport meta, `lang`, crawlable `<a href>` links with descriptive text, a valid `robots.txt` (an SPA fallback that serves `index.html` for it fails the audit), a canonical URL on indexable pages, and HTTP 200 on audited routes.

## Stack rules

{{STACK:performance}}
