#!/usr/bin/env python
"""
Fixture Validation Utility for ShopSphere.
Verifies JSON integrity, mandatory relational fields, and schema consistency.
"""

import json
import os
import sys
from pathlib import Path


def validate_fixtures_directory(fixtures_dir: Path) -> bool:
    """Validate all JSON fixture files within the directory."""
    if not fixtures_dir.exists():
        print(f"[ERROR] Fixtures directory not found: {fixtures_dir}")
        return False

    all_valid = True
    json_files = list(fixtures_dir.glob("*.json"))
    print(f"[INFO] Found {len(json_files)} fixture files in {fixtures_dir}")

    for file_path in json_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            if not isinstance(data, list):
                print(f"[FAIL] {file_path.name}: Root JSON must be an array of records.")
                all_valid = False
                continue

            # Verify Django fixture format
            record_count = len(data)
            for idx, record in enumerate(data):
                if not isinstance(record, dict) or "model" not in record or "pk" not in record:
                    print(f"[FAIL] {file_path.name}: Record #{idx} missing 'model' or 'pk' fields.")
                    all_valid = False
                    break
            else:
                print(f"[OK] {file_path.name}: Validated {record_count} fixture records.")

        except Exception as e:
            print(f"[ERROR] {file_path.name}: JSON parse failure - {e}")
            all_valid = False

    return all_valid


if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent.parent
    target_fixtures = base_dir / "fixtures"
    success = validate_fixtures_directory(target_fixtures)
    sys.exit(0 if success else 1)
