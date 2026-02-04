#!/bin/bash
# Start script for Render deployment
# Serves both frontend and backend on a single web service

set -e  # Exit on error

echo "======================================"
echo "Starting Cohort Web Application"
echo "======================================"

# Change to backend directory
cd backend

# Start Gunicorn WSGI server
echo "🚀 Starting Gunicorn server..."
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers ${WEB_CONCURRENCY:-2} \
    --timeout ${GUNICORN_TIMEOUT:-120} \
    --worker-class sync \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    --capture-output \
    --enable-stdio-inheritance
