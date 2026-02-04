# Configuration Tools

This directory contains tools to help manage and validate the centralized configuration system.

## Tools Overview

### 1. Environment Validation (`backend/validate_env.py`)

Validates that all required environment variables are properly set.

**Usage:**
```bash
# Validate development environment
python backend/validate_env.py

# Validate production environment
python backend/validate_env.py --env production

# Validate with strict mode (fail on warnings)
python backend/validate_env.py --env production --strict
```

**What it checks:**
- ✅ Required variables are set
- ✅ Recommended variables are present
- ✅ No dangerous/default values in production
- ✅ SECRET_KEY is strong enough
- ✅ DEBUG is False in production
- ✅ No test passwords in production
- ✅ DATABASE_URL doesn't contain localhost

**Example output:**
```
============================================================
Environment Variables Validation - PRODUCTION
============================================================

ERRORS:
------------------------------------------------------------
❌ REQUIRED: SECRET_KEY is not set
❌ SECURITY: DEBUG must be False in production

SUMMARY:
------------------------------------------------------------
Errors:   2
Warnings: 0
Checks:   5

❌ VALIDATION FAILED
```

### 2. Configuration Tests (`backend/tests/test_configuration.py`)

Unit tests for the configuration system.

**Usage:**
```bash
# Run all configuration tests
python backend/tests/test_configuration.py

# Or with pytest
pytest backend/tests/test_configuration.py -v
```

**What it tests:**
- ✅ `get_test_password()` returns values
- ✅ `get_test_email()` generates correct emails
- ✅ `get_test_user_data()` creates complete user data
- ✅ `validate_railway_db()` works correctly
- ✅ Environment variables override defaults
- ✅ Production warning is shown
- ✅ Passwords are not empty

**Example output:**
```
test_custom_admin_password ... ok
test_get_test_email ... ok
test_get_test_password_returns_value ... ok
test_passwords_not_empty ... ok
test_validate_railway_db_with_env ... ok

----------------------------------------------------------------------
Ran 12 tests in 0.234s

OK
```

### 3. Pre-commit Hook (`.githooks/pre-commit`)

Git hook that prevents committing hardcoded values.

**Installation:**
```bash
# Make executable
chmod +x .githooks/pre-commit

# Configure git to use custom hooks directory
git config core.hooksPath .githooks

# Verify installation
git config core.hooksPath
```

**What it checks:**
- 🚫 Hardcoded URLs (`http://localhost:8000`)
- 🚫 Hardcoded passwords (`admin123`, `pass123#`, etc.)
- 🚫 Hardcoded database credentials
- 🚫 Exposed secret keys
- 🚫 `.env` files being committed

**Example output:**
```
🔍 Checking for hardcoded values...
Checking 5 files...

📡 Checking for hardcoded URLs...
🔐 Checking for hardcoded passwords...
🗄️  Checking for hardcoded database credentials...
🔑 Checking for exposed secret keys...
📄 Checking for .env files...

============================================================
✅ No hardcoded values detected - commit allowed
```

**Bypass (use sparingly):**
```bash
git commit --no-verify
```

### 4. Environment Setup Helper (`setup_env.py`)

Interactive script to create `.env` files with proper values.

**Usage:**
```bash
# Interactive setup for both frontend and backend
python setup_env.py

# Setup for production
python setup_env.py --env production

# Setup frontend only
python setup_env.py --frontend

# Setup backend only
python setup_env.py --backend
```

**What it does:**
- ✅ Generates strong SECRET_KEY and JWT_SECRET_KEY
- ✅ Creates `.env` from templates
- ✅ Prompts for environment-specific values
- ✅ Sets appropriate defaults for development/production
- ✅ Includes only safe values for each environment

**Example interaction:**
```
============================================================
Environment Setup - PRODUCTION
============================================================

📦 Setting up Frontend Environment
------------------------------------------------------------

Backend API URL (e.g., https://api.yourapp.com/api): https://api.myapp.com/api
Frontend URL (e.g., https://yourapp.com): https://myapp.com
✅ Created .env
   API URL: https://api.myapp.com/api
   App URL: https://myapp.com

🔧 Setting up Backend Environment
------------------------------------------------------------

Database URL (leave empty to skip): postgresql://user:pass@host:5432/db
Allowed hosts (comma-separated): .myapp.com
CORS allowed origins (comma-separated): https://myapp.com
✅ Created backend/.env
   SECRET_KEY: xK9m2nV... (generated)
   JWT_SECRET_KEY: pL8h3dW... (generated)
   DEBUG: False
   DATABASE_URL: postgresql://user:pass@hos...

============================================================
✅ Setup Complete!
============================================================

Next steps:
1. Review the generated .env files
2. Update any placeholder values
3. Never commit .env files to git
4. Run 'python backend/validate_env.py' to verify
```

## Workflow

### Initial Setup (New Developer)

```bash
# 1. Clone repository
git clone <repo-url>
cd cohort

# 2. Run setup helper
python setup_env.py

# 3. Validate environment
python backend/validate_env.py

# 4. Install pre-commit hook
chmod +x .githooks/pre-commit
git config core.hooksPath .githooks

# 5. Run tests
python backend/tests/test_configuration.py
```

### Before Deployment

```bash
# 1. Create production environment
python setup_env.py --env production

# 2. Update values in .env files
# (DATABASE_URL, CORS_ALLOWED_ORIGINS, etc.)

# 3. Validate production config
python backend/validate_env.py --env production --strict

# 4. Fix any errors/warnings

# 5. Deploy!
```

### Daily Development

```bash
# Pre-commit hook runs automatically
git add .
git commit -m "Add feature"

# If hook fails:
# - Fix the hardcoded values
# - Or bypass with --no-verify (not recommended)
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Configuration Validation

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      
      - name: Validate Development Config
        run: python backend/validate_env.py --env development
      
      - name: Run Configuration Tests
        run: python backend/tests/test_configuration.py
      
      - name: Check for Hardcoded Values
        run: |
          chmod +x .githooks/pre-commit
          .githooks/pre-commit
```

### GitLab CI Example

```yaml
validate_config:
  script:
    - python backend/validate_env.py --env production --strict
    - python backend/tests/test_configuration.py
    - chmod +x .githooks/pre-commit && .githooks/pre-commit
  only:
    - merge_requests
    - main
```

## Troubleshooting

### "SECRET_KEY too short" error

```bash
# Generate a new strong key
python -c "import secrets; print(secrets.token_urlsafe(50))"

# Add to backend/.env
SECRET_KEY=<generated-key>
```

### "RAILWAY_DATABASE_URL not set" in tests

This is expected - Railway DB URL should only be set when running migration scripts:

```bash
export RAILWAY_DATABASE_URL='postgresql://...'
python backend/push_users_to_railway.py
```

### Pre-commit hook not working

```bash
# Check git config
git config core.hooksPath

# Should output: .githooks

# If not set:
git config core.hooksPath .githooks

# Make executable
chmod +x .githooks/pre-commit
```

### Tests failing on import

```bash
# Make sure you're in the project root
cd C:\Python310\cohort_webapp\cohort

# Run with proper path
python backend/tests/test_configuration.py
```

## File Locations

```
cohort/
├── setup_env.py                           # Environment setup helper
├── .githooks/
│   └── pre-commit                         # Pre-commit hook
└── backend/
    ├── validate_env.py                    # Environment validator
    ├── test_config.py                     # Test configuration
    └── tests/
        └── test_configuration.py          # Configuration tests
```

## Related Documentation

- [CONFIG_QUICK_REFERENCE.md](CONFIG_QUICK_REFERENCE.md) - Quick reference for developers
- [CONFIGURATION_SYSTEM.md](CONFIGURATION_SYSTEM.md) - Complete configuration guide
- [HARDCODED_VALUES_ELIMINATION_REPORT.md](HARDCODED_VALUES_ELIMINATION_REPORT.md) - Technical report
- [.env.example](.env.example) - Frontend environment template
- [backend/.env.example](backend/.env.example) - Backend environment template

## Support

For issues or questions:
1. Check the error message and fix accordingly
2. Review the relevant documentation
3. Run validation with verbose output
4. Check .env.example files for expected values

## Contributing

When adding new environment variables:
1. Add to appropriate `.env.example` file
2. Update `validate_env.py` checks if required
3. Add tests to `test_configuration.py`
4. Update documentation
5. Update pre-commit hook if needed
