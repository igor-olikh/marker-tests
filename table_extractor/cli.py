"""Command line interface for table extraction."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .extractor import extract_tables_from_html


def main() -> None:
    """Extract tables from an HTML file and output JSON to stdout."""
    parser = argparse.ArgumentParser(description="Extract tables from an HTML file")
    parser.add_argument("input", type=Path, help="Path to HTML file")
    args = parser.parse_args()

    html = args.input.read_text(encoding="utf-8")
    tables = extract_tables_from_html(html)
    json.dump(tables, fp=sys.stdout)


if __name__ == "__main__":
    main()
