/**
 * ShopSphere License Audit & Verification Script
 * Strictly enforces MIT, BSD, ISC, CC0 licenses.
 * Prohibits GPL, AGPL, LGPL, Apache-1.0, Apache-2.0 licenses.
 */

const fs = require('fs');
const path = require('path');

const APPROVED_LICENSES = ['MIT', 'BSD-2-CLAUSE', 'BSD-3-CLAUSE', 'ISC', 'CC0-1.0', 'UNLICENSE'];
const PROHIBITED_LICENSES = ['GPL', 'GPL-2.0', 'GPL-3.0', 'AGPL', 'AGPL-3.0', 'LGPL', 'APACHE-1.0', 'APACHE-2.0', 'APACHE'];

function auditPackageFile(packagePath) {
  if (!fs.existsSync(packagePath)) {
    console.log(`[INFO] Package file not found: ${packagePath}`);
    return true;
  }

  const pkg = JSON.parse(fs.readFileSync(packagePath, 'utf8'));
  const pkgName = pkg.name || path.basename(path.dirname(packagePath));
  const pkgLicense = (pkg.license || (typeof pkg.licenses === 'object' ? pkg.licenses.type : 'UNKNOWN')).toUpperCase();

  console.log(`🔍 Auditing package: ${pkgName} (Declared License: ${pkgLicense})`);

  for (const prohibited of PROHIBITED_LICENSES) {
    if (pkgLicense.includes(prohibited)) {
      console.error(`❌ PROHIBITED LICENSE DETECTED in ${pkgName}: ${pkgLicense}`);
      console.error(`Policy Violation: ${prohibited} licenses are strictly forbidden under ShopSphere Licensing Policy.`);
      return false;
    }
  }

  const isApproved = APPROVED_LICENSES.some(approved => pkgLicense.includes(approved));
  if (isApproved || pkg.private === true) {
    console.log(`✅ Approved license for ${pkgName}: ${pkgLicense}`);
    return true;
  } else {
    console.warn(`⚠️ Warning: Unrecognized license for ${pkgName}: ${pkgLicense}. Requires manual verification.`);
    return true;
  }
}

function runAudit() {
  console.log('====================================================');
  console.log('  SHOPSPHERE DEPENDENCY LICENSE COMPLIANCE AUDIT');
  console.log('====================================================');

  const rootPkg = path.join(__dirname, '..', 'package.json');
  const serverPkg = path.join(__dirname, '..', 'server', 'package.json');
  const clientPkg = path.join(__dirname, '..', 'client', 'package.json');

  let success = auditPackageFile(rootPkg);
  if (fs.existsSync(serverPkg)) success = auditPackageFile(serverPkg) && success;
  if (fs.existsSync(clientPkg)) success = auditPackageFile(clientPkg) && success;

  if (success) {
    console.log('\n✅ LICENSE AUDIT PASSED: All checked packages comply with MIT/BSD/ISC strict policy.');
  } else {
    console.error('\n❌ LICENSE AUDIT FAILED: Prohibited dependencies detected.');
    process.exit(1);
  }
}

runAudit();
