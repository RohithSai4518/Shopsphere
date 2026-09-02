import React, { useState, useEffect } from 'react';
import { apiRequest } from '../services/apiClient';
import { useCart } from '../context/CartContext';

export default function WishlistPage() {
  const [wishlists, setWishlists] = useState([]);
  const [activeWishlist, setActiveWishlist] = useState(null);
  const [newListName, setNewListName] = useState('');
  const [loading, setLoading] = useState(true);
  const { addToCart } = useCart();

  useEffect(() => {
    loadWishlists();
  }, []);

  async function loadWishlists() {
    try {
      setLoading(true);
      const res = await apiRequest('/wishlist');
      setWishlists(res.data || []);
      if (res.data && res.data.length > 0) {
        setActiveWishlist(res.data[0]);
      }
    } catch (err) {
      console.error('Failed to load wishlists:', err);
    } finally {
      setLoading(false);
    }
  }

  const handleCreateList = async (e) => {
    e.preventDefault();
    if (!newListName.trim()) return;
    try {
      const res = await apiRequest('/wishlist', 'POST', { name: newListName, isPublic: false });
      setWishlists(res.data);
      setNewListName('');
      alert('Wishlist created!');
    } catch (err) {
      alert(`Error: ${err.message}`);
    }
  };

  const handleRemoveItem = async (itemId) => {
    try {
      const res = await apiRequest(`/wishlist/items/${itemId}`, 'DELETE');
      setWishlists(res.data);
    } catch (err) {
      alert(`Error: ${err.message}`);
    }
  };

  if (loading) return <div className="container" style={{ paddingTop: '3rem', textAlign: 'center' }}>Loading Saved Lists...</div>;

  return (
    <div className="container" style={{ paddingTop: '2.5rem' }}>
      <h1 className="heading-lg" style={{ marginBottom: '2rem' }}>Custom Saved Wishlists & Price Alerts</h1>

      <div style={{ display: 'grid', gridTemplateColumns: '280px 1fr', gap: '2rem' }}>
        {/* Sidebar Lists */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <div className="glass-panel" style={{ padding: '1.25rem' }}>
            <h3 className="heading-md" style={{ marginBottom: '1rem' }}>Your Lists</h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', marginBottom: '1.5rem' }}>
              {wishlists.map(w => (
                <button
                  key={w.id}
                  onClick={() => setActiveWishlist(w)}
                  className={`btn ${activeWishlist?.id === w.id ? 'btn-primary' : 'btn-secondary'}`}
                  style={{ textAlign: 'left', width: '100%' }}
                >
                  {w.name} ({w.items ? w.items.length : 0})
                </button>
              ))}
            </div>

            <form onSubmit={handleCreateList} style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
              <input
                type="text"
                className="input-control"
                placeholder="New list name..."
                value={newListName}
                onChange={(e) => setNewListName(e.target.value)}
              />
              <button type="submit" className="btn btn-secondary">Create List</button>
            </form>
          </div>
        </div>

        {/* Wishlist Items Content */}
        <div className="glass-panel" style={{ padding: '2rem' }}>
          <h2 className="heading-md" style={{ marginBottom: '1.5rem' }}>
            {activeWishlist ? activeWishlist.name : 'Saved Wishlist Items'}
          </h2>

          {(!activeWishlist || !activeWishlist.items || activeWishlist.items.length === 0) ? (
            <p className="text-muted">No saved items in this wishlist yet.</p>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              {activeWishlist.items.map(item => (
                <div key={item.wishlist_item_id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '1rem', borderBottom: '1px solid var(--border-light)' }}>
                  <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
                    <img src={item.primary_image} alt={item.name} style={{ width: '60px', height: '60px', objectFit: 'cover', borderRadius: '8px' }} />
                    <div>
                      <div style={{ fontWeight: 600, fontSize: '1rem' }}>{item.name}</div>
                      <div style={{ color: 'var(--accent-teal)', fontWeight: 700 }}>${parseFloat(item.base_price).toFixed(2)}</div>
                    </div>
                  </div>

                  <div style={{ display: 'flex', gap: '0.5rem' }}>
                    <button
                      onClick={() => addToCart(item.product_id, 1)}
                      className="btn btn-primary"
                      style={{ padding: '0.5rem 1rem', fontSize: '0.85rem' }}
                    >
                      Move to Cart
                    </button>
                    <button
                      onClick={() => handleRemoveItem(item.wishlist_item_id)}
                      className="btn btn-secondary"
                      style={{ padding: '0.5rem 1rem', fontSize: '0.85rem', color: 'var(--danger)' }}
                    >
                      Remove
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
