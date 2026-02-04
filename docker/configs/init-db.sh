#!/bin/bash
# Database initialization script

set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    -- Create extensions
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    CREATE EXTENSION IF NOT EXISTS "pg_trgm";
    
    -- Set timezone
    SET timezone = 'UTC';
    
    -- Performance tuning
    ALTER DATABASE $POSTGRES_DB SET work_mem = '16MB';
    ALTER DATABASE $POSTGRES_DB SET maintenance_work_mem = '128MB';
    ALTER DATABASE $POSTGRES_DB SET effective_cache_size = '1GB';
    
    -- Create indexes after tables are created by Django migrations
    -- These will be created by Django, but we can optimize settings
    
    GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DB TO $POSTGRES_USER;
EOSQL

echo "Database initialization completed successfully"
