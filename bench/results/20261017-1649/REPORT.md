# Benchmark 20261017-1649

Model `sonnet`, fixture `bench/fixture` (Vite + React, pnpm, 9 unit and 18 E2E tests, 8 s production build). Baseline v1.2.0; deltas are relative to it, ✅ means lower.

## Summary

| Metric | v1.2.0 | v1.5.1 |
| --- | --- | --- |
| Runs | 12 | 12 |
| Hidden acceptance tests passed | 12/12 | 9/12 |
| All suites green after the agent (unit, E2E, typecheck, lint) | 12/12 | 12/12 |
| Test-first, red seen before the fix | 9/9 | 9/9 |
| Wall time per run, min (range) | 0.47 (0.18–0.91) | 0.52 (0.15–0.89) |
| Mean wall time (min) | 0.47 | 0.52 (+11% ⚠️) |
| Mean time inside checks (s) | 7.10 | 10.02 (+41% ⚠️) |
| Mean cost (USD) | 0.16 | 0.15 (-5% ✅) |
| Mean turns | 6.50 | 6.83 (+5% ⚠️) |
| Question rounds (total) | 3 | 0 |
| Unit tests executed by the agent (mean) | 17.75 | 16.08 (-9% ✅) |
| E2E tests executed by the agent (mean) | 2.50 | 7.75 (+210% ⚠️) |
| Full unit suite runs (total) | 12 | 4 (-67% ✅) |
| Full E2E suite runs (total; forbidden without a request) | 0 | 0 |
| E2E runs paying a production build (mean) | 0.33 | 0.58 (+75% ⚠️) |
| Subagents spawned (total) | 0 | 0 |

## By task

| Task | Version | Hidden | Suites green | Test-first | Min (mean) | USD (mean) | Questions | E2E tests run (mean) | Check time s (mean) | Failing specs after the agent |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| t1-typo | v1.2.0 | 3/3 | 3/3 | n/a | 0.21 | 0.08 | 0 | 0.0 | 2.7 | — |
| t1-typo | v1.5.1 | 3/3 | 3/3 | n/a | 0.16 | 0.08 | 0 | 0.0 | 1.6 | — |
| t2-total | v1.2.0 | 3/3 | 3/3 | 3/3 | 0.36 | 0.13 | 0 | 0.0 | 2.9 | — |
| t2-total | v1.5.1 | 3/3 | 3/3 | 3/3 | 0.42 | 0.14 | 0 | 3.3 | 8.0 | — |
| t3-remove | v1.2.0 | 3/3 | 3/3 | 3/3 | 0.78 | 0.28 | 3 | 4.0 | 11.7 | — |
| t3-remove | v1.5.1 | 0/3 | 3/3 | 3/3 | 0.88 | 0.21 | 0 | 12.7 | 16.2 | — |
| t4-currency | v1.2.0 | 3/3 | 3/3 | 3/3 | 0.52 | 0.14 | 0 | 6.0 | 11.2 | — |
| t4-currency | v1.5.1 | 3/3 | 3/3 | 3/3 | 0.60 | 0.16 | 0 | 15.0 | 14.2 | — |

## Tasks

- `t1-typo` (trivial): Los botones de los productos dicen "Add to crat". Corrige el typo.
- `t2-total` (small): El total del carrito está mal cuando se agrega el mismo producto más de una vez. Corrígelo.
- `t3-remove` (medium): Permite que el usuario quite productos del carrito. The answer contradicts the natural default (remove the whole row): an agent that does not ask fails the hidden test.
- `t4-currency` (small): Muestra todos los precios en soles peruanos, con el formato "S/ 3.00". formatPrice lives in the cart module but the catalog uses it too: specs tagged @catalog break although no catalog file changes. Selecting E2E specs by touched-module tag alone misses them; the full suite run by the harness catches it.
