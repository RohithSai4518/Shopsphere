import React, { createContext, useContext, useState, useEffect } from 'react';
import { apiRequest } from '../services/apiClient';
import { useAuth } from './AuthContext';

const CartContext = createContext();

export function CartProvider({ children }) {
  const { user } = useAuth();
  const [cart, setCart] = useState({ items: [], summary: { subtotal: 0, taxEstimate: 0, shippingEstimate: 0, total: 0 } });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (user) {
      fetchCart();
    } else {
      setCart({ items: [], summary: { subtotal: 0, taxEstimate: 0, shippingEstimate: 0, total: 0 } });
    }
  }, [user]);

  async function fetchCart() {
    try {
      setLoading(true);
      const res = await apiRequest('/cart');
      setCart(res.data);
    } catch (err) {
      console.error('Failed to fetch cart:', err);
    } finally {
      setLoading(false);
    }
  }

  async function addToCart(variantId, quantity = 1) {
    try {
      const res = await apiRequest('/cart/items', 'POST', { variantId, quantity });
      setCart(res.data);
      alert('Product added to cart!');
    } catch (err) {
      alert(`Cart error: ${err.message}`);
    }
  }

  async function updateQuantity(cartItemId, quantity) {
    try {
      const res = await apiRequest(`/cart/items/${cartItemId}`, 'PUT', { quantity });
      setCart(res.data);
    } catch (err) {
      alert(`Cart update error: ${err.message}`);
    }
  }

  async function removeFromCart(cartItemId) {
    try {
      const res = await apiRequest(`/cart/items/${cartItemId}`, 'DELETE');
      setCart(res.data);
    } catch (err) {
      alert(`Cart removal error: ${err.message}`);
    }
  }

  return (
    <CartContext.Provider value={{ cart, loading, fetchCart, addToCart, updateQuantity, removeFromCart }}>
      {children}
    </CartContext.Provider>
  );
}

export function useCart() {
  return useContext(CartContext);
}
