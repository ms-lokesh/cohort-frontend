import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from './AuthContext';
import './Auth.css';

export const ForgotPassword = () => {
  const { requestPasswordReset } = useAuth();
  
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!email) {
      setError('Email is required');
      return;
    }

    if (!/\S+@\S+\.\S+/.test(email)) {
      setError('Please enter a valid email address');
      return;
    }

    setIsSubmitting(true);
    setError('');
    setSuccess(false);

    try {
      const { error: resetError } = await requestPasswordReset(email.trim());

      if (resetError) {
        setError(resetError.message || 'Failed to send reset email');
        return;
      }

      setSuccess(true);
      setEmail('');
    } catch (err) {
      console.error('Password reset error:', err);
      setError('An unexpected error occurred. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="auth-header">
          <h1>Forgot Password</h1>
          <p>Enter your email to receive a password reset link</p>
        </div>

        {error && (
          <div className="auth-error" role="alert">
            {error}
          </div>
        )}

        {success && (
          <div className="auth-success" role="alert">
            <strong>Check your email!</strong>
            <p>
              We've sent a password reset link to <strong>{email}</strong>.
              Click the link in the email to reset your password.
            </p>
          </div>
        )}

        {!success ? (
          <form onSubmit={handleSubmit} className="auth-form">
            <div className="form-group">
              <label htmlFor="email">Email Address</label>
              <input
                type="email"
                id="email"
                name="email"
                value={email}
                onChange={(e) => {
                  setEmail(e.target.value);
                  setError('');
                }}
                placeholder="you@example.com"
                disabled={isSubmitting}
                autoComplete="email"
                required
              />
            </div>

            <button
              type="submit"
              className="btn btn-primary"
              disabled={isSubmitting}
            >
              {isSubmitting ? 'Sending...' : 'Send Reset Link'}
            </button>

            <div className="auth-footer">
              <Link to="/login" className="back-link">
                ← Back to login
              </Link>
            </div>
          </form>
        ) : (
          <div className="auth-footer">
            <p>Didn't receive the email?</p>
            <button
              onClick={() => setSuccess(false)}
              className="btn btn-secondary"
            >
              Try again
            </button>
            <Link to="/login" className="back-link">
              ← Back to login
            </Link>
          </div>
        )}
      </div>
    </div>
  );
};
