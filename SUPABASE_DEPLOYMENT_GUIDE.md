# Supabase Database Deployment Guide

This guide walks you through migrating from Render DB to Supabase PostgreSQL while maintaining the exact table schema.

## 📋 Overview

- **Database Provider**: Supabase (PostgreSQL 15+)
- **Schema Preservation**: All existing tables and relationships maintained
- **Migration Method**: Direct database migration using pg_dump/pg_restore or Django migrations
- **Zero Downtime**: Can be achieved with proper planning

---

## 🚀 Quick Start

### Step 1: Create Supabase Project

1. Go to [https://supabase.com](https://supabase.com) and sign in/up
2. Click **"New Project"**
3. Fill in project details:
   - **Name**: `cohort-production` (or your preferred name)
   - **Database Password**: Generate a strong password (save this!)
   - **Region**: Choose closest to your users
   - **Pricing Plan**: Free tier works for development
4. Click **"Create new project"**
5. Wait 2-3 minutes for provisioning

### Step 2: Get Database Connection String

1. In your Supabase project, go to **Settings** → **Database**
2. Under **Connection string**, select **URI** format
3. You'll see something like:
   ```
   postgresql://postgres.[project-ref]:[YOUR-PASSWORD]@aws-0-[region].pooler.supabase.com:6543/postgres
   ```
4. **Replace `[YOUR-PASSWORD]`** with your actual database password
5. Copy this complete string

### Step 3: Configure Django Application

#### Update Environment Variables

Create or update `.env` file in `backend/` directory:

```env
# Production Database (Supabase)
DATABASE_URL=postgresql://postgres.[project-ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres

# Django Settings
DEBUG=False
SECRET_KEY=your-generated-secret-key-here
ALLOWED_HOSTS=.vercel.app,.railway.app,.render.com,yourdomain.com

# CORS for Frontend
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.vercel.app

# JWT Settings
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=60
JWT_REFRESH_TOKEN_LIFETIME_DAYS=7
```

**Important Notes:**
- Never commit `.env` file to Git
- Use different secrets for production
- Update `ALLOWED_HOSTS` with your actual domains
- Update `CORS_ALLOWED_ORIGINS` with your frontend URL

### Step 4: Test Database Connection Locally

```bash
cd backend
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Test connection
python3 manage.py check --database default

# Should output: System check identified no issues (0 silenced).
```

### Step 5: Run Migrations

```bash
# Create all tables in Supabase
python3 manage.py migrate

# Verify migrations
python3 manage.py showmigrations

# Create superuser
python3 manage.py createsuperuser
```

### Step 6: Test Application

```bash
# Run development server
python3 manage.py runserver

# Test API endpoints
curl http://localhost:8000/api/auth/token/ -X POST \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass"}'
```

---

## 🔄 Migration from Existing Database

### Option A: Using Django Migrations (Recommended)

This creates a fresh database with the exact same schema:

```bash
# 1. Backup your current data (if needed)
python3 manage.py dumpdata --natural-foreign --natural-primary \
  --exclude contenttypes --exclude auth.permission \
  --indent 2 > backup_data.json

# 2. Update DATABASE_URL to Supabase
export DATABASE_URL="postgresql://postgres.[ref]:[pass]@aws-0-[region].pooler.supabase.com:6543/postgres"

# 3. Run migrations (creates all tables)
python3 manage.py migrate

# 4. Load data (if you backed up)
python3 manage.py loaddata backup_data.json

# 5. Verify data
python3 manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.count()
```

### Option B: Direct Database Copy (pg_dump)

For large databases with lots of data:

```bash
# 1. Export from old database
pg_dump $OLD_DATABASE_URL -Fc -f cohort_backup.dump

# 2. Import to Supabase
pg_restore --no-owner --no-acl -d $SUPABASE_DATABASE_URL cohort_backup.dump

# 3. Verify tables
psql $SUPABASE_DATABASE_URL -c "\dt"
```

### Option C: Using Supabase Dashboard

1. Go to **Database** → **Replication**
2. Click **"Create a new replication"**
3. Connect to your old database
4. Select tables to replicate
5. Start replication process

---

## 🚢 Deployment Configuration

### For Railway.app

Update `railway.json`:
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "pip install -r requirements.txt"
  },
  "deploy": {
    "startCommand": "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

**Environment Variables in Railway:**
```
DATABASE_URL=<your-supabase-connection-string>
SECRET_KEY=<generated-secret>
DEBUG=False
ALLOWED_HOSTS=.railway.app
CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app
```

### For Render.com

Update `render.yaml` (already updated in your project):
```yaml
services:
  - type: web
    name: cohort-backend
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: python manage.py migrate && gunicorn config.wsgi:application
    envVars:
      - key: DATABASE_URL
        sync: false  # Set manually in Render dashboard
```

**In Render Dashboard:**
1. Go to your service → Environment
2. Add `DATABASE_URL` with your Supabase connection string

### For Vercel

Create `vercel.json`:
```json
{
  "builds": [
    {
      "src": "backend/config/wsgi.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "backend/config/wsgi.py"
    }
  ],
  "env": {
    "DATABASE_URL": "@database_url"
  }
}
```

Add secrets via Vercel CLI:
```bash
vercel env add DATABASE_URL production
# Paste your Supabase connection string
```

---

## 🔒 Security Best Practices

### 1. Connection Pooling

Supabase uses PgBouncer for connection pooling. Use port **6543** for pooled connections:
```
postgresql://postgres.[ref]:[pass]@aws-0-[region].pooler.supabase.com:6543/postgres
```

For direct connections (migrations only), use port **5432**:
```
postgresql://postgres.[ref]:[pass]@db.[ref].supabase.co:5432/postgres
```

### 2. SSL Requirements

Update Django settings (already configured in settings.py):
```python
DATABASES['default']['OPTIONS'] = {
    'sslmode': 'require',
    'connect_timeout': 10,
}
```

### 3. Environment Variables

Never hardcode database credentials:
```python
# ✅ Good
DATABASE_URL = os.getenv('DATABASE_URL')

# ❌ Bad
DATABASE_URL = 'postgresql://user:pass@host:5432/db'
```

### 4. Row Level Security (RLS)

Enable RLS in Supabase for additional security:
```sql
-- In Supabase SQL Editor
ALTER TABLE your_table ENABLE ROW LEVEL SECURITY;

-- Create policies as needed
CREATE POLICY "Users can view own data" ON your_table
  FOR SELECT USING (auth.uid() = user_id);
```

---

## 📊 Database Management

### Supabase Dashboard Features

1. **SQL Editor**: Run queries directly
2. **Table Editor**: GUI for data management
3. **Database Backups**: Automatic daily backups (paid plans)
4. **Logs**: Real-time database logs
5. **API**: Auto-generated REST & GraphQL APIs

### Useful SQL Queries

```sql
-- Check database size
SELECT pg_size_pretty(pg_database_size('postgres'));

-- List all tables
SELECT tablename FROM pg_tables WHERE schemaname = 'public';

-- Check table sizes
SELECT 
  schemaname,
  tablename,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- View active connections
SELECT count(*) FROM pg_stat_activity;
```

### Django Management Commands

```bash
# Check migrations status
python3 manage.py showmigrations

# Create new migration
python3 manage.py makemigrations

# Apply migrations
python3 manage.py migrate

# Rollback migration
python3 manage.py migrate app_name 0001_previous_migration

# Reset database (careful!)
python3 manage.py flush

# Create superuser
python3 manage.py createsuperuser

# Collect static files
python3 manage.py collectstatic --noinput
```

---

## 🧪 Testing

### Local Testing with Supabase

```bash
# Set environment variable
export DATABASE_URL="your-supabase-url"

# Run tests
python3 manage.py test

# Run specific test
python3 manage.py test apps.clt.tests

# Check database connection
python3 manage.py dbshell
```

### Integration Tests

Create `backend/test_supabase_connection.py`:
```python
import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

def test_connection():
    """Test Supabase connection"""
    try:
        conn = psycopg.connect(os.getenv('DATABASE_URL'))
        print("✅ Connection successful!")
        
        cur = conn.cursor()
        cur.execute("SELECT version();")
        print(f"PostgreSQL version: {cur.fetchone()[0]}")
        
        cur.execute("SELECT current_database();")
        print(f"Database: {cur.fetchone()[0]}")
        
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    test_connection()
```

Run test:
```bash
python3 test_supabase_connection.py
```

---

## 🐛 Troubleshooting

### Connection Issues

**Error: "connection refused"**
- Check if DATABASE_URL is correct
- Verify Supabase project is not paused
- Check your IP is not blocked

**Error: "password authentication failed"**
- Verify password in connection string
- Check for special characters (URL encode them)
- Reset database password in Supabase dashboard

**Error: "too many connections"**
- Use pooled connection (port 6543)
- Reduce CONN_MAX_AGE in settings.py
- Upgrade Supabase plan for more connections

### SSL Issues

**Error: "SSL connection required"**
```python
# Update settings.py
DATABASES['default']['OPTIONS'] = {
    'sslmode': 'require',
}
```

### Migration Issues

**Error: "relation already exists"**
```bash
# Reset migrations (careful - deletes data!)
python3 manage.py migrate --fake-initial

# Or migrate app by app
python3 manage.py migrate app_name
```

**Error: "migration conflicts"**
```bash
# Show migration tree
python3 manage.py showmigrations

# Merge migrations
python3 manage.py makemigrations --merge
```

---

## 📈 Performance Optimization

### 1. Connection Pooling

Always use pooled connections in production:
```
postgresql://...@aws-0-region.pooler.supabase.com:6543/postgres
                                              ^^^^
```

### 2. Database Indexes

Add indexes for frequently queried fields:
```python
# In your models.py
class Student(models.Model):
    email = models.EmailField(unique=True, db_index=True)
    roll_number = models.CharField(max_length=20, db_index=True)
```

### 3. Query Optimization

```python
# Use select_related for foreign keys
students = Student.objects.select_related('mentor').all()

# Use prefetch_related for many-to-many
students = Student.objects.prefetch_related('submissions').all()

# Use only() to fetch specific fields
students = Student.objects.only('id', 'name', 'email')
```

### 4. Caching

Enable Redis caching:
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': os.getenv('REDIS_URL', 'redis://localhost:6379/1'),
    }
}
```

---

## 🔄 Backup Strategy

### Automatic Backups (Supabase)

- **Free Plan**: Daily backups, 7-day retention
- **Pro Plan**: Daily backups, 14-day retention + point-in-time recovery
- **Enterprise**: Custom retention policies

### Manual Backups

```bash
# Backup entire database
pg_dump $DATABASE_URL -Fc -f backup_$(date +%Y%m%d).dump

# Backup specific tables
pg_dump $DATABASE_URL -Fc -t auth_user -t profiles_student -f users_backup.dump

# Backup schema only
pg_dump $DATABASE_URL -Fc --schema-only -f schema_backup.dump

# Backup data only
pg_dump $DATABASE_URL -Fc --data-only -f data_backup.dump
```

### Restore from Backup

```bash
# Restore entire database
pg_restore --clean --no-owner --no-acl -d $DATABASE_URL backup.dump

# Restore specific tables
pg_restore --clean --no-owner --no-acl -d $DATABASE_URL -t auth_user backup.dump
```

---

## 📚 Additional Resources

- **Supabase Docs**: https://supabase.com/docs/guides/database
- **Django Database Docs**: https://docs.djangoproject.com/en/4.2/ref/databases/
- **PostgreSQL Docs**: https://www.postgresql.org/docs/
- **psycopg3 Docs**: https://www.psycopg.org/psycopg3/docs/

---

## ✅ Deployment Checklist

- [ ] Supabase project created
- [ ] Database connection string obtained
- [ ] Environment variables configured
- [ ] Local connection tested
- [ ] Migrations applied successfully
- [ ] Superuser created
- [ ] Data migrated (if applicable)
- [ ] SSL configuration verified
- [ ] Connection pooling enabled
- [ ] Production settings updated
- [ ] Deployment platform configured
- [ ] Application deployed and tested
- [ ] Backup strategy implemented
- [ ] Monitoring enabled

---

## 🆘 Support

If you encounter issues:

1. Check Supabase status: https://status.supabase.com
2. Review Django logs: `python3 manage.py runserver --verbosity 3`
3. Check Supabase logs in dashboard
4. Test connection with `psql` directly
5. Contact Supabase support (for paid plans)

---

**Last Updated**: January 2026  
**Database**: Supabase PostgreSQL 15+  
**Django Version**: 4.2.7  
**Python Version**: 3.10+
