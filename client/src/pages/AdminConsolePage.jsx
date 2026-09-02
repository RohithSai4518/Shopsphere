import React, { useState, useEffect } from 'react';
import { apiRequest } from '../services/apiClient';

export default function AdminConsolePage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadAnalytics() {
      try {
        const res = await apiRequest('/admin/analytics');
        setData(res.data);
      } catch (err) {
        console.error('Failed to load admin analytics:', err);
      } finally {
        setLoading(false);
      }
    }
    loadAnalytics();
  }, []);

  const handleApproveSeller = async (sellerId) => {
    try {
      await apiRequest(`/admin/sellers/${sellerId}/approve`, 'POST', { action: 'APPROVE', commissionRate: 8.5 });
      alert('Seller approved successfully!');
      const res = await apiRequest('/admin/analytics');
      setData(res.data);
    } catch (err) {
      alert(`Approval error: ${err.message}`);
    }
  };

  if (loading) return <div className="container" style={{ paddingTop: '3rem', textAlign: 'center' }}>Loading Admin Console...</div>;

  const metrics = data?.metrics || {};

  return (
    <div className="container" style={{ paddingTop: '2.5rem' }}>
      <h1 className="heading-lg" style={{ marginBottom: '2rem' }}>Platform Governance & Analytics Console</h1>

      {/* Global Metrics */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1.5rem', marginBottom: '3rem' }}>
        <div className="glass-panel" style={{ padding: '1.5rem' }}>
          <div className="text-muted" style={{ fontSize: '0.85rem' }}>Platform Revenue</div>
          <div style={{ fontSize: '1.8rem', fontWeight: 800, color: 'var(--success)' }}>${(metrics.totalRevenue || 0).toFixed(2)}</div>
        </div>
        <div className="glass-panel" style={{ padding: '1.5rem' }}>
          <div className="text-muted" style={{ fontSize: '0.85rem' }}>Total Active Users</div>
          <div style={{ fontSize: '1.8rem', fontWeight: 800 }}>{metrics.totalUsers || 0}</div>
        </div>
        <div className="glass-panel" style={{ padding: '1.5rem' }}>
          <div className="text-muted" style={{ fontSize: '0.85rem' }}>Active Sellers</div>
          <div style={{ fontSize: '1.8rem', fontWeight: 800 }}>{metrics.totalSellers || 0}</div>
        </div>
        <div className="glass-panel" style={{ padding: '1.5rem' }}>
          <div className="text-muted" style={{ fontSize: '0.85rem' }}>Catalog Products</div>
          <div style={{ fontSize: '1.8rem', fontWeight: 800 }}>{metrics.totalProducts || 0}</div>
        </div>
      </div>

      {/* Pending Seller Registrations */}
      <div className="glass-panel" style={{ padding: '2rem' }}>
        <h3 className="heading-md" style={{ marginBottom: '1.5rem' }}>Pending Seller Approval Requests</h3>
        {!data?.pendingSellers || data.pendingSellers.length === 0 ? (
          <p className="text-muted">No pending seller registration requests requiring review.</p>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            {data.pendingSellers.map(s => (
              <div key={s.id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '1rem', borderBottom: '1px solid var(--border-light)' }}>
                <div>
                  <h4 style={{ fontWeight: 600 }}>{s.business_name}</h4>
                  <div className="text-muted" style={{ fontSize: '0.85rem' }}>Applicant: {s.first_name} {s.last_name} ({s.email})</div>
                </div>
                <button onClick={() => handleApproveSeller(s.id)} className="btn btn-primary" style={{ padding: '0.5rem 1rem', fontSize: '0.85rem' }}>
                  Approve Seller
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
