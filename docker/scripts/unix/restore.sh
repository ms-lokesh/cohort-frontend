#!/bin/bash
# ==============================================
# Database Restore Script for Docker
# ==============================================
# Usage: ./restore.sh backup_file.sql.gz

set -e

# Configuration
COMPOSE_FILE="docker/compose/docker-compose.prod.yml"
DB_CONTAINER="cohort_db_prod"
DB_USER="cohort_user"
DB_NAME="cohort_db"

# Check if backup file provided
if [ -z "$1" ]; then
    echo "❌ Error: No backup file specified"
    echo "Usage: ./restore.sh backup_file.sql.gz"
    echo ""
    echo "Available backups:"
    ls -lh ./backups/
    exit 1
fi

BACKUP_FILE=$1

# Check if backup file exists
if [ ! -f "$BACKUP_FILE" ]; then
    echo "❌ Error: Backup file not found: $BACKUP_FILE"
    exit 1
fi

echo "⚠️  WARNING: This will replace the current database!"
echo "📦 Backup file: ${BACKUP_FILE}"
echo "🗄️  Database: ${DB_NAME}"
read -p "Are you sure you want to continue? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "❌ Restore cancelled"
    exit 0
fi

echo "🔄 Starting database restore..."

# Stop backend to prevent connections
echo "⏸️  Stopping backend services..."
docker-compose -f "$COMPOSE_FILE" stop backend

# Drop and recreate database
echo "🗑️  Dropping existing database..."
docker-compose -f "$COMPOSE_FILE" exec -T db psql -U "$DB_USER" -d postgres <<-EOSQL
    SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '${DB_NAME}';
    DROP DATABASE IF EXISTS ${DB_NAME};
    CREATE DATABASE ${DB_NAME};
    GRANT ALL PRIVILEGES ON DATABASE ${DB_NAME} TO ${DB_USER};
EOSQL

# Restore backup
echo "📥 Restoring backup..."
gunzip -c "$BACKUP_FILE" | docker-compose -f "$COMPOSE_FILE" exec -T db psql -U "$DB_USER" -d "$DB_NAME"

if [ $? -eq 0 ]; then
    echo "✅ Restore completed successfully!"
else
    echo "❌ Restore failed!"
    exit 1
fi

# Start backend
echo "▶️  Starting backend services..."
docker-compose -f "$COMPOSE_FILE" start backend

echo "✨ Restore process completed!"
echo "🔍 Verify the restore with: docker-compose -f $COMPOSE_FILE exec backend python manage.py showmigrations"
