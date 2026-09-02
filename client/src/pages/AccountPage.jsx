import React, { useState, useEffect } from 'react';
import { apiRequest } from '../services/apiClient';
import { useAuth } from '../context/AuthContext';

export default function AccountPage() {
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState('profile');
  const [addresses, setAddresses] = useState([]);
  const [sessions, setSessions] = useState([]);
  const [preferences, setPreferences] = useState({});
  const [loading, setLoading] = useState(true);

  // Address form
  const [newAddr, setNewAddr] = useState({
    fullName: '',
    streetAddress1: '',
    city: '',
    state: '',
    postalCode: '',
    country: 'United States',
    isDefault: true
  });

  useEffect(() => {
    async function loadAccountData() {
      try {
        setLoading(true);
        const [addrRes, sessRes, prefRes] = await Promise.all([
          apiRequest('/account/addresses'),
          apiRequest('/account/sessions'),
          apiRequest('/account/preferences')
        ]);
        setAddresses(addrRes.data || []);
        setSessions(sessRes.data || []);
        setPreferences(prefRes.data || {});
      } catch (err) {
        console.error('Failed to load account data:', err);
      } finally {
        setLoading(false);
      }
    }
    loadAccountData();
  }, []);

  const handleAddAddress = async (e) => {
    e.preventDefault();
    try {
      const res = await apiRequest('/account/addresses', 'POST', newAddr);
      setAddresses(res.data);
      setNewAddr({ fullName: '', streetAddress1: '', city: '', state: '', postalCode: '', country: 'United States', isDefault: false });
      alert('Address saved!');
    } catch (err) {
      alert(`Error: ${err.message}`);
    }
  };

  const handleDeleteAddress = async (id) => {
    try {
      const res = await apiRequest(`/account/addresses/${id}`, 'DELETE');
      setAddresses(res.data);
    } catch (err) {
      alert(`Error: ${err.message}`);
    }
  };

  if (loading) return <div className="container" style={{ paddingTop: '3rem', textAlign: 'center' }}>Loading Account Center...</div>;

  return (
    <div className="container" style={{ paddingTop: '2.5rem' }}>
      <h1 className="heading-lg" style={{ marginBottom: '2rem' }}>Customer Account Security & Profile Center</h1>

      {/* Tabs */}
      <div style={{ display: 'flex', gap: '0.75rem', marginBottom: '2rem', borderBottom: '1px solid var(--border-light)', paddingBottom: '0.75rem' }}>
        <button onClick={() => setActiveTab('profile')} className={`btn ${activeTab === 'profile' ? 'btn-primary' : 'btn-secondary'}`}>
          Profile & Security
        </button>
        <button onClick={() => setActiveTab('addresses')} className={`btn ${activeTab === 'addresses' ? 'btn-primary' : 'btn-secondary'}`}>
          Saved Addresses ({addresses.length})
        </button>
        <button onClick={() => setActiveTab('sessions')} className={`btn ${activeTab === 'sessions' ? 'btn-primary' : 'btn-secondary'}`}>
          Active Device Sessions
        </button>
      </div>

      {activeTab === 'profile' && (
        <div className="glass-panel" style={{ padding: '2rem', maxWidth: '600px' }}>
          <h3 className="heading-md" style={{ marginBottom: '1rem' }}>Personal Profile</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', fontSize: '0.95rem' }}>
            <div><strong className="text-muted">Account Email:</strong> {user?.email}</div>
            <div><strong className="text-muted">Full Name:</strong> {user?.firstName} {user?.lastName}</div>
            <div><strong className="text-muted">Role Privilege:</strong> <span className="badge badge-primary">{user?.role}</span></div>
          </div>
        </div>
      )}

      {activeTab === 'addresses' && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '2rem' }}>
          {/* Address List */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <h3 className="heading-md">Your Address Book</h3>
            {addresses.map(a => (
              <div key={a.id} className="glass-panel" style={{ padding: '1.25rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                  <strong style={{ fontSize: '1rem' }}>{a.full_name}</strong>
                  {a.is_default === 1 && <span className="badge badge-success">DEFAULT</span>}
                </div>
                <div className="text-muted" style={{ fontSize: '0.9rem' }}>
                  {a.street_address_1} {a.street_address_2}<br />
                  {a.city}, {a.state} {a.postal_code}, {a.country}
                </div>
                <button onClick={() => handleDeleteAddress(a.id)} style={{ marginTop: '0.75rem', background: 'none', border: 'none', color: 'var(--danger)', fontSize: '0.85rem', cursor: 'pointer' }}>
                  Delete Address
                </button>
              </div>
            ))}
          </div>

          {/* Add Address Form */}
          <div className="glass-panel" style={{ padding: '1.5rem' }}>
            <h3 className="heading-md" style={{ marginBottom: '1rem' }}>Add New Shipping Address</h3>
            <form onSubmit={handleAddAddress} style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
              <input
                type="text"
                className="input-control"
                placeholder="Full Name"
                value={newAddr.fullName}
                onChange={(e) => setNewAddr({ ...newAddr, fullName: e.target.value })}
                required
              />
              <input
                type="text"
                className="input-control"
                placeholder="Street Address"
                value={newAddr.streetAddress1}
                onChange={(e) => setNewAddr({ ...newAddr, streetAddress1: e.target.value })}
                required
              />
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.5rem' }}>
                <input
                  type="text"
                  className="input-control"
                  placeholder="City"
                  value={newAddr.city}
                  onChange={(e) => setNewAddr({ ...newAddr, city: e.target.value })}
                  required
                />
                <input
                  type="text"
                  className="input-control"
                  placeholder="State"
                  value={newAddr.state}
                  onChange={(e) => setNewAddr({ ...newAddr, state: e.target.value })}
                  required
                />
              </div>
              <input
                type="text"
                className="input-control"
                placeholder="Postal Code"
                value={newAddr.postalCode}
                onChange={(e) => setNewAddr({ ...newAddr, postalCode: e.target.value })}
                required
              />
              <button type="submit" className="btn btn-primary">Save Address</button>
            </form>
          </div>
        </div>
      )}

      {activeTab === 'sessions' && (
        <div className="glass-panel" style={{ padding: '2rem' }}>
          <h3 className="heading-md" style={{ marginBottom: '1rem' }}>Active Device & Login Sessions</h3>
          {sessions.length === 0 ? (
            <p className="text-muted">No active sessions tracked.</p>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
              {sessions.map(s => (
                <div key={s.id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '0.85rem', borderBottom: '1px solid var(--border-light)' }}>
                  <div>
                    <div style={{ fontWeight: 600 }}>IP: {s.ip_address}</div>
                    <div className="text-muted" style={{ fontSize: '0.8rem' }}>Agent: {s.user_agent || 'Web Client'} | Login: {new Date(s.created_at).toLocaleString()}</div>
                  </div>
                  <span className="badge badge-success">ACTIVE SESSION</span>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

    </div>
  );
}
