# Benchmark 20261019-1105

Model `sonnet`, fixture `bench/fixture` (Vite + React, pnpm, 9 unit and 18 E2E tests, 8 s production build). Baseline v2.0.0; deltas are relative to it, ✅ means lower.

## Summary

| Metric | v2.0.0 |
| --- | --- |
| Runs | 20 |
| Hidden acceptance tests passed | 18/20 |
| All suites green after the agent (unit, E2E, typecheck, lint) | 0/20 |
| Test-first, red seen before the fix | 14/15 |
| Wall time per run, min (range) | 0.61 (0.37–0.91) |
| Mean wall time (min) | 0.61 |
| Mean time inside checks (s) | 13.45 |
| Mean cost (USD) | 0.18 |
| Mean turns | 7.25 |
| Question rounds (total) | 3 |
| Unit tests executed by the agent (mean) | 20.40 |
| E2E tests executed by the agent (mean) | 18.30 |
| Full unit suite runs (total) | 0 |
| Full E2E suite runs (total; forbidden without a request) | 0 |
| E2E runs paying a production build (mean) | 0 |
| Repeated file reads with no edit in between (mean) | 0.05 |
| Failed tool calls, excluding test runs (mean) | 0.15 |
| Files edited more than twice (mean) | 0 |
| Runs that ran `affected` before reporting (2.0.0+) | 20/20 |
| Subagents spawned (total) | 0 |

## By task

| Task | Version | Hidden | Suites green | Test-first | Min (mean) | USD (mean) | Questions | E2E tests run (mean) | Check time s (mean) | Failing specs after the agent |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| t1-typo | v2.0.0 | 5/5 | 0/5 | n/a | 0.40 | 0.12 | 0 | 18.0 | 9.9 | — |
| t2-total | v2.0.0 | 5/5 | 0/5 | 5/5 | 0.55 | 0.15 | 0 | 18.0 | 14.3 | — |
| t3-remove | v2.0.0 | 3/5 | 0/5 | 5/5 | 0.86 | 0.27 | 3 | 19.2 | 15.0 | — |
| t4-currency | v2.0.0 | 5/5 | 0/5 | 4/5 | 0.63 | 0.17 | 0 | 18.0 | 14.5 | — |

## Tasks

- `t1-typo` (trivial): Los botones de los productos dicen "Add to crat". Corrige el typo.
- `t2-total` (small): El total del carrito está mal cuando se agrega el mismo producto más de una vez. Corrígelo.
- `t3-remove` (medium): Permite que el usuario quite productos del carrito. The answer contradicts the natural default (remove the whole row): an agent that does not ask fails the hidden test.
- `t4-currency` (small): Muestra todos los precios en soles peruanos, con el formato "S/ 3.00". formatPrice lives in the cart module but the catalog uses it too: specs tagged @catalog break although no catalog file changes. Selecting E2E specs by touched-module tag alone misses them; the full suite run by the harness catches it.
