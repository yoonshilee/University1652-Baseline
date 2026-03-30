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
    parser.add_argument("--query-root", default="data/test/query_street", help="Directory containing challenge query images.")
    parser.add_argument("--gallery-root", default="data/test/gallery_satellite", help="Directory containing challenge gallery images.")
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

    if not query_root.is_dir():
        message = f"Missing query root directory: {query_root}"
        if args.strict:
            raise FileNotFoundError(message)
        print(message)
        return 1
    if not gallery_root.is_dir():
        message = f"Missing gallery root directory: {gallery_root}"
        if args.strict:
            raise FileNotFoundError(message)
        print(message)
        return 1

    query_order = read_query_order(query_order_path)
    query_name_index = build_query_name_index(query_root)
    gallery_id_index = build_gallery_id_index(gallery_root)

    query_image_count = sum(len(paths) for paths in query_name_index.values())
    gallery_image_count = sum(len(paths) for paths in gallery_id_index.values())

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
        query_image_count=query_image_count,
        gallery_count=len(gallery_id_index),
        gallery_image_count=gallery_image_count,
        missing_query_count=missing_query_count,
        duplicate_query_name_count=duplicate_query_name_count,
        duplicate_gallery_id_count=duplicate_gallery_id_count,
        empty_directory_count=len(empty_dirs),
    )
    write_report(report, report_path)

    print("Data check finished.")
    print(f"- query_count: {report.query_count}")
    print(f"- query_image_count: {report.query_image_count}")
    print(f"- gallery_count: {report.gallery_count}")
    print(f"- gallery_image_count: {report.gallery_image_count}")
    print(f"- missing_query_count: {report.missing_query_count}")
    print(f"- duplicate_query_name_count: {report.duplicate_query_name_count}")
    print(f"- duplicate_gallery_id_count: {report.duplicate_gallery_id_count}")
    print(f"- empty_directory_count: {report.empty_directory_count}")
    print(f"- query_manifest: {query_manifest_path.as_posix()}")
    print(f"- gallery_manifest: {gallery_manifest_path.as_posix()}")
    print(f"- report: {report_path.as_posix()}")

    if report.missing_query_count == report.query_count and report.query_image_count == report.query_count:
        sample_names = sorted(query_name_index.keys())[:20]
        print("All queries are missing, but query_image_count matches query_count.")
        print("This usually means you are using a non-masked/incorrect query set, or the query_root is wrong.")
        print(f"Canonical query names come from: {query_order_path.as_posix()}")
        print(f"Local query_root is: {query_root.as_posix()}")
        print(f"Local query filename samples: {sample_names}")

    has_issue = any(
        [
            report.query_image_count == 0,
            report.gallery_image_count == 0,
            report.missing_query_count,
            report.duplicate_query_name_count,
            report.duplicate_gallery_id_count,
            report.empty_directory_count,
        ]
    )

    if report.query_image_count == 0:
        print(f"No query images found under: {query_root}")
    if report.gallery_image_count == 0:
        print(f"No gallery images found under: {gallery_root}")
    return 1 if args.strict and has_issue else 0


if __name__ == "__main__":
    raise SystemExit(main())

