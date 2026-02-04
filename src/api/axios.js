import axios from 'axios';
import { auth } from '../auth/supabaseClient';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

// Request interceptor to add Supabase JWT token
api.interceptors.request.use(
  async (config) => {
    try {
      // Get Supabase access token
      const token = await auth.getAccessToken();
      
      if (token) {
        // Add token to Authorization header
        config.headers.Authorization = `Bearer ${token}`;
      }
    } catch (error) {
      console.error('Error getting access token:', error);
    }
    
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;

    // Handle 401 Unauthorized (invalid/expired token)
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        // Try to refresh the session
        const { session } = await auth.getSession();
        
        if (session?.access_token) {
          // Update the failed request with new token
          originalRequest.headers.Authorization = `Bearer ${session.access_token}`;
          return api(originalRequest);
        } else {
          // No valid session, redirect to login
          window.location.href = '/login';
        }
      } catch (refreshError) {
        console.error('Token refresh failed:', refreshError);
        window.location.href = '/login';
      }
    }

    // Handle other errors
    return Promise.reject(error);
  }
);

// Exported API methods
export const apiClient = {
  // Generic methods
  get: (url, config) => api.get(url, config),
  post: (url, data, config) => api.post(url, data, config),
  put: (url, data, config) => api.put(url, data, config),
  patch: (url, data, config) => api.patch(url, data, config),
  delete: (url, config) => api.delete(url, config),

  // User endpoints
  getCurrentUser: () => api.get('/me'),
  updateProfile: (data) => api.patch('/me', data),

  // Protected endpoint example
  getProtectedData: () => api.get('/protected'),

  // Dashboard endpoints
  getDashboard: () => api.get('/dashboard'),
  
  // Add more endpoints as needed
};

export default api;
