# Benchmark 20261018-1637

Model `sonnet`, fixture `bench/fixture` (Vite + React, pnpm, 9 unit and 18 E2E tests, 8 s production build). Baseline v1.4.0; deltas are relative to it, ✅ means lower.

## Summary

| Metric | v1.4.0 | v1.7.0 |
| --- | --- | --- |
| Runs | 20 | 20 |
| Hidden acceptance tests passed | 20/20 | 19/20 |
| All suites green after the agent (unit, E2E, typecheck, lint) | 20/20 | 19/20 |
| Test-first, red seen before the fix | 15/15 | 14/15 |
| Wall time per run, min (range) | 0.52 (0.22–1.07) | 0.55 (0.26–0.94) |
| Mean wall time (min) | 0.52 | 0.55 (+6% ⚠️) |
| Mean time inside checks (s) | 9.07 | 10.75 (+18% ⚠️) |
| Mean cost (USD) | 0.18 | 0.18 (+0% ⚠️) |
| Mean turns | 6.50 | 7.30 (+12% ⚠️) |
| Question rounds (total) | 7 | 4 |
| Unit tests executed by the agent (mean) | 17.15 | 15.80 (-8% ✅) |
| E2E tests executed by the agent (mean) | 2.05 | 12.45 (+507% ⚠️) |
| Full unit suite runs (total) | 22 | 0 (-100% ✅) |
| Full E2E suite runs (total; forbidden without a request) | 0 | 0 |
| E2E runs paying a production build (mean) | 0.35 | 0 (-100% ✅) |
| Repeated file reads with no edit in between (mean) | 0.10 | 0 (-100% ✅) |
| Failed tool calls, excluding test runs (mean) | 0.05 | 0.05 (+0%) |
| Files edited more than twice (mean) | 0 | 0 |
| Runs that ran `affected` before reporting (2.0.0+) | 0/20 | 13/20 |
| Subagents spawned (total) | 0 | 0 |

## By task

| Task | Version | Hidden | Suites green | Test-first | Min (mean) | USD (mean) | Questions | E2E tests run (mean) | Check time s (mean) | Failing specs after the agent |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| t1-typo | v1.4.0 | 5/5 | 5/5 | n/a | 0.23 | 0.09 | 0 | 0.0 | 3.9 | — |
| t1-typo | v1.7.0 | 5/5 | 5/5 | n/a | 0.38 | 0.11 | 0 | 14.4 | 12.7 | — |
| t2-total | v1.4.0 | 5/5 | 5/5 | 5/5 | 0.38 | 0.13 | 0 | 0.0 | 4.7 | — |
| t2-total | v1.7.0 | 5/5 | 5/5 | 5/5 | 0.39 | 0.13 | 0 | 3.6 | 6.5 | — |
| t3-remove | v1.4.0 | 5/5 | 5/5 | 5/5 | 0.94 | 0.30 | 5 | 6.4 | 18.6 | — |
| t3-remove | v1.7.0 | 4/5 | 5/5 | 5/5 | 0.88 | 0.30 | 4 | 19.2 | 12.7 | — |
| t4-currency | v1.4.0 | 5/5 | 5/5 | 5/5 | 0.53 | 0.19 | 2 | 1.8 | 9.2 | — |
| t4-currency | v1.7.0 | 5/5 | 4/5 | 4/5 | 0.55 | 0.16 | 0 | 12.6 | 11.1 | cart.spec.ts, catalog.spec.ts |

## Tasks

- `t1-typo` (trivial): Los botones de los productos dicen "Add to crat". Corrige el typo.
- `t2-total` (small): El total del carrito está mal cuando se agrega el mismo producto más de una vez. Corrígelo.
- `t3-remove` (medium): Permite que el usuario quite productos del carrito. The answer contradicts the natural default (remove the whole row): an agent that does not ask fails the hidden test.
- `t4-currency` (small): Muestra todos los precios en soles peruanos, con el formato "S/ 3.00". formatPrice lives in the cart module but the catalog uses it too: specs tagged @catalog break although no catalog file changes. Selecting E2E specs by touched-module tag alone misses them; the full suite run by the harness catches it.
