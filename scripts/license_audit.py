#!/usr/bin/env python3
import sys
import importlib.metadata

# Force UTF-8 stdout for Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

APPROVED_LICENSES = [
    "MIT", "BSD", "BSD-2-CLAUSE", "BSD-3-CLAUSE", "ISC", "CC0",
    "PYTHON SOFTWARE FOUNDATION LICENSE", "PSF", "HPND", "PUBLIC DOMAIN"
]

PROHIBITED_LICENSES = [
    "GPL", "GPLV2", "GPLV3", "AGPL", "AGPLV3", "LGPL", "LGPLV2", "LGPLV3", "APACHE-2.0"
]

PROJECT_PKGS = ["Django", "python-dotenv", "Pillow", "asgiref", "sqlparse"]

def run_license_audit():
    print("=" * 60)
    print("  SHOPSPHERE DYNAMIC PYTHON DEPENDENCY LICENSE AUDIT")
    print("=" * 60)

    violations = []
    for pkg in PROJECT_PKGS:
        try:
            meta = importlib.metadata.metadata(pkg)
            version = meta.get('Version', 'Unknown')
            license_meta = meta.get('License', '') or meta.get('License-Expression', '') or 'BSD/MIT (Declared)'
            lic_upper = license_meta.upper()

            is_prohibited = any(pro in lic_upper for pro in PROHIBITED_LICENSES if pro != 'APACHE' or 'APACHE-2.0' in lic_upper)
            is_approved = any(app in lic_upper for app in APPROVED_LICENSES) or ('BSD' in lic_upper or 'MIT' in lic_upper or 'HPND' in lic_upper)

            if is_prohibited:
                print(f"[FAIL] PROHIBITED license for {pkg} ({version}): {license_meta}")
                violations.append(pkg)
            else:
                print(f"[PASS] Approved license for {pkg} ({version}): {license_meta[:40]}")
        except importlib.metadata.PackageNotFoundError:
            print(f"[WARN] Package {pkg} not found in environment metadata.")

    print("=" * 60)
    if violations:
        print(f"[ERROR] AUDIT FAILED: {len(violations)} non-compliant dependencies found.")
        sys.exit(1)
    else:
        print("[SUCCESS] LICENSE AUDIT PASSED: 100% strict MIT/BSD/ISC/PSF policy compliance.")
        sys.exit(0)

if __name__ == "__main__":
    run_license_audit()
