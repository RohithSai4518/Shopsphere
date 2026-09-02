import React, { useState, useEffect } from 'react';
import { apiRequest } from '../services/apiClient';

export default function SupportPage() {
  const [tickets, setTickets] = useState([]);
  const [activeTicket, setActiveTicket] = useState(null);
  const [messages, setMessages] = useState([]);
  const [replyText, setReplyText] = useState('');
  const [newTicket, setNewTicket] = useState({ subject: '', category: 'GENERAL', priority: 'MEDIUM', initialMessage: '' });
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadTickets();
  }, []);

  async function loadTickets() {
    try {
      setLoading(true);
      const res = await apiRequest('/support/tickets');
      setTickets(res.data || []);
      if (res.data && res.data.length > 0) {
        loadTicketDetails(res.data[0].id);
      }
    } catch (err) {
      console.error('Failed to load support tickets:', err);
    } finally {
      setLoading(false);
    }
  }

  async function loadTicketDetails(ticketId) {
    try {
      const res = await apiRequest(`/support/tickets/${ticketId}`);
      setActiveTicket(res.data.ticket);
      setMessages(res.data.messages || []);
    } catch (err) {
      console.error('Failed to load ticket details:', err);
    }
  }

  const handleCreateTicket = async (e) => {
    e.preventDefault();
    try {
      await apiRequest('/support/tickets', 'POST', newTicket);
      setShowCreateModal(false);
      setNewTicket({ subject: '', category: 'GENERAL', priority: 'MEDIUM', initialMessage: '' });
      loadTickets();
      alert('Support ticket created successfully!');
    } catch (err) {
      alert(`Error: ${err.message}`);
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!replyText.trim() || !activeTicket) return;
    try {
      await apiRequest(`/support/tickets/${activeTicket.id}/messages`, 'POST', { messageText: replyText });
      setReplyText('');
      loadTicketDetails(activeTicket.id);
    } catch (err) {
      alert(`Error: ${err.message}`);
    }
  };

  if (loading) return <div className="container" style={{ paddingTop: '3rem', textAlign: 'center' }}>Loading Customer Support Center...</div>;

  return (
    <div className="container" style={{ paddingTop: '2.5rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <div>
          <h1 className="heading-lg">Customer Support & Dispute Center</h1>
          <p className="text-muted">24/7 SLA Priority Helpdesk & Order Ticket Resolution</p>
        </div>
        <button onClick={() => setShowCreateModal(true)} className="btn btn-primary">
          + Open Support Ticket
        </button>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '320px 1fr', gap: '2rem' }}>
        {/* Ticket List */}
        <div className="glass-panel" style={{ padding: '1.25rem' }}>
          <h3 className="heading-md" style={{ marginBottom: '1rem' }}>Your Support Tickets</h3>
          {tickets.length === 0 ? (
            <p className="text-muted">No support tickets found.</p>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
              {tickets.map(t => (
                <div
                  key={t.id}
                  onClick={() => loadTicketDetails(t.id)}
                  style={{
                    padding: '1rem',
                    borderRadius: '8px',
                    cursor: 'pointer',
                    background: activeTicket?.id === t.id ? 'rgba(0, 240, 255, 0.1)' : 'rgba(255, 255, 255, 0.02)',
                    border: activeTicket?.id === t.id ? '1px solid var(--accent-teal)' : '1px solid var(--border-light)'
                  }}
                >
                  <div style={{ fontWeight: 600, fontSize: '0.95rem' }}>{t.ticket_number}</div>
                  <div style={{ fontSize: '0.85rem', color: 'var(--text-main)', margin: '0.25rem 0' }}>{t.subject}</div>
                  <div style={{ display: 'flex', gap: '0.5rem', marginTop: '0.5rem' }}>
                    <span className="badge badge-primary">{t.status}</span>
                    <span className="badge badge-success">{t.priority}</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Message Thread */}
        <div className="glass-panel" style={{ padding: '2rem', display: 'flex', flexDirection: 'column', height: '600px' }}>
          {activeTicket ? (
            <>
              <div style={{ borderBottom: '1px solid var(--border-light)', paddingBottom: '1rem', marginBottom: '1rem' }}>
                <h2 className="heading-md">{activeTicket.ticket_number}: {activeTicket.subject}</h2>
                <div className="text-muted" style={{ fontSize: '0.85rem' }}>Category: {activeTicket.category} | SLA Priority: {activeTicket.priority}</div>
              </div>

              <div style={{ flex: 1, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '1rem', paddingRight: '0.5rem' }}>
                {messages.map(m => (
                  <div
                    key={m.id}
                    style={{
                      padding: '1rem',
                      borderRadius: '10px',
                      maxWidth: '80%',
                      alignSelf: m.sender_role === 'CUSTOMER' ? 'flex-end' : 'flex-start',
                      background: m.sender_role === 'CUSTOMER' ? 'rgba(0, 240, 255, 0.15)' : 'rgba(255, 255, 255, 0.08)'
                    }}
                  >
                    <div style={{ fontWeight: 600, fontSize: '0.85rem', marginBottom: '0.25rem' }}>
                      {m.first_name} {m.last_name} ({m.sender_role})
                    </div>
                    <div style={{ fontSize: '0.95rem' }}>{m.message}</div>
                    <div className="text-muted" style={{ fontSize: '0.75rem', marginTop: '0.4rem', textAlign: 'right' }}>
                      {new Date(m.created_at).toLocaleString()}
                    </div>
                  </div>
                ))}
              </div>

              <form onSubmit={handleSendMessage} style={{ display: 'flex', gap: '0.75rem', marginTop: '1rem' }}>
                <input
                  type="text"
                  className="input-control"
                  placeholder="Type message reply..."
                  value={replyText}
                  onChange={(e) => setReplyText(e.target.value)}
                  style={{ flex: 1 }}
                />
                <button type="submit" className="btn btn-primary">Send Reply</button>
              </form>
            </>
          ) : (
            <p className="text-muted">Select a ticket to view conversation history.</p>
          )}
        </div>
      </div>

      {/* Create Modal */}
      {showCreateModal && (
        <div style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, background: 'rgba(0,0,0,0.8)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000 }}>
          <div className="glass-panel" style={{ padding: '2rem', maxWidth: '500px', width: '100%' }}>
            <h3 className="heading-md" style={{ marginBottom: '1rem' }}>Open Support Ticket</h3>
            <form onSubmit={handleCreateTicket} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              <input
                type="text"
                className="input-control"
                placeholder="Ticket Subject"
                value={newTicket.subject}
                onChange={(e) => setNewTicket({ ...newTicket, subject: e.target.value })}
                required
              />
              <select
                className="input-control"
                value={newTicket.category}
                onChange={(e) => setNewTicket({ ...newTicket, category: e.target.value })}
              >
                <option value="GENERAL">General Query</option>
                <option value="ORDER_ISSUE">Order Issue / Delivery</option>
                <option value="REFUND">Refund / Return Request</option>
                <option value="TECHNICAL">Technical Platform Support</option>
              </select>
              <textarea
                className="input-control"
                placeholder="Initial message description..."
                rows={4}
                value={newTicket.initialMessage}
                onChange={(e) => setNewTicket({ ...newTicket, initialMessage: e.target.value })}
                required
              />
              <div style={{ display: 'flex', gap: '0.75rem', justifyContent: 'flex-end' }}>
                <button type="button" onClick={() => setShowCreateModal(false)} className="btn btn-secondary">Cancel</button>
                <button type="submit" className="btn btn-primary">Submit Ticket</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
