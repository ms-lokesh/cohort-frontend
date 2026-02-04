import React, { createContext, useContext, useEffect, useState } from 'react';
import { auth } from './supabaseClient';

const AuthContext = createContext({});

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [session, setSession] = useState(null);
  const [accessToken, setAccessToken] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Initialize auth state
    const initAuth = async () => {
      try {
        const { session: currentSession, accessToken: token } = await auth.getSession();
        setSession(currentSession);
        setUser(currentSession?.user ?? null);
        setAccessToken(token);
      } catch (error) {
        console.error('Auth initialization error:', error);
      } finally {
        setLoading(false);
      }
    };

    initAuth();

    // Listen for auth changes
    const { data: authListener } = auth.onAuthStateChange(async (event, session) => {
      console.log('Supabase auth event:', event);
      setSession(session);
      setUser(session?.user ?? null);
      setAccessToken(session?.access_token ?? null);
      setLoading(false);
    });

    return () => {
      authListener?.subscription?.unsubscribe();
    };
  }, []);

  const signIn = async (email, password) => {
    setLoading(true);
    try {
      const { user, session, accessToken, error } = await auth.signIn(email, password);
      if (error) throw error;
      
      setUser(user);
      setSession(session);
      setAccessToken(accessToken);

      // Persist tokens to localStorage for pages using direct localStorage access
      try {
        if (accessToken) {
          localStorage.setItem('supabase_access_token', accessToken);
          localStorage.setItem('accessToken', accessToken);
        }
        const refresh = session?.refresh_token;
        if (refresh) {
          localStorage.setItem('supabase_refresh_token', refresh);
          localStorage.setItem('refreshToken', refresh);
        }
        console.log('AuthContext - signIn stored tokens, access:', accessToken ? 'present' : 'missing');
      } catch (e) {
        console.warn('AuthContext - failed to persist tokens', e);
      }
      
      return { user, error: null };
    } catch (error) {
      return { user: null, error };
    } finally {
      setLoading(false);
    }
  };

  const signOut = async () => {
    setLoading(true);
    try {
      const { error } = await auth.signOut();
      if (error) throw error;
      
      setUser(null);
      setSession(null);
      setAccessToken(null);
      
      return { error: null };
    } catch (error) {
      return { error };
    } finally {
      setLoading(false);
    }
  };

  const requestPasswordReset = async (email) => {
    return await auth.requestPasswordReset(email);
  };

  const updatePassword = async (newPassword) => {
    return await auth.updatePassword(newPassword);
  };

  const getToken = async () => {
    if (accessToken) return accessToken;
    return await auth.getAccessToken();
  };

  const value = {
    user,
    session,
    accessToken,
    loading,
    signIn,
    signOut,
    requestPasswordReset,
    updatePassword,
    getToken,
    isAuthenticated: !!user,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
