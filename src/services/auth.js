import axios from 'axios';
import { API_CONFIG } from '../config';
import { supabase } from '../auth/supabaseClient';

const API_BASE_URL = API_CONFIG.BASE_URL;

/**
 * Authentication API Service
 * Handles login, logout, token refresh, and user management
 */

export const authService = {
  /**
   * Login user and get JWT tokens
   * @param {string} username - Username or email
   * @param {string} password - Password
   * @returns {Promise} - User data with tokens
   */
  login: async (username, password) => {
    console.log('Auth service - attempting Supabase login with:', username);

    try {
      const { data, error } = await supabase.auth.signInWithPassword({
        email: username,
        password: password,
      });

      if (error) {
        console.error('Supabase login error:', error);
        throw error;
      }

      const session = data?.session;
      const user = data?.user;
      const access = session?.access_token;
      const refresh = session?.refresh_token;

      // Persist tokens for compatibility with older code
      if (access) localStorage.setItem('supabase_access_token', access);
      if (refresh) localStorage.setItem('supabase_refresh_token', refresh);

      // Also set legacy keys to avoid breaking existing pages
      if (access) localStorage.setItem('accessToken', access);
      if (refresh) localStorage.setItem('refreshToken', refresh);

      if (user) localStorage.setItem('user', JSON.stringify(user));

      console.log('Auth service - Supabase login successful');

      return { access, refresh, user };
    } catch (error) {
      console.error('Auth service - login error:', error);
      throw error;
    }
  },

  /**
   * Logout user and clear tokens
   */
  logout: async () => {
    try {
      await supabase.auth.signOut();
    } catch (e) {
      console.warn('Supabase signOut failed:', e);
    }

    localStorage.removeItem('supabase_access_token');
    localStorage.removeItem('supabase_refresh_token');
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('user');
  },

  /**
   * Refresh access token using refresh token
   * @returns {Promise} - New access token
   */
  refreshToken: async () => {
    // Supabase SDK auto-refreshes tokens; fallback: return stored refresh token
    return localStorage.getItem('supabase_refresh_token') || localStorage.getItem('refreshToken');
  },

  /**
   * Get current user from localStorage
   * @returns {Object|null} - User object or null
   */
  getCurrentUser: () => {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
  },

  /**
   * Check if user is authenticated
   * @returns {boolean}
   */
  isAuthenticated: () => {
    return !!(localStorage.getItem('supabase_access_token') || localStorage.getItem('accessToken'));
  },

  /**
   * Get access token
   * @returns {string|null}
   */
  getAccessToken: () => {
    return localStorage.getItem('supabase_access_token') || localStorage.getItem('accessToken');
  },
};

export default authService;
