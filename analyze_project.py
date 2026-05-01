#!/usr/bin/env python3
"""Simple project analyzer.

Scans a directory, counts files by extension, and prints basic stats.
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import argparse


def analyze_project(root: Path) -> dict:
    ignored_dirs = {".git", "node_modules", ".venv", "venv", "__pycache__"}

    files = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in ignored_dirs for part in path.parts):
            continue
        files.append(path)

    ext_counter = Counter(p.suffix.lower() or "<no_ext>" for p in files)
    total_size = sum(p.stat().st_size for p in files)

    largest_files = sorted(files, key=lambda p: p.stat().st_size, reverse=True)[:10]

    return {
        "root": root,
        "total_files": len(files),
        "total_size": total_size,
        "by_extension": ext_counter,
        "largest_files": largest_files,
    }


def format_size(size: int) -> str:
    units = ["B", "KB", "MB", "GB"]
    value = float(size)
    for unit in units:
        if value < 1024 or unit == units[-1]:
            return f"{value:.2f} {unit}"
        value /= 1024
    return f"{size} B"


def print_report(report: dict) -> None:
    print(f"Project path: {report['root']}")
    print(f"Total files: {report['total_files']}")
    print(f"Total size: {format_size(report['total_size'])}")

    print("\nFiles by extension:")
    for ext, count in report["by_extension"].most_common():
        print(f"  {ext:10} {count}")

    print("\nTop 10 largest files:")
    for path in report["largest_files"]:
        print(f"  {format_size(path.stat().st_size):>10}  {path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze files in a project folder")
    parser.add_argument("path", nargs="?", default=".", help="Path to project folder")
    args = parser.parse_args()

    root = Path(args.path).resolve()
    if not root.exists() or not root.is_dir():
        raise SystemExit(f"Not a directory: {root}")

    report = analyze_project(root)
    print_report(report)


if __name__ == "__main__":
    main()
