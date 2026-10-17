"""Render the template at a given version into a workspace, without an agent.

Fills {{VARIABLES}}, {{STACK:<snippet>}} markers, and the {{RUN:}}/{{EXEC:}}/{{DLX:}}
package-manager forms (pnpm), so a benchmark measures the rules and not the variance
of an agent applying them.
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PM_FORMS = {"RUN": "pnpm run", "EXEC": "pnpm exec", "DLX": "pnpm dlx"}


def read_tree(ref: str, prefix: str) -> dict[str, tuple[str, bool]]:
    """Return {relative path: (content, is_symlink)} for files under prefix at ref."""
    files: dict[str, tuple[str, bool]] = {}
    if ref == "WORKTREE":
        root = REPO / prefix
        for dirpath, dirnames, filenames in os.walk(root):
            for name in dirnames + filenames:
                path = Path(dirpath) / name
                rel = str(path.relative_to(root))
                if path.is_symlink():
                    files[rel] = (os.readlink(path), True)
                    if name in dirnames:
                        dirnames.remove(name)
                elif path.is_file():
                    files[rel] = (path.read_text(), False)
        return files
    listing = subprocess.run(
        ["git", "ls-tree", "-r", ref, prefix], cwd=REPO, check=True, capture_output=True, text=True
    ).stdout
    for line in listing.splitlines():
        meta, path = line.split("\t", 1)
        mode = meta.split()[0]
        content = subprocess.run(
            ["git", "show", f"{ref}:{path}"], cwd=REPO, check=True, capture_output=True, text=True
        ).stdout
        files[path[len(prefix) + 1 :]] = (content, mode == "120000")
    return files


def read_file(ref: str, path: str) -> str:
    if ref == "WORKTREE":
        return (REPO / path).read_text()
    return subprocess.run(
        ["git", "show", f"{ref}:{path}"], cwd=REPO, check=True, capture_output=True, text=True
    ).stdout


def stack_snippets(text: str) -> dict[str, str]:
    snippets: dict[str, str] = {}
    for match in re.finditer(r"^### (\S+)\n(.*?)(?=^### |\Z)", text, re.S | re.M):
        snippets[match.group(1)] = match.group(2).strip()
    return snippets


def fill(text: str, values: dict[str, str], snippets: dict[str, str]) -> str:
    text = re.sub(r"\{\{STACK:([a-z0-9-]+)\}\}", lambda m: snippets[m.group(1)], text)
    # `(?!\})` keeps `${PORT}}}` intact: the form closes on the last pair of braces.
    text = re.sub(
        r"\{\{(RUN|EXEC|DLX):(.*?)\}\}(?!\})", lambda m: f"{PM_FORMS[m.group(1)]} {m.group(2)}", text
    )
    return re.sub(r"\{\{([A-Z0-9_]+)\}\}", lambda m: values.get(m.group(1), m.group(0)), text)


def render(version: str, out: Path) -> list[str]:
    config = json.loads((REPO / "bench" / "versions.json").read_text())
    spec = config["versions"][version]
    values = {**config["common"], **spec["vars"], "TEMPLATE_VERSION": version}
    snippets = stack_snippets(read_file(spec["ref"], f"stacks/{values['STACK']}.md"))
    leftovers: list[str] = []
    for rel, (content, is_symlink) in read_tree(spec["ref"], "template").items():
        target = out / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if is_symlink:
            if target.exists() or target.is_symlink():
                target.unlink()
            target.symlink_to(content)
            continue
        rendered = fill(content, values, snippets)
        leftovers += [f"{rel}: {m}" for m in re.findall(r"\{\{[^}]*\}\}", rendered)]
        target.write_text(rendered)
    return leftovers


if __name__ == "__main__":
    left = render(sys.argv[1], Path(sys.argv[2]))
    print("\n".join(left) if left else "rendered without leftovers")
