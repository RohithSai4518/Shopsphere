const fs = require('fs');
const path = require('path');
const db = require('./db');

function runMigrations() {
  console.log('🚀 Initializing ShopSphere Database Migrations...');
  const schemaPath = path.join(__dirname, 'schema.sql');
  const schemaSql = fs.readFileSync(schemaPath, 'utf8');

  db.exec(schemaSql);
  console.log('✅ Schema migration completed successfully: 20 relational tables created.');
}

if (require.main === module) {
  try {
    runMigrations();
  } catch (error) {
    console.error('❌ Migration failed:', error);
    process.exit(1);
  }
}

module.exports = { runMigrations };
