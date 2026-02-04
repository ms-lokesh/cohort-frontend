# Configuration Quick Reference

Quick guide for using the new centralized configuration system.

## For Frontend Developers

### Import Configuration
```javascript
import { API_CONFIG, UPLOAD_CONFIG, TIMEOUT_CONFIG } from '../config';
```

### Common Use Cases

**API Calls:**
```javascript
// ✅ DO THIS
fetch(`${API_CONFIG.BASE_URL}/users/`)

// ❌ NOT THIS
fetch('http://localhost:8000/api/users/')
```

**File Upload Checks:**
```javascript
// ✅ DO THIS
if (file.size > UPLOAD_CONFIG.MAX_FILE_SIZE) {
  alert(`Max size: ${UPLOAD_CONFIG.MAX_FILE_SIZE_MB}MB`);
}

// ❌ NOT THIS
if (file.size > 10485760) {
  alert('File too large');
}
```

**Timeouts:**
```javascript
// ✅ DO THIS
axios.create({ timeout: API_CONFIG.TIMEOUT })

// ❌ NOT THIS
axios.create({ timeout: 30000 })
```

### Available Configs

- `API_CONFIG` - API URLs, timeouts, retry settings
- `FRONTEND_CONFIG` - App name, URLs, pagination
- `OAUTH_CONFIG` - Google/LinkedIn client IDs
- `UPLOAD_CONFIG` - File size limits, allowed types
- `TIMEOUT_CONFIG` - Various timeout values
- `PAGINATION_CONFIG` - Page size settings
- `DEBUG_CONFIG` - Debug flags
- `CACHE_CONFIG` - Caching settings

## For Backend Developers

### Import Test Config
```python
from test_config import get_test_password, get_test_email, get_test_user_data
```

### Common Use Cases

**Creating Test Users:**
```python
# ✅ DO THIS
from test_config import get_test_password

user = User.objects.create_user(
    username='testuser',
    password=get_test_password('student')
)

# ❌ NOT THIS
user = User.objects.create_user(
    username='testuser',
    password='pass123#'
)
```

**Generating Test Emails:**
```python
# ✅ DO THIS
from test_config import get_test_email

email = get_test_email('student1')  # student1@test.cohort.com

# ❌ NOT THIS
email = 'student1@test.com'
```

**Railway Database Access:**
```python
# ✅ DO THIS
from test_config import validate_railway_db, RAILWAY_DB_URL

if not validate_railway_db():
    sys.exit(1)
    
conn = psycopg.connect(RAILWAY_DB_URL)

# ❌ NOT THIS
conn = psycopg.connect('postgresql://user:pass@host:port/db')
```

### Available Functions

- `get_test_password(user_type)` - Get test password
- `get_test_email(username, domain)` - Generate test email
- `validate_railway_db()` - Check Railway DB URL is set
- `get_test_user_data(user_type, index)` - Get complete user data dict

## Environment Variables

### Required for Development

**Frontend (.env):**
```bash
VITE_API_URL=http://localhost:8000/api
```

**Backend (.env):**
```bash
# Optional - uses SQLite if not set
DATABASE_URL=postgresql://user:pass@localhost/dbname
```

### Required for Production

**Frontend (.env):**
```bash
VITE_API_URL=https://your-backend.railway.app/api
VITE_APP_URL=https://your-frontend.vercel.app
```

**Backend (.env):**
```bash
SECRET_KEY=<strong-random-key>
DEBUG=False
DATABASE_URL=<provided-by-platform>
CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app
JWT_SECRET_KEY=<strong-random-key>
```

## Testing Changes

### Test Frontend Config
```bash
# Start dev server
npm run dev

# Check console for API_CONFIG values
# Should use http://localhost:8000/api by default
```

### Test Backend Config
```bash
# Start Django server
python manage.py runserver

# Create test user
python backend/create_superuser.py

# Should use admin123 password (from test_config)
```

## Common Errors

### "Cannot find module '../config'"
- **Fix:** Check import path - should be relative to current file
- **Example:** `import { API_CONFIG } from '../config';`

### "Module 'test_config' not found"
- **Fix:** Add sys.path.insert or run from correct directory
- **Example:** `sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))`

### "RAILWAY_DATABASE_URL environment variable not set"
- **Fix:** Set environment variable before running script
- **Example:** `export RAILWAY_DATABASE_URL='postgresql://...'`

### "API calls returning 404"
- **Fix:** Check VITE_API_URL includes /api suffix
- **Correct:** `http://localhost:8000/api`
- **Wrong:** `http://localhost:8000`

## Quick Links

- Full Documentation: [CONFIGURATION_SYSTEM.md](CONFIGURATION_SYSTEM.md)
- Frontend Config: [src/config/index.js](src/config/index.js)
- Backend Config: [backend/test_config.py](backend/test_config.py)
- Frontend .env Template: [.env.example](.env.example)
- Backend .env Template: [backend/.env.example](backend/.env.example)
- Elimination Report: [HARDCODED_VALUES_ELIMINATION_REPORT.md](HARDCODED_VALUES_ELIMINATION_REPORT.md)

## Need Help?

1. Check [CONFIGURATION_SYSTEM.md](CONFIGURATION_SYSTEM.md) for detailed examples
2. Look at existing service files for patterns
3. Review .env.example files for available options
4. Check console/logs for configuration errors

---

**Last Updated:** 2024
**Maintained By:** Development Team
