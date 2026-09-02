import React from 'react';
import { useParams, Link } from 'react-router-dom';

export default function OrderSuccessPage() {
  const { orderNumber } = useParams();

  return (
    <div className="container" style={{ paddingTop: '4rem', maxWidth: '600px', textAlign: 'center' }}>
      <div className="glass-panel" style={{ padding: '3rem 2rem' }}>
        <div style={{ fontSize: '3.5rem', marginBottom: '1rem' }}>🎉</div>
        <span className="badge badge-success" style={{ marginBottom: '1rem' }}>ORDER CONFIRMED</span>
        <h1 className="heading-lg" style={{ marginBottom: '0.5rem' }}>Thank You For Your Order!</h1>
        <p className="text-muted" style={{ marginBottom: '1.5rem' }}>
          Your order record <strong style={{ color: 'var(--text-main)' }}>#{orderNumber}</strong> has been confirmed and submitted to our merchant fulfillment network.
        </p>

        <div style={{ padding: '1rem', background: 'rgba(15, 23, 42, 0.6)', borderRadius: 'var(--radius-md)', marginBottom: '2rem', fontSize: '0.9rem' }} className="text-muted">
          📦 Estimated Delivery: 2-4 Business Days via Tracked Express Logistics.
        </div>

        <Link to="/" className="btn btn-primary" style={{ padding: '0.85rem 2rem' }}>
          Continue Shopping →
        </Link>
      </div>
    </div>
  );
}
