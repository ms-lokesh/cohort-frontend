# Django + Supabase Authentication Architecture

## 📋 Overview

This is a **hybrid authentication architecture** where:
- **Supabase** handles authentication (login, JWT tokens, password reset)
- **Django** handles all data and business logic
- No public signup - users are pre-created by admins
- JWT tokens from Supabase are verified by Django middleware

---

## 📁 Folder Structure

```
backend/
├── apps/
│   └── auth_supabase/
│       ├── __init__.py
│       ├── models.py            # SupabaseUserMapping model
│       ├── middleware.py        # JWT verification middleware
│       ├── decorators.py        # @supabase_auth_required decorator
│       ├── views.py             # Example API endpoints
│       ├── urls.py              # URL routing
│       ├── admin.py             # Django admin integration
│       └── apps.py              # App config
├── scripts/
│   ├── create_supabase_users.py # Create single user
│   ├── import_users_from_csv.py # Bulk import from CSV
│   └── users_template.csv       # CSV template
└── config/
    └── settings.py              # Django settings

src/
├── auth/
│   ├── supabaseClient.js        # Supabase client (anon key only)
│   ├── AuthContext.jsx          # React auth state management
│   ├── Login.jsx                # Login page
│   ├── ForgotPassword.jsx       # Forgot password page
│   ├── ResetPassword.jsx        # Reset password page
│   ├── ProtectedRoute.jsx       # Route protection
│   └── Auth.css                 # Auth styles
└── api/
    └── axios.js                 # Axios with JWT interceptor
```

---

## 🔧 Setup Instructions

### 1. Install Dependencies

**Backend:**
```bash
cd backend
pip install django djangorestframework supabase PyJWT requests
```

**Frontend:**
```bash
cd ../
npm install @supabase/supabase-js axios
```

### 2. Environment Variables

**Frontend (`.env`):**
```bash
# Supabase public config (safe for frontend)
VITE_SUPABASE_URL=https://YOUR_PROJECT.supabase.co
VITE_SUPABASE_ANON_KEY=your_anon_key_here

# Django API
VITE_API_URL=http://localhost:8000/api
```

**Backend (`.env` or `settings.py`):**
```python
# Supabase config
SUPABASE_URL = 'https://YOUR_PROJECT.supabase.co'
SUPABASE_ANON_KEY = 'your_anon_key_here'
SUPABASE_JWT_SECRET = 'your_jwt_secret_here'

# Admin script only (NEVER in frontend!)
SUPABASE_SERVICE_ROLE_KEY = 'your_service_role_key_here'
```

### 3. Configure Django Settings

**Add to `INSTALLED_APPS`:**
```python
INSTALLED_APPS = [
    # ...
    'apps.auth_supabase',
]
```

**Add middleware:**
```python
MIDDLEWARE = [
    # ...
    'apps.auth_supabase.middleware.SupabaseAuthMiddleware',
    # Add after Django's AuthenticationMiddleware
]
```

**Add URL routes:**
```python
# config/urls.py
urlpatterns = [
    path('api/', include('apps.auth_supabase.urls')),
    # ...
]
```

### 4. Run Migrations

```bash
python manage.py makemigrations auth_supabase
python manage.py migrate
```

### 5. Configure Supabase Dashboard

#### A. Disable Public Signup
1. Go to **Authentication** → **Providers**
2. Find **Email** provider
3. **Disable** "Enable sign ups"

#### B. Set Redirect URLs
1. Go to **Authentication** → **URL Configuration**
2. Add these redirect URLs:
   ```
   http://localhost:5173/reset-password
   https://yourdomain.com/reset-password
   ```

#### C. Get JWT Secret
1. Go to **Settings** → **API**
2. Copy **JWT Secret** (needed for Django token verification)

#### D. Get Keys
- **anon key**: For frontend (public, safe to expose)
- **service_role key**: For admin scripts (NEVER expose in frontend!)

---

## 🚀 Usage

### Create Single User

```bash
python backend/scripts/create_supabase_users.py \
  --email john@example.com \
  --username john_doe \
  --password SecurePass123 \
  --first-name John \
  --last-name Doe
```

**With email notification:**
```bash
python backend/scripts/create_supabase_users.py \
  --email john@example.com \
  --username john_doe \
  --password TempPass123 \
  --send-email
```

### Bulk Import from CSV

**1. Prepare CSV file:**
```csv
email,username,first_name,last_name,is_staff,is_superuser
john@example.com,john_doe,John,Doe,0,0
admin@example.com,admin,Admin,User,1,1
```

**2. Import:**
```bash
python backend/scripts/import_users_from_csv.py \
  --csv users.csv \
  --send-email
```

**3. With default password (all users same password):**
```bash
python backend/scripts/import_users_from_csv.py \
  --csv users.csv \
  --default-password WelcomeCohort2024
```

---

## 🔐 Authentication Flow

### Login Flow
```
1. User enters email/password in Login.jsx
2. Frontend calls Supabase signInWithPassword()
3. Supabase returns JWT access token
4. Token stored in localStorage by AuthContext
5. Axios interceptor adds token to all API requests
6. Django middleware verifies JWT signature
7. Django maps Supabase user → Django user
8. request.user available in Django views
```

### Password Reset Flow
```
1. User clicks "Forgot Password"
2. User enters email in ForgotPassword.jsx
3. Supabase sends reset email with magic link
4. User clicks link → redirected to /reset-password
5. ResetPassword.jsx calls updatePassword()
6. User can now login with new password
```

---

## 🛡️ Security Best Practices

### ✅ DO:
- Use `SUPABASE_ANON_KEY` in frontend
- Use `SUPABASE_SERVICE_ROLE_KEY` only in backend scripts
- Verify JWT tokens in Django middleware
- Use HTTPS in production
- Set proper CORS headers
- Rotate JWT secrets regularly

### ❌ DON'T:
- Never expose `SERVICE_ROLE_KEY` in frontend
- Never allow public signups
- Never skip JWT verification
- Never trust client-side auth checks
- Never log tokens/passwords

---

## 📝 Example API Usage

### Protected Endpoint

**Django:**
```python
from apps.auth_supabase.decorators import supabase_auth_required

@supabase_auth_required
def my_view(request):
    user = request.user  # Authenticated Django user
    return JsonResponse({
        'username': user.username,
        'email': user.email,
    })
```

**React:**
```javascript
import { apiClient } from './api/axios';

const MyComponent = () => {
  const fetchData = async () => {
    const { data } = await apiClient.get('/protected');
    console.log(data);
  };
  
  return <button onClick={fetchData}>Fetch Data</button>;
};
```

### Current User Endpoint

**GET `/api/me`**
```javascript
const { data } = await apiClient.getCurrentUser();
// {
//   id: 1,
//   username: 'john_doe',
//   email: 'john@example.com',
//   first_name: 'John',
//   is_staff: false
// }
```

---

## 🧪 Testing

### 1. Test Login
```javascript
// In browser console
const { signIn } = useAuth();
const { user, error } = await signIn('john@example.com', 'password123');
console.log(user, error);
```

### 2. Test Protected API
```javascript
const { data } = await apiClient.getProtectedData();
console.log(data); // Should return protected data
```

### 3. Test JWT Verification
```bash
# Make request with invalid token
curl -H "Authorization: Bearer invalid_token" \
  http://localhost:8000/api/protected

# Should return 401 Unauthorized
```

---

## 🐛 Troubleshooting

### Issue: "Invalid token" error
- **Check**: JWT_SECRET matches Supabase settings
- **Check**: Token hasn't expired (default 1 hour)
- **Check**: Middleware is properly configured

### Issue: "No Django user found"
- **Check**: User exists in SupabaseUserMapping table
- **Check**: supabase_id matches token's `sub` claim

### Issue: Password reset email not sent
- **Check**: Redirect URL is whitelisted in Supabase
- **Check**: Email provider configured in Supabase

### Issue: CORS errors
- **Check**: CORS_ALLOWED_ORIGINS in Django settings
- **Check**: Axios baseURL matches backend URL

---

## 📚 Key Concepts

### Why This Architecture?

1. **Supabase for Auth**: Battle-tested auth system with JWT, email verification, password reset
2. **Django for Data**: Full control over business logic, complex queries, admin panel
3. **JWT as Bridge**: Stateless authentication, no session management needed
4. **Admin Control**: No public signup, admins pre-create users

### User Mapping

```python
SupabaseUserMapping:
  supabase_id (UUID) ←→ django_user (User)
```

When JWT arrives:
1. Extract `sub` claim (Supabase user ID)
2. Look up in `SupabaseUserMapping`
3. Get linked `django_user`
4. Attach to `request.user`

---

## 🎯 Routes

### Frontend Routes
- `/login` - Login page
- `/forgot-password` - Request reset email
- `/reset-password` - Set new password (from email link)
- `/dashboard` - Protected dashboard

### API Endpoints
- `GET /api/me` - Current user info
- `GET /api/protected` - Protected data example
- `GET /api/admin/stats` - Admin-only endpoint
- `GET /api/health` - Health check (public)

---

## ✅ Deployment Checklist

- [ ] Set all environment variables
- [ ] Run migrations
- [ ] Disable Supabase public signup
- [ ] Add production redirect URLs
- [ ] Test password reset flow
- [ ] Create admin users
- [ ] Import regular users from CSV
- [ ] Test JWT verification
- [ ] Enable HTTPS
- [ ] Configure CORS
- [ ] Set up monitoring

---

## 🔗 Additional Resources

- [Supabase Auth Docs](https://supabase.com/docs/guides/auth)
- [JWT.io Debugger](https://jwt.io/)
- [Django Authentication](https://docs.djangoproject.com/en/stable/topics/auth/)

---

**Created by:** Senior Backend Engineer  
**Architecture:** Django + Supabase Hybrid Auth  
**Last Updated:** 2024
