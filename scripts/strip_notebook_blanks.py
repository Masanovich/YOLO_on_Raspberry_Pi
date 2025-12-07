#!/usr/bin/env python3
"""Strip leading blank lines from code cells in Jupyter notebooks.

Usage:
    python scripts/strip_notebook_blanks.py path/to/notebook.ipynb [more.ipynb ...]

It edits files in-place and prints which files were modified.
"""
import json
import sys
from pathlib import Path


def is_blank_line(s: str) -> bool:
    return s.strip() == ""


def strip_leading_blank_lines_from_cell(cell: dict) -> bool:
    """Return True if the cell was modified."""
    if cell.get("cell_type") != "code":
        return False
    src = cell.get("source", [])
    if not isinstance(src, list):
        # older notebooks may store as a single string
        src = src.splitlines(keepends=True)

    i = 0
    while i < len(src) and is_blank_line(src[i]):
        i += 1
    if i == 0:
        return False
    # remove first i items
    new_src = src[i:]
    cell["source"] = new_src
    return True


def process_notebook(path: Path) -> bool:
    data = json.loads(path.read_text(encoding="utf-8"))
    modified = False
    for cell in data.get("cells", []):
        try:
            if strip_leading_blank_lines_from_cell(cell):
                modified = True
        except Exception:
            # ignore malformed cells
            continue
    if modified:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return modified


def main(argv):
    if len(argv) < 2:
        print("Usage: strip_notebook_blanks.py path/to/notebook.ipynb [...]")
        return 2
    ok = True
    for p in argv[1:]:
        path = Path(p)
        if not path.exists():
            print(f"Not found: {path}")
            ok = False
            continue
        try:
            modified = process_notebook(path)
            print(f"{path}: {'modified' if modified else 'unchanged'}")
        except Exception as e:
            print(f"Error processing {path}: {e}")
            ok = False
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
