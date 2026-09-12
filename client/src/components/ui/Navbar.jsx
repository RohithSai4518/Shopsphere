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
    <header style={{ background: 'var(--bg-header)', color: '#FFFFFF', borderBottom: '1px solid #232F3E', position: 'sticky', top: 0, zIndex: 100, boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
      <div className="container" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0.75rem 1.5rem', gap: '1.5rem' }}>
        
        {/* Brand Logo */}
        <Link to="/" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', textDecoration: 'none' }}>
          <div style={{ width: '34px', height: '34px', borderRadius: '8px', background: 'var(--accent-gradient)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: '800', fontSize: '1.15rem', color: '#111827', boxShadow: '0 1px 3px rgba(0,0,0,0.2)' }}>
            S
          </div>
          <span style={{ fontSize: '1.35rem', fontWeight: '800', color: '#FFFFFF' }}>
            Shop<span style={{ color: 'var(--accent-primary)' }}>Sphere</span>
          </span>
        </Link>

        {/* Search Bar */}
        <form onSubmit={handleSearchSubmit} style={{ display: 'flex', flex: 1, maxWidth: '600px', position: 'relative' }}>
          <input
            type="text"
            className="input-control"
            placeholder="Search products, brands, essentials..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            style={{ borderRadius: '6px', paddingRight: '5rem', background: '#FFFFFF', color: '#0F172A', border: '1px solid #CBD5E1' }}
          />
          <button type="submit" className="btn btn-primary" style={{ position: 'absolute', right: '3px', top: '3px', bottom: '3px', borderRadius: '4px', padding: '0 1.25rem', fontSize: '0.88rem' }}>
            Search
          </button>
        </form>

        {/* Navigation & User Menu */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '1.25rem' }}>
          <Link to="/cart" style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', color: '#FFFFFF', position: 'relative' }}>
            <span style={{ fontSize: '1.2rem' }}>🛒</span>
            <span style={{ fontWeight: 600, fontSize: '0.92rem' }}>Cart</span>
            {cartCount > 0 && (
              <span className="badge" style={{ position: 'absolute', top: '-8px', right: '-12px', background: 'var(--accent-primary)', color: '#111827', fontWeight: 800 }}>
                {cartCount}
              </span>
            )}
          </Link>

          {user ? (
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
              <div style={{ textAlign: 'right' }}>
                <div style={{ fontSize: '0.85rem', fontWeight: 600, color: '#FFFFFF' }}>Hi, {user.firstName}</div>
                <div style={{ fontSize: '0.75rem', color: 'var(--accent-primary)', fontWeight: 600 }}>{user.role}</div>
              </div>

              {user.role === 'SELLER' && (
                <Link to="/seller" className="btn btn-secondary" style={{ padding: '0.35rem 0.75rem', fontSize: '0.82rem' }}>
                  Seller Portal
                </Link>
              )}

              {user.role === 'ADMIN' && (
                <Link to="/admin" className="btn btn-secondary" style={{ padding: '0.35rem 0.75rem', fontSize: '0.82rem' }}>
                  Admin Console
                </Link>
              )}

              <button onClick={logout} className="btn btn-secondary" style={{ padding: '0.35rem 0.75rem', fontSize: '0.82rem' }}>
                Logout
              </button>
            </div>
          ) : (
            <Link to="/login" className="btn btn-primary" style={{ padding: '0.45rem 1.2rem', fontSize: '0.88rem' }}>
              Sign In
            </Link>
          )}
        </div>

      </div>
    </header>
  );
}
