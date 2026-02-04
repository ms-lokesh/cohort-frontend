# ==============================================
# Production Deployment Script (Windows)
# ==============================================
# Usage: .\deploy.ps1

# Configuration
$COMPOSE_FILE = "docker\compose\docker-compose.prod.yml"
$BACKUP_DIR = ".\backups"

Write-Host "🚀 Starting production deployment..." -ForegroundColor Cyan

# Check if .env exists
if (-not (Test-Path .env)) {
    Write-Host "❌ Error: .env file not found" -ForegroundColor Red
    Write-Host "Please copy .env.example to .env and configure it" -ForegroundColor Yellow
    exit 1
}

# Create backup directory
if (-not (Test-Path $BACKUP_DIR)) {
    New-Item -ItemType Directory -Path $BACKUP_DIR | Out-Null
}

# Backup database before deployment
Write-Host "📦 Creating pre-deployment backup..." -ForegroundColor Yellow
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$BACKUP_FILE = "$BACKUP_DIR\pre_deploy_$timestamp.sql.gz"
docker-compose -f $COMPOSE_FILE exec -T db pg_dump -U cohort_user cohort_db 2>$null | gzip > $BACKUP_FILE
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  No existing database to backup" -ForegroundColor Yellow
}

# Pull latest changes
Write-Host "📥 Pulling latest code..." -ForegroundColor Cyan
git pull origin main

# Build new images
Write-Host "🏗️  Building Docker images..." -ForegroundColor Cyan
docker-compose -f $COMPOSE_FILE build --no-cache

# Stop services
Write-Host "⏸️  Stopping services..." -ForegroundColor Yellow
docker-compose -f $COMPOSE_FILE down

# Start database first
Write-Host "🗄️  Starting database..." -ForegroundColor Cyan
docker-compose -f $COMPOSE_FILE up -d db redis

# Wait for database to be ready
Write-Host "⏳ Waiting for database..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Run migrations
Write-Host "🔄 Running database migrations..." -ForegroundColor Cyan
docker-compose -f $COMPOSE_FILE run --rm backend python manage.py migrate

# Collect static files
Write-Host "📂 Collecting static files..." -ForegroundColor Cyan
docker-compose -f $COMPOSE_FILE run --rm backend python manage.py collectstatic --noinput

# Start all services
Write-Host "▶️  Starting all services..." -ForegroundColor Green
docker-compose -f $COMPOSE_FILE up -d

# Wait for services to be healthy
Write-Host "⏳ Waiting for services to be healthy..." -ForegroundColor Yellow
Start-Sleep -Seconds 15

# Check health
Write-Host "🏥 Checking service health..." -ForegroundColor Cyan
docker-compose -f $COMPOSE_FILE ps

# Show logs
Write-Host "📋 Recent logs:" -ForegroundColor Yellow
docker-compose -f $COMPOSE_FILE logs --tail=20

Write-Host ""
Write-Host "✅ Deployment completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Your application should be running at:" -ForegroundColor Cyan
Write-Host "   Frontend: http://localhost" -ForegroundColor White
Write-Host "   Backend API: http://localhost:8000/api" -ForegroundColor White
Write-Host "   Admin: http://localhost:8000/admin" -ForegroundColor White
Write-Host ""
Write-Host "📊 To view logs: docker-compose -f $COMPOSE_FILE logs -f" -ForegroundColor Yellow
Write-Host "📈 To view stats: docker stats" -ForegroundColor Yellow
