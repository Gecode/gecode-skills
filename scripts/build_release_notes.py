#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def changed_skills(diff_range: str, cwd: Path | None = None) -> list[str]:
    out = subprocess.check_output(
        ["git", "diff", "--name-only", diff_range], text=True, cwd=cwd
    )
    names: set[str] = set()
    for line in out.splitlines():
        parts = line.split("/")
        if len(parts) >= 3 and parts[0] == "skills" and parts[1]:
            names.add(parts[1])
    return sorted(names)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--from-ref", required=True)
    ap.add_argument("--to-ref", required=True)
    ap.add_argument("--version", required=True)
    ap.add_argument("--repo", required=True, help="owner/repo")
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    diff_range = f"{args.from_ref}..{args.to_ref}"
    skills = changed_skills(diff_range)

    lines = []
    lines.append(f"# {args.version}")
    lines.append("")
    if skills:
        lines.append("## Changed skills")
        lines.append("")
        for s in skills:
            lines.append(f"- `{s}`")
        lines.append("")
    else:
        lines.append("No skill directory changes detected in this release range.")
        lines.append("")

    lines.append("## Install")
    lines.append("")
    lines.append(f"```bash\nnpx skills add {args.repo}\n```")
    lines.append("")
    lines.append("List available skills:")
    lines.append("")
    lines.append(f"```bash\nnpx skills add {args.repo} --list\n```")

    Path(args.output).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
