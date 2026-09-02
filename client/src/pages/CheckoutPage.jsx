import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { apiRequest } from '../services/apiClient';

export default function CheckoutPage({ cart, onOrderSuccess }) {
  const location = useLocation();
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    fullName: 'Jane Shopper',
    streetAddress1: '100 Synthetic Way',
    streetAddress2: 'Apt 4B',
    city: 'Innovation City',
    state: 'CA',
    postalCode: '90210',
    country: 'United States',
    paymentMethodToken: 'mock_token_success'
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const couponCode = location.state?.couponCode || null;

  const handleSubmitOrder = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const payload = {
        shippingAddress: {
          fullName: formData.fullName,
          streetAddress1: formData.streetAddress1,
          streetAddress2: formData.streetAddress2,
          city: formData.city,
          state: formData.state,
          postalCode: formData.postalCode,
          country: formData.country
        },
        couponCode,
        paymentMethodToken: formData.paymentMethodToken
      };

      const res = await apiRequest('/orders', 'POST', payload);
      if (onOrderSuccess) onOrderSuccess();
      navigate(`/order-success/${res.data.orderNumber}`, { state: { order: res.data } });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container" style={{ paddingTop: '2.5rem', maxWidth: '800px' }}>
      <h1 className="heading-lg" style={{ marginBottom: '1.5rem' }}>Checkout & Payment Authorization</h1>

      {error && (
        <div style={{ padding: '1rem', background: 'rgba(239, 68, 68, 0.2)', border: '1px solid var(--danger)', borderRadius: 'var(--radius-md)', color: '#FCA5A5', marginBottom: '1.5rem' }}>
          {error}
        </div>
      )}

      <form onSubmit={handleSubmitOrder} className="glass-panel" style={{ padding: '2rem', display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
        <h3 className="heading-md" style={{ borderBottom: '1px solid var(--border-light)', paddingBottom: '0.75rem' }}>
          1. Shipping Address (Demo Mode)
        </h3>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
          <div>
            <label style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Full Name</label>
            <input
              type="text"
              className="input-control"
              value={formData.fullName}
              onChange={(e) => setFormData({ ...formData, fullName: e.target.value })}
              required
            />
          </div>
          <div>
            <label style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Street Address</label>
            <input
              type="text"
              className="input-control"
              value={formData.streetAddress1}
              onChange={(e) => setFormData({ ...formData, streetAddress1: e.target.value })}
              required
            />
          </div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '1rem' }}>
          <div>
            <label style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>City</label>
            <input
              type="text"
              className="input-control"
              value={formData.city}
              onChange={(e) => setFormData({ ...formData, city: e.target.value })}
              required
            />
          </div>
          <div>
            <label style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>State</label>
            <input
              type="text"
              className="input-control"
              value={formData.state}
              onChange={(e) => setFormData({ ...formData, state: e.target.value })}
              required
            />
          </div>
          <div>
            <label style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Postal Code</label>
            <input
              type="text"
              className="input-control"
              value={formData.postalCode}
              onChange={(e) => setFormData({ ...formData, postalCode: e.target.value })}
              required
            />
          </div>
        </div>

        <h3 className="heading-md" style={{ borderBottom: '1px solid var(--border-light)', paddingBottom: '0.75rem', marginTop: '1rem' }}>
          2. Abstract Payment Method (Sandbox Gateway)
        </h3>

        <div style={{ padding: '1rem', background: 'rgba(99, 102, 241, 0.1)', border: '1px solid var(--border-glow)', borderRadius: 'var(--radius-md)' }}>
          <div style={{ fontSize: '0.9rem', fontWeight: 600, color: 'var(--accent-primary)', marginBottom: '0.25rem' }}>
            🔒 Zero Plaintext Credit Card Storage Architecture
          </div>
          <div className="text-muted" style={{ fontSize: '0.85rem' }}>
            This platform uses payment tokenization. No card numbers, CVVs, or banking PINs are ever collected or stored on our servers.
          </div>
        </div>

        <button
          type="submit"
          className="btn btn-gold"
          disabled={loading}
          style={{ padding: '1rem', fontSize: '1.1rem', marginTop: '1rem' }}
        >
          {loading ? 'Processing Transaction...' : 'Confirm Order & Pay Securely →'}
        </button>
      </form>
    </div>
  );
}
