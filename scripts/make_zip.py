#!/usr/bin/env python3
import os
import zipfile
import shutil

EXCLUDE_DIRS = {'.venv', 'venv', 'env', '__pycache__', '.pytest_cache', '.idea', '.vscode', '.git'}
EXCLUDE_FILES = {'db.sqlite3', 'repo.zip', '.DS_Store', '.env', '.env.local', '.env.development', '.env.production'}
EXCLUDE_EXTS = {'.pyc', '.pyo', '.pyd'}

def create_clean_repository_zip():
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    parent_dir = os.path.dirname(repo_dir)

    zip_in_repo = os.path.join(repo_dir, 'repo.zip')
    zip_in_parent = os.path.join(parent_dir, 'repo.zip')

    # Remove existing zip files if present
    for zpath in [zip_in_repo, zip_in_parent]:
        if os.path.exists(zpath):
            try:
                os.remove(zpath)
            except Exception as e:
                print(f"Warning removing old zip {zpath}: {e}")

    print(f"Packaging clean repository zip from {repo_dir} (including .git)...")

    file_count = 0
    total_bytes = 0

    with zipfile.ZipFile(zip_in_repo, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(repo_dir):
            # Prune excluded directories in-place (except keep .git)
            dirs[:] = [d for d in dirs if d in {'.git'} or d not in EXCLUDE_DIRS]

            for file in files:
                if file in EXCLUDE_FILES or file.startswith('.env'):
                    continue
                if any(file.endswith(ext) for ext in EXCLUDE_EXTS):
                    continue

                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, repo_dir)

                zipf.write(full_path, rel_path)
                file_count += 1
                total_bytes += os.path.getsize(full_path)

    # Copy to parent directory (Desktop)
    shutil.copy2(zip_in_repo, zip_in_parent)

    zip_size_mb = os.path.getsize(zip_in_repo) / (1024 * 1024)
    print(f"[SUCCESS] Created clean repository zip with {file_count} files ({zip_size_mb:.2f} MB).")
    print(f"Saved at: {zip_in_repo}")
    print(f"Saved at: {zip_in_parent}")

if __name__ == '__main__':
    create_clean_repository_zip()
