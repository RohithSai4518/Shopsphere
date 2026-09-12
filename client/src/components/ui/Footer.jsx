import React from 'react';
import { Link } from 'react-router-dom';

export default function Footer() {
  return (
    <footer style={{ marginTop: '4rem', background: 'var(--bg-footer)', borderTop: '1px solid #232F3E', padding: '3.5rem 0 2rem 0', color: '#CBD5E1' }}>
      <div className="container" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '2.5rem', marginBottom: '2.5rem' }}>
        <div>
          <h4 style={{ color: '#FFFFFF', marginBottom: '0.75rem', fontSize: '1.1rem', fontWeight: 800 }}>Shop<span style={{ color: 'var(--accent-primary)' }}>Sphere</span></h4>
          <p style={{ color: '#94A3B8', fontSize: '0.88rem', lineHeight: '1.6' }}>
            Your trusted marketplace for quality products, everyday essentials, and verified merchants with fast doorstep delivery.
          </p>
        </div>
        <div>
          <h4 style={{ color: '#FFFFFF', marginBottom: '0.85rem', fontSize: '0.9rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.06em' }}>Shop Categories</h4>
          <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.5rem', fontSize: '0.88rem', color: '#94A3B8' }}>
            <li>Electronics & Gadgets</li>
            <li>Laptops & Workstations</li>
            <li>Headphones & Audio</li>
            <li>Home & Kitchen Appliances</li>
          </ul>
        </div>
        <div>
          <h4 style={{ color: '#FFFFFF', marginBottom: '0.85rem', fontSize: '0.9rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.06em' }}>Merchant Center</h4>
          <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.5rem', fontSize: '0.88rem', color: '#94A3B8' }}>
            <li>Sell on ShopSphere</li>
            <li>Seller Command Center</li>
            <li>Fulfillment & Shipping</li>
            <li>Seller Community Standards</li>
          </ul>
        </div>
        <div>
          <h4 style={{ color: '#FFFFFF', marginBottom: '0.85rem', fontSize: '0.9rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.06em' }}>Customer Care</h4>
          <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.5rem', fontSize: '0.88rem', color: '#94A3B8' }}>
            <li>Track Your Order</li>
            <li>Shipping Rates & Policies</li>
            <li>Returns & Replacements</li>
            <li>Help & Customer Support</li>
          </ul>
        </div>
      </div>
      <div style={{ textAlign: 'center', borderTop: '1px solid #232F3E', paddingTop: '1.5rem', fontSize: '0.82rem', color: '#64748B' }}>
        © {new Date().getFullYear()} ShopSphere Marketplace Inc. All rights reserved. Powered by Harsha and Rohith.
      </div>
    </footer>
  );
}
