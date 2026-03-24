from __future__ import annotations

import argparse
from pathlib import Path

from university1652_baseline.data_interface import (
    DataCheckReport,
    build_gallery_id_index,
    build_query_name_index,
    find_empty_directories,
    read_query_order,
    write_gallery_manifest,
    write_query_manifest,
    write_report,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check challenge data layout and generate manifests.")
    parser.add_argument("--query-order", default="docs/requirement/query_street_name.txt", help="Canonical query order file.")
    parser.add_argument("--query-root", default="data/raw/University-Release/test/query_street", help="Directory containing challenge query images.")
    parser.add_argument("--gallery-root", default="data/raw/University-Release/test/gallery_satellite", help="Directory containing challenge gallery images.")
    parser.add_argument("--manifest-dir", default="data/manifest", help="Output directory for generated manifests.")
    parser.add_argument("--strict", action="store_true", help="Return non-zero exit code if any issue is found.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    query_order_path = Path(args.query_order)
    query_root = Path(args.query_root)
    gallery_root = Path(args.gallery_root)
    manifest_dir = Path(args.manifest_dir)

    if not query_order_path.is_file():
        raise FileNotFoundError(f"Missing query order file: {query_order_path}")

    query_order = read_query_order(query_order_path)
    query_name_index = build_query_name_index(query_root)
    gallery_id_index = build_gallery_id_index(gallery_root)

    query_manifest_path = manifest_dir / "query_manifest.tsv"
    gallery_manifest_path = manifest_dir / "gallery_manifest.tsv"
    report_path = manifest_dir / "data_check_report.json"

    missing_query_count, duplicate_query_name_count = write_query_manifest(
        query_order=query_order,
        query_name_index=query_name_index,
        output_path=query_manifest_path,
    )
    duplicate_gallery_id_count = write_gallery_manifest(
        gallery_id_index=gallery_id_index,
        output_path=gallery_manifest_path,
    )

    empty_dirs = find_empty_directories(query_root) + find_empty_directories(gallery_root)

    report = DataCheckReport(
        query_count=len(query_order),
        gallery_count=len(gallery_id_index),
        missing_query_count=missing_query_count,
        duplicate_query_name_count=duplicate_query_name_count,
        duplicate_gallery_id_count=duplicate_gallery_id_count,
        empty_directory_count=len(empty_dirs),
    )
    write_report(report, report_path)

    print("Data check finished.")
    print(f"- query_count: {report.query_count}")
    print(f"- gallery_count: {report.gallery_count}")
    print(f"- missing_query_count: {report.missing_query_count}")
    print(f"- duplicate_query_name_count: {report.duplicate_query_name_count}")
    print(f"- duplicate_gallery_id_count: {report.duplicate_gallery_id_count}")
    print(f"- empty_directory_count: {report.empty_directory_count}")
    print(f"- query_manifest: {query_manifest_path.as_posix()}")
    print(f"- gallery_manifest: {gallery_manifest_path.as_posix()}")
    print(f"- report: {report_path.as_posix()}")

    has_issue = any(
        [
            report.missing_query_count,
            report.duplicate_query_name_count,
            report.duplicate_gallery_id_count,
            report.empty_directory_count,
        ]
    )
    return 1 if args.strict and has_issue else 0


if __name__ == "__main__":
    raise SystemExit(main())
