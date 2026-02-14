from pathlib import Path
from typing import List


def preview_renames(directory: Path, pattern: str, replacement: str) -> List[dict]:
    previews = []
    for path in directory.iterdir():
        if path.is_file() and pattern in path.name:
            new_name = path.name.replace(pattern, replacement)
            previews.append({"old": path.name, "new": new_name})
    return previews


def apply_renames(directory: Path, pattern: str, replacement: str) -> List[dict]:
    applied = []
    for path in directory.iterdir():
        if path.is_file() and pattern in path.name:
            new_name = path.name.replace(pattern, replacement)
            target = path.with_name(new_name)
            path.rename(target)
            applied.append({"old": path.name, "new": target.name})
    return applied
