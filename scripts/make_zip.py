#!/usr/bin/env python3
import os
import zipfile
import shutil

EXCLUDE_DIRS = {'.venv', 'venv', 'env', '__pycache__', '.pytest_cache', '.idea', '.vscode', 'node_modules'}
EXCLUDE_FILES = {'db.sqlite3', 'repo.zip', 'Amazon_Clone.zip', '.DS_Store', '.env', '.env.local', '.env.development', '.env.production'}
EXCLUDE_EXTS = {'.pyc', '.pyo', '.pyd', '.zip'}

def create_clean_repository_zip():
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    parent_dir = os.path.dirname(repo_dir)

    primary_zip = os.path.join(repo_dir, 'Amazon_Clone.zip')

    # Remove existing zip if present
    if os.path.exists(primary_zip):
        try:
            os.remove(primary_zip)
        except Exception as e:
            print(f"Warning removing old zip {primary_zip}: {e}")

    print(f"Packaging clean repository zip from {repo_dir} (including .git, excluding node_modules/cache)...")

    file_count = 0
    total_bytes = 0

    with zipfile.ZipFile(primary_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
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

    zip_size_mb = os.path.getsize(primary_zip) / (1024 * 1024)
    print(f"[SUCCESS] Created clean repository zip with {file_count} files ({zip_size_mb:.2f} MB).")

    # Target destination: Local Disk E:
    destinations = []
    if os.path.exists('E:\\'):
        destinations.append('E:\\Amazon_Clone.zip')
    else:
        destinations.append(os.path.join(parent_dir, 'Amazon_Clone.zip'))

    for dest in destinations:
        try:
            shutil.copy2(primary_zip, dest)
            print(f"Saved at: {dest}")
        except Exception as err:
            print(f"Error copying to {dest}: {err}")

if __name__ == '__main__':
    create_clean_repository_zip()
