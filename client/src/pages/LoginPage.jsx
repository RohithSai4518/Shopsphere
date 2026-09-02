import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function LoginPage() {
  const [isRegister, setIsRegister] = useState(false);
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    firstName: '',
    lastName: '',
    role: 'CUSTOMER',
    businessName: ''
  });
  const [error, setError] = useState(null);
  const { login, register } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    try {
      if (isRegister) {
        await register(formData);
      } else {
        await login(formData.email, formData.password);
      }
      navigate('/');
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="container" style={{ paddingTop: '4rem', maxWidth: '450px' }}>
      <div className="glass-panel" style={{ padding: '2.5rem' }}>
        <h2 className="heading-lg" style={{ textAlign: 'center', marginBottom: '0.5rem' }}>
          {isRegister ? 'Create Account' : 'Sign In to ShopSphere'}
        </h2>
        <p className="text-muted" style={{ textAlign: 'center', fontSize: '0.9rem', marginBottom: '2rem' }}>
          {isRegister ? 'Join our multi-tenant marketplace platform' : 'Enter your credentials to manage your account'}
        </p>

        {error && (
          <div style={{ padding: '0.75rem', background: 'rgba(239, 68, 68, 0.2)', border: '1px solid var(--danger)', borderRadius: 'var(--radius-md)', color: '#FCA5A5', fontSize: '0.85rem', marginBottom: '1.25rem' }}>
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          {isRegister && (
            <>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem' }}>
                <input
                  type="text"
                  className="input-control"
                  placeholder="First Name"
                  value={formData.firstName}
                  onChange={(e) => setFormData({ ...formData, firstName: e.target.value })}
                  required
                />
                <input
                  type="text"
                  className="input-control"
                  placeholder="Last Name"
                  value={formData.lastName}
                  onChange={(e) => setFormData({ ...formData, lastName: e.target.value })}
                  required
                />
              </div>

              <select
                className="input-control"
                value={formData.role}
                onChange={(e) => setFormData({ ...formData, role: e.target.value })}
              >
                <option value="CUSTOMER">Account Type: Customer / Shopper</option>
                <option value="SELLER">Account Type: Merchant / Seller</option>
              </select>

              {formData.role === 'SELLER' && (
                <input
                  type="text"
                  className="input-control"
                  placeholder="Business Store Name"
                  value={formData.businessName}
                  onChange={(e) => setFormData({ ...formData, businessName: e.target.value })}
                  required
                />
              )}
            </>
          )}

          <input
            type="email"
            className="input-control"
            placeholder="Email Address"
            value={formData.email}
            onChange={(e) => setFormData({ ...formData, email: e.target.value })}
            required
          />
          <input
            type="password"
            className="input-control"
            placeholder="Password"
            value={formData.password}
            onChange={(e) => setFormData({ ...formData, password: e.target.value })}
            required
          />

          <button type="submit" className="btn btn-primary" style={{ padding: '0.85rem', fontSize: '1rem', marginTop: '0.5rem' }}>
            {isRegister ? 'Complete Registration →' : 'Sign In →'}
          </button>
        </form>

        <div style={{ textAlign: 'center', marginTop: '1.5rem', fontSize: '0.85rem' }} className="text-muted">
          {isRegister ? 'Already have an account?' : "Don't have an account yet?"}{' '}
          <button
            onClick={() => { setIsRegister(!isRegister); setError(null); }}
            style={{ background: 'none', border: 'none', color: 'var(--accent-primary)', fontWeight: 600, cursor: 'pointer' }}
          >
            {isRegister ? 'Sign In' : 'Register Now'}
          </button>
        </div>
      </div>
    </div>
  );
}
