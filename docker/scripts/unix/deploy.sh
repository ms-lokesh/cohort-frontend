#!/bin/bash
# ==============================================
# Production Deployment Script
# ==============================================
# Usage: ./deploy.sh

set -e

echo "🚀 Starting production deployment..."

# Configuration
COMPOSE_FILE="docker/compose/docker-compose.prod.yml"
BACKUP_DIR="./backups"

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found"
    echo "Please copy .env.example to .env and configure it"
    exit 1
fi

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Backup database before deployment
echo "📦 Creating pre-deployment backup..."
BACKUP_FILE="${BACKUP_DIR}/pre_deploy_$(date +%Y%m%d_%H%M%S).sql.gz"
docker-compose -f "$COMPOSE_FILE" exec -T db pg_dump -U cohort_user cohort_db | gzip > "$BACKUP_FILE" 2>/dev/null || echo "⚠️  No existing database to backup"

# Pull latest changes
echo "📥 Pulling latest code..."
git pull origin main

# Build new images
echo "🏗️  Building Docker images..."
docker-compose -f "$COMPOSE_FILE" build --no-cache

# Stop services
echo "⏸️  Stopping services..."
docker-compose -f "$COMPOSE_FILE" down

# Start database first
echo "🗄️  Starting database..."
docker-compose -f "$COMPOSE_FILE" up -d db redis

# Wait for database to be ready
echo "⏳ Waiting for database..."
sleep 10

# Run migrations
echo "🔄 Running database migrations..."
docker-compose -f "$COMPOSE_FILE" run --rm backend python manage.py migrate

# Collect static files
echo "📂 Collecting static files..."
docker-compose -f "$COMPOSE_FILE" run --rm backend python manage.py collectstatic --noinput

# Start all services
echo "▶️  Starting all services..."
docker-compose -f "$COMPOSE_FILE" up -d

# Wait for services to be healthy
echo "⏳ Waiting for services to be healthy..."
sleep 15

# Check health
echo "🏥 Checking service health..."
docker-compose -f "$COMPOSE_FILE" ps

# Show logs
echo "📋 Recent logs:"
docker-compose -f "$COMPOSE_FILE" logs --tail=20

echo "✅ Deployment completed successfully!"
echo ""
echo "🌐 Your application should be running at:"
echo "   Frontend: http://localhost"
echo "   Backend API: http://localhost:8000/api"
echo "   Admin: http://localhost:8000/admin"
echo ""
echo "📊 To view logs: docker-compose -f $COMPOSE_FILE logs -f"
echo "📈 To view stats: docker stats"
