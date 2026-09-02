const db = require('../database/db');
const AppError = require('../utils/appError');
const HTTP_STATUS = require('../constants/statusCodes');
const ERROR_CODES = require('../constants/errorCodes');

class SupportService {
  static createTicket(userId, { subject, category, priority = 'MEDIUM', orderId, initialMessage }) {
    const ticketId = `tkt_${Date.now()}_${Math.random().toString(36).substr(2, 4)}`;
    const ticketNumber = `TKT-${Math.floor(10000 + Math.random() * 90000)}`;

    return db.transaction(() => {
      db.prepare(`
        INSERT INTO support_tickets (id, ticket_number, user_id, order_id, subject, category, priority, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, 'OPEN')
      `).run(ticketId, ticketNumber, userId, orderId || null, subject, category || 'GENERAL', priority);

      if (initialMessage) {
        const msgId = `msg_${Date.now()}_${Math.random().toString(36).substr(2, 4)}`;
        db.prepare('INSERT INTO support_messages (id, ticket_id, sender_id, message) VALUES (?, ?, ?, ?)').run(msgId, ticketId, userId, initialMessage);
      }

      return { ticketId, ticketNumber, status: 'OPEN' };
    })();
  }

  static getTicketDetails(userId, ticketId) {
    const ticket = db.prepare('SELECT * FROM support_tickets WHERE (id = ? OR ticket_number = ?) AND user_id = ?').get(ticketId, ticketId, userId);
    if (!ticket) throw new AppError('Support ticket not found.', HTTP_STATUS.NOT_FOUND, ERROR_CODES.RESOURCE_NOT_FOUND);

    const messages = db.prepare(`
      SELECT sm.*, u.first_name, u.last_name, u.role as sender_role
      FROM support_messages sm
      JOIN users u ON sm.sender_id = u.id
      WHERE sm.ticket_id = ?
      ORDER BY sm.created_at ASC
    `).all(ticket.id);

    return { ticket, messages };
  }

  static addMessage(senderId, ticketId, messageText, isInternalNote = false) {
    const ticket = db.prepare('SELECT id FROM support_tickets WHERE id = ? OR ticket_number = ?').get(ticketId, ticketId);
    if (!ticket) throw new AppError('Support ticket not found.', HTTP_STATUS.NOT_FOUND, ERROR_CODES.RESOURCE_NOT_FOUND);

    const msgId = `msg_${Date.now()}_${Math.random().toString(36).substr(2, 4)}`;
    db.prepare('INSERT INTO support_messages (id, ticket_id, sender_id, message, is_internal_note) VALUES (?, ?, ?, ?, ?)').run(msgId, ticket.id, senderId, messageText, isInternalNote ? 1 : 0);

    db.prepare("UPDATE support_tickets SET status = 'IN_PROGRESS', updated_at = datetime('now') WHERE id = ?").run(ticket.id);

    return { msgId, ticketId: ticket.id, messageText };
  }

  static getUserTickets(userId) {
    return db.prepare('SELECT * FROM support_tickets WHERE user_id = ? ORDER BY updated_at DESC').all(userId);
  }

  static getAllTicketsAdmin() {
    return db.prepare(`
      SELECT st.*, u.first_name, u.last_name, u.email
      FROM support_tickets st
      JOIN users u ON st.user_id = u.id
      ORDER BY st.updated_at DESC
    `).all();
  }
}

module.exports = SupportService;
