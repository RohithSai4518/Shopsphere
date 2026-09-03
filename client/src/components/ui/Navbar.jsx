import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

export default function Navbar({ cartCount = 0, onSearch }) {
  const { user, logout } = useAuth();
  const [searchTerm, setSearchTerm] = useState('');
  const navigate = useNavigate();

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    if (onSearch) onSearch(searchTerm);
    navigate(`/?search=${encodeURIComponent(searchTerm)}`);
  };

  return (
    <header className="glass-panel" style={{ borderRadius: 0, borderTop: 'none', borderLeft: 'none', borderRight: 'none', position: 'sticky', top: 0, zIndex: 100 }}>
      <div className="container" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0.85rem 1.5rem', gap: '1.5rem' }}>
        
        {/* Brand Logo */}
        <Link to="/" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', textDecoration: 'none' }}>
          <div style={{ width: '36px', height: '36px', borderRadius: '10px', background: 'var(--accent-gradient)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: '800', fontSize: '1.2rem', color: '#FFF' }}>
            S
          </div>
          <span style={{ fontSize: '1.4rem', fontWeight: '800', background: 'linear-gradient(135deg, #FFFFFF 0%, #34D399 50%, #818CF8 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
            ShopSphere
          </span>
        </Link>

        {/* Search Bar */}
        <form onSubmit={handleSearchSubmit} style={{ display: 'flex', flex: 1, maxWidth: '600px', position: 'relative' }}>
          <input
            type="text"
            className="input-control"
            placeholder="Search millions of products, brands, and categories..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            style={{ borderRadius: 'var(--radius-full)', paddingRight: '4rem' }}
          />
          <button type="submit" className="btn btn-primary" style={{ position: 'absolute', right: '4px', top: '4px', bottom: '4px', borderRadius: 'var(--radius-full)', padding: '0 1.25rem' }}>
            Search
          </button>
        </form>

        {/* Navigation & User Menu */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '1.25rem' }}>
          <Link to="/cart" style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', color: 'var(--text-main)', position: 'relative' }}>
            <span style={{ fontSize: '1.2rem' }}>🛒</span>
            <span style={{ fontWeight: 600 }}>Cart</span>
            {cartCount > 0 && (
              <span className="badge badge-primary" style={{ position: 'absolute', top: '-8px', right: '-12px' }}>
                {cartCount}
              </span>
            )}
          </Link>

          {user ? (
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
              <div style={{ textAlign: 'right' }}>
                <div style={{ fontSize: '0.85rem', fontWeight: 600 }}>Hi, {user.firstName}</div>
                <div style={{ fontSize: '0.75rem', color: 'var(--accent-primary)' }}>{user.role}</div>
              </div>

              {user.role === 'SELLER' && (
                <Link to="/seller" className="btn btn-secondary" style={{ padding: '0.4rem 0.8rem', fontSize: '0.85rem' }}>
                  Seller Portal
                </Link>
              )}

              {user.role === 'ADMIN' && (
                <Link to="/admin" className="btn btn-secondary" style={{ padding: '0.4rem 0.8rem', fontSize: '0.85rem' }}>
                  Admin Console
                </Link>
              )}

              <button onClick={logout} className="btn btn-secondary" style={{ padding: '0.4rem 0.8rem', fontSize: '0.85rem' }}>
                Logout
              </button>
            </div>
          ) : (
            <Link to="/login" className="btn btn-primary" style={{ padding: '0.5rem 1.2rem', fontSize: '0.9rem' }}>
              Sign In
            </Link>
          )}
        </div>

      </div>
    </header>
  );
}
