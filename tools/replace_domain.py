#!/usr/bin/env python3
"""
Replace hardcoded domain strings across the repo for safe deployment.

Usage:
  python tools/replace_domain.py --from kronus.co --to mydomain.com --apply
  python tools/replace_domain.py --from kronus.co --to mydomain.local --dry-run
"""
import argparse
import os
import fnmatch
from pathlib import Path

TEXT_EXT = {
    "*.py", "*.rs", "*.toml", "*.json", "*.md", "*.txt", "*.html", "*.lua", "*.yml", "*.yaml"
}


def iter_files(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        # skip .git and binary dirs
        if ".git" in dirpath.split(os.sep):
            continue
        for name in filenames:
            full = Path(dirpath) / name
            for pat in TEXT_EXT:
                if fnmatch.fnmatch(name, pat):
                    yield full
                    break


def replace_in_file(path: Path, frm: str, to: str, apply: bool) -> int:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return 0
    if frm not in text:
        return 0
    new = text.replace(frm, to)
    if apply:
        path.write_text(new, encoding="utf-8")
    return text.count(frm)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--from", dest="frm", required=True)
    p.add_argument("--to", dest="to", required=True)
    p.add_argument("--apply", action="store_true")
    p.add_argument("--root", default=".")
    args = p.parse_args()

    root = Path(args.root)
    total = 0
    results = []
    for f in iter_files(root):
        count = replace_in_file(f, args.frm, args.to, args.apply)
        if count:
            results.append((str(f), count))
            total += count

    for fp, cnt in results:
        print(f"{cnt} occurrence(s) in {fp}")
    print(f"Total replacements found: {total}")
    if not args.apply:
        print("Dry-run complete. Rerun with --apply to modify files.")


if __name__ == "__main__":
    main()
