"""Behavioral benchmark: run the same tasks with different template versions and measure.

Every (task, rep) runs all versions as a pair, and pairs run concurrently up to --jobs,
so CPU contention stays symmetric between versions. Each run: render the template
version, run `claude -p` headless, answer up to two question rounds with the task's
canned answer if the agent asks, then check quality with hidden tests and full suites
the agent never saw.
"""

import argparse
import collections
import concurrent.futures as futures
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import tempfile
import threading
import time
from pathlib import Path

from render import render

BENCH = Path(__file__).resolve().parent
CONFIG = json.loads((BENCH / "versions.json").read_text())
E2E = "pnpm exec playwright test --config=e2e/playwright.config.ts"
MAX_RESUMES = 2
PRINT = threading.Lock()


def log(message: str) -> None:
    with PRINT:
        print(f"[{dt.datetime.now():%H:%M:%S}] {message}", flush=True)


def sh(cmd: str, cwd: Path, env: dict | None = None, timeout: int = 900) -> tuple[int, str]:
    try:
        proc = subprocess.run(
            cmd, cwd=cwd, shell=True, capture_output=True, text=True, timeout=timeout,
            env={**os.environ, **(env or {})},
        )
        return proc.returncode, proc.stdout + proc.stderr
    except subprocess.TimeoutExpired as error:
        return 124, f"timeout after {timeout}s: {error}"


def check_node() -> None:
    """The fixture's toolchain (Vitest 5) needs the Node major in fixture/.nvmrc; an older
    Node makes every unit run fail silently and poisons the whole benchmark."""
    wanted = (BENCH / "fixture" / ".nvmrc").read_text().strip()
    code, version = sh("node -p process.versions.node", BENCH)
    major = int(version.strip().split(".")[0]) if code == 0 and version.strip() else 0
    if major < 22:
        raise SystemExit(f"Node {version.strip() or 'missing'} found; the fixture needs {wanted} (Node 24). Run `nvm use 24` first.")


def prepare_base(workdir: Path) -> Path:
    """Installed copy of the fixture. Only node_modules is cached; sources are synced every time."""
    base = workdir / "base"
    lock = (BENCH / "fixture" / "pnpm-lock.yaml").read_text()
    cached = (base / "node_modules").exists() and (base / "pnpm-lock.yaml").read_text() == lock
    if not cached:
        shutil.rmtree(base, ignore_errors=True)
    base.mkdir(parents=True, exist_ok=True)
    for entry in base.iterdir():
        if entry.name != "node_modules":
            shutil.rmtree(entry) if entry.is_dir() and not entry.is_symlink() else entry.unlink()
    shutil.copytree(BENCH / "fixture", base, dirs_exist_ok=True)
    if not cached:
        code, out = sh("pnpm install --frozen-lockfile", base, timeout=600)
        if code:
            raise SystemExit(f"pnpm install failed:\n{out}")
    return base


def prepare_workspace(base: Path, ws: Path, version: str) -> None:
    # APFS clone when available: node_modules is copied in milliseconds.
    if sh(f"cp -cR '{base}' '{ws}'", base.parent)[0]:
        shutil.copytree(base, ws, symlinks=True)
    variant = CONFIG["versions"][version]["playwright"]
    shutil.copy(BENCH / "variants" / variant / "playwright.config.ts", ws / "e2e" / "playwright.config.ts")
    leftovers = render(version, ws)
    if leftovers:
        raise SystemExit(f"{version} rendered with leftovers: {leftovers}")
    sh("git init -q && git add -A && git -c user.email=bench@local -c user.name=bench commit -qm baseline", ws)


def claude(ws: Path, prompt: str, model: str, port: int, transcript: Path, resume: str | None) -> dict:
    cmd = [
        "claude", "-p", prompt, "--output-format", "stream-json", "--verbose", "--model", model,
        "--dangerously-skip-permissions", "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}',
        "--setting-sources", "project,local",
    ]
    if resume:
        cmd += ["--resume", resume]
    start = time.time()
    events = []
    # Stamp each event on arrival: stream-json has no timestamps, and tool latency
    # (time inside test commands) is the difference between a tool_use and its result.
    with subprocess.Popen(
        cmd, cwd=ws, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
        env={**os.environ, "E2E_PORT": str(port)},
    ) as proc, transcript.open("w") as out:
        timer = threading.Timer(1800, proc.kill)
        timer.start()
        for line in proc.stdout:
            if line.startswith("{"):
                event = json.loads(line)
                event["_t"] = round(time.time() - start, 3)
                events.append(event)
                out.write(json.dumps(event) + "\n")
        timer.cancel()
    result = next((e for e in reversed(events) if e.get("type") == "result"), {})
    return {"events": events, "result": result, "wall_s": time.time() - start}


def changed_files(ws: Path) -> list[str]:
    out = sh("git status --porcelain", ws)[1]
    return [line[3:] for line in out.splitlines() if line.strip()]


def split_heredocs(command: str) -> tuple[str, list[str]]:
    """Return the shell text with heredoc bodies replaced by placeholders, and the bodies."""
    bodies: list[str] = []

    def keep(match: re.Match) -> str:
        bodies.append(match.group(2))
        return f"__HEREDOC_{len(bodies) - 1}__"

    shell = re.sub(r"<<-?\s*['\"]?(\w+)['\"]?[^\n]*\n(.*?)\n\1\b", keep, command, flags=re.S)
    return shell, bodies


def classify(command: str, variant: str) -> list[str]:
    """Label each test-related part of a shell command."""
    labels = []
    for part in re.split(r"&&|\|\||;|\|", command):
        if "affected-tests" in part:
            labels.append("affected")
        elif "playwright test" in part or re.search(r"run (test:)?e2e", part):
            if "--list" in part:
                labels.append("e2e_list")
                continue
            focused = re.search(r"\.spec\.ts|--grep|-g |--only-changed|--last-failed|zz-|\$\(|`|tests/\S", part)
            prod = variant == "prod-always" or "E2E_PROD" in part or "E2E_BUILD" in part or "CI=" in part
            labels.append(f"e2e_{'focused' if focused else 'full'}_{'prod' if prod else 'dev'}")
        elif "vitest" in part or re.search(r"\b(pnpm|npm|yarn)( run)? test\b", part):
            if "watch" in part:
                labels.append("unit_watch")
            elif re.search(r"related|\.test\.tsx?|src/", part):
                labels.append("unit_focused")
            else:
                labels.append("unit_full")
        elif "tsc" in part or "typecheck" in part:
            labels.append("typecheck")
        elif "eslint" in part or "run lint" in part:
            labels.append("lint")
        elif re.search(r"run build|vite build", part):
            labels.append("build")
    return labels


def tests_in_output(text: str) -> tuple[int, int]:
    """(unit tests, E2E tests) reported by Vitest and Playwright summaries in tool output."""
    # Vitest: "Tests  1 failed | 7 passed (8)". Playwright: "  18 passed (2.2s)", "  1 failed".
    unit = sum(int(n) for n in re.findall(r"^\s*Tests\s+[^\n]*?\((\d+)\)", text, re.M))
    e2e = sum(int(n) for n in re.findall(r"^\s*(\d+) (?:passed|failed|flaky)(?: \([\d.]+m?s\))?\s*$", text, re.M))
    return unit, e2e


def transcript_metrics(events: list[dict], variant: str) -> dict:
    tool_calls, commands, edits, labels, subagents, seq = 0, [], [], [], 0, 0
    reads: list[tuple[int, str]] = []
    failed_tool_calls = 0
    pending: dict[str, tuple[float, list[str]]] = {}
    check_s = unit_tests = e2e_tests = 0.0
    for event in events:
        content = event.get("message", {}).get("content", [])
        if event.get("type") == "user" and isinstance(content, list):
            for block in content:
                if block.get("type") == "tool_result" and block.get("is_error"):
                    # A red test run is an expected failure, not a wasted action.
                    started = pending.get(block.get("tool_use_id"))
                    if not (started and started[1]):
                        failed_tool_calls += 1
                if block.get("type") != "tool_result" or block.get("tool_use_id") not in pending:
                    continue
                started, kinds = pending.pop(block["tool_use_id"])
                output = block.get("content")
                if isinstance(output, list):
                    output = "\n".join(item.get("text", "") for item in output if isinstance(item, dict))
                if kinds and "_t" in event:
                    check_s += event["_t"] - started
                units, e2es = tests_in_output(output or "")
                unit_tests += units
                e2e_tests += e2es
            continue
        if event.get("type") != "assistant":
            continue
        for block in content:
            if block.get("type") != "tool_use":
                continue
            tool_calls += 1
            seq += 1
            name, data = block.get("name"), block.get("input", {})
            if name in ("Task", "Agent"):
                subagents += 1
            elif name == "Bash":
                command = data.get("command", "")
                commands.append(command)
                shell, bodies = split_heredocs(command)
                kinds: list[str] = []
                # cat/head/tail/sed -n on a source, test, or doc file count as reads too.
                for part in re.split(r"\n|&&|\|\||;", shell):
                    if re.match(r"\s*(cat|head|tail|sed -n|bat)\b", part):
                        reads += [(seq, f"/{path}") for path in re.findall(r"[\w./-]+\.(?:tsx?|jsx?|css|md|json)\b", part)]
                # Walk the command in order: heredoc scripts that write files (python3 - <<EOF ...
                # open(p, 'w')) and shell edits (sed -i, perl -pi, redirects) are edits; the rest
                # is classified as checks. Sub-steps keep their order inside one command.
                for step, part in enumerate(re.split(r"\n|&&|\|\||;", shell)):
                    at = seq + step / 1000
                    for index in map(int, re.findall(r"__HEREDOC_(\d+)__", part)):
                        body = bodies[index]
                        if re.search(r"\.write\(|write_text|writeFileSync|open\([^)]*['\"]w", body):
                            edits += [(at, f"/{path}") for path in re.findall(r"['\"]([\w./-]+\.(?:tsx?|jsx?|css))['\"]", body)]
                    if re.search(r"sed -i|perl -p?i|>\s*\S+\.(tsx?|jsx?)|\btee\b", part):
                        edits += [(at, f"/{path}") for path in re.findall(r"[\w./-]+\.(?:tsx?|jsx?|css)\b", part)]
                    part_labels = classify(part, variant)
                    labels += [(at, label) for label in part_labels]
                    kinds += [label for label in part_labels if label != "e2e_list"]
                pending[block.get("id", "")] = (event.get("_t", 0.0), kinds)
            elif name in ("Edit", "Write", "MultiEdit", "NotebookEdit"):
                edits.append((seq, data.get("file_path", "")))
            elif name == "Read":
                reads.append((seq, data.get("file_path", "")))
    is_test = lambda p: bool(re.search(r"\.test\.|\.spec\.|/e2e/", p))
    is_src = lambda p: "/src/" in p and not is_test(p)
    first_test = next((i for i, p in edits if is_test(p)), None)
    first_src = next((i for i, p in edits if is_src(p)), None)
    test_first = first_test is not None and (first_src is None or first_test < first_src)
    red_seen = test_first and any(
        first_test < i < (first_src if first_src is not None else 10**9) and l.startswith(("unit_", "e2e_f"))
        for i, l in labels
    )
    count = lambda prefix: sum(1 for _, l in labels if l.startswith(prefix))
    edits_per_file = collections.Counter(path.rsplit("/", 1)[-1] for _, path in edits)
    edit_churn = sum(1 for n in edits_per_file.values() if n > 2)
    repeated_reads, last_read = 0, {}
    for at, path in sorted(reads):
        name = path.rsplit("/", 1)[-1]
        if name in last_read and not any(last_read[name] < i < at and p.endswith(name) for i, p in edits):
            repeated_reads += 1
        last_read[name] = at
    return {
        "tool_calls": tool_calls, "bash_commands": len(commands), "edits": len(edits), "subagents": subagents,
        "unit_focused": count("unit_focused"), "unit_full": count("unit_full"),
        "e2e_focused": count("e2e_focused"), "e2e_full": count("e2e_full"),
        "e2e_prod_runs": count("e2e_focused_prod") + count("e2e_full_prod"),
        "builds": count("build"), "typecheck": count("typecheck"), "lint": count("lint"), "affected_runs": count("affected"),
        "unit_tests_executed": int(unit_tests), "e2e_tests_executed": int(e2e_tests),
        "check_time_s": round(check_s, 1),
        "test_first": test_first, "red_seen": red_seen, "repeated_reads": repeated_reads,
        "failed_tool_calls": failed_tool_calls, "edit_churn": edit_churn, "commands": commands,
    }


def quality(ws: Path, logs: Path, task: dict, port: int) -> dict:
    """Full suites plus hidden tests, in one pass per runner, with the runners in parallel."""
    agent_diff = sh("git diff HEAD", ws)[1] + "".join(
        (ws / f).read_text(errors="ignore") for f in changed_files(ws) if (ws / f).is_file()
    )
    for item in task["hidden"]:
        shutil.copy(BENCH / "tasks" / task["id"] / item["src"], ws / item["dest"])
    unit_json, e2e_json = ws / ".bench-unit.json", ws / ".bench-e2e.json"
    commands = {
        "unit": (f"pnpm exec vitest run --reporter=json --outputFile={unit_json}", {}),
        "typecheck": ("pnpm exec tsc --noEmit", {}),
        "lint": ("pnpm exec eslint --ignore-pattern '**/zz-hidden.*' .", {}),
        "e2e": (f"{E2E} --reporter=json", {"E2E_PORT": str(port), "E2E_PROD": "1", "E2E_BUILD": "1", "PLAYWRIGHT_JSON_OUTPUT_NAME": str(e2e_json)}),
    }
    with futures.ThreadPoolExecutor(len(commands)) as pool:
        jobs = {name: pool.submit(sh, cmd, ws, env) for name, (cmd, env) in commands.items()}
        outputs = {name: job.result() for name, job in jobs.items()}
        codes = {name: code for name, (code, _) in outputs.items()}
    # Keep each check's output: a suite that is red after the agent needs a cause (agent or flake).
    for name, (_, text) in outputs.items():
        (logs / f"quality-{name}.log").write_text(text)

    def hidden_split(outcomes: list[tuple[str, bool]]) -> tuple[bool, bool | None]:
        visible = [ok for file, ok in outcomes if "zz-hidden" not in file]
        hidden = [ok for file, ok in outcomes if "zz-hidden" in file]
        return all(visible) and bool(visible), (all(hidden) if hidden else None)

    unit_outcomes, e2e_outcomes = [], []
    if unit_json.exists():
        report = json.loads(unit_json.read_text())
        unit_outcomes = [(r["name"], r["status"] == "passed") for r in report.get("testResults", [])]
    if e2e_json.exists():
        def walk(suite: dict) -> None:
            for spec in suite.get("specs", []):
                e2e_outcomes.append((spec.get("file", suite.get("file", "")), spec.get("ok", False)))
            for child in suite.get("suites", []):
                walk(child)
        for suite in json.loads(e2e_json.read_text()).get("suites", []):
            walk(suite)
    unit_ok, unit_hidden = hidden_split(unit_outcomes)
    e2e_ok, e2e_hidden = hidden_split(e2e_outcomes)
    hidden = [h for h in (unit_hidden, e2e_hidden) if h is not None]
    return {
        "unit": unit_ok, "typecheck": codes["typecheck"] == 0, "lint": codes["lint"] == 0, "e2e": e2e_ok,
        "hidden": bool(hidden) and all(hidden) and len(hidden) == len({i["kind"] for i in task["hidden"]}),
        "no_wait_for_timeout": "waitForTimeout" not in agent_diff,
        "e2e_failed_files": sorted({Path(f).name for f, ok in e2e_outcomes if not ok}),
    }


def run_one(version: str, task: dict, rep: int, model: str, base: Path, workdir: Path, out: Path, port: int) -> dict:
    run_id = f"{task['id']}__{version}__r{rep}"
    ws, logs = workdir / "runs" / run_id, out / "runs" / run_id
    shutil.rmtree(ws, ignore_errors=True)
    ws.parent.mkdir(parents=True, exist_ok=True)
    logs.mkdir(parents=True, exist_ok=True)
    prepare_workspace(base, ws, version)
    variant = CONFIG["versions"][version]["playwright"]

    sessions = [claude(ws, task["prompt"], model, port, logs / "transcript-0.jsonl", None)]
    while not changed_files(ws) and len(sessions) <= MAX_RESUMES and sessions[-1]["result"].get("session_id"):
        session_id = sessions[-1]["result"]["session_id"]
        transcript = logs / f"transcript-{len(sessions)}.jsonl"
        sessions.append(claude(ws, task["answer"], model, port, transcript, session_id))

    results = [s["result"] for s in sessions]
    usage = lambda key: sum((r.get("usage") or {}).get(key, 0) for r in results)
    record = {
        "run_id": run_id, "version": version, "task": task["id"], "size": task["size"], "rep": rep,
        "model": model, "playwright": variant, "completed": bool(changed_files(ws)),
        "question_rounds": len(sessions) - 1,
        "wall_s": round(sum(s["wall_s"] for s in sessions), 1),
        "duration_s": round(sum(r.get("duration_ms", 0) for r in results) / 1000, 1),
        "cost_usd": round(sum(r.get("total_cost_usd", 0) for r in results), 4),
        "turns": sum(r.get("num_turns", 0) for r in results),
        "input_tokens": usage("input_tokens") + usage("cache_read_input_tokens") + usage("cache_creation_input_tokens"),
        "output_tokens": usage("output_tokens"),
        "errors": [r.get("subtype") for r in results if r.get("subtype") != "success"],
        "final_message": (results[-1].get("result") or "")[:1500] if results else "",
        **transcript_metrics([e for s in sessions for e in s["events"]], variant),
        "changed_files": changed_files(ws),
    }
    record["quality"] = quality(ws, logs, task, port + 1)
    (logs / "metrics.json").write_text(json.dumps(record, indent=2, ensure_ascii=False))
    shutil.rmtree(ws, ignore_errors=True)
    return record


def rescore(results: Path) -> None:
    """Recompute transcript metrics for saved runs, without running agents again."""
    records = []
    for metrics_file in sorted(results.glob("runs/*/metrics.json")):
        record = json.loads(metrics_file.read_text())
        events = [
            json.loads(line)
            for transcript in sorted(metrics_file.parent.glob("transcript-*.jsonl"))
            for line in transcript.read_text().splitlines()
            if line.startswith("{")
        ]
        # Old results may name a version that versions.json no longer lists (a working tree later renamed).
        variant = record.get("playwright") or CONFIG["versions"].get(record["version"], {}).get("playwright", "dev-build")
        record.update(transcript_metrics(events, variant))
        metrics_file.write_text(json.dumps(record, indent=2, ensure_ascii=False))
        records.append(record)
    (results / "records.json").write_text(json.dumps(records, indent=2, ensure_ascii=False))
    print(f"rescored {len(records)} runs in {results}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--versions", default="1.4.0,2.0.1")
    parser.add_argument("--tasks", default="all")
    parser.add_argument("--reps", type=int, default=5)
    parser.add_argument("--model", default="sonnet")
    parser.add_argument("--jobs", type=int, default=6, help="concurrent runs; versions of one (task, rep) start together")
    parser.add_argument("--workdir", default=str(Path(tempfile.gettempdir()) / "mew-agents-bench"))
    parser.add_argument("--rescore", help="recompute metrics from the transcripts in this results directory")
    parser.add_argument("--resume", help="continue an interrupted run in this results directory, skipping finished runs")
    args = parser.parse_args()
    if args.rescore:
        return rescore(Path(args.rescore))

    versions = args.versions.split(",")
    task_ids = sorted(p.name for p in (BENCH / "tasks").iterdir()) if args.tasks == "all" else args.tasks.split(",")
    tasks = [json.loads((BENCH / "tasks" / t / "task.json").read_text()) for t in task_ids]
    workdir = Path(args.workdir)
    workdir.mkdir(parents=True, exist_ok=True)
    check_node()
    out = Path(args.resume) if args.resume else BENCH / "results" / dt.datetime.now().strftime("%Y%m%d-%H%M")
    out.mkdir(parents=True, exist_ok=True)
    base = prepare_base(workdir)

    # Pairs in order (rep-major), each version of a pair submitted back to back.
    jobs = [(v, task, rep) for rep in range(1, args.reps + 1) for task in tasks for v in versions]
    records = [json.loads(m.read_text()) for m in sorted(out.glob("runs/*/metrics.json"))]
    done = {r["run_id"] for r in records}
    jobs = [(v, task, rep) for v, task, rep in jobs if f"{task['id']}__{v}__r{rep}" not in done]
    started = time.time()
    log(f"{len(jobs)} runs, {args.jobs} at a time, model {args.model}")
    with futures.ThreadPoolExecutor(args.jobs) as pool:
        pending = {
            pool.submit(run_one, v, task, rep, args.model, base, workdir, out, 4500 + 10 * i): (v, task["id"], rep)
            for i, (v, task, rep) in enumerate(jobs)
        }
        for job in futures.as_completed(pending):
            record = job.result()
            records.append(record)
            q = record["quality"]
            log(f"{record['run_id']}: {record['wall_s']}s ${record['cost_usd']} hidden={q['hidden']} e2e={q['e2e']} ({len(records) - len(done)}/{len(jobs)})")
            (out / "records.json").write_text(json.dumps(records, indent=2, ensure_ascii=False))
    log(f"done in {(time.time() - started) / 60:.1f} min: {out}")


if __name__ == "__main__":
    main()
