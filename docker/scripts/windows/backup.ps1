# ==============================================
# Database Backup Script for Docker (Windows)
# ==============================================
# Usage: .\backup.ps1 [backup_name]

param(
    [string]$BackupName = "backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
)

# Configuration
$BACKUP_DIR = ".\backups"
$COMPOSE_FILE = "docker\compose\docker-compose.prod.yml"
$DB_USER = "cohort_user"
$DB_NAME = "cohort_db"
$RETENTION_DAYS = 30

# Create backup directory if it doesn't exist
if (-not (Test-Path $BACKUP_DIR)) {
    New-Item -ItemType Directory -Path $BACKUP_DIR | Out-Null
}

$BACKUP_FILE = "$BACKUP_DIR\$BackupName.sql.gz"

Write-Host "🔄 Starting database backup..." -ForegroundColor Cyan
Write-Host "📦 Backup file: $BACKUP_FILE" -ForegroundColor Yellow

# Create backup
try {
    docker-compose -f $COMPOSE_FILE exec -T db pg_dump -U $DB_USER $DB_NAME | gzip > $BACKUP_FILE
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Backup completed successfully!" -ForegroundColor Green
        $size = (Get-Item $BACKUP_FILE).Length / 1MB
        Write-Host "📊 Backup size: $([math]::Round($size, 2)) MB" -ForegroundColor Cyan
    } else {
        Write-Host "❌ Backup failed!" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "❌ Error during backup: $_" -ForegroundColor Red
    exit 1
}

# Remove old backups
Write-Host "🧹 Removing backups older than $RETENTION_DAYS days..." -ForegroundColor Cyan
$cutoffDate = (Get-Date).AddDays(-$RETENTION_DAYS)
Get-ChildItem -Path $BACKUP_DIR -Filter "backup_*.sql.gz" | 
    Where-Object { $_.LastWriteTime -lt $cutoffDate } | 
    Remove-Item -Force

Write-Host "📋 Current backups:" -ForegroundColor Yellow
Get-ChildItem -Path $BACKUP_DIR -Filter "*.sql.gz" | 
    Format-Table Name, @{Label="Size (MB)"; Expression={[math]::Round($_.Length/1MB, 2)}}, LastWriteTime

Write-Host "✨ Backup process completed!" -ForegroundColor Green
