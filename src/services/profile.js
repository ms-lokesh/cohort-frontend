import axios from 'axios';
import { API_CONFIG } from '../config';

const API_BASE_URL = `${API_CONFIG.BASE_URL}/profiles`;

// Create axios instance with interceptors
const profileAxios = axios.create({
  baseURL: API_BASE_URL,
});

// Request interceptor to add auth token
profileAxios.interceptors.request.use(
  config => {
    const token = localStorage.getItem('supabase_access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  error => Promise.reject(error)
);

// Response interceptor for error handling
profileAxios.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('supabase_access_token');
      localStorage.removeItem('supabase_refresh_token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

/**
 * Get current user's profile
 */
export const getUserProfile = async () => {
  const response = await profileAxios.get('/me/');
  return response.data;
};

/**
 * Update user profile
 * @param {Object} data - Profile data to update
 * @param {string} data.leetcode_id - LeetCode username
 * @param {string} data.github_id - GitHub username
 * @param {string} data.linkedin_id - LinkedIn profile URL or ID
 */
export const updateUserProfile = async (data) => {
  const response = await profileAxios.patch('/me/', data);
  return response.data;
};

export default {
  getUserProfile,
  updateUserProfile,
};
