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
        <p className="text-muted" style={{ marginBottom: '1.5rem', color: '#64748B' }}>
          Your order <strong style={{ color: '#0F172A' }}>#{orderNumber}</strong> has been confirmed! We're preparing your items for delivery.
        </p>

        <div style={{ padding: '1rem', background: '#F8FAFC', border: '1px solid #E2E8F0', borderRadius: 'var(--radius-md)', marginBottom: '2rem', fontSize: '0.9rem', color: '#334155' }}>
          📦 Estimated Delivery: 2-4 business days with tracking included.
        </div>

        <Link to="/" className="btn btn-primary" style={{ padding: '0.85rem 2rem' }}>
          Continue Shopping →
        </Link>
      </div>
    </div>
  );
}
