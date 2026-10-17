// Prints, per audited URL, the median Lighthouse scores and the audits that cost points.
// Run from the project root after the `lighthouse` command: node .agents/skills/web-performance/scripts/lighthouse-audits.mjs
import { readFileSync, readdirSync } from 'node:fs';
const dir = '.lighthouseci';
const runs = readdirSync(dir).filter((f) => /^lhr-.*\.json$/.test(f)).map((f) => JSON.parse(readFileSync(`${dir}/${f}`, 'utf8')));
const byUrl = Object.groupBy(runs, (r) => r.requestedUrl);
for (const [url, lhrs] of Object.entries(byUrl)) {
  const median = lhrs.sort((a, b) => a.categories.performance.score - b.categories.performance.score)[Math.floor(lhrs.length / 2)];
  console.log(`\n${url}`);
  for (const category of Object.values(median.categories)) {
    console.log(`  ${category.title}: ${Math.round(category.score * 100)}`);
    for (const ref of category.auditRefs.filter((r) => r.weight > 0)) {
      const audit = median.audits[ref.id];
      if (audit.score !== null && audit.score < 0.9) console.log(`    - ${audit.id} (${audit.score}): ${audit.title}${audit.displayValue ? ` — ${audit.displayValue}` : ''}`);
    }
  }
}
