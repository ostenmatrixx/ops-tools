from io import BytesIO
from pathlib import PurePosixPath
from typing import Iterable, List
from zipfile import ZIP_DEFLATED, ZipFile


def _normalize_relpath(raw_name: str) -> str:
    return raw_name.replace("\\", "/").lstrip("/")


def preview_renames(files: Iterable, pattern: str, replacement: str) -> List[dict]:
    previews = []
    for file_obj in files:
        raw_name = getattr(file_obj, "filename", "") or ""
        if not raw_name:
            continue

        rel_path = _normalize_relpath(raw_name)
        path_obj = PurePosixPath(rel_path)
        original_name = path_obj.name
        if pattern not in original_name:
            continue

        new_name = original_name.replace(pattern, replacement)
        new_rel = str(path_obj.with_name(new_name))
        previews.append({"old": rel_path, "new": new_rel})
    return previews


def _unique_name(desired_name: str, used_names: set[str]) -> str:
    if desired_name not in used_names:
        used_names.add(desired_name)
        return desired_name

    path_obj = PurePosixPath(desired_name)
    stem = path_obj.stem
    suffix = path_obj.suffix
    parent = path_obj.parent
    index = 1

    while True:
        candidate_base = f"{stem}_{index}{suffix}"
        candidate = str(parent / candidate_base) if str(parent) != "." else candidate_base
        if candidate not in used_names:
            used_names.add(candidate)
            return candidate
        index += 1


def apply_renames(files: Iterable, pattern: str, replacement: str) -> tuple[BytesIO, List[dict]]:
    archive = BytesIO()
    applied: List[dict] = []
    used_output_names: set[str] = set()

    with ZipFile(archive, mode="w", compression=ZIP_DEFLATED) as zip_file:
        for file_obj in files:
            raw_name = getattr(file_obj, "filename", "") or ""
            if not raw_name:
                continue

            rel_path = _normalize_relpath(raw_name)
            path_obj = PurePosixPath(rel_path)
            original_name = path_obj.name
            if pattern not in original_name:
                continue

            new_name = original_name.replace(pattern, replacement)
            new_rel = str(path_obj.with_name(new_name))
            unique_rel = _unique_name(new_rel, used_output_names)

            data = file_obj.read()
            file_obj.stream.seek(0)
            zip_file.writestr(unique_rel, data)
            applied.append({"old": rel_path, "new": unique_rel})

    archive.seek(0)
    return archive, applied
