// PreToolUse guard for shell commands, shared by Claude Code (.claude/settings.json) and Codex
// (.codex/config.toml). Both send the same JSON on stdin ({ tool_name, tool_input: { command } })
// and both treat exit code 2 as "deny", with stderr as the reason shown to the agent.
//
// 1. A full unit or E2E suite runs only on explicit request: the command must carry FULL_SUITE=1,
//    which makes that request visible in the transcript. Level 4 of the ladder in AGENTS.md.
// 2. E2E runs only against local or test environments: a base URL whose host does not look like
//    one is denied. Add a project host to TEST_HOSTS if it is a dev, staging, or QA environment.
import { readFileSync } from 'node:fs';

const TEST_HOSTS = /^(localhost|127\.0\.0\.1|0\.0\.0\.0|\[::1\])$|(^|[.-])(local|dev|develop|development|staging|stage|test|testing|qa|uat|preview|sandbox)([.-]|$)/i;
const UNIT_RUNNER = /\b(vitest|jest|ng test|karma start)\b|\b(npm|pnpm|yarn|bun)\s+(run\s+)?test(:unit)?(?![:\w-])/;
const UNIT_SELECTION = /\b(related|list|--changed|--related|--include=|--findRelatedTests|--onlyChanged|--changedSince|--testNamePattern|--testPathPattern)|\s-t\s|[\w./\\-]+\.(test|spec)\.[cm]?[jt]sx?/;
// A positional path (a test file or folder) is a selection; the value of a flag such as --root is not.
const positionalPath = (part) => /\s[\w.\\-]*[\/\\][\w./\\-]+/.test(part.replace(/--[\w-]+(=\S+|\s+(?!-)\S+)?/g, ''));
const E2E_RUNNER = /\bplaywright test\b|\b(npm|pnpm|yarn|bun)\s+(run\s+)?(test:e2e|e2e)(?![:\w-])/;
const E2E_SELECTION = /--grep\b|-g\s|--only-changed|--last-failed|--list|--ui\b|[\w./-]+\.(spec|test)\.[cm]?[jt]sx?/;

let input = {};
try {
  input = JSON.parse(readFileSync(0, 'utf8') || '{}');
} catch {
  process.exit(0);
}
const command = input?.tool_input?.command;
if (typeof command !== 'string') process.exit(0);

// Heredoc bodies are data (scripts the agent writes), not commands.
const withoutHeredocs = command.replace(/<<-?\s*['"]?(\w+)['"]?[\s\S]*?\n\1\b/g, '');
const parts = withoutHeredocs.split(/\n|&&|\|\||;|\|/).map((p) => p.trim()).filter(Boolean);
// FULL_SUITE=1 anywhere in the command (POSIX prefix, or `$env:FULL_SUITE=1;` in PowerShell) is the explicit request.
const explicit = /\bFULL_SUITE\s*=\s*['"]?1\b/.test(withoutHeredocs);

const deny = (reason) => {
  process.stderr.write(`${reason}\n`);
  process.exit(2);
};

for (const part of parts) {
  if (E2E_RUNNER.test(part) && !E2E_SELECTION.test(part) && !explicit) {
    deny('Blocked: this runs the complete E2E suite. Pass spec paths, --grep, --only-changed, or --last-failed (run the `affected` command for the level 2 selection). Only when the user explicitly asked for the full suite, prefix the command with FULL_SUITE=1.');
  }
  if (UNIT_RUNNER.test(part) && !UNIT_SELECTION.test(part) && !positionalPath(part) && !explicit) {
    deny('Blocked: this runs the complete unit suite. Pass a test file, `related` with the touched files, or --changed (the `affected` command prints the selection). Prefix the command with FULL_SUITE=1 (PowerShell: `$env:FULL_SUITE=1;` first) only when the user asked for the full suite, or when test config, dependencies, or a module imported almost everywhere changed; say which in the report.');
  }
  for (const match of part.matchAll(/\b[A-Z0-9_]*BASE_URL=['"]?(https?:\/\/[^\s'"/]+)/g)) {
    const host = new URL(match[1]).hostname;
    if (!TEST_HOSTS.test(host)) {
      deny(`Blocked: E2E against ${host} looks like a production environment. E2E runs only against local or test environments (local, dev, staging). If ${host} is a test environment, add it to TEST_HOSTS in .agents/hooks/guard.mjs.`);
    }
  }
}
process.exit(0);
