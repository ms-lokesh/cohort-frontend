# ==============================================
# Docker Deployment Guide
# ==============================================
# Comprehensive guide for deploying the Cohort Web Application with Docker

## Overview

This Docker setup provides:
- ✅ Production-ready containers for Django backend and React frontend
- ✅ PostgreSQL database with optimizations
- ✅ Redis cache for performance
- ✅ Nginx reverse proxy with load balancing
- ✅ Health checks and auto-restart
- ✅ Volume persistence for data
- ✅ Scalable architecture (can add more instances)

## Architecture

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
       ↓
┌─────────────────┐
│  Nginx (Port 80)│ ← Frontend (React SPA)
│  Load Balancer  │
└────────┬────────┘
         │
         ├─→ /api/* ─→ Backend (Django + Gunicorn)
         └─→ /*     ─→ React Static Files
                           │
                           ↓
                    ┌──────────────┐
                    │  PostgreSQL  │
                    │  Redis Cache │
                    └──────────────┘
```

## Prerequisites

- Docker 20.10+
- Docker Compose 2.0+
- 4GB+ RAM available
- 10GB+ disk space

## Quick Start

### Development Environment

```bash
# 1. Clone repository
git clone <repo-url>
cd cohort

# 2. Create environment file
cp backend/.env.example backend/.env

# 3. Update backend/.env with development settings
# DATABASE_URL will be set automatically by docker-compose

# 4. Build and start services
docker-compose -f docker/docker-compose.yml up --build

# 5. Access application
# Frontend: http://localhost
# Backend API: http://localhost:8000/api
# Admin: http://localhost:8000/admin
```

### Production Environment

```bash
# 1. Create production environment file
cp backend/.env.example backend/.env.production

# 2. Update .env.production with production values
# REQUIRED:
#   - SECRET_KEY (generate with: python -c "import secrets; print(secrets.token_urlsafe(50))")
#   - JWT_SECRET_KEY (generate similarly)
#   - POSTGRES_PASSWORD (strong password)
#   - REDIS_PASSWORD (strong password)
#   - ALLOWED_HOSTS (your domain)
#   - CORS_ALLOWED_ORIGINS (your frontend URL)

# 3. Build production images
docker-compose -f docker/docker-compose.prod.yml build

# 4. Start services
docker-compose -f docker/docker-compose.prod.yml up -d

# 5. Run migrations
docker-compose -f docker/docker-compose.prod.yml exec backend python manage.py migrate

# 6. Create superuser
docker-compose -f docker-compose.prod.yml exec backend python manage.py createsuperuser

# 7. Collect static files
docker-compose -f docker-compose.prod.yml exec backend python manage.py collectstatic --noinput
```

## Environment Variables

### Required for Production

#### Backend (.env)
```bash
# Django Core
SECRET_KEY=<50+ char random string>
DEBUG=False
DJANGO_ENV=production
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database (managed by docker-compose)
DATABASE_URL=postgresql://user:password@db:5432/dbname

# CORS
CORS_ALLOWED_ORIGINS=https://yourdomain.com

# JWT
JWT_SECRET_KEY=<32+ char random string>
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=60
JWT_REFRESH_TOKEN_LIFETIME_DAYS=7

# Redis
REDIS_URL=redis://:password@redis:6379/0
```

#### Docker Compose (.env in root)
```bash
# PostgreSQL
POSTGRES_DB=cohort_db
POSTGRES_USER=cohort_user
POSTGRES_PASSWORD=<strong-password>

# Redis
REDIS_PASSWORD=<strong-password>

# Backend
SECRET_KEY=<50+ char random string>
JWT_SECRET_KEY=<32+ char random string>
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CORS_ALLOWED_ORIGINS=https://yourdomain.com

# Frontend
VITE_API_URL=https://yourdomain.com/api
```

## Docker Commands

### Basic Operations

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Restart a service
docker-compose restart backend

# Execute command in container
docker-compose exec backend python manage.py shell
```

### Database Operations

```bash
# Run migrations
docker-compose exec backend python manage.py migrate

# Create superuser
docker-compose exec backend python manage.py createsuperuser

# Backup database
docker-compose exec db pg_dump -U cohort_user cohort_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore database
docker-compose exec -T db psql -U cohort_user cohort_db < backup.sql

# Access PostgreSQL shell
docker-compose exec db psql -U cohort_user -d cohort_db
```

### Scaling Operations

```bash
# Scale backend instances
docker-compose -f docker-compose.prod.yml up -d --scale backend=3

# View running containers
docker-compose ps

# Check resource usage
docker stats
```

### Maintenance

```bash
# Remove stopped containers
docker-compose down --remove-orphans

# Clean up unused images
docker image prune -a

# Clean up volumes (WARNING: deletes data)
docker volume prune

# Full cleanup (WARNING: deletes everything)
docker system prune -a --volumes
```

## Health Checks

All services have health checks configured:

```bash
# Check service health
docker-compose ps

# View health check logs
docker inspect --format='{{json .State.Health}}' cohort_backend_prod | jq
```

## Monitoring

### Container Stats

```bash
# Real-time stats
docker stats

# Specific container
docker stats cohort_backend_prod
```

### Logs

```bash
# All services
docker-compose logs -f --tail=100

# Backend only
docker-compose logs -f backend --tail=100

# Filter by time
docker-compose logs --since 1h backend
```

## Performance Tuning

### Backend Gunicorn Workers

Adjust in `backend/Dockerfile`:
```dockerfile
CMD ["gunicorn", "config.wsgi:application", \
    "--workers", "4",      # 2-4 × CPU cores
    "--threads", "2",      # 2-4 threads per worker
    "--timeout", "120"]    # Request timeout
```

### PostgreSQL Settings

Adjust in `docker-compose.prod.yml`:
```yaml
db:
  environment:
    - POSTGRES_SHARED_BUFFERS=256MB
    - POSTGRES_EFFECTIVE_CACHE_SIZE=1GB
    - POSTGRES_WORK_MEM=16MB
```

### Nginx Tuning

Adjust in `docker/nginx.conf`:
```nginx
worker_connections 2048;    # Concurrent connections
client_max_body_size 20M;   # Max upload size
keepalive_timeout 65;       # Keep-alive duration
```

## Security Best Practices

### 1. Use Strong Secrets

```bash
# Generate strong SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(50))"

# Generate JWT secret
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Generate database password
openssl rand -base64 32
```

### 2. Enable HTTPS

```bash
# Add SSL certificates to docker/ssl/
# - cert.pem
# - key.pem

# Update nginx configuration to use port 443
# Uncomment SSL directives in docker/nginx.conf
```

### 3. Limit Access

```yaml
# In docker-compose.prod.yml, don't expose database ports
db:
  # ports:
  #   - "5432:5432"  # Remove this in production
```

### 4. Regular Updates

```bash
# Update base images
docker-compose pull

# Rebuild with updated dependencies
docker-compose build --no-cache

# Apply security patches
docker-compose up -d
```

## Troubleshooting

### Backend won't start

```bash
# Check logs
docker-compose logs backend

# Common issues:
# 1. Database not ready - wait for db health check
# 2. Missing migrations - run: docker-compose exec backend python manage.py migrate
# 3. Wrong DATABASE_URL - check .env file
```

### Frontend shows API errors

```bash
# Check backend is running
curl http://localhost:8000/api/health/

# Check CORS settings
# Verify CORS_ALLOWED_ORIGINS includes your frontend URL

# Check nginx logs
docker-compose logs frontend
```

### Database connection issues

```bash
# Check database is running
docker-compose ps db

# Test connection
docker-compose exec backend python manage.py dbshell

# Reset database (WARNING: deletes data)
docker-compose down -v
docker-compose up -d
```

### High memory usage

```bash
# Check stats
docker stats

# Reduce Gunicorn workers
# Edit backend/Dockerfile: --workers 2

# Limit container memory
# Add to docker-compose.prod.yml:
deploy:
  resources:
    limits:
      memory: 512M
```

## Backup and Restore

### Database Backup

```bash
# Create backup directory
mkdir -p backups

# Automated backup script
docker-compose exec db pg_dump -U cohort_user cohort_db | gzip > backups/backup_$(date +%Y%m%d_%H%M%S).sql.gz

# Schedule with cron (Linux/Mac)
crontab -e
# Add: 0 2 * * * cd /path/to/cohort && ./backup.sh
```

### Volume Backup

```bash
# Backup all volumes
docker run --rm \
  -v cohort_postgres_prod:/data \
  -v $(pwd)/backups:/backup \
  alpine tar czf /backup/postgres_backup.tar.gz /data

# Restore volume
docker run --rm \
  -v cohort_postgres_prod:/data \
  -v $(pwd)/backups:/backup \
  alpine tar xzf /backup/postgres_backup.tar.gz -C /
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Build and Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Build images
        run: docker-compose -f docker-compose.prod.yml build
      
      - name: Push to registry
        run: |
          docker tag cohort_backend:latest registry.example.com/cohort_backend:latest
          docker push registry.example.com/cohort_backend:latest
      
      - name: Deploy to production
        run: |
          ssh user@server 'cd /app && docker-compose -f docker-compose.prod.yml pull'
          ssh user@server 'cd /app && docker-compose -f docker-compose.prod.yml up -d'
```

## Resources

- Docker Documentation: https://docs.docker.com/
- Docker Compose: https://docs.docker.com/compose/
- Nginx: https://nginx.org/en/docs/
- PostgreSQL: https://www.postgresql.org/docs/
- Gunicorn: https://docs.gunicorn.org/

## Support

For issues or questions:
1. Check logs: `docker-compose logs -f`
2. Verify health checks: `docker-compose ps`
3. Review configuration files
4. Check environment variables

---

**Last Updated:** January 29, 2026
**Docker Version:** 20.10+
**Compose Version:** 2.0+
