const db = require('../database/db');

class AuditService {
  static logEvent(userId, action, module, entityType, entityId, ipAddress = '127.0.0.1', metadata = {}) {
    const auditId = `aud_${Date.now()}_${Math.random().toString(36).substr(2, 4)}`;
    db.prepare(`
      INSERT INTO security_audit_logs (id, user_id, action, module, entity_type, entity_id, ip_address, metadata_json)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    `).run(auditId, userId || null, action, module, entityType, entityId || null, ipAddress, JSON.stringify(metadata));
    return auditId;
  }

  static getAuditLogs(page = 1, limit = 20) {
    const offset = (page - 1) * limit;
    const logs = db.prepare(`
      SELECT sal.*, u.email as actor_email, u.role as actor_role
      FROM security_audit_logs sal
      LEFT JOIN users u ON sal.user_id = u.id
      ORDER BY sal.created_at DESC
      LIMIT ? OFFSET ?
    `).all(parseInt(limit), parseInt(offset));

    const totalRow = db.prepare('SELECT COUNT(*) as count FROM security_audit_logs').get();
    return {
      logs: logs.map(l => ({ ...l, metadata: JSON.parse(l.metadata_json || '{}') })),
      total: totalRow ? totalRow.count : 0,
      page: parseInt(page),
      limit: parseInt(limit)
    };
  }
}

module.exports = AuditService;
