import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

export default function CartPage({ cart, onUpdateQuantity, onRemoveItem }) {
  const [couponCode, setCouponCode] = useState('');
  const [appliedCoupon, setAppliedCoupon] = useState(null);
  const [couponError, setCouponError] = useState(null);
  const navigate = useNavigate();

  const handleApplyCoupon = (e) => {
    e.preventDefault();
    setCouponError(null);
    if (couponCode.trim().toUpperCase() === 'WELCOME10') {
      setAppliedCoupon({ code: 'WELCOME10', discount: 10 });
    } else {
      setCouponError('Invalid coupon code. Try WELCOME10');
    }
  };

  const subtotal = cart?.summary?.subtotal || 0;
  const discountAmount = appliedCoupon ? (subtotal * appliedCoupon.discount) / 100 : 0;
  const taxEstimate = cart?.summary?.taxEstimate || 0;
  const shippingEstimate = cart?.summary?.shippingEstimate || 0;
  const grandTotal = Math.max(0, subtotal - discountAmount + taxEstimate + shippingEstimate);

  return (
    <div className="container" style={{ paddingTop: '2.5rem' }}>
      <h1 className="heading-lg" style={{ marginBottom: '2rem' }}>Shopping Cart ({cart?.summary?.itemCount || 0} items)</h1>

      {!cart?.items || cart.items.length === 0 ? (
        <div className="glass-panel" style={{ padding: '4rem', textAlign: 'center' }}>
          <p className="text-muted" style={{ fontSize: '1.1rem', marginBottom: '1.5rem' }}>Your shopping cart is empty.</p>
          <Link to="/" className="btn btn-primary">Browse Marketplace Catalog</Link>
        </div>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '2rem' }}>
          {/* Cart Items List */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            {cart.items.map(item => (
              <div key={item.cartItemId} className="glass-panel" style={{ padding: '1.25rem', display: 'flex', gap: '1.25rem', alignItems: 'center' }}>
                <img
                  src={item.primaryImage || 'https://images.unsplash.com/photo-1526738549149-8e07eca6c147?auto=format&fit=crop&w=500&q=80'}
                  alt={item.productName}
                  style={{ width: '80px', height: '80px', objectFit: 'cover', borderRadius: 'var(--radius-sm)' }}
                />
                <div style={{ flex: 1 }}>
                  <h4 style={{ fontSize: '1rem', fontWeight: 600, marginBottom: '0.25rem' }}>{item.productName}</h4>
                  <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '0.5rem' }}>
                    Variant: {item.variantName} | Seller: {item.sellerName}
                  </div>
                  <div style={{ fontSize: '1.1rem', fontWeight: 700 }}>${item.unitPrice.toFixed(2)}</div>
                </div>

                <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: '0.5rem' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <button
                      onClick={() => onUpdateQuantity(item.cartItemId, item.quantity - 1)}
                      className="btn btn-secondary"
                      style={{ padding: '0.2rem 0.6rem', fontSize: '0.9rem' }}
                    >
                      -
                    </button>
                    <span style={{ fontWeight: 600 }}>{item.quantity}</span>
                    <button
                      onClick={() => onUpdateQuantity(item.cartItemId, item.quantity + 1)}
                      className="btn btn-secondary"
                      style={{ padding: '0.2rem 0.6rem', fontSize: '0.9rem' }}
                    >
                      +
                    </button>
                  </div>
                  <button
                    onClick={() => onRemoveItem(item.cartItemId)}
                    style={{ background: 'none', border: 'none', color: 'var(--danger)', fontSize: '0.8rem', cursor: 'pointer' }}
                  >
                    Remove
                  </button>
                </div>
              </div>
            ))}
          </div>

          {/* Order Summary Sidebar */}
          <div>
            <div className="glass-panel" style={{ padding: '1.75rem' }}>
              <h3 className="heading-md" style={{ marginBottom: '1.25rem' }}>Order Summary</h3>

              {/* Coupon Form */}
              <form onSubmit={handleApplyCoupon} style={{ marginBottom: '1.5rem', display: 'flex', gap: '0.5rem' }}>
                <input
                  type="text"
                  className="input-control"
                  placeholder="Coupon Code (e.g. WELCOME10)"
                  value={couponCode}
                  onChange={(e) => setCouponCode(e.target.value)}
                  style={{ textTransform: 'uppercase' }}
                />
                <button type="submit" className="btn btn-secondary" style={{ padding: '0.5rem 1rem' }}>
                  Apply
                </button>
              </form>

              {appliedCoupon && (
                <div className="badge badge-success" style={{ marginBottom: '1rem', width: '100%', textAlign: 'center' }}>
                  Coupon {appliedCoupon.code} Applied (-{appliedCoupon.discount}%)
                </div>
              )}

              {couponError && (
                <div style={{ color: 'var(--danger)', fontSize: '0.85rem', marginBottom: '1rem' }}>
                  {couponError}
                </div>
              )}

              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', fontSize: '0.95rem', borderBottom: '1px solid var(--border-light)', paddingBottom: '1rem', marginBottom: '1rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span className="text-muted">Subtotal</span>
                  <span>${subtotal.toFixed(2)}</span>
                </div>
                {discountAmount > 0 && (
                  <div style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--success)' }}>
                    <span>Discount</span>
                    <span>-${discountAmount.toFixed(2)}</span>
                  </div>
                )}
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span className="text-muted">Tax Estimate</span>
                  <span>${taxEstimate.toFixed(2)}</span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span className="text-muted">Shipping</span>
                  <span>{shippingEstimate === 0 ? 'FREE' : `$${shippingEstimate.toFixed(2)}`}</span>
                </div>
              </div>

              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '1.25rem', fontWeight: 800, marginBottom: '1.5rem' }}>
                <span>Order Total</span>
                <span>${grandTotal.toFixed(2)}</span>
              </div>

              <button
                onClick={() => navigate('/checkout', { state: { couponCode: appliedCoupon?.code } })}
                className="btn btn-gold"
                style={{ width: '100%', padding: '0.9rem', fontSize: '1rem' }}
              >
                Proceed to Checkout →
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
