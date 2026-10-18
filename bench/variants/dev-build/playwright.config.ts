import { defineConfig, devices } from '@playwright/test';

// The benchmark runner sets E2E_PORT so parallel workspaces do not collide.
const PORT = Number(process.env.E2E_PORT ?? 4173);
const PROD = Boolean(process.env.CI || process.env.E2E_BUILD);

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  retries: process.env.CI ? 1 : 0,
  reporter: [['list'], ['html', { outputFolder: 'playwright-report', open: 'never' }]],
  outputDir: 'test-results',
  use: {
    baseURL: `http://localhost:${PORT}`,
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
  },
  projects: [{ name: 'chromium', use: { ...devices['Desktop Chrome'] } }],
  webServer: {
    // Iteration runs against the dev server; e2e-build and CI against the production build.
    command: PROD
      ? `pnpm run build && pnpm run preview --port ${PORT} --strictPort`
      : `pnpm run dev --port ${PORT} --strictPort`,
    port: PORT,
    reuseExistingServer: false,
    timeout: PROD ? 120_000 : 60_000,
  },
});
