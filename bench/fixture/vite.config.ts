/// <reference types="vitest/config" />
import { defineConfig, type Plugin } from 'vite';
import react from '@vitejs/plugin-react';

// Production builds of real projects take minutes. This keeps a fixed cost on
// `vite build` so test runs that pay for a build cost what they would in practice.
const productionBuildCost: Plugin = {
  name: 'production-build-cost',
  apply: 'build',
  buildStart: () => new Promise((resolve) => setTimeout(resolve, 8000)),
};

export default defineConfig({
  plugins: [react(), productionBuildCost],
  test: {
    environment: 'jsdom',
    setupFiles: ['./src/setupTests.ts'],
    include: ['src/**/*.test.{ts,tsx}'],
  },
});
