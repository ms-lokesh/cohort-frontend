# ============================================================================
# SUPABASE DASHBOARD CONFIGURATION STEPS
# ============================================================================

## 1. DISABLE PUBLIC SIGNUP (REQUIRED)
   
   Navigation: Authentication → Providers → Email
   
   Settings to configure:
   - ✅ Enable email provider: ON
   - ❌ Enable email signup: OFF (CRITICAL - prevents public registration)
   - ✅ Enable email confirmations: ON (users must verify email)
   - ✅ Secure email change: ON
   
   Why: We don't want public signups. Only admins can create users.


## 2. SET REDIRECT URLs FOR PASSWORD RESET

   Navigation: Authentication → URL Configuration
   
   Add these redirect URLs:
   ```
   http://localhost:5173/reset-password
   http://localhost:3000/reset-password
   https://cohort-37ur.onrender.com/reset-password
   https://yourdomain.com/reset-password
   ```
   
   Site URL: https://cohort-37ur.onrender.com
   
   Why: When users click "Forgot Password", Supabase sends them to this URL.


## 3. GET YOUR API KEYS

   Navigation: Settings → API
   
   Copy these keys:
   
   a) Project URL:
      Example: https://xxxxx.supabase.co
      → Add to .env as SUPABASE_URL
   
   b) anon public (public):
      → Add to .env as SUPABASE_ANON_KEY
      → Safe for frontend use
   
   c) service_role (secret):
      → Add to .env as SUPABASE_SERVICE_ROLE_KEY
      → NEVER expose in frontend - only for admin scripts!
   
   d) JWT Secret:
      Found under "JWT Settings" section
      → Add to .env as SUPABASE_JWT_SECRET
      → Used by Django to verify JWT tokens


## 4. EMAIL TEMPLATES (OPTIONAL - CUSTOMIZE)

   Navigation: Authentication → Email Templates
   
   Templates to customize:
   - Confirm signup (when admin creates user with email confirmation)
   - Reset password (for forgot password flow)
   - Magic Link (if you want to use magic links)
   
   Variables available:
   - {{ .Token }}
   - {{ .SiteURL }}
   - {{ .Email }}
   - {{ .RedirectTo }}


## 5. ENVIRONMENT VARIABLES TO ADD

Add these to your .env file:

```bash
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_anon_key_here
SUPABASE_JWT_SECRET=your_jwt_secret_here
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key_here

# Frontend (add to .env in root)
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your_anon_key_here
```


## 6. VERIFY CONFIGURATION

After configuration, test:

1. Try to signup manually (should fail - signup disabled)
2. Create user via admin script
3. User should receive welcome email (if configured)
4. User can login with email + password
5. Forgot password should send reset email
6. Reset link should redirect to /reset-password


## 7. SECURITY CHECKLIST

- [ ] Public signup is DISABLED
- [ ] Service role key is NOT in frontend code
- [ ] Redirect URLs are whitelisted
- [ ] JWT secret is added to Django settings
- [ ] Email confirmations are enabled
- [ ] HTTPS is used in production


## 8. TROUBLESHOOTING

**Issue**: "User already registered" when creating user
**Fix**: Check Supabase dashboard → Authentication → Users
        Delete existing test users if needed

**Issue**: Password reset email not received
**Fix**: Check spam folder, verify SMTP is configured in Supabase

**Issue**: JWT verification fails in Django
**Fix**: Ensure SUPABASE_JWT_SECRET matches the one in Supabase dashboard

**Issue**: CORS errors
**Fix**: Add your frontend URL to Supabase → Settings → API → CORS


## QUICK START COMMAND

After configuring Supabase dashboard and .env:

```bash
# Import all users from CSV
cd backend
python import_dummy_users_supabase.py
```

This will create all 11 users from the CSV file.
