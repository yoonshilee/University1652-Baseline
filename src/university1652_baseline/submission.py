from __future__ import annotations

from pathlib import Path
import zipfile


EXPECTED_QUERY_COUNT = 2579
EXPECTED_TOPK = 10
FORBIDDEN_SUFFIXES = (".jpg", ".jpeg", ".png")


def _read_nonempty_lines(path: Path) -> list[str]:
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def validate_submission(answer_path: Path, query_order_path: Path, archive_path: Path | None = None) -> None:
    if not answer_path.is_file():
        raise FileNotFoundError(f"Missing answer file: {answer_path}")
    if answer_path.name != "answer.txt":
        raise ValueError(f"Answer file must be named answer.txt, got {answer_path.name}.")
    if not query_order_path.is_file():
        raise FileNotFoundError(f"Missing query order file: {query_order_path}")

    query_lines = _read_nonempty_lines(query_order_path)
    if len(query_lines) != EXPECTED_QUERY_COUNT:
        raise ValueError(
            f"Expected {EXPECTED_QUERY_COUNT} queries in {query_order_path}, got {len(query_lines)}."
        )

    answer_lines = answer_path.read_text(encoding="utf-8").splitlines()
    if len(answer_lines) != len(query_lines):
        raise ValueError(
            f"Expected {len(query_lines)} lines in {answer_path}, got {len(answer_lines)}."
        )

    for line_number, raw_line in enumerate(answer_lines, start=1):
        tokens = raw_line.split()
        if len(tokens) != EXPECTED_TOPK:
            raise ValueError(
                f"Line {line_number} must contain exactly {EXPECTED_TOPK} identifiers, got {len(tokens)}."
            )
        bad_tokens = [token for token in tokens if token.lower().endswith(FORBIDDEN_SUFFIXES)]
        if bad_tokens:
            raise ValueError(
                f"Line {line_number} contains identifiers with image suffixes: {', '.join(bad_tokens)}."
            )

    if archive_path is not None:
        if archive_path.name != "answer.zip":
            raise ValueError(f"Archive must be named answer.zip, got {archive_path.name}.")
        if not archive_path.is_file():
            raise FileNotFoundError(f"Missing archive: {archive_path}")
        with zipfile.ZipFile(archive_path) as zf:
            names = {name.replace('\\', '/') for name in zf.namelist()}
        if "answer.txt" not in names:
            raise ValueError("answer.zip must contain answer.txt at the archive root.")
