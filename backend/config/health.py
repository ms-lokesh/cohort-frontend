"""
Health check endpoint for Render deployment monitoring
"""
from django.http import JsonResponse
from django.db import connection
from django.conf import settings
import os

def health_check(request):
    """
    Health check endpoint for monitoring
    Returns 200 OK if service is healthy
    """
    status = {
        'status': 'healthy',
        'service': 'cohort-web-app',
        'environment': 'production' if not settings.DEBUG else 'development',
    }
    
    # Check database connection
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        status['database'] = 'connected'
    except Exception as e:
        status['database'] = 'error'
        status['database_error'] = str(e)
        return JsonResponse(status, status=500)
    
    # Check Supabase connection
    if os.getenv('SUPABASE_URL'):
        status['supabase'] = 'configured'
    else:
        status['supabase'] = 'not configured'
    
    return JsonResponse(status)
