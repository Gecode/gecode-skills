#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = REPO_ROOT / "skills"
EVALS_DIR = REPO_ROOT / "evals"
MARKDOWN_REFERENCE_RE = re.compile(
    r"`([^`\n]+\.md(?:#[^`\n]+)?)`|"
    r"\[[^\]\n]*\]\(([^)\s]+\.md(?:#[^)\s]+)?)\)"
)
FRONTMATTER_FIELDS = {"name", "description"}
INTERFACE_FIELDS = {"display_name", "short_description", "default_prompt"}


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


def validate_trigger_evals(skill_name: str, errors: list[str]) -> None:
    eval_path = EVALS_DIR / f"{skill_name}-trigger-evals.json"
    if not eval_path.is_file():
        errors.append(f"{skill_name}: missing trigger evals: {eval_path}")
        return

    try:
        cases = json.loads(eval_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as error:
        errors.append(f"{eval_path}: invalid JSON: {error}")
        return

    if not isinstance(cases, list) or not cases:
        errors.append(f"{eval_path}: expected a non-empty JSON array")
        return

    seen_queries: set[str] = set()
    outcomes: set[bool] = set()
    for index, case in enumerate(cases):
        location = f"{eval_path}[{index}]"
        if not isinstance(case, dict):
            errors.append(f"{location}: expected an object")
            continue
        query = case.get("query")
        should_trigger = case.get("should_trigger")
        if not isinstance(query, str) or not query.strip():
            errors.append(f"{location}: query must be a non-empty string")
        elif query in seen_queries:
            errors.append(f"{location}: duplicate query")
        else:
            seen_queries.add(query)
        if not isinstance(should_trigger, bool):
            errors.append(f"{location}: should_trigger must be a boolean")
        else:
            outcomes.add(should_trigger)

    if outcomes != {False, True}:
        errors.append(f"{eval_path}: include both triggering and non-triggering cases")


def markdown_references(source: Path) -> set[str]:
    references = set()
    for match in MARKDOWN_REFERENCE_RE.finditer(source.read_text(encoding="utf-8")):
        reference = match.group(1) or match.group(2)
        references.add(reference.split("#", 1)[0])
    return references


def validate_reference_graph(skill_dir: Path) -> list[str]:
    skill_dir = skill_dir.resolve()
    skill_md = skill_dir / "SKILL.md"
    markdown_files = {path.resolve() for path in skill_dir.rglob("*.md")}
    graph: dict[Path, set[Path]] = {path: set() for path in markdown_files}
    errors: list[str] = []

    for source in markdown_files:
        for reference in markdown_references(source):
            target = (source.parent / reference).resolve()
            try:
                target.relative_to(skill_dir)
            except ValueError:
                errors.append(f"{source}: Markdown reference escapes skill: {reference}")
                continue
            if not target.is_file():
                errors.append(f"{source}: referenced Markdown file does not exist: {reference}")
                continue
            graph[source].add(target)

    reachable: set[Path] = set()
    pending = [skill_md]
    while pending:
        source = pending.pop()
        if source in reachable:
            continue
        reachable.add(source)
        pending.extend(graph.get(source, ()))

    references_dir = skill_dir / "references"
    reference_files = (
        {path.resolve() for path in references_dir.rglob("*.md")}
        if references_dir.is_dir()
        else set()
    )
    for orphan in sorted(reference_files - reachable):
        errors.append(f"{orphan}: reference is not reachable from {skill_md}")

    return errors


def main() -> int:
    if not SKILLS_DIR.exists():
        print(f"ERROR: skills directory not found: {SKILLS_DIR}")
        return 1

    errors: list[str] = []
    seen_names: dict[str, Path] = {}

    skill_dirs = sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir())
    if not skill_dirs:
        errors.append("no skills found")

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

        unexpected_fields = sorted(set(fm) - FRONTMATTER_FIELDS)
        if unexpected_fields:
            errors.append(
                f"{skill_md}: unsupported frontmatter fields: {', '.join(unexpected_fields)}"
            )

        errors.extend(validate_reference_graph(skill_dir))

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

        agents_dir = skill_dir / "agents"
        if agents_dir.exists():
            openai_yaml = agents_dir / "openai.yaml"
            if not openai_yaml.is_file():
                errors.append(f"{skill_dir}: agents/ exists but agents/openai.yaml is missing")
            else:
                metadata = openai_yaml.read_text(encoding="utf-8")
                for field in sorted(INTERFACE_FIELDS):
                    if not re.search(rf"(?m)^\s{{2}}{field}:\s*\S", metadata):
                        errors.append(f"{openai_yaml}: missing interface field '{field}'")

        validate_trigger_evals(skill_dir.name, errors)

    if errors:
        print("Skill validation failed:")
        for e in errors:
            print(f"- {e}")
        return 1

    print(f"Validated {len(skill_dirs)} skill successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
