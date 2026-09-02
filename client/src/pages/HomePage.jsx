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
      <div className="glass-panel" style={{ padding: '3rem 2.5rem', marginBottom: '3rem', background: 'linear-gradient(135deg, rgba(30,41,59,0.9) 0%, rgba(15,23,42,0.95) 100%)', borderRadius: 'var(--radius-lg)', position: 'relative', overflow: 'hidden' }}>
        <div style={{ maxWidth: '650px', position: 'relative', zIndex: 2 }}>
          <span className="badge badge-primary" style={{ marginBottom: '1rem' }}>SHOP SPHERE MARKETPLACE</span>
          <h1 className="heading-xl" style={{ marginBottom: '1rem' }}>
            Discover High-Performance Tech & Lifestyle Essentials
          </h1>
          <p className="text-muted" style={{ fontSize: '1.1rem', marginBottom: '1.5rem' }}>
            Explore verified merchant products with fast shipping, server-side transaction protection, and guaranteed best prices.
          </p>
          <div style={{ display: 'flex', gap: '1rem' }}>
            <a href="#catalog" className="btn btn-primary" style={{ padding: '0.85rem 1.8rem' }}>
              Explore Catalog ↓
            </a>
            <span className="btn btn-gold" style={{ cursor: 'default' }}>
              Coupon: WELCOME10 (10% OFF)
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
