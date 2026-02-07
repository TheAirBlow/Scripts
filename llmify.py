#!/usr/bin/env python3
import argparse
import traceback
from pathlib import Path

parser = argparse.ArgumentParser(description="Convert files into a single LLM-friendly prompt")
parser.add_argument("paths", nargs="+", help="List of files and directories")
parser.add_argument("-e", "--exclude", nargs="+", help="Folder names to exclude", default=[])

args = parser.parse_args()

ignore_list = {'.git', '__pycache__', '.DS_Store', 'venv', '.env'}
if args.exclude:
    ignore_list.update(args.exclude)

for path_str in paths:
    root_path = Path(path_str)

    if not root_path.exists():
        print(f"[!] {path_str} does not exist")
        exit(1)

    files_to_process = root_path.rglob('*') if root_path.is_dir() else [root_path]

    for p in files_to_process:
        if p.is_dir() or any(part in ignore_list for part in p.parts):
            continue

        try:
            content = p.read_text(encoding='utf-8', errors='replace')

            safe_content = content.replace("```", "``\\`")

            print(f"`{p}`:")
            print("```")
            print(safe_content)
            print("```\n")
        except Exception as e:
            traceback.print_exc()
            exit(1)
