// Lists the unit tests and E2E specs that cover the touched files, and the level 2 commands to run.
// Usage, from the project root: node .agents/scripts/affected-tests.mjs [<base>]
// Without <base> it looks at uncommitted changes; with a branch or commit it also includes what was
// committed since. The commands it embeds were filled in when the template was applied (see Toolchain).
import { execSync } from 'node:child_process';
import { existsSync, readdirSync, readFileSync, statSync } from 'node:fs';
import { dirname, join } from 'node:path';

const BASE = process.argv[2] ?? 'HEAD';
const E2E_DIR = '{{E2E_DIR}}';
const UNIT_LIST = '{{CMD_TEST_LIST_CHANGED}}'; // `n/a` when the unit runner cannot list by changed files
const UNIT_RELATED = '{{CMD_TEST_RELATED}}';
const E2E = '{{CMD_E2E}}';

const sh = (cmd) => {
  try {
    return execSync(cmd, { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] });
  } catch (error) {
    return error.stdout ?? '';
  }
};
const lines = (text) => text.split('\n').map((l) => l.trim()).filter(Boolean);
const isUnitTest = (f) => /\.(test|spec)\.[cm]?[jt]sx?$/.test(f) && !f.startsWith(E2E_DIR);
const isCode = (f) => /\.([cm]?[jt]sx?|vue|svelte|html|css|scss)$/.test(f) && !f.startsWith('.'); // dot folders hold agent config, not app code

const touched = [...new Set([...lines(sh(`git diff --name-only ${BASE} --`)), ...lines(sh('git ls-files --others --exclude-standard'))])]
  .filter((f) => existsSync(f));
const source = touched.filter((f) => isCode(f) && !isUnitTest(f) && !f.startsWith(E2E_DIR));
const changedUnitTests = touched.filter(isUnitTest);

// Specs tagged with a module: `{ tag: '@<module>' }`, where the module is a folder name in the touched paths.
const specs = [];
const walk = (dir) => {
  if (!existsSync(dir)) return;
  for (const name of readdirSync(dir)) {
    const path = join(dir, name);
    if (statSync(path).isDirectory()) walk(path);
    else if (/\.spec\.[cm]?[jt]sx?$/.test(name)) specs.push(path);
  }
};
walk(E2E_DIR);
const tagsOf = (spec) => [...readFileSync(spec, 'utf8').matchAll(/@([\w-]+)/g)].map((m) => m[1]);
const allTags = new Set(specs.flatMap(tagsOf));
const segments = (f) => dirname(f).split('/').filter(Boolean);
// Unit tests the runner relates to the change through imports: a module whose tests react to the
// change is affected even when none of its files changed (a shared helper used by another module).
const unitFiles = UNIT_LIST === 'n/a' ? null : lines(sh(UNIT_LIST.replace('<base>', BASE))).filter((l) => /\.(test|spec)\.[cm]?[jt]sx?$/.test(l));
const modules = [...new Set([...source, ...(unitFiles ?? [])].flatMap(segments).filter((s) => allTags.has(s)))];
const untagged = source.filter((f) => !segments(f).some((s) => allTags.has(s)));
const taggedSpecs = specs.filter((spec) => tagsOf(spec).some((t) => modules.includes(t)));

// Specs Playwright itself relates to the change (changed specs, page objects, helpers).
const specPath = (printed) => [printed, join(dirname(E2E_DIR), printed), join(E2E_DIR, printed)].find((p) => existsSync(p)) ?? printed;
const changedSpecs = [...new Set(lines(sh(`${E2E} --list --only-changed=${BASE}`))
  .map((l) => l.match(/([\w./-]+\.spec\.[cm]?[jt]sx?)/)?.[1]).filter(Boolean).map(specPath))];
const e2eSelection = [...new Set([...changedSpecs, ...taggedSpecs])];

const show = (title, items) => console.log(`${title}: ${items.length ? items.join(' ') : '(none)'}`);
show(`Touched since ${BASE}`, touched);
show('Source files', source);
show('Modules with tagged specs (from the touched files and the unit tests related to them)', modules);
if (untagged.length) show('Source files whose module has no tagged spec (find their specs by route, page object, or visible text)', untagged);
if (unitFiles) show('Unit tests the runner relates to the change', unitFiles);
show('Changed unit test files', changedUnitTests);
show('E2E specs Playwright relates to the change', changedSpecs);
show('E2E specs tagged with the touched modules', taggedSpecs);

console.log('\nLevel 2 commands:');
if (source.length) {
  console.log(`  ${UNIT_RELATED.includes('<files>') ? UNIT_RELATED.replace('<files>', source.join(' ')) : `${UNIT_RELATED}   # with the specs of: ${source.join(' ')}`}`);
} else if (changedUnitTests.length) {
  console.log(`  test-file with: ${changedUnitTests.join(' ')}`);
} else {
  console.log('  (no unit tests to run)');
}
if (e2eSelection.length) {
  console.log(`  ${E2E} ${e2eSelection.join(' ')}`);
} else {
  console.log('  (no spec selected: this is not green when the change touches user-visible behavior; find the specs by route, page object, or visible text, run them, and report the missing tag)');
}
