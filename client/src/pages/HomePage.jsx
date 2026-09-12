import React, { useState, useEffect } from 'react';
import { apiRequest } from '../services/apiClient';
import ProductCard from '../components/customer/ProductCard';

export default function HomePage({ onAddToCart }) {
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        setLoading(true);
        const catRes = await apiRequest('/categories');
        setCategories(catRes.data || []);

        let endpoint = '/products';
        if (selectedCategory) {
          endpoint += `?categoryId=${selectedCategory}`;
        }
        const prodRes = await apiRequest(endpoint);
        setProducts(prodRes.data || []);
      } catch (err) {
        console.error('Failed to load marketplace catalog:', err);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, [selectedCategory]);

  return (
    <div className="container" style={{ paddingTop: '2rem' }}>
      
      {/* Hero Banner */}
      <div style={{ padding: '3.5rem 3rem', marginBottom: '3rem', background: 'linear-gradient(135deg, #F1F5F9 0%, #E2E8F0 60%, #F8FAFC 100%)', border: '1px solid #CBD5E1', borderRadius: 'var(--radius-lg)', position: 'relative', overflow: 'hidden', boxShadow: 'var(--shadow-sm)' }}>
        <div style={{ maxWidth: '650px', position: 'relative', zIndex: 2 }}>
          <span className="badge" style={{ marginBottom: '1rem', background: '#FEF3C7', color: '#92400E', border: '1px solid #FDE68A', padding: '4px 10px' }}>
            FEATURED COLLECTION • DEALS OF THE WEEK
          </span>
          <h1 className="heading-xl" style={{ marginBottom: '1rem', color: '#0F172A' }}>
            Everything for your home, tech, and everyday life.
          </h1>
          <p style={{ color: '#475569', fontSize: '1.1rem', lineHeight: '1.6', marginBottom: '1.75rem' }}>
            Explore thousands of customer favorites, verified top-tier tech, and seasonal deals with fast free delivery and 30-day easy returns.
          </p>
          <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
            <a href="#catalog" className="btn btn-primary" style={{ padding: '0.85rem 1.8rem', borderRadius: '8px' }}>
              Explore Catalog ↓
            </a>
            <span style={{ padding: '0.65rem 1.25rem', background: '#FEF3C7', color: '#92400E', border: '1px solid #FDE68A', borderRadius: '8px', fontWeight: 700, fontSize: '0.88rem' }}>
              Code: WELCOME10 (10% OFF)
            </span>
          </div>
        </div>
      </div>

      {/* Category Pills Bar */}
      <div style={{ marginBottom: '2rem' }}>
        <h3 className="heading-md" style={{ marginBottom: '1rem' }}>Browse Categories</h3>
        <div style={{ display: 'flex', gap: '0.75rem', overflowX: 'auto', paddingBottom: '0.5rem' }}>
          <button
            onClick={() => setSelectedCategory(null)}
            className={`btn ${selectedCategory === null ? 'btn-primary' : 'btn-secondary'}`}
            style={{ borderRadius: 'var(--radius-full)', padding: '0.5rem 1.25rem', fontSize: '0.9rem', whiteSpace: 'nowrap' }}
          >
            All Products
          </button>
          {categories.map(cat => (
            <button
              key={cat.id}
              onClick={() => setSelectedCategory(cat.id)}
              className={`btn ${selectedCategory === cat.id ? 'btn-primary' : 'btn-secondary'}`}
              style={{ borderRadius: 'var(--radius-full)', padding: '0.5rem 1.25rem', fontSize: '0.9rem', whiteSpace: 'nowrap' }}
            >
              {cat.name}
            </button>
          ))}
        </div>
      </div>

      {/* Product Catalog Grid */}
      <div id="catalog">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
          <h2 className="heading-lg">Featured Products</h2>
          <span className="text-muted">{products.length} products available</span>
        </div>

        {loading ? (
          <div className="glass-panel" style={{ padding: '3rem', textAlign: 'center' }}>
            <p className="text-muted">Loading product catalog...</p>
          </div>
        ) : products.length === 0 ? (
          <div className="glass-panel" style={{ padding: '3rem', textAlign: 'center' }}>
            <p className="text-muted">No products found in this category.</p>
          </div>
        ) : (
          <div className="grid-products">
            {products.map(p => (
              <ProductCard key={p.id} product={p} onAddToCart={onAddToCart} />
            ))}
          </div>
        )}
      </div>

    </div>
  );
}
