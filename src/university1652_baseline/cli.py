from __future__ import annotations

import argparse
from pathlib import Path

from .submission import validate_submission


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cross-view-g2s",
        description="Utilities for the University-1652 ground-to-satellite challenge workflow.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    layout_parser = subparsers.add_parser("layout", help="Show the repository layout and recommended uv commands.")
    layout_parser.set_defaults(func=run_layout)

    validate_parser = subparsers.add_parser(
        "validate-submission",
        help="Validate answer.txt and optional answer.zip against challenge rules.",
    )
    validate_parser.add_argument("--answer", default="answer.txt", help="Path to answer.txt.")
    validate_parser.add_argument(
        "--query-order",
        default="docs/requirement/query_street_name.txt",
        help="Path to the canonical query order file.",
    )
    validate_parser.add_argument(
        "--archive",
        default=None,
        help="Optional path to answer.zip. When provided, the archive must contain answer.txt at the root.",
    )
    validate_parser.set_defaults(func=run_validate_submission)
    return parser


def run_layout(_: argparse.Namespace) -> int:
    print("Project layout")
    print("  src/university1652_baseline/   reusable model and utility modules")
    print("  scripts/                       training, evaluation, demo, and data-prep entrypoints")
    print("  docs/requirement/              challenge rules and provided examples")
    print("  docs/reference/                legacy reference files from the upstream baseline")
    print("  third_party/gpu_re_ranking/    optional reranking extension")
    print("  model/                         checkpoints and exported opts.yaml files")
    print("  data/                          local datasets (gitignored)")
    print("")
    print("Recommended commands")
    print("  uv sync")
    print("  uv run python scripts/train.py --help")
    print("  uv run python scripts/test.py --help")
    print("  uv run cross-view-g2s validate-submission --answer answer.txt --archive answer.zip")
    return 0


def run_validate_submission(args: argparse.Namespace) -> int:
    validate_submission(
        answer_path=Path(args.answer),
        query_order_path=Path(args.query_order),
        archive_path=Path(args.archive) if args.archive else None,
    )
    print("Submission validation passed.")
    return 0


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
