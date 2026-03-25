from __future__ import annotations

import argparse
from pathlib import Path
import zipfile

import numpy as np
import scipy.io

from university1652_baseline.submission import validate_submission


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export challenge-compliant answer.txt from feature mat output.")
    parser.add_argument("--mat", default="outputs/pytorch_result.mat", help="Path to mat file containing query/gallery features.")
    parser.add_argument("--query-order", default="docs/requirement/query_street_name.txt", help="Canonical query order file.")
    parser.add_argument("--answer", default="outputs/answer.txt", help="Output answer.txt path.")
    parser.add_argument("--archive", default="outputs/answer.zip", help="Output answer.zip path.")
    parser.add_argument("--topk", default=10, type=int, help="Top-k gallery ids per query.")
    parser.add_argument("--query-paths", default="outputs/query_name.txt", help="Optional query path list written by scripts/test.py.")
    parser.add_argument("--gallery-paths", default="outputs/gallery_name.txt", help="Optional gallery path list written by scripts/test.py.")
    return parser.parse_args()


def _read_lines(path: Path) -> list[str]:
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _load_path_list(path: Path) -> list[str] | None:
    return _read_lines(path) if path.is_file() else None


def _to_string_list(raw: object) -> list[str]:
    arr = np.array(raw).squeeze()
    if arr.ndim == 0:
        return [str(arr.item())]
    return [str(x.item() if hasattr(x, "item") else x) for x in arr]


def _stem_from_path(path: str) -> str:
    return Path(path).stem


def _name_from_path(path: str) -> str:
    return Path(path).name


def _zip_answer(answer_path: Path, archive_path: Path) -> None:
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.write(answer_path, arcname="answer.txt")


def main() -> int:
    args = parse_args()
    mat_path = Path(args.mat)
    query_order_path = Path(args.query_order)
    answer_path = Path(args.answer)
    archive_path = Path(args.archive)

    if not mat_path.is_file():
        raise FileNotFoundError(f"Missing mat file: {mat_path}")
    if not query_order_path.is_file():
        raise FileNotFoundError(f"Missing query order file: {query_order_path}")

    mat = scipy.io.loadmat(mat_path)
    if "query_f" not in mat or "gallery_f" not in mat:
        raise KeyError("mat file must contain `query_f` and `gallery_f`.")

    query_f = np.asarray(mat["query_f"], dtype=np.float32)
    gallery_f = np.asarray(mat["gallery_f"], dtype=np.float32)

    query_paths = _load_path_list(Path(args.query_paths))
    gallery_paths = _load_path_list(Path(args.gallery_paths))

    if query_paths is None:
        if "query_path" not in mat:
            raise KeyError("Missing query paths: provide --query-paths or include `query_path` in mat.")
        query_paths = _to_string_list(mat["query_path"])
    if gallery_paths is None:
        if "gallery_path" not in mat:
            raise KeyError("Missing gallery paths: provide --gallery-paths or include `gallery_path` in mat.")
        gallery_paths = _to_string_list(mat["gallery_path"])

    if len(query_paths) != len(query_f):
        raise ValueError(f"query paths count ({len(query_paths)}) != query_f rows ({len(query_f)}).")
    if len(gallery_paths) != len(gallery_f):
        raise ValueError(f"gallery paths count ({len(gallery_paths)}) != gallery_f rows ({len(gallery_f)}).")

    if args.topk <= 0:
        raise ValueError(f"--topk must be positive, got {args.topk}.")
    if args.topk > len(gallery_paths):
        raise ValueError(f"--topk ({args.topk}) cannot exceed gallery size ({len(gallery_paths)}).")

    query_name_to_index: dict[str, int] = {}
    for i, path in enumerate(query_paths):
        name = _name_from_path(path)
        if name in query_name_to_index:
            raise ValueError(f"Duplicate query filename detected: {name}")
        query_name_to_index[name] = i

    gallery_ids = [_stem_from_path(path) for path in gallery_paths]

    query_order = _read_lines(query_order_path)
    scores = np.matmul(query_f, gallery_f.T)

    answer_lines: list[str] = []
    for query_name in query_order:
        if query_name not in query_name_to_index:
            raise ValueError(f"Query not found in extracted features: {query_name}")
        q_idx = query_name_to_index[query_name]
        row = scores[q_idx]
        topk_idx = np.argpartition(-row, args.topk - 1)[: args.topk]
        topk_idx = topk_idx[np.argsort(-row[topk_idx])]
        topk_ids = [gallery_ids[i] for i in topk_idx]
        answer_lines.append(" ".join(topk_ids))

    answer_path.parent.mkdir(parents=True, exist_ok=True)
    answer_path.write_text("\n".join(answer_lines) + "\n", encoding="utf-8")

    _zip_answer(answer_path, archive_path)
    validate_submission(answer_path=answer_path, query_order_path=query_order_path, archive_path=archive_path)

    print("Submission export completed.")
    print(f"- answer: {answer_path.as_posix()}")
    print(f"- archive: {archive_path.as_posix()}")
    print(f"- lines: {len(answer_lines)}")
    print(f"- topk: {args.topk}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
