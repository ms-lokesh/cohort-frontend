#!/bin/bash
# Build script for Render deployment
# This script prepares the application for production deployment

set -e  # Exit on error

echo "======================================"
echo "Starting Render Build Process"
echo "======================================"

# 1. Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r backend/requirements.txt

# 2. Install Supabase Python client
echo "🔌 Installing Supabase client..."
pip install supabase

# 3. Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
npm install

# 4. Build frontend
echo "🏗️  Building React frontend..."
npm run build

# 5. Collect Django static files
echo "📦 Collecting Django static files..."
cd backend
python manage.py collectstatic --noinput

# 7. Run database migrations
echo "🗄️  Running database migrations..."
python manage.py migrate --noinput

# 8. Create cache tables (if using database cache)
echo "💾 Creating cache tables..."
python manage.py createcachetable || true

# 9. Health check
echo "✅ Build completed successfully!"
echo "======================================"
echo "Ready for deployment"
echo "======================================"

cd ..
