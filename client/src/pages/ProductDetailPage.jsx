import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { apiRequest } from '../services/apiClient';

export default function ProductDetailPage({ onAddToCart }) {
  const { id } = useParams();
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [selectedVariant, setSelectedVariant] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchDetail() {
      try {
        setLoading(true);
        const res = await apiRequest(`/products/${id}`);
        setData(res.data);
        if (res.data.variants && res.data.variants.length > 0) {
          setSelectedVariant(res.data.variants[0]);
        }
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    fetchDetail();
  }, [id]);

  if (loading) return <div className="container" style={{ paddingTop: '3rem', textAlign: 'center' }}>Loading product details...</div>;
  if (error || !data) return <div className="container" style={{ paddingTop: '3rem', textAlign: 'center' }}>Product not found.</div>;

  const { product, variants, images, reviews } = data;
  const primaryImage = images && images.length > 0 ? images[0].image_url : 'https://images.unsplash.com/photo-1526738549149-8e07eca6c147?auto=format&fit=crop&w=500&q=80';

  return (
    <div className="container" style={{ paddingTop: '2.5rem' }}>
      <button onClick={() => navigate(-1)} className="btn btn-secondary" style={{ marginBottom: '1.5rem', padding: '0.4rem 0.8rem', fontSize: '0.85rem' }}>
        ← Back
      </button>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '3rem' }}>
        {/* Gallery */}
        <div className="glass-panel" style={{ padding: '1rem', display: 'flex', alignItems: 'center', justifyContent: 'center', height: '420px', overflow: 'hidden' }}>
          <img src={primaryImage} alt={product.name} style={{ maxWidth: '100%', maxHeight: '100%', objectFit: 'contain' }} />
        </div>

        {/* Product Meta & Actions */}
        <div>
          <span className="badge badge-primary" style={{ marginBottom: '0.5rem' }}>{product.category_name}</span>
          <h1 className="heading-lg" style={{ marginBottom: '0.5rem' }}>{product.name}</h1>
          <div style={{ fontSize: '0.88rem', color: '#475569', marginBottom: '1.25rem', display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
            <span>Sold by <strong style={{ color: '#0F172A' }}>{product.seller_name}</strong></span>
            <span style={{ color: '#F59E0B', fontWeight: 700 }}>★ {product.seller_rating}</span>
            <span>•</span>
            <span style={{ color: '#16A34A', fontWeight: 600 }}>● In Stock</span>
          </div>

          <div style={{ display: 'flex', alignItems: 'baseline', gap: '1rem', marginBottom: '1.5rem' }}>
            <span style={{ fontSize: '2.2rem', fontWeight: 800, color: '#0F172A' }}>${product.effective_price.toFixed(2)}</span>
            {product.discount_percent > 0 && (
              <span style={{ fontSize: '1.1rem', color: '#94A3B8', textDecoration: 'line-through' }}>
                ${product.base_price.toFixed(2)}
              </span>
            )}
            {product.discount_percent > 0 && (
              <span style={{ background: '#DC2626', color: '#FFFFFF', padding: '3px 8px', borderRadius: '4px', fontSize: '0.78rem', fontWeight: 800 }}>
                Save {product.discount_percent}%
              </span>
            )}
          </div>

          <p style={{ color: '#334155', lineHeight: '1.65', marginBottom: '2rem' }}>
            {product.description}
          </p>

          {/* Variant Selectors */}
          {variants && variants.length > 0 && (
            <div style={{ marginBottom: '2rem' }}>
              <h4 style={{ fontSize: '0.9rem', marginBottom: '0.75rem', color: '#0F172A', fontWeight: 700 }}>Select Variant:</h4>
              <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
                {variants.map(v => (
                  <button
                    key={v.id}
                    onClick={() => setSelectedVariant(v)}
                    className={`btn ${selectedVariant?.id === v.id ? 'btn-primary' : 'btn-secondary'}`}
                    style={{ fontSize: '0.85rem', padding: '0.5rem 1rem' }}
                  >
                    {v.variant_name} ({v.quantity_on_hand > 0 ? `${v.quantity_on_hand} in stock` : 'Out of stock'})
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Add to Cart */}
          <div style={{ display: 'flex', gap: '1rem' }}>
            <button
              onClick={() => onAddToCart(product, selectedVariant)}
              className="btn btn-primary"
              style={{ flex: 1, padding: '0.85rem', fontSize: '1rem', borderRadius: '8px' }}
            >
              Add to Shopping Cart 🛒
            </button>
          </div>
        </div>
      </div>

      {/* Customer Reviews Section */}
      <div style={{ marginTop: '4rem' }}>
        <h3 className="heading-lg" style={{ marginBottom: '1.5rem' }}>Customer Reviews & Ratings</h3>
        {reviews.length === 0 ? (
          <div className="glass-panel" style={{ padding: '2rem', textAlign: 'center' }}>
            <p className="text-muted">No customer reviews yet. Be the first to rate this product!</p>
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            {reviews.map(r => (
              <div key={r.id} className="glass-panel" style={{ padding: '1.25rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                  <span style={{ fontWeight: 600 }}>{r.first_name} {r.last_name}</span>
                  <span style={{ color: '#F59E0B' }}>{'★'.repeat(r.rating)}</span>
                </div>
                <h4 style={{ fontSize: '0.95rem', fontWeight: 600, marginBottom: '0.25rem' }}>{r.title}</h4>
                <p className="text-muted" style={{ fontSize: '0.9rem' }}>{r.comment}</p>
              </div>
            ))}
          </div>
        )}
      </div>

    </div>
  );
}
