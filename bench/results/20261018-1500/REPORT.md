# Benchmark 20261018-1500

Model `sonnet`, fixture `bench/fixture` (Vite + React, pnpm, 9 unit and 18 E2E tests, 8 s production build). Baseline v1.0.0; deltas are relative to it, ✅ means lower.

## Summary

| Metric | v1.0.0 | v1.2.0 | v1.3.0 | v1.4.0 | v1.5.0 | v1.6.1 |
| --- | --- | --- | --- | --- | --- | --- |
| Runs | 20 | 20 | 20 | 20 | 20 | 20 |
| Hidden acceptance tests passed | 15/20 | 19/20 | 19/20 | 20/20 | 15/20 | 18/20 |
| All suites green after the agent (unit, E2E, typecheck, lint) | 20/20 | 20/20 | 19/20 | 20/20 | 20/20 | 20/20 |
| Test-first, red seen before the fix | 14/15 | 14/15 | 15/15 | 12/15 | 15/15 | 15/15 |
| Wall time per run, min (range) | 0.40 (0.22–0.72) | 0.48 (0.24–0.96) | 0.54 (0.21–0.96) | 0.56 (0.22–1.09) | 0.46 (0.16–0.96) | 0.73 (0.27–1.97) |
| Mean wall time (min) | 0.40 | 0.48 (+21% ⚠️) | 0.54 (+35% ⚠️) | 0.56 (+39% ⚠️) | 0.46 (+16% ⚠️) | 0.73 (+83% ⚠️) |
| Mean time inside checks (s) | 6.47 | 7.74 (+19% ⚠️) | 10.64 (+64% ⚠️) | 10.03 (+55% ⚠️) | 9.60 (+48% ⚠️) | 18.19 (+181% ⚠️) |
| Mean cost (USD) | 0.13 | 0.16 (+23% ⚠️) | 0.18 (+41% ⚠️) | 0.18 (+45% ⚠️) | 0.14 (+6% ⚠️) | 0.18 (+41% ⚠️) |
| Mean turns | 7.35 | 6.20 (-16% ✅) | 6.40 (-13% ✅) | 6.45 (-12% ✅) | 6.10 (-17% ✅) | 7.05 (-4% ✅) |
| Question rounds (total) | 0 | 5 | 8 | 8 | 0 | 4 |
| Unit tests executed by the agent (mean) | 16.65 | 14.50 (-13% ✅) | 16.60 (-0% ✅) | 15.70 (-6% ✅) | 15.20 (-9% ✅) | 17.90 (+8% ⚠️) |
| E2E tests executed by the agent (mean) | 0.95 | 2.10 (+121% ⚠️) | 3.90 (+311% ⚠️) | 3.45 (+263% ⚠️) | 8.05 (+747% ⚠️) | 9.50 (+900% ⚠️) |
| Full unit suite runs (total) | 17 | 15 (-12% ✅) | 22 (+29% ⚠️) | 18 (+6% ⚠️) | 1 (-94% ✅) | 1 (-94% ✅) |
| Full E2E suite runs (total; forbidden without a request) | 0 | 0 | 0 | 0 | 0 | 0 |
| E2E runs paying a production build (mean) | 0.15 | 0.30 (+100% ⚠️) | 0.50 (+233% ⚠️) | 0.45 (+200% ⚠️) | 0.35 (+133% ⚠️) | 0.50 (+233% ⚠️) |
| Repeated file reads with no edit in between (mean) | 0.05 | 0.05 (+0%) | 0.05 (+0%) | 0.25 (+400% ⚠️) | 0.05 (+0%) | 0.15 (+200% ⚠️) |
| Failed tool calls, excluding test runs (mean) | 0.10 | 0.10 (+0%) | 0.05 (-50% ✅) | 0 (-100% ✅) | 0 (-100% ✅) | 0.15 (+50% ⚠️) |
| Files edited more than twice (mean) | 0.05 | 0 (-100% ✅) | 0 (-100% ✅) | 0 (-100% ✅) | 0.05 (+0%) | 0 (-100% ✅) |
| Subagents spawned (total) | 0 | 0 | 0 | 0 | 0 | 0 |

## By task

| Task | Version | Hidden | Suites green | Test-first | Min (mean) | USD (mean) | Questions | E2E tests run (mean) | Check time s (mean) | Failing specs after the agent |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| t1-typo | v1.0.0 | 5/5 | 5/5 | n/a | 0.24 | 0.08 | 0 | 0.0 | 4.2 | — |
| t1-typo | v1.2.0 | 5/5 | 5/5 | n/a | 0.26 | 0.09 | 0 | 0.0 | 4.1 | — |
| t1-typo | v1.3.0 | 5/5 | 5/5 | n/a | 0.23 | 0.09 | 0 | 0.0 | 3.8 | — |
| t1-typo | v1.4.0 | 5/5 | 5/5 | n/a | 0.25 | 0.09 | 0 | 0.0 | 3.8 | — |
| t1-typo | v1.5.0 | 5/5 | 5/5 | n/a | 0.19 | 0.08 | 0 | 0.0 | 2.7 | — |
| t1-typo | v1.6.1 | 5/5 | 5/5 | n/a | 0.37 | 0.11 | 0 | 3.2 | 10.4 | — |
| t2-total | v1.0.0 | 5/5 | 5/5 | 5/5 | 0.37 | 0.13 | 0 | 0.0 | 4.7 | — |
| t2-total | v1.2.0 | 5/5 | 5/5 | 5/5 | 0.32 | 0.12 | 0 | 0.0 | 2.8 | — |
| t2-total | v1.3.0 | 4/5 | 4/5 | 5/5 | 0.34 | 0.12 | 0 | 0.0 | 4.4 | cart-empty.spec.ts, cart.spec.ts, catalog-accessibility.spec.ts, catalog.spec.ts |
| t2-total | v1.4.0 | 5/5 | 5/5 | 5/5 | 0.32 | 0.12 | 0 | 0.0 | 4.3 | — |
| t2-total | v1.5.0 | 5/5 | 5/5 | 5/5 | 0.32 | 0.12 | 0 | 0.0 | 5.0 | — |
| t2-total | v1.6.1 | 5/5 | 5/5 | 5/5 | 0.44 | 0.13 | 0 | 2.0 | 9.9 | — |
| t3-remove | v1.0.0 | 0/5 | 5/5 | 5/5 | 0.52 | 0.16 | 0 | 0.2 | 7.8 | — |
| t3-remove | v1.2.0 | 4/5 | 5/5 | 5/5 | 0.84 | 0.27 | 4 | 4.8 | 14.8 | — |
| t3-remove | v1.3.0 | 5/5 | 5/5 | 5/5 | 0.93 | 0.30 | 5 | 6.6 | 17.8 | — |
| t3-remove | v1.4.0 | 5/5 | 5/5 | 5/5 | 1.02 | 0.32 | 5 | 6.6 | 17.5 | — |
| t3-remove | v1.5.0 | 0/5 | 5/5 | 5/5 | 0.81 | 0.20 | 0 | 21.4 | 17.9 | — |
| t3-remove | v1.6.1 | 3/5 | 5/5 | 5/5 | 1.42 | 0.29 | 3 | 16.6 | 33.3 | — |
| t4-currency | v1.0.0 | 5/5 | 5/5 | 4/5 | 0.46 | 0.14 | 0 | 3.6 | 9.3 | — |
| t4-currency | v1.2.0 | 5/5 | 5/5 | 4/5 | 0.52 | 0.16 | 1 | 3.6 | 9.3 | — |
| t4-currency | v1.3.0 | 5/5 | 5/5 | 5/5 | 0.67 | 0.20 | 3 | 9.0 | 16.6 | — |
| t4-currency | v1.4.0 | 5/5 | 5/5 | 2/5 | 0.63 | 0.21 | 3 | 7.2 | 14.6 | — |
| t4-currency | v1.5.0 | 5/5 | 5/5 | 5/5 | 0.53 | 0.15 | 0 | 10.8 | 12.9 | — |
| t4-currency | v1.6.1 | 5/5 | 5/5 | 5/5 | 0.69 | 0.19 | 1 | 16.2 | 19.2 | — |

## Tasks

- `t1-typo` (trivial): Los botones de los productos dicen "Add to crat". Corrige el typo.
- `t2-total` (small): El total del carrito está mal cuando se agrega el mismo producto más de una vez. Corrígelo.
- `t3-remove` (medium): Permite que el usuario quite productos del carrito. The answer contradicts the natural default (remove the whole row): an agent that does not ask fails the hidden test.
- `t4-currency` (small): Muestra todos los precios en soles peruanos, con el formato "S/ 3.00". formatPrice lives in the cart module but the catalog uses it too: specs tagged @catalog break although no catalog file changes. Selecting E2E specs by touched-module tag alone misses them; the full suite run by the harness catches it.
