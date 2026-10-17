# Benchmark 20261017-1638

Model: `sonnet`. Fixture: `bench/fixture` (Vite + React, pnpm). Baseline: v1.2.0. Deltas are relative to the baseline; ✅ means better.

## Summary

| Metric | v1.2.0 | v1.5.1 |
| --- | --- | --- |
| Runs | 6 | 6 |
| Hidden acceptance tests passed | 6/6 | 6/6 |
| All suites green (unit, E2E, typecheck, lint) | 6/6 | 6/6 |
| Test-first (tasks that require it) | 4/4 | 4/4 |
| Red test seen before the fix | 4/4 | 4/4 |
| Mean wall time (min) | 0.37 | 0.42 (+12% ⚠️) |
| Mean cost (USD) | 0.14 | 0.15 (+5% ⚠️) |
| Mean turns | 6 | 6.67 (+11% ⚠️) |
| Mean tool calls | 4.83 | 5.67 (+17% ⚠️) |
| Question rounds (total) | 1 | 0 (-100% ✅) |
| Focused unit runs (mean) | 1.83 | 2.17 |
| Full unit suite runs (mean) | 0.17 | 0 (-100% ✅) |
| Focused E2E runs (mean) | 0.17 | 0.50 |
| Full E2E suite runs (total; forbidden without a request) | 0 | 0 |
| E2E runs paying a production build (mean) | 0.17 | 0.50 (+200% ⚠️) |
| Subagents spawned (total) | 0 | 0 |

## Per task

| Task | Version | Hidden | Suites | Min | USD | Turns | Questions | Unit focused/full | E2E focused/full | Prod E2E runs | Test-first |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| t1-typo | v1.2.0 | ✅ | ✅ | 0.2 | 0.08 | 4 | 0 | 2/0 | 0/0 | 0 | n/a |
| t1-typo | v1.2.0 | ✅ | ✅ | 0.2 | 0.09 | 4 | 0 | 2/0 | 0/0 | 0 | n/a |
| t1-typo | v1.5.1 | ✅ | ✅ | 0.2 | 0.08 | 3 | 0 | 1/0 | 0/0 | 0 | n/a |
| t1-typo | v1.5.1 | ✅ | ✅ | 0.2 | 0.09 | 3 | 0 | 1/0 | 0/0 | 0 | n/a |
| t2-total | v1.2.0 | ✅ | ✅ | 0.3 | 0.12 | 7 | 0 | 2/0 | 0/0 | 0 | ✅ red |
| t2-total | v1.2.0 | ✅ | ✅ | 0.3 | 0.12 | 7 | 0 | 2/0 | 0/0 | 0 | ✅ red |
| t2-total | v1.5.1 | ✅ | ✅ | 0.4 | 0.14 | 7 | 0 | 3/0 | 0/0 | 0 | ✅ red |
| t2-total | v1.5.1 | ✅ | ✅ | 0.4 | 0.14 | 9 | 0 | 2/0 | 1/0 | 1 | ✅ red |
| t3-remove | v1.2.0 | ✅ | ✅ | 0.7 | 0.28 | 7 | 1 | 2/0 | 1/0 | 1 | ✅ red |
| t3-remove | v1.2.0 | ✅ | ✅ | 0.5 | 0.16 | 7 | 0 | 1/1 | 0/0 | 0 | ✅ red |
| t3-remove | v1.5.1 | ✅ | ✅ | 0.6 | 0.21 | 9 | 0 | 2/0 | 1/0 | 1 | ✅ red |
| t3-remove | v1.5.1 | ✅ | ✅ | 0.8 | 0.22 | 9 | 0 | 4/0 | 1/0 | 1 | ✅ red |
