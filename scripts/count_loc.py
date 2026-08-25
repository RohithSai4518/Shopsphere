#!/usr/bin/env python3
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

EXCLUDE_DIRS = {
    "node_modules", ".git", ".venv", "venv", "__pycache__", "dist", "build",
    "site-packages", ".pytest_cache", ".idea", ".vscode", "brain", ".system_generated"
}

ALLOWED_EXTENSIONS = {
    ".py": "Python Source",
    ".html": "Django HTML Templates",
    ".css": "CSS Stylesheets",
    ".js": "Vanilla JavaScript Assets",
    ".sql": "SQL Schemas & Migration Queries",
    ".md": "Documentation Documents",
    ".json": "Configuration Data & Fixtures"
}

def count_file_lines(filepath):
    meaningful_count = 0
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            stripped = line.strip()
            if stripped and not stripped.startswith('#') and not stripped.startswith('//') and not stripped.startswith('/*') and not stripped.startswith('<!--'):
                meaningful_count += 1
    return meaningful_count

def count_loc():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    totals_by_ext = {ext: 0 for ext in ALLOWED_EXTENSIONS}
    file_count = 0

    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]

        for file in filenames:
            ext = os.path.splitext(file)[1].lower()
            if ext in ALLOWED_EXTENSIONS:
                filepath = os.path.join(dirpath, file)
                lines = count_file_lines(filepath)
                totals_by_ext[ext] += lines
                file_count += 1

    print("=" * 60)
    print("  SHOPSPHERE MEANINGFUL SOURCE LINE COUNT (PYTHON FULLSTACK)")
    print("=" * 60)
    print(f"Total Source Files Analyzed: {file_count}")
    print("LOC Breakdown by Source Category:")
    for ext, label in ALLOWED_EXTENSIONS.items():
        print(f"  - {ext} ({label}): {totals_by_ext[ext]} meaningful lines")

    total_loc = sum(totals_by_ext.values())
    print("-" * 60)
    print(f"TOTAL MEANINGFUL SOURCE LOC: {total_loc} LOC")
    print("=" * 60)

if __name__ == "__main__":
    count_loc()
