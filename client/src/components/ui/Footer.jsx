import React from 'react';
import { Link } from 'react-router-dom';

export default function Footer() {
  return (
    <footer style={{ marginTop: '4rem', background: '#090D16', borderTop: '1px solid var(--border-light)', padding: '3rem 0 2rem 0' }}>
      <div className="container" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '2rem', marginBottom: '2rem' }}>
        <div>
          <h4 className="heading-md" style={{ marginBottom: '1rem' }}>ShopSphere</h4>
          <p className="text-muted" style={{ fontSize: '0.9rem' }}>
            Next-generation independent marketplace platform supporting thousands of merchants and millions of synthetic products.
          </p>
        </div>
        <div>
          <h4 style={{ color: 'var(--text-main)', marginBottom: '1rem', fontSize: '1rem' }}>Shop Categories</h4>
          <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.5rem', fontSize: '0.9rem' }} className="text-muted">
            <li>Electronics & Gadgets</li>
            <li>Laptops & Workstations</li>
            <li>Headphones & Audio</li>
            <li>Home & Kitchen Appliances</li>
          </ul>
        </div>
        <div>
          <h4 style={{ color: 'var(--text-main)', marginBottom: '1rem', fontSize: '1rem' }}>Merchant Center</h4>
          <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.5rem', fontSize: '0.9rem' }} className="text-muted">
            <li>Sell on ShopSphere</li>
            <li>Seller Portal Login</li>
            <li>Fulfillment Services</li>
            <li>Merchant Policy</li>
          </ul>
        </div>
        <div>
          <h4 style={{ color: 'var(--text-main)', marginBottom: '1rem', fontSize: '1rem' }}>Security & Trust</h4>
          <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.5rem', fontSize: '0.9rem' }} className="text-muted">
            <li>100% Original Architecture</li>
            <li>Zero Copyleft Licenses</li>
            <li>Encrypted Auth & Payments</li>
            <li>Verified Purchase Ratings</li>
          </ul>
        </div>
      </div>
      <div style={{ textAlign: 'center', borderTop: '1px solid var(--border-light)', paddingTop: '1.5rem', fontSize: '0.85rem', color: 'var(--text-subtle)' }}>
        © {new Date().getFullYear()} ShopSphere Marketplace Platform. All rights reserved. Powered by Harsha and Rohith.
      </div>
    </footer>
  );
}
