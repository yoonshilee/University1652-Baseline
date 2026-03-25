from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json

IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}


@dataclass
class DataCheckReport:
    query_count: int
    query_image_count: int
    gallery_count: int
    gallery_image_count: int
    missing_query_count: int
    duplicate_query_name_count: int
    duplicate_gallery_id_count: int
    empty_directory_count: int


def iter_image_files(root: Path) -> list[Path]:
    if not root.is_dir():
        return []
    return sorted(
        p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in IMAGE_SUFFIXES
    )


def identifier_from_image(path: Path) -> str:
    return path.stem


def read_query_order(query_order_path: Path) -> list[str]:
    return [line.strip() for line in query_order_path.read_text(encoding="utf-8").splitlines() if line.strip()]


def build_query_name_index(query_root: Path) -> dict[str, list[Path]]:
    index: dict[str, list[Path]] = {}
    for path in iter_image_files(query_root):
        index.setdefault(path.name, []).append(path)
    return index


def build_gallery_id_index(gallery_root: Path) -> dict[str, list[Path]]:
    index: dict[str, list[Path]] = {}
    for path in iter_image_files(gallery_root):
        index.setdefault(identifier_from_image(path), []).append(path)
    return index


def find_empty_directories(root: Path) -> list[Path]:
    if not root.is_dir():
        return []
    empty: list[Path] = []
    for d in sorted([p for p in root.rglob("*") if p.is_dir()]):
        has_file = any(child.is_file() for child in d.rglob("*"))
        if not has_file:
            empty.append(d)
    return empty


def write_query_manifest(query_order: list[str], query_name_index: dict[str, list[Path]], output_path: Path) -> tuple[int, int]:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    missing = 0
    duplicated = 0
    lines = ["query_index\tquery_name\tquery_path\tstatus"]
    for i, query_name in enumerate(query_order, start=1):
        matched = query_name_index.get(query_name, [])
        if not matched:
            missing += 1
            lines.append(f"{i}\t{query_name}\t\tmissing")
            continue
        if len(matched) > 1:
            duplicated += 1
            paths = "|".join(str(p.as_posix()) for p in matched)
            lines.append(f"{i}\t{query_name}\t{paths}\tduplicate")
            continue
        lines.append(f"{i}\t{query_name}\t{matched[0].as_posix()}\tok")
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return missing, duplicated


def write_gallery_manifest(gallery_id_index: dict[str, list[Path]], output_path: Path) -> int:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    duplicate_ids = 0
    lines = ["gallery_id\tgallery_path\tstatus"]
    for gallery_id in sorted(gallery_id_index.keys()):
        matched = gallery_id_index[gallery_id]
        if len(matched) > 1:
            duplicate_ids += 1
            paths = "|".join(str(p.as_posix()) for p in matched)
            lines.append(f"{gallery_id}\t{paths}\tduplicate")
            continue
        lines.append(f"{gallery_id}\t{matched[0].as_posix()}\tok")
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return duplicate_ids


def write_report(report: DataCheckReport, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report.__dict__, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
