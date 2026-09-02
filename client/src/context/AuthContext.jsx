import React, { createContext, useContext, useState, useEffect } from 'react';
import { apiRequest } from '../services/apiClient';

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function checkAuth() {
      try {
        const token = localStorage.getItem('accessToken');
        if (token) {
          const res = await apiRequest('/auth/me', 'GET', null, token);
          setUser(res.data.user);
        }
      } catch (err) {
        localStorage.removeItem('accessToken');
        setUser(null);
      } finally {
        setLoading(false);
      }
    }
    checkAuth();
  }, []);

  const login = async (email, password) => {
    const res = await apiRequest('/auth/login', 'POST', { email, password });
    localStorage.setItem('accessToken', res.data.accessToken);
    setUser(res.data.user);
    return res.data.user;
  };

  const register = async (userData) => {
    const res = await apiRequest('/auth/register', 'POST', userData);
    localStorage.setItem('accessToken', res.data.accessToken);
    setUser(res.data.user);
    return res.data.user;
  };

  const logout = () => {
    localStorage.removeItem('accessToken');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
