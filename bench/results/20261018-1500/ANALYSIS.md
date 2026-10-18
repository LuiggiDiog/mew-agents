# Analysis 20261018-1500

Six milestone versions, 4 tasks, 5 repetitions each (120 runs, Sonnet, Node 24, 16.7 min). See `REPORT.md` for the full tables. With 5 repetitions, differences under about 20% in time or cost are noise.

## Always-loaded context per version (rendered AGENTS.md)

| Version | Lines | Words | Skills | Mean input tokens per run |
| --- | --- | --- | --- | --- |
| 1.0.0 | 211 | 2046 | 4 | 220k |
| 1.2.0 | 225 | 2346 | 4 | 216k |
| 1.3.0 | 260 | 2710 | 4 | 224k |
| 1.4.0 | 260 | 2710 | 5 | 237k |
| 1.5.0 | 250 | 3020 | 5 | 218k |
| 1.6.1 | 272 | 3568 | 6 | 264k |

## Findings

1. **Lighthouse fires on small UI changes (1.6.1).** 3 of 5 `t3-remove` runs ran `pnpm dlx @lhci/cli autorun` for a new cart button: about 40 s each (package download plus 3 runs), which doubles check time (33 s vs 18 s in 1.5.0) and wall time (85 s vs 49–62 s). One run also reported a pre-existing SEO failure in the fixture. The rule trigger ("touches UI") is too wide for the cost, and `DLX` pays the download on every task.
2. **Production E2E for changes that cannot differ in production (1.6.1).** `t1-typo` paid a production build in 2 of 5 runs (3.2 E2E tests on a text change) and `t2-total` in 1 of 5; 1.5.0 paid none on those tasks. Check time on `t1-typo` went from 2.7–4.2 s to 10.4 s. Level 2 E2E is useful when a page object or spec changed, but the production build adds 8 s for nothing when only text or a service changed.
3. **The requirement round works but is diluted.** `t3-remove` (ambiguous): 1.0.0 and 1.5.0 never ask and fail 0/5; 1.2.0 asks 4/5; 1.3.0 and 1.4.0 ask 5/5; 1.6.1 asks 3/5 and passes exactly those 3. The requirements text is identical in 1.3.0 and 1.6.1, so the drop goes with the longer file (3568 words, +18% input tokens), which matches the published guidance to keep instruction files short. Needs more repetitions to confirm.
4. **The ladder removes full unit runs.** Full `vitest run` executions per 20 runs: 17, 15, 22, 18 (1.0.0–1.4.0) versus 1 (1.5.0, 1.6.1). No version ran the full E2E suite. E2E tests executed by the agent rose from about 1 to 8–10 per run: more coverage, paid in check time.
5. **Questions on clear tasks cost time.** `t4-currency` asked in 3/5 runs on 1.3.0 and 1.4.0 (currency conversion or format only), 1/5 on 1.6.1, 0/5 on 1.5.0. The question is defensible, but each round adds about 10 s and one turn.
6. **Test-first misses come from bulk `sed` edits.** 1.4.0 `t4-currency` saw red before the fix in only 2/5 runs: the agent edited tests and source in one `sed` command before running anything. 1.5.0 and 1.6.1 scored 5/5 (15/15 overall).
7. **One suite left red (1.3.0, `t2-total` r3).** The agent changed only `cart.ts` and its test, yet every E2E spec failed afterwards, including catalog specs: almost certainly a harness flake (web server or port), not the agent. Check outputs are now saved per run (`quality-*.log`) so the next such case has a cause.
8. **Harness regression found and fixed.** The first attempt ran under Node 20, where Vitest 5 runs no tests; every unit result read as failed. The runner now refuses to start below Node 22.

## Ranking

Quality first, then speed: 1.4.0 (20/20 hidden, 20/20 green, 0.56 min) and 1.3.0 (19/20, 19/20, 0.54 min) are the best balance. 1.6.1 keeps quality (18/20, 20/20 green, 15/15 test-first, 1 full unit run) but is the slowest (0.73 min, +30% over 1.4.0) because of findings 1 and 2. 1.5.0 is fast and cheap but fails every ambiguous task.
