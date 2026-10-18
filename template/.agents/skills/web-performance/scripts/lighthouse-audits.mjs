// Prints, per audited URL, the scores of the median run (by performance score), the budgeted metrics (LCP, CLS, TBT), and the audits that cost points.
// Run from the project root after the `lighthouse` command: node .agents/skills/web-performance/scripts/lighthouse-audits.mjs
import { existsSync, readFileSync, readdirSync } from 'node:fs';
const dir = '.lighthouseci';
if (!existsSync(dir)) {
  console.error(`${dir}/ not found: run the \`lighthouse\` command first`);
  process.exit(1);
}
const runs = readdirSync(dir).filter((f) => /^lhr-.*\.json$/.test(f)).map((f) => JSON.parse(readFileSync(`${dir}/${f}`, 'utf8')));
const byUrl = runs.reduce((acc, r) => ((acc[r.requestedUrl] ??= []).push(r), acc), {});
for (const [url, lhrs] of Object.entries(byUrl)) {
  const median = lhrs.sort((a, b) => a.categories.performance.score - b.categories.performance.score)[Math.floor(lhrs.length / 2)];
  console.log(`\n${url}`);
  for (const id of ['largest-contentful-paint', 'cumulative-layout-shift', 'total-blocking-time']) {
    const audit = median.audits[id];
    if (audit) console.log(`  ${audit.title}: ${audit.displayValue ?? audit.numericValue}`);
  }
  for (const category of Object.values(median.categories)) {
    console.log(`  ${category.title}: ${Math.round(category.score * 100)}`);
    for (const ref of category.auditRefs.filter((r) => r.weight > 0)) {
      const audit = median.audits[ref.id];
      if (audit.score !== null && audit.score < 0.9) console.log(`    - ${audit.id} (${audit.score}): ${audit.title}${audit.displayValue ? ` — ${audit.displayValue}` : ''}`);
    }
  }
}
