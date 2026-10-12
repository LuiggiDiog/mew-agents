# Stack: Next.js App Router

Snippets for `{{STACK:<name>}}` markers. Each `###` section body replaces the marker with the same name. Based on a Next.js 16 App Router project with React 19, TypeScript, Tailwind CSS v4, Vitest, and Playwright.

### profile-defaults

| Variable | Typical value |
| --- | --- |
| `{{PM}}` / `{{PM_EXEC}}` | `pnpm` / `pnpm exec` |
| `{{FRAMEWORK_DOCS}}` | `` `node_modules/next/dist/docs/` `` (the guides for the installed version) |
| `{{SOURCE_DIR}}` | `` `app/` (routes) and `modules/` (features) `` |
| `{{STYLE_TOKENS_FILE}}` | `app/globals.css` |
| `{{E2E_DIR}}` / `{{E2E_CONFIG}}` | `tests/e2e` / `playwright.config.ts` |
| `{{CMD_DEV}}` / `{{CMD_BUILD}}` | `pnpm dev` / `pnpm build` |
| `{{CMD_LINT}}` / `{{CMD_TYPECHECK}}` | `pnpm lint` / `pnpm typecheck` |
| `{{CMD_TEST}}` / `{{CMD_TEST_WATCH}}` / `{{CMD_TEST_FILE}}` | `pnpm test` / `pnpm test:watch` / `pnpm test <file>` |
| `{{CMD_E2E}}` | `pnpm exec playwright test` |

### toolchain

- Next.js App Router (`app/` at the repo root), React, TypeScript `strict`, Tailwind CSS v4, ESLint flat config (`eslint.config.mjs`).
- Import alias: `@/*` maps to the repo root.
- Before using any Next.js API (routing, caching, data fetching, Server Actions, metadata, config), read the matching guide in `node_modules/next/dist/docs/`. The installed version may differ from training data.
- `next dev` writes and re-adds the `<!-- BEGIN:nextjs-agent-rules -->` block in `AGENTS.md`. Leave it in place.

### architecture

- Keep `app/` thin: routes, layouts, and route-level composition. Put feature code outside `app/` and import it.
- Default to Server Components; add `"use client"` only where interactivity or browser APIs require it, and keep client boundaries as low in the tree as possible.
- Server Components, Route Handlers, and Server Actions call services directly. The app never calls its own HTTP API from the server.
- Validate all external input at the boundary (Route Handler, Server Action, repository response).

### ui-rules

- One component per file where practical. Typed props. Keep components focused; extract logic when a component grows or mixes concerns.
- Avoid deeply nested component definitions in a single file.
- Co-locate component and behavior tests next to the code they cover.
- Semantic HTML and native controls first; every control has an accessible name and visible focus. Do not convey meaning by color alone.

```tsx
type PropsT = {
  title: string;
};

export default function WelcomeHello(props: PropsT) {
  const { title } = props;

  return <h1>{title}</h1>;
}
```

### test-layers

- Unit and component tests: Vitest + Testing Library, co-located as `*.test.ts` / `*.test.tsx`. Test pure logic and services without network or real providers; use fakes or mocks at external boundaries only.
- End-to-end tests: Playwright, in `tests/e2e/*.spec.ts`. Use them for user-visible flows across routes, and for async Server Components, which Vitest cannot render.

### testing-map

| Behavior | Layer |
| --- | --- |
| Business rule, calculation, mapping, validation | Vitest unit test on the service |
| Client Component interaction or rendering | Vitest + Testing Library |
| Synchronous Server Component rendering | Vitest + Testing Library |
| Route Handler | Vitest (call the handler) or E2E |
| Async Server Component, routing, redirects, full flow | Playwright E2E |

Vitest does not support async Server Components. Cover them with E2E, and keep their logic in services that can be unit tested.

### layout

```txt
app/                      # Routes, layouts, route-level composition only
  (group)/route/page.tsx
  api/<resource>/route.ts # Route Handlers: parse, validate, delegate to services
modules/
  <feature>/
    components/           # UI pieces for this feature (+ co-located *.test.tsx)
    services/             # Business logic and orchestration (+ *.test.ts)
    repositories/         # Data access behind a narrow interface
    types/
    mocks/                # Fakes used by tests
shared/                   # Only code that is genuinely reused by 2+ modules
tests/
  e2e/                    # Playwright specs, pages/, helpers/, fixtures/
docs/                     # All project documentation except the root files
```

```mermaid
flowchart LR
  ROUTE[app/ route or layout] --> COMP[modules/*/components]
  ROUTE --> SVC[modules/*/services]
  HANDLER[app/api Route Handler] --> SVC
  ACTION[Server Action] --> SVC
  SVC --> REPO[modules/*/repositories]
  REPO --> DATA[(External API / DB)]
```

### testing-setup

Unit and component tests (installed as dev dependencies: `vitest`, `@vitejs/plugin-react`, `jsdom`, `@testing-library/react`, `@testing-library/dom`, `@testing-library/jest-dom`, `@testing-library/user-event`):

```bash
pnpm add -D vitest @vitejs/plugin-react jsdom @testing-library/react @testing-library/dom @testing-library/jest-dom @testing-library/user-event
```

`vitest.config.mts`:

```ts
import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  resolve: { tsconfigPaths: true },
  test: {
    environment: "jsdom",
    setupFiles: ["./vitest.setup.ts"],
    // Explicit include keeps Vitest away from Playwright *.spec.ts files.
    include: ["**/*.test.{ts,tsx}"],
    exclude: ["node_modules/**", ".next/**", "tests/e2e/**"],
  },
});
```

`vitest.setup.ts`:

```ts
import "@testing-library/jest-dom/vitest";
import { cleanup } from "@testing-library/react";
import { afterEach } from "vitest";

afterEach(() => {
  cleanup();
});
```

Conventions: query the DOM by role and accessible name, then label, then text, test ID last. Simulate interactions with `@testing-library/user-event`. Node-only tests can declare `// @vitest-environment node`.

End-to-end tests (`@playwright/test` with Chromium; `pnpm exec playwright install chromium` once per machine):

`playwright.config.ts`:

```ts
import { defineConfig, devices } from "@playwright/test";

const PORT = 3107;
const BASE_URL = `http://127.0.0.1:${PORT}`;

export default defineConfig({
  testDir: "./tests/e2e",
  fullyParallel: true,
  forbidOnly: Boolean(process.env.CI),
  retries: process.env.CI ? 1 : 0,
  // An auto-opened HTML report keeps the process alive after a failure.
  reporter: [["list"], ["html", { open: "never" }]],
  use: {
    baseURL: BASE_URL,
    trace: "retain-on-failure",
    screenshot: "only-on-failure",
  },
  projects: [{ name: "chromium", use: { ...devices["Desktop Chrome"] } }],
  webServer: {
    // E2E runs against a production build on a dedicated port.
    command: `pnpm build && pnpm start --hostname 127.0.0.1 --port ${PORT}`,
    url: BASE_URL,
    reuseExistingServer: false,
    timeout: 180_000,
    env: {
      // Test-only values and fake providers go here. Never real secrets.
    },
  },
});
```

The dedicated port avoids clashing with `pnpm dev` on 3000. Expect the first step of each run to be the build.

`package.json` scripts and `engines`:

```json
{
  "engines": { "node": ">=24" },
  "scripts": {
    "typecheck": "tsc --noEmit",
    "test": "vitest run",
    "test:watch": "vitest",
    "test:e2e": "playwright test",
    "test:e2e:ui": "playwright test --ui",
    "test:e2e:report": "playwright show-report"
  }
}
```

`.gitignore` additions: `/test-results/`, `/playwright-report/`, `/blob-report/`, `/playwright/.cache/`, and `!.env.example` after `.env*`.

### e2e-gotchas

**Server-side fetches:** `page.route()` only intercepts requests made by the browser. Fetches made by Server Components, Route Handlers, or Server Actions run on the Next.js server and are invisible to it. Fake those through test-only env vars in `webServer.env` (for example, pointing a provider base URL at a local fake) or a fake adapter selected by env.

**Hydration:** in client-interactive pages, assert an element that only appears or enables after hydration before interacting; a click before hydration does nothing.

| Symptom | Typical cause | Fix |
| --- | --- | --- |
| `page.route` mock has no effect | Request is made on the Next.js server | Fake through `webServer.env` or a fake adapter |
| Click does nothing right after load | Interaction before hydration | Assert a hydrated-only state first |
