# Analysis 20261018-1637

1.4.0 (best measured earlier version) against the working tree before the 2.0.0 review fixes, labeled 1.7.0 in `REPORT.md`. 4 tasks, 5 repetitions each, Sonnet, Node 24, 6.5 min.

## Findings

1. **Efficiency goals met.** Full unit suite runs 22 to 0; E2E runs paying a production build 0.35 to 0 per run; Lighthouse never fired (no task changes routes, assets, or build config); repeated file reads 0.10 to 0. Wall time +6% and cost identical, inside noise.
2. **Quality held, one miss.** Hidden tests 19/20 (the ambiguous task was asked about in 4 of 5 runs, as in 1.2.0), suites green 19/20, test-first 14/15.
3. **`affected` adoption is partial.** 12 of 20 runs ran it. All `t3-remove` runs did; `t2-total` (a service-only fix) did not in 4 of 5, which is acceptable since no spec covers it, but one `t4-currency` run skipped it, concluded "no E2E specs exist", skipped E2E, and left `cart.spec.ts` and `catalog.spec.ts` red. The rule now says level 2 always starts with `affected`, never concludes that no spec applies without running it, and quotes its selection in the report.
4. **More E2E per run, by design.** 12.45 E2E tests per run against 2.05: `affected` selects the specs Playwright relates to a change plus the tagged ones, so a page-object edit (`t1-typo`) selects every spec. Check time on `t1-typo` rose from 3.9 s to 12.7 s on the dev server; the earlier 1.6.1 version paid a production build for the same task.
5. **The guard never fired.** No run attempted a full suite, so no block was needed.
