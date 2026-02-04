import { createClient } from '@supabase/supabase-js';

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseAnonKey) {
  throw new Error('Missing Supabase environment variables');
}

export const supabase = createClient(supabaseUrl, supabaseAnonKey, {
  auth: {
    autoRefreshToken: true,
    persistSession: true,
    detectSessionInUrl: true,
    storageKey: 'cohort-supabase-auth',
  },
});

/**
 * Authentication methods for Supabase
 * NOTE: Signup is disabled - users are pre-created by admin
 */
export const auth = {
  /**
   * Sign in with email and password
   * Users must be pre-created by admin in Supabase
   */
  signIn: async (email, password) => {
    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password,
    });

    // Persist tokens for compatibility with existing code paths
    const session = data?.session;
    if (session) {
      try {
        const access = session.access_token;
        const refresh = session.refresh_token;
        if (access) {
          localStorage.setItem('supabase_access_token', access);
          localStorage.setItem('accessToken', access);
        }
        if (refresh) {
          localStorage.setItem('supabase_refresh_token', refresh);
          localStorage.setItem('refreshToken', refresh);
        }
        if (data.user) {
          localStorage.setItem('user', JSON.stringify(data.user));
        }
      } catch (e) {
        console.warn('Failed to persist Supabase session to localStorage', e);
      }
    }

    return { 
      user: data?.user, 
      session: session,
      accessToken: session?.access_token,
      error 
    };
  },

  /**
   * Sign out current user
   */
  signOut: async () => {
    const { error } = await supabase.auth.signOut();
    return { error };
  },

  /**
   * Get current session with JWT token
   */
  getSession: async () => {
    const { data, error } = await supabase.auth.getSession();
    const session = data?.session;

    // Keep localStorage in sync if session exists
    if (session) {
      try {
        const access = session.access_token;
        const refresh = session.refresh_token;
        if (access) {
          localStorage.setItem('supabase_access_token', access);
          localStorage.setItem('accessToken', access);
        }
        if (refresh) {
          localStorage.setItem('supabase_refresh_token', refresh);
          localStorage.setItem('refreshToken', refresh);
        }
      } catch (e) {
        console.warn('Failed to sync Supabase session to localStorage', e);
      }
    }

    return { 
      session: session,
      accessToken: session?.access_token,
      error 
    };
  },

  /**
   * Get current user
   */
  getUser: async () => {
    const { data, error } = await supabase.auth.getUser();
    return { user: data?.user, error };
  },

  /**
   * Send password reset email
   * User will receive email with reset link
   */
  requestPasswordReset: async (email) => {
    const { error } = await supabase.auth.resetPasswordForEmail(email, {
      redirectTo: `${window.location.origin}/reset-password`,
    });
    return { error };
  },

  /**
   * Update user password after reset
   * Called from reset-password page with token in URL
   */
  updatePassword: async (newPassword) => {
    const { data, error } = await supabase.auth.updateUser({
      password: newPassword,
    });
    return { user: data?.user, error };
  },

  /**
   * Subscribe to auth state changes
   */
  onAuthStateChange: (callback) => {
    return supabase.auth.onAuthStateChange(callback);
  },

  /**
   * Get access token for Django API requests
   */
  getAccessToken: async () => {
    const { data, error } = await supabase.auth.getSession();
    if (error || !data.session) {
      return null;
    }
    return data.session.access_token;
  },
};
