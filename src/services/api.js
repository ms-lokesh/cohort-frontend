import axios from 'axios';
import { API_CONFIG } from '../config';

// Base API configuration
const API_BASE_URL = API_CONFIG.BASE_URL;

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    let token = localStorage.getItem('supabase_access_token');

    // Fallback: Supabase client persists the full session JSON under
    // the key `cohort-supabase-auth`. If the simple key is missing,
    // try to parse that JSON and extract `access_token`.
    if (!token) {
      try {
        const raw = localStorage.getItem('cohort-supabase-auth');
        if (raw) {
          const parsed = JSON.parse(raw);
          token = parsed?.access_token || parsed?.accessToken || null;
        }
      } catch (e) {
        // ignore parse errors
      }
    }

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle token expiry
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    // If 401, clear Supabase session and redirect to login
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      localStorage.removeItem('supabase_access_token');
      localStorage.removeItem('supabase_refresh_token');
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }

    return Promise.reject(error);
  }
);

export default api;
