#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import subprocess
import sys

TAG_RE = re.compile(r"^v(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


def validate_version_tag(value: str) -> str:
    value = value.strip()
    if not TAG_RE.fullmatch(value):
        raise ValueError("version must be in form vX.Y.Z")
    return value


def latest_tag() -> tuple[int, int, int]:
    out = subprocess.check_output(
        ["git", "tag", "--list", "v*", "--sort=-v:refname"], text=True
    ).strip()
    if not out:
        return (0, 0, 0)
    for tag in out.splitlines():
        m = TAG_RE.match(tag.strip())
        if m:
            return tuple(int(m.group(i)) for i in (1, 2, 3))
    return (0, 0, 0)


def bump_from_labels(labels: list[str]) -> str:
    s = set(labels)
    if "release:major" in s:
        return "major"
    if "release:minor" in s:
        return "minor"
    return "patch"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bump", choices=["major", "minor", "patch", "auto"], default="auto")
    ap.add_argument("--labels", default="")
    ap.add_argument("--current", default="")
    ap.add_argument("--validate", default="", metavar="VERSION")
    args = ap.parse_args()

    if args.validate:
        try:
            print(validate_version_tag(args.validate))
        except ValueError as error:
            print(f"ERROR: {error}", file=sys.stderr)
            return 1
        return 0

    if args.current:
        try:
            current = validate_version_tag(args.current)
        except ValueError as error:
            print(f"ERROR: --current {error}", file=sys.stderr)
            return 1
        m = TAG_RE.fullmatch(current)
        assert m is not None
        cur = (int(m.group(1)), int(m.group(2)), int(m.group(3)))
    else:
        cur = latest_tag()

    bump = args.bump
    if bump == "auto":
        labels = [x.strip() for x in args.labels.split(",") if x.strip()]
        bump = bump_from_labels(labels)

    major, minor, patch = cur
    if bump == "major":
        nxt = (major + 1, 0, 0)
    elif bump == "minor":
        nxt = (major, minor + 1, 0)
    else:
        nxt = (major, minor, patch + 1)

    print(f"v{nxt[0]}.{nxt[1]}.{nxt[2]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
