#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = REPO_ROOT / "skills"


def parse_frontmatter(skill_md: Path) -> dict[str, str]:
    text = skill_md.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing opening frontmatter delimiter '---'")

    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        raise ValueError("missing closing frontmatter delimiter '---'")

    fm = {}
    kv_re = re.compile(r"^([A-Za-z0-9_-]+):\s*(.*)$")
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m = kv_re.match(line)
        if not m:
            continue
        key, raw_val = m.group(1), m.group(2).strip()
        if raw_val.startswith('"') and raw_val.endswith('"') and len(raw_val) >= 2:
            raw_val = raw_val[1:-1]
        if raw_val.startswith("'") and raw_val.endswith("'") and len(raw_val) >= 2:
            raw_val = raw_val[1:-1]
        fm[key] = raw_val
    return fm


def main() -> int:
    errors: list[str] = []
    seen_names: dict[str, Path] = {}
    validated = 0

    if not SKILLS_DIR.exists():
        print("No skills directory found; validation succeeded with 0 skills.")
        return 0

    skill_dirs = sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir())
    if not skill_dirs:
        print("No skill directories found; validation succeeded with 0 skills.")
        return 0

    for skill_dir in skill_dirs:
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            errors.append(f"{skill_dir}: missing SKILL.md")
            continue

        try:
            fm = parse_frontmatter(skill_md)
        except ValueError as e:
            errors.append(f"{skill_md}: {e}")
            continue

        for req in ("name", "description"):
            if req not in fm or not fm[req].strip():
                errors.append(f"{skill_md}: missing required frontmatter field '{req}'")

        name = fm.get("name", "")
        if name and name != skill_dir.name:
            errors.append(
                f"{skill_md}: frontmatter name '{name}' does not match directory '{skill_dir.name}'"
            )

        if name:
            if name in seen_names:
                errors.append(
                    f"duplicate skill name '{name}' in {skill_md} and {seen_names[name]}"
                )
            else:
                seen_names[name] = skill_md
            validated += 1

        agents_dir = skill_dir / "agents"
        if agents_dir.exists() and not (agents_dir / "openai.yaml").exists():
            errors.append(f"{skill_dir}: agents/ exists but agents/openai.yaml is missing")

    if errors:
        print("Skill validation failed:")
        for e in errors:
            print(f"- {e}")
        return 1

    noun = "skill" if validated == 1 else "skills"
    print(f"Validated {validated} {noun} successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
