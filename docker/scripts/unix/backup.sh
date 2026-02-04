#!/bin/bash
# ==============================================
# Database Backup Script for Docker
# ==============================================
# Usage: ./backup.sh [backup_name]

set -e

# Configuration
BACKUP_DIR="./backups"
COMPOSE_FILE="docker/compose/docker-compose.prod.yml"
DB_CONTAINER="cohort_db_prod"
DB_USER="cohort_user"
DB_NAME="cohort_db"
RETENTION_DAYS=30

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Generate backup filename
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME=${1:-"backup_${TIMESTAMP}"}
BACKUP_FILE="${BACKUP_DIR}/${BACKUP_NAME}.sql.gz"

echo "🔄 Starting database backup..."
echo "📦 Backup file: ${BACKUP_FILE}"

# Create backup
docker-compose -f "$COMPOSE_FILE" exec -T db pg_dump -U "$DB_USER" "$DB_NAME" | gzip > "$BACKUP_FILE"

if [ $? -eq 0 ]; then
    echo "✅ Backup completed successfully!"
    echo "📊 Backup size: $(du -h "$BACKUP_FILE" | cut -f1)"
else
    echo "❌ Backup failed!"
    exit 1
fi

# Remove old backups
echo "🧹 Removing backups older than ${RETENTION_DAYS} days..."
find "$BACKUP_DIR" -name "backup_*.sql.gz" -mtime +${RETENTION_DAYS} -delete

echo "📋 Current backups:"
ls -lh "$BACKUP_DIR"

echo "✨ Backup process completed!"
