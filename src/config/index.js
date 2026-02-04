/**
 * Centralized Configuration File
 * 
 * This file provides a single source of truth for all configuration values.
 * All hardcoded URLs, ports, and endpoints should be removed and use this config instead.
 */

// API Configuration
export const API_CONFIG = {
  // Base URL for backend API
  BASE_URL: import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api',
  
  // Get full API URL
  getApiUrl: (path = '') => {
    const base = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api';
    return path ? `${base}${path.startsWith('/') ? path : '/' + path}` : base;
  },
  
  // Backend base (without /api suffix)
  BACKEND_BASE: import.meta.env.VITE_API_URL?.replace('/api', '') || 'http://127.0.0.1:8000',
};

// Frontend Configuration
export const FRONTEND_CONFIG = {
  // Current frontend URL (for OAuth callbacks, etc.)
  BASE_URL: import.meta.env.VITE_APP_URL || 'http://localhost:5173',
  
  // Default port
  PORT: import.meta.env.VITE_PORT || 5173,
};

// OAuth Configuration
export const OAUTH_CONFIG = {
  // LinkedIn OAuth
  LINKEDIN_CLIENT_ID: import.meta.env.VITE_LINKEDIN_CLIENT_ID || '',
  LINKEDIN_REDIRECT_URI: import.meta.env.VITE_LINKEDIN_REDIRECT_URI || `${FRONTEND_CONFIG.BASE_URL}/iipc/callback`,
  
  // Google OAuth (if needed in future)
  GOOGLE_CLIENT_ID: import.meta.env.VITE_GOOGLE_CLIENT_ID || '',
};

// Timeout Configuration
export const TIMEOUT_CONFIG = {
  // API request timeout (ms)
  API_TIMEOUT: parseInt(import.meta.env.VITE_API_TIMEOUT) || 30000,
  
  // Success message display duration (ms)
  SUCCESS_MESSAGE_DURATION: parseInt(import.meta.env.VITE_SUCCESS_DURATION) || 3000,
  
  // Error message display duration (ms)
  ERROR_MESSAGE_DURATION: parseInt(import.meta.env.VITE_ERROR_DURATION) || 5000,
  
  // Notification polling interval (ms)
  NOTIFICATION_POLL_INTERVAL: parseInt(import.meta.env.VITE_NOTIFICATION_INTERVAL) || 30000,
};

// File Upload Configuration
export const UPLOAD_CONFIG = {
  // Maximum file size (bytes)
  MAX_FILE_SIZE: parseInt(import.meta.env.VITE_MAX_FILE_SIZE) || 10 * 1024 * 1024, // 10MB default
  
  // Allowed file types
  ALLOWED_FILE_TYPES: (import.meta.env.VITE_ALLOWED_FILE_TYPES || 'pdf,jpg,jpeg,png,doc,docx').split(','),
  
  // Maximum files per upload
  MAX_FILES_PER_UPLOAD: parseInt(import.meta.env.VITE_MAX_FILES) || 10,
};

// Pagination Configuration
export const PAGINATION_CONFIG = {
  // Default page size
  DEFAULT_PAGE_SIZE: parseInt(import.meta.env.VITE_PAGE_SIZE) || 20,
  
  // Page size options
  PAGE_SIZE_OPTIONS: [10, 20, 50, 100],
};

// Debug/Development Configuration
export const DEBUG_CONFIG = {
  // Enable debug mode
  ENABLED: import.meta.env.DEV || false,
  
  // Enable verbose logging
  VERBOSE_LOGGING: import.meta.env.VITE_VERBOSE_LOGGING === 'true',
  
  // Show API responses in console
  LOG_API_RESPONSES: import.meta.env.VITE_LOG_API === 'true',
};

// Cache Configuration
export const CACHE_CONFIG = {
  // Enable client-side caching
  ENABLED: import.meta.env.VITE_ENABLE_CACHE === 'true',
  
  // Cache TTL in seconds
  TTL: parseInt(import.meta.env.VITE_CACHE_TTL) || 300, // 5 minutes default
};

// Export all as default
export default {
  API_CONFIG,
  FRONTEND_CONFIG,
  OAUTH_CONFIG,
  TIMEOUT_CONFIG,
  UPLOAD_CONFIG,
  PAGINATION_CONFIG,
  DEBUG_CONFIG,
  CACHE_CONFIG,
};
