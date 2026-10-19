"""Build the comparison table from a results directory (default: the latest)."""

import json
import statistics
import sys
from pathlib import Path

BENCH = Path(__file__).resolve().parent
SUITES = ("unit", "e2e", "typecheck", "lint")


def mean(values: list[float]) -> float:
    return statistics.mean(values) if values else 0.0


def rate(values: list[bool]) -> str:
    return f"{sum(values)}/{len(values)}" if values else "n/a"


def spread(values: list[float]) -> str:
    return f"{mean(values):.2f} ({min(values):.2f}–{max(values):.2f})" if values else "n/a"


def delta(new: float, base: float) -> str:
    if not base:
        return ""
    change = (new - base) / base * 100
    mark = "✅" if change < 0 else "⚠️" if change > 0 else ""
    return f" ({change:+.0f}% {mark})".replace(" )", ")")


def green(record: dict) -> bool:
    return all(record["quality"][k] for k in SUITES)


def needs_test_first(record: dict) -> bool:
    return record["task"] != "t1-typo"


ROWS = [
    # (label, value function, lower is better: True / higher is better: False / neutral: None)
    ("Runs", lambda rs: len(rs), None),
    ("Hidden acceptance tests passed", lambda rs: rate([r["quality"]["hidden"] for r in rs]), None),
    ("All suites green after the agent (unit, E2E, typecheck, lint)", lambda rs: rate([green(r) for r in rs]), None),
    ("Test-first, red seen before the fix", lambda rs: rate([r["red_seen"] for r in rs if needs_test_first(r)]), None),
    ("Wall time per run, min (range)", lambda rs: spread([r["wall_s"] / 60 for r in rs]), None),
    ("Mean wall time (min)", lambda rs: mean([r["wall_s"] / 60 for r in rs]), True),
    ("Mean time inside checks (s)", lambda rs: mean([r.get("check_time_s", 0) for r in rs]), True),
    ("Mean cost (USD)", lambda rs: mean([r["cost_usd"] for r in rs]), True),
    ("Mean turns", lambda rs: mean([r["turns"] for r in rs]), True),
    ("Question rounds (total)", lambda rs: sum(r["question_rounds"] for r in rs), None),
    ("Unit tests executed by the agent (mean)", lambda rs: mean([r.get("unit_tests_executed", 0) for r in rs]), True),
    ("E2E tests executed by the agent (mean)", lambda rs: mean([r.get("e2e_tests_executed", 0) for r in rs]), True),
    ("Full unit suite runs (total)", lambda rs: sum(r["unit_full"] for r in rs), True),
    ("Full E2E suite runs (total; forbidden without a request)", lambda rs: sum(r["e2e_full"] for r in rs), True),
    ("E2E runs paying a production build (mean)", lambda rs: mean([r["e2e_prod_runs"] for r in rs]), True),
    ("Repeated file reads with no edit in between (mean)", lambda rs: mean([r.get("repeated_reads", 0) for r in rs]), True),
    ("Failed tool calls, excluding test runs (mean)", lambda rs: mean([r.get("failed_tool_calls", 0) for r in rs]), True),
    ("Files edited more than twice (mean)", lambda rs: mean([r.get("edit_churn", 0) for r in rs]), True),
    ("Runs that ran `affected` before reporting (2.0.0+)", lambda rs: rate([r.get("affected_runs", 0) > 0 for r in rs]), None),
    ("Subagents spawned (total)", lambda rs: sum(r["subagents"] for r in rs), None),
]


def summarize(records: list[dict], versions: list[str]) -> str:
    by_version = {v: [r for r in records if r["version"] == v] for v in versions}
    lines = ["| Metric | " + " | ".join(f"v{v}" for v in versions) + " |", "|" + " --- |" * (len(versions) + 1)]
    for label, fn, lower_better in ROWS:
        cells = []
        for v in versions:
            value = fn(by_version[v])
            text = f"{value:.2f}" if isinstance(value, float) else str(value)
            if lower_better and v != versions[0] and isinstance(value, (int, float)):
                text += delta(float(value), float(fn(by_version[versions[0]])))
            cells.append(text)
        lines.append(f"| {label} | " + " | ".join(cells) + " |")
    return "\n".join(lines)


def by_task(records: list[dict], versions: list[str]) -> str:
    lines = [
        "| Task | Version | Hidden | Suites green | Test-first | Min (mean) | USD (mean) | Questions | E2E tests run (mean) | Check time s (mean) | Failing specs after the agent |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for task in sorted({r["task"] for r in records}):
        for v in versions:
            rs = [r for r in records if r["task"] == task and r["version"] == v]
            if not rs:
                continue
            failing = sorted({f for r in rs for f in r["quality"].get("e2e_failed_files", []) if "zz-hidden" not in f})
            tf = "n/a" if not needs_test_first(rs[0]) else rate([r["red_seen"] for r in rs])
            lines.append(
                f"| {task} | v{v} | {rate([r['quality']['hidden'] for r in rs])} | {rate([green(r) for r in rs])} | {tf} | "
                f"{mean([r['wall_s'] / 60 for r in rs]):.2f} | {mean([r['cost_usd'] for r in rs]):.2f} | "
                f"{sum(r['question_rounds'] for r in rs)} | {mean([r.get('e2e_tests_executed', 0) for r in rs]):.1f} | "
                f"{mean([r.get('check_time_s', 0) for r in rs]):.1f} | {', '.join(failing) or '—'} |"
            )
    return "\n".join(lines)


def main() -> None:
    results = BENCH / "results"
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else max(p for p in results.iterdir() if p.is_dir())
    records = json.loads((target / "records.json").read_text())
    versions = sorted({r["version"] for r in records}, key=lambda v: [int(x) for x in v.split(".")])
    tasks = {t.name: json.loads((t / "task.json").read_text()) for t in (BENCH / "tasks").iterdir() if (t / "task.json").exists()}
    notes = "\n".join(
        f"- `{name}` ({task['size']}): {task['prompt']}" + (f" {task['note']}" if task.get("note") else "")
        for name, task in sorted(tasks.items()) if name in {r["task"] for r in records}
    )
    report = (
        f"# Benchmark {target.name}\n\n"
        f"Model `{records[0]['model']}`, fixture `bench/fixture` (Vite + React, pnpm, 9 unit and 18 E2E tests, "
        f"8 s production build). Baseline v{versions[0]}; deltas are relative to it, ✅ means lower.\n\n"
        f"## Summary\n\n{summarize(records, versions)}\n\n## By task\n\n{by_task(records, versions)}\n\n## Tasks\n\n{notes}\n"
    )
    (target / "REPORT.md").write_text(report)
    print(report)


if __name__ == "__main__":
    main()
