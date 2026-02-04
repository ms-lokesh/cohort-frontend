# Configuration System Documentation

## Overview

This document describes the centralized configuration system implemented to eliminate hardcoded values throughout the Cohort Web Application.

## Architecture

### Frontend Configuration

**Location:** `src/config/index.js`

The frontend uses a single configuration file that exports multiple configuration objects:

#### 1. API_CONFIG
Controls all API-related settings:
```javascript
{
  BASE_URL: string,           // Backend API base URL
  TIMEOUT: number,            // Request timeout in ms
  RETRY_ATTEMPTS: number,     // Number of retry attempts
  RETRY_DELAY: number         // Delay between retries in ms
}
```

#### 2. FRONTEND_CONFIG
Frontend application settings:
```javascript
{
  APP_URL: string,            // Frontend base URL
  APP_NAME: string,           // Application name
  DEFAULT_PAGE_SIZE: number,  // Pagination default
  MAX_PAGE_SIZE: number       // Max items per page
}
```

#### 3. OAUTH_CONFIG
OAuth provider credentials:
```javascript
{
  GOOGLE_CLIENT_ID: string,
  LINKEDIN_CLIENT_ID: string
}
```

#### 4. TIMEOUT_CONFIG
Various timeout settings:
```javascript
{
  API_TIMEOUT: number,              // API request timeout
  NOTIFICATION_DURATION: number,    // Notification display time
  SESSION_TIMEOUT: number,          // Session expiry time
  IDLE_TIMEOUT: number             // Idle logout time
}
```

#### 5. UPLOAD_CONFIG
File upload constraints:
```javascript
{
  MAX_FILE_SIZE: number,      // Max file size in bytes
  MAX_FILE_SIZE_MB: number,   // Max file size in MB
  ALLOWED_TYPES: string[]     // Allowed file extensions
}
```

#### 6. PAGINATION_CONFIG
Pagination settings:
```javascript
{
  DEFAULT_PAGE_SIZE: number,
  MAX_PAGE_SIZE: number,
  PAGE_SIZE_OPTIONS: number[]
}
```

#### 7. DEBUG_CONFIG
Development debugging options:
```javascript
{
  ENABLE_LOGGING: boolean,
  ENABLE_REDUX_DEVTOOLS: boolean,
  ENABLE_PERFORMANCE_METRICS: boolean
}
```

#### 8. CACHE_CONFIG
Client-side caching:
```javascript
{
  ENABLED: boolean,
  DURATION: number,      // Cache duration in ms
  MAX_SIZE: number       // Max cache entries
}
```

### Backend Configuration

**Location:** `backend/config/settings.py`

Django settings use environment variables with sensible defaults:

```python
# Core Settings
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Database
DATABASE_URL = os.getenv('DATABASE_URL', '')  # Falls back to SQLite if empty

# CORS
CORS_ALLOWED_ORIGINS = os.getenv(
    'CORS_ALLOWED_ORIGINS',
    'http://localhost:5173,http://localhost:5174'
).split(',')
CORS_ALLOW_ALL_ORIGINS = os.getenv('CORS_ALLOW_ALL_ORIGINS', 'False').lower() in ('true', '1', 't')
```

### Test Configuration

**Location:** `backend/test_config.py`

Centralized test user credentials and settings:

```python
DEFAULT_PASSWORDS = {
    'admin': os.getenv('TEST_ADMIN_PASSWORD', 'admin123'),
    'mentor': os.getenv('TEST_MENTOR_PASSWORD', 'mentor123'),
    'student': os.getenv('TEST_STUDENT_PASSWORD', 'pass123#'),
    'floorwing': os.getenv('TEST_FLOORWING_PASSWORD', 'floorwing123'),
    'testuser': os.getenv('TEST_USER_PASSWORD', 'testpass123'),
    'default': os.getenv('TEST_DEFAULT_PASSWORD', 'test123'),
}

# Railway database URL (must be set via environment)
RAILWAY_DB_URL = os.getenv('RAILWAY_DATABASE_URL', None)
```

**Helper Functions:**
- `get_test_password(user_type)` - Get password for specific user type
- `get_test_email(username, domain)` - Generate test email address
- `validate_railway_db()` - Ensure Railway DB URL is set
- `get_test_user_data(user_type, index)` - Generate complete user data dict

## Environment Variables

### Frontend (.env)

```bash
# Required
VITE_API_URL=http://localhost:8000/api

# Optional (with defaults)
VITE_APP_URL=http://localhost:5173
VITE_APP_NAME="Cohort Management System"
VITE_MAX_FILE_SIZE_MB=10
VITE_API_TIMEOUT_MS=30000
VITE_DEFAULT_PAGE_SIZE=20
VITE_ENABLE_CACHE=true

# OAuth (if needed)
VITE_GOOGLE_CLIENT_ID=your-google-client-id
VITE_LINKEDIN_CLIENT_ID=your-linkedin-client-id

# Feature Flags
VITE_ENABLE_GAMIFICATION=true
VITE_ENABLE_CHAT=true
VITE_ENABLE_NOTIFICATIONS=true
VITE_ENABLE_ANALYTICS=false

# Debug (development only)
VITE_DEBUG_LOGGING=false
VITE_ENV=development
```

### Backend (.env)

```bash
# Required for Production
SECRET_KEY=your-secret-key-here-change-in-production
DATABASE_URL=postgresql://user:pass@host:port/dbname

# Optional (with defaults)
DEBUG=False
DJANGO_ENV=production
ALLOWED_HOSTS=.render.com,.railway.app,localhost
CORS_ALLOWED_ORIGINS=https://frontend.com,http://localhost:5173
CORS_ALLOW_ALL_ORIGINS=False

# JWT Settings
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=60
JWT_REFRESH_TOKEN_LIFETIME_DAYS=7
JWT_ALGORITHM=HS256
JWT_SECRET_KEY=your-jwt-secret-key

# Test Credentials (Development/Testing ONLY)
TEST_ADMIN_PASSWORD=admin123
TEST_MENTOR_PASSWORD=mentor123
TEST_STUDENT_PASSWORD=pass123#
TEST_FLOORWING_PASSWORD=floorwing123
RAILWAY_DATABASE_URL=postgresql://...  # For migration scripts only
```

## Usage Examples

### Frontend

**Importing Configuration:**
```javascript
import { API_CONFIG, UPLOAD_CONFIG } from '../config';

// Use in API calls
const response = await fetch(`${API_CONFIG.BASE_URL}/users/`);

// Check file size
if (file.size > UPLOAD_CONFIG.MAX_FILE_SIZE) {
  throw new Error(`File too large. Max size: ${UPLOAD_CONFIG.MAX_FILE_SIZE_MB}MB`);
}
```

**In Service Files:**
```javascript
// src/services/api.js
import axios from 'axios';
import { API_CONFIG } from '../config';

const api = axios.create({
  baseURL: API_CONFIG.BASE_URL,
  timeout: API_CONFIG.TIMEOUT,
  withCredentials: true,
});
```

### Backend

**Using Test Config:**
```python
# In test/setup scripts
from test_config import get_test_password, get_test_email

# Create test user
user = User.objects.create_user(
    username='testuser',
    email=get_test_email('testuser'),
    password=get_test_password('student')
)
```

**Validating Railway DB:**
```python
from test_config import validate_railway_db, RAILWAY_DB_URL

if not validate_railway_db():
    print("ERROR: Set RAILWAY_DATABASE_URL environment variable")
    sys.exit(1)

# Safe to use RAILWAY_DB_URL now
conn = psycopg.connect(RAILWAY_DB_URL)
```

## Migration Guide

### For New Code

**DON'T:**
```javascript
// ❌ Hardcoded URL
fetch('http://localhost:8000/api/users/')

// ❌ Hardcoded password
user.set_password('admin123')

// ❌ Hardcoded timeout
axios.create({ timeout: 30000 })
```

**DO:**
```javascript
// ✅ Use configuration
import { API_CONFIG } from '../config';
fetch(`${API_CONFIG.BASE_URL}/users/`)

// ✅ Use test config
from test_config import get_test_password
user.set_password(get_test_password('admin'))

// ✅ Use configuration
import { API_CONFIG } from '../config';
axios.create({ timeout: API_CONFIG.TIMEOUT })
```

### For Existing Code

1. **Find hardcoded values:**
   ```bash
   # Search for hardcoded URLs
   grep -r "localhost:8000" src/
   
   # Search for hardcoded passwords
   grep -r "password.*=.*['\"]admin123" backend/
   ```

2. **Replace with config:**
   - Frontend: Import from `src/config/index.js`
   - Backend: Import from `test_config.py`

3. **Update .env files:**
   - Copy `.env.example` to `.env`
   - Fill in actual values for your environment

## Security Best Practices

### ⚠️ CRITICAL SECURITY RULES

1. **NEVER commit actual .env files**
   - Always use `.env.example` as template
   - Add `.env` to `.gitignore`

2. **NEVER hardcode production credentials**
   - Use environment variables
   - Use secrets management in production

3. **NEVER use test passwords in production**
   - test_config.py passwords are for development ONLY
   - Use strong, unique passwords in production

4. **NEVER expose database URLs**
   - Push_users_to_railway.py now requires RAILWAY_DATABASE_URL env var
   - Script will fail if environment variable not set

5. **Use different credentials per environment**
   - Development: Use test_config defaults
   - Staging: Use staging-specific credentials
   - Production: Use strong, unique credentials

### Environment-Specific Settings

**Development:**
```bash
DEBUG=True
CORS_ALLOW_ALL_ORIGINS=True  # OK for local dev
TEST_ADMIN_PASSWORD=admin123  # OK for local dev
```

**Production:**
```bash
DEBUG=False
CORS_ALLOW_ALL_ORIGINS=False
CORS_ALLOWED_ORIGINS=https://your-frontend.com
# Never set TEST_* variables in production
```

## Testing

### Frontend Tests

```javascript
import { API_CONFIG } from '../config';

describe('API Configuration', () => {
  it('should have valid BASE_URL', () => {
    expect(API_CONFIG.BASE_URL).toBeDefined();
    expect(API_CONFIG.BASE_URL).toContain('/api');
  });
});
```

### Backend Tests

```python
from test_config import get_test_password

def test_password_configuration():
    """Test passwords come from environment"""
    password = get_test_password('admin')
    assert password is not None
    assert len(password) > 0
```

## Files Modified

### Frontend Files Updated
- `src/config/index.js` (NEW) - Centralized configuration
- `src/services/api.js` - Using API_CONFIG
- `src/services/auth.js` - Using API_CONFIG
- `src/services/admin.js` - Using API_CONFIG
- `src/services/cfc.js` - Using API_CONFIG
- `src/services/iipc.js` - Using API_CONFIG
- `src/components/NotificationBell.jsx` - Using API_CONFIG
- `src/pages/admin/assignments/StudentMentorAssignment.jsx` - Using API_CONFIG
- `src/pages/admin_1/assignments/StudentMentorAssignment.jsx` - Using API_CONFIG
- `src/pages/mentor/SubmissionReview.jsx` - Using API_CONFIG

### Backend Files Updated
- `backend/test_config.py` (NEW) - Test configuration
- `backend/config/settings.py` - Using environment variables for CORS
- `backend/create_superuser.py` - Using test_config
- `backend/import_dummy_users.py` - Using test_config
- `backend/import_dummy_users_floor2.py` - Using test_config
- `backend/import_students_final.py` - Using test_config
- `backend/import_students_book1.py` - Using test_config
- `backend/import_students_from_excel.py` - Using test_config
- `backend/create_mentor_tech_f2_m3.py` - Using test_config
- `backend/check_floorwing_user.py` - Using test_config
- `backend/call_setup_mentors.py` - Using test_config
- `backend/call_setup_floorwings.py` - Using test_config
- `backend/setup_floorwings_railway.py` - Using test_config
- `backend/set_floorwing_passwords.py` - Using test_config
- `backend/reset_mentor_passwords.py` - Using test_config
- `backend/test_iipc_endpoints.py` - Using test_config
- `backend/test_scd_endpoints.py` - Using test_config
- `backend/verify_mentors.py` - Using test_config
- `backend/import_users_simple.py` - Using test_config
- `backend/push_users_to_railway.py` - Now requires RAILWAY_DATABASE_URL env var

### Configuration Files
- `.env.example` (NEW) - Frontend environment template
- `backend/.env.example` (UPDATED) - Backend environment template with all new options

## Deployment Checklist

### Before Deployment

- [ ] Copy `.env.example` to `.env`
- [ ] Set all required environment variables
- [ ] Use strong, unique SECRET_KEY
- [ ] Set DEBUG=False
- [ ] Configure DATABASE_URL for production database
- [ ] Set CORS_ALLOWED_ORIGINS to actual frontend URL
- [ ] Remove or comment out TEST_* variables
- [ ] Set JWT_SECRET_KEY to strong random value
- [ ] Verify ALLOWED_HOSTS includes your domain

### After Deployment

- [ ] Test API connectivity from frontend
- [ ] Verify CORS is working correctly
- [ ] Test authentication flow
- [ ] Verify file uploads work
- [ ] Check that debug mode is disabled
- [ ] Monitor logs for configuration errors

## Support

For issues or questions about configuration:
1. Check `.env.example` files for available options
2. Review this documentation
3. Check `src/config/index.js` or `backend/test_config.py` for defaults
4. Ensure environment variables are properly set in deployment platform

## Changelog

### Version 1.0 (Current)
- Created centralized configuration system
- Eliminated 40+ hardcoded URLs
- Removed 20+ hardcoded passwords
- Secured database credentials
- Updated all test and setup scripts
- Created comprehensive .env.example files
- Added test_config.py with helper functions
- Updated CORS configuration to use environment variables
