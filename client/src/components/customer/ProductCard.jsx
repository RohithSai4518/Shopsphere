import React from 'react';
import { Link } from 'react-router-dom';

export default function ProductCard({ product, onAddToCart }) {
  const effectivePrice = product.effective_price || product.base_price;
  const hasDiscount = product.discount_percent > 0;

  return (
    <div className="glass-panel" style={{ display: 'flex', flexDirection: 'column', overflow: 'hidden', height: '100%' }}>
      {/* Product Image Box */}
      <div style={{ position: 'relative', width: '100%', height: '200px', backgroundColor: '#090D16', display: 'flex', alignItems: 'center', justifyContent: 'center', overflow: 'hidden' }}>
        <img
          src={product.primary_image || 'https://images.unsplash.com/photo-1526738549149-8e07eca6c147?auto=format&fit=crop&w=500&q=80'}
          alt={product.name}
          style={{ width: '100%', height: '100%', objectFit: 'cover' }}
        />
        {hasDiscount && (
          <span className="badge badge-warning" style={{ position: 'absolute', top: '10px', right: '10px' }}>
            -{product.discount_percent}% OFF
          </span>
        )}
      </div>

      {/* Product Information */}
      <div style={{ padding: '1.25rem', display: 'flex', flexDirection: 'column', flex: 1, justifyContent: 'space-between', gap: '0.75rem' }}>
        <div>
          <div style={{ fontSize: '0.75rem', color: 'var(--accent-primary)', fontWeight: 600, textTransform: 'uppercase', marginBottom: '0.25rem' }}>
            {product.brand || 'ShopSphere Seller'}
          </div>
          <Link to={`/products/${product.id}`} style={{ textDecoration: 'none' }}>
            <h3 className="heading-md" style={{ fontSize: '1.05rem', lineHeight: '1.4', marginBottom: '0.5rem', height: '2.8em', overflow: 'hidden' }}>
              {product.name}
            </h3>
          </Link>

          {/* Rating */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.85rem' }}>
            <span style={{ color: '#F59E0B' }}>★</span>
            <span style={{ fontWeight: 600 }}>{(product.rating_avg || 4.8).toFixed(1)}</span>
            <span className="text-muted">({product.review_count || 12} reviews)</span>
          </div>
        </div>

        {/* Price & Action */}
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginTop: '0.5rem' }}>
          <div>
            <div style={{ fontSize: '1.25rem', fontWeight: 800, color: 'var(--text-main)' }}>
              ${effectivePrice.toFixed(2)}
            </div>
            {hasDiscount && (
              <div style={{ fontSize: '0.8rem', color: 'var(--text-subtle)', textDecoration: 'line-through' }}>
                ${product.base_price.toFixed(2)}
              </div>
            )}
          </div>

          <button
            onClick={() => onAddToCart(product)}
            className="btn btn-primary"
            style={{ padding: '0.5rem 0.9rem', fontSize: '0.85rem' }}
          >
            + Cart
          </button>
        </div>

      </div>
    </div>
  );
}
