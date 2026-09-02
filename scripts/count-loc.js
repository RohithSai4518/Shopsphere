const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');

const ALLOWED_EXTENSIONS = ['.js', '.jsx', '.json', '.sql', '.css', '.md'];
const IGNORED_DIRS = ['node_modules', '.git', 'dist', 'build', 'coverage', '.cache', 'data'];

let totalLines = 0;
let totalFiles = 0;
const breakdown = {};

function scanDir(dirPath) {
  const items = fs.readdirSync(dirPath);

  for (const item of items) {
    if (IGNORED_DIRS.includes(item)) continue;

    const fullPath = path.join(dirPath, item);
    const stat = fs.statSync(fullPath);

    if (stat.isDirectory()) {
      scanDir(fullPath);
    } else if (stat.isFile()) {
      const ext = path.extname(item);
      if (ALLOWED_EXTENSIONS.includes(ext)) {
        const content = fs.readFileSync(fullPath, 'utf8');
        const lines = content.split('\n').filter(line => line.trim().length > 0).length;

        totalLines += lines;
        totalFiles += 1;

        breakdown[ext] = (breakdown[ext] || 0) + lines;
      }
    }
  }
}

console.log('====================================================');
console.log('  SHOPSPHERE MEANINGFUL SOURCE LINE COUNT (LOC)');
console.log('====================================================');

scanDir(ROOT);

console.log(`\n📁 Total Source Files Analyzed: ${totalFiles}`);
console.log('📊 LOC Breakdown by File Extension:');
for (const [ext, count] of Object.entries(breakdown)) {
  console.log(`  - ${ext}: ${count} meaningful lines`);
}

console.log(`\n🚀 TOTAL MEANINGFUL SOURCE LOC: ${totalLines} LOC`);
console.log('====================================================');
