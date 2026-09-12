import React from 'react';
import { Link } from 'react-router-dom';

export default function ProductCard({ product, onAddToCart }) {
  const effectivePrice = product.effective_price || product.base_price;
  const hasDiscount = product.discount_percent > 0;

  return (
    <div className="glass-panel" style={{ display: 'flex', flexDirection: 'column', overflow: 'hidden', height: '100%', background: '#FFFFFF', border: '1px solid #E2E8F0', borderRadius: '12px', boxShadow: 'var(--shadow-card)' }}>
      {/* Product Image Box */}
      <div style={{ position: 'relative', width: '100%', height: '200px', backgroundColor: '#F8FAFC', display: 'flex', alignItems: 'center', justifyContent: 'center', overflow: 'hidden', borderBottom: '1px solid #E2E8F0' }}>
        <img
          src={product.primary_image || 'https://images.unsplash.com/photo-1526738549149-8e07eca6c147?auto=format&fit=crop&w=500&q=80'}
          alt={product.name}
          style={{ width: '100%', height: '100%', objectFit: 'contain', padding: '12px' }}
        />
        {hasDiscount && (
          <span style={{ position: 'absolute', top: '10px', left: '10px', background: '#DC2626', color: '#FFFFFF', padding: '3px 8px', borderRadius: '4px', fontSize: '0.75rem', fontWeight: 800 }}>
            -{product.discount_percent}%
          </span>
        )}
      </div>

      {/* Product Information */}
      <div style={{ padding: '1.25rem', display: 'flex', flexDirection: 'column', flex: 1, justifyContent: 'space-between', gap: '0.75rem' }}>
        <div>
          <div style={{ fontSize: '0.72rem', color: '#64748B', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '0.25rem' }}>
            {product.brand || 'Verified Merchant'}
          </div>
          <Link to={`/products/${product.id}`} style={{ textDecoration: 'none' }}>
            <h3 className="heading-md" style={{ fontSize: '1rem', lineHeight: '1.4', marginBottom: '0.5rem', height: '2.8em', overflow: 'hidden', color: '#0F172A' }}>
              {product.name}
            </h3>
          </Link>

          {/* Rating */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem', fontSize: '0.85rem' }}>
            <span style={{ color: '#F59E0B' }}>★</span>
            <span style={{ fontWeight: 700, color: '#0F172A' }}>{(product.rating_avg || 4.8).toFixed(1)}</span>
            <span style={{ color: '#64748B', fontSize: '0.8rem' }}>({product.review_count || 128})</span>
          </div>
        </div>

        {/* Price & Action */}
        <div style={{ display: 'flex', alignItems: 'baseline', justifyContent: 'space-between', marginTop: '0.5rem', paddingTop: '0.75rem', borderTop: '1px solid #E2E8F0' }}>
          <div>
            <div style={{ fontSize: '1.3rem', fontWeight: 800, color: '#0F172A' }}>
              ${effectivePrice.toFixed(2)}
            </div>
            {hasDiscount && (
              <div style={{ fontSize: '0.82rem', color: '#94A3B8', textDecoration: 'line-through' }}>
                ${product.base_price.toFixed(2)}
              </div>
            )}
          </div>

          <button
            onClick={() => onAddToCart(product)}
            className="btn btn-primary"
            style={{ padding: '0.45rem 1rem', fontSize: '0.85rem', borderRadius: '6px' }}
          >
            Add to Cart
          </button>
        </div>

      </div>
    </div>
  );
}
