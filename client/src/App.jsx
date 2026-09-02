import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { CartProvider } from './context/CartContext';
import Navbar from './components/ui/Navbar';
import Footer from './components/ui/Footer';

import HomePage from './pages/HomePage';
import ProductDetailPage from './pages/ProductDetailPage';
import CartPage from './pages/CartPage';
import CheckoutPage from './pages/CheckoutPage';
import OrderSuccessPage from './pages/OrderSuccessPage';
import AccountPage from './pages/AccountPage';
import WishlistPage from './pages/WishlistPage';
import SupportPage from './pages/SupportPage';
import SellerPortalPage from './pages/SellerPortalPage';
import AdminConsolePage from './pages/AdminConsolePage';
import LoginPage from './pages/LoginPage';

function ProtectedRoute({ children, allowedRoles }) {
  const { user, loading } = useAuth();
  if (loading) return <div style={{ padding: '3rem', textAlign: 'center' }}>Authenticating ShopSphere session...</div>;
  if (!user) return <Navigate to="/login" replace />;
  if (allowedRoles && !allowedRoles.includes(user.role)) return <Navigate to="/" replace />;
  return children;
}

export default function App() {
  return (
    <AuthProvider>
      <CartProvider>
        <Router>
          <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh', background: 'var(--bg-dark)', color: 'var(--text-main)' }}>
            <Navbar />
            <main style={{ flex: 1, paddingBottom: '4rem' }}>
              <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/product/:slug" element={<ProductDetailPage />} />
                <Route path="/cart" element={<CartPage />} />
                <Route path="/checkout" element={<ProtectedRoute><CheckoutPage /></ProtectedRoute>} />
                <Route path="/order-success" element={<ProtectedRoute><OrderSuccessPage /></ProtectedRoute>} />
                <Route path="/account" element={<ProtectedRoute><AccountPage /></ProtectedRoute>} />
                <Route path="/wishlist" element={<ProtectedRoute><WishlistPage /></ProtectedRoute>} />
                <Route path="/support" element={<ProtectedRoute><SupportPage /></ProtectedRoute>} />
                <Route path="/seller" element={<ProtectedRoute allowedRoles={['SELLER', 'ADMIN']}><SellerPortalPage /></ProtectedRoute>} />
                <Route path="/admin" element={<ProtectedRoute allowedRoles={['ADMIN']}><AdminConsolePage /></ProtectedRoute>} />
                <Route path="/login" element={<LoginPage />} />
              </Routes>
            </main>
            <Footer />
          </div>
        </Router>
      </CartProvider>
    </AuthProvider>
  );
}
