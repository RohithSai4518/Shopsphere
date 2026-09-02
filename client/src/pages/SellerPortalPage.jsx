import React, { useState, useEffect } from 'react';
import { apiRequest } from '../services/apiClient';

export default function SellerPortalPage() {
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showProductModal, setShowProductModal] = useState(false);
  const [newProd, setNewProd] = useState({
    name: '',
    categoryId: 'cat_laptops_02',
    basePrice: '',
    discountPercent: '0',
    description: '',
    stockQuantity: '50'
  });

  useEffect(() => {
    async function loadSeller() {
      try {
        const res = await apiRequest('/seller/dashboard');
        setDashboard(res.data);
      } catch (err) {
        console.error('Failed to load seller dashboard:', err);
      } finally {
        setLoading(false);
      }
    }
    loadSeller();
  }, []);

  const handleCreateProduct = async (e) => {
    e.preventDefault();
    try {
      await apiRequest('/products', 'POST', {
        ...newProd,
        basePrice: parseFloat(newProd.basePrice),
        discountPercent: parseFloat(newProd.discountPercent),
        stockQuantity: parseInt(newProd.stockQuantity)
      });
      alert('Product created successfully!');
      setShowProductModal(false);
      const res = await apiRequest('/seller/dashboard');
      setDashboard(res.data);
    } catch (err) {
      alert(`Error: ${err.message}`);
    }
  };

  if (loading) return <div className="container" style={{ paddingTop: '3rem', textAlign: 'center' }}>Loading Seller Dashboard...</div>;

  const metrics = dashboard?.metrics || { totalProducts: 0, totalOrders: 0, totalRevenue: 0 };

  return (
    <div className="container" style={{ paddingTop: '2.5rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <div>
          <h1 className="heading-lg">Seller Center Dashboard</h1>
          <p className="text-muted">{dashboard?.sellerProfile?.business_name || 'Apex Electronics Store'}</p>
        </div>
        <button onClick={() => setShowProductModal(true)} className="btn btn-primary">
          + Add New Product
        </button>
      </div>

      {/* Metrics Row */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1.5rem', marginBottom: '3rem' }}>
        <div className="glass-panel" style={{ padding: '1.5rem' }}>
          <div className="text-muted" style={{ fontSize: '0.85rem' }}>Total Sales Revenue</div>
          <div style={{ fontSize: '1.8rem', fontWeight: 800, color: 'var(--success)' }}>${metrics.totalRevenue.toFixed(2)}</div>
        </div>
        <div className="glass-panel" style={{ padding: '1.5rem' }}>
          <div className="text-muted" style={{ fontSize: '0.85rem' }}>Listed Products</div>
          <div style={{ fontSize: '1.8rem', fontWeight: 800 }}>{metrics.totalProducts}</div>
        </div>
        <div className="glass-panel" style={{ padding: '1.5rem' }}>
          <div className="text-muted" style={{ fontSize: '0.85rem' }}>Total Merchant Orders</div>
          <div style={{ fontSize: '1.8rem', fontWeight: 800 }}>{metrics.totalOrders}</div>
        </div>
      </div>

      {/* Product Add Modal */}
      {showProductModal && (
        <div style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, background: 'rgba(0,0,0,0.8)', zIndex: 200, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <div className="glass-panel" style={{ padding: '2rem', width: '100%', maxWidth: '550px', background: '#1E293B' }}>
            <h3 className="heading-md" style={{ marginBottom: '1.5rem' }}>Create New Merchant Product</h3>
            <form onSubmit={handleCreateProduct} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              <input
                type="text"
                className="input-control"
                placeholder="Product Name"
                value={newProd.name}
                onChange={(e) => setNewProd({ ...newProd, name: e.target.value })}
                required
              />
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                <input
                  type="number"
                  step="0.01"
                  className="input-control"
                  placeholder="Base Price ($)"
                  value={newProd.basePrice}
                  onChange={(e) => setNewProd({ ...newProd, basePrice: e.target.value })}
                  required
                />
                <input
                  type="number"
                  className="input-control"
                  placeholder="Initial Stock Qty"
                  value={newProd.stockQuantity}
                  onChange={(e) => setNewProd({ ...newProd, stockQuantity: e.target.value })}
                  required
                />
              </div>
              <textarea
                className="input-control"
                placeholder="Full Description"
                rows="4"
                value={newProd.description}
                onChange={(e) => setNewProd({ ...newProd, description: e.target.value })}
                required
              ></textarea>
              <div style={{ display: 'flex', gap: '1rem', justifyContent: 'flex-end', marginTop: '1rem' }}>
                <button type="button" onClick={() => setShowProductModal(false)} className="btn btn-secondary">
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary">
                  Publish Product
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

    </div>
  );
}
