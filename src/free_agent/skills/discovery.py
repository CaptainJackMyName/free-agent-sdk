"""Filesystem discovery of SKILL.md files."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, List, Optional


def discover_skills(paths: Optional[Iterable[str]] = None) -> List[Path]:
    """Find all ``SKILL.md`` files under the given directories.

    When ``paths`` is empty, searches the conventional skill roots:
    ``.claude/skills`` and ``.free_agent/skills`` relative to the current
    working directory.
    """
    roots: List[Path] = []
    if paths:
        roots = [Path(p).expanduser() for p in paths]
    else:
        roots = [
            Path.cwd() / ".claude" / "skills",
            Path.cwd() / ".free_agent" / "skills",
        ]

    found: List[Path] = []
    for root in roots:
        if not root.exists():
            continue
        if root.is_file() and root.name == "SKILL.md":
            found.append(root)
        elif root.is_dir():
            found.extend(sorted(root.rglob("SKILL.md")))
    return found


__all__ = ["discover_skills"]
