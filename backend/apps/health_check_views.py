"""
Health Check Endpoints

Provides system health monitoring without breaking existing functionality.
These endpoints help detect issues before they affect users.
"""

from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
from django.utils import timezone
from django.conf import settings
import time


def health_check(request):
    """
    Main health check endpoint: /health/
    
    Returns system status including:
    - Database connectivity
    - Cache availability (if enabled)
    - Response time
    - Application readiness
    
    This endpoint is safe to call frequently (every 30s) for monitoring.
    """
    start_time = time.time()
    health_status = {
        'status': 'healthy',
        'timestamp': timezone.now().isoformat(),
        'checks': {}
    }
    
    # Check database
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        health_status['checks']['database'] = {
            'status': 'up',
            'message': 'Database connection successful'
        }
    except Exception as e:
        health_status['status'] = 'unhealthy'
        health_status['checks']['database'] = {
            'status': 'down',
            'message': f'Database error: {str(e)}'
        }
    
    # Check cache (only if caching is enabled)
    if settings.USE_NOTIFICATION_CACHE or settings.USE_ANALYTICS_SUMMARY:
        try:
            cache_key = 'health_check_test'
            cache.set(cache_key, 'ok', 10)
            result = cache.get(cache_key)
            if result == 'ok':
                health_status['checks']['cache'] = {
                    'status': 'up',
                    'message': 'Cache is working'
                }
            else:
                health_status['checks']['cache'] = {
                    'status': 'degraded',
                    'message': 'Cache not storing values correctly'
                }
        except Exception as e:
            health_status['status'] = 'degraded'
            health_status['checks']['cache'] = {
                'status': 'down',
                'message': f'Cache error: {str(e)}'
            }
    else:
        health_status['checks']['cache'] = {
            'status': 'disabled',
            'message': 'Caching not enabled'
        }
    
    # Response time
    response_time_ms = int((time.time() - start_time) * 1000)
    health_status['response_time_ms'] = response_time_ms
    
    # Feature flags status
    health_status['features'] = {
        'analytics_summary': settings.USE_ANALYTICS_SUMMARY,
        'notification_cache': settings.USE_NOTIFICATION_CACHE,
        'cloud_storage': settings.USE_CLOUD_STORAGE,
        'async_tasks': settings.USE_ASYNC_TASKS,
    }
    
    # Determine HTTP status code
    if health_status['status'] == 'healthy':
        status_code = 200
    elif health_status['status'] == 'degraded':
        status_code = 200  # Still operational
    else:
        status_code = 503  # Service unavailable
    
    return JsonResponse(health_status, status=status_code)


def readiness_check(request):
    """
    Readiness check endpoint: /health/ready/
    
    Used by load balancers to determine if app can accept traffic.
    Checks if all critical dependencies are available.
    """
    ready = True
    checks = {}
    
    # Database must be ready
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        checks['database'] = True
    except Exception:
        checks['database'] = False
        ready = False
    
    # Cache should be ready if enabled
    if settings.USE_NOTIFICATION_CACHE:
        try:
            cache.set('ready_test', 'ok', 5)
            checks['cache'] = cache.get('ready_test') == 'ok'
            ready = ready and checks['cache']
        except Exception:
            checks['cache'] = False
            ready = False
    
    return JsonResponse({
        'ready': ready,
        'checks': checks,
        'timestamp': timezone.now().isoformat()
    }, status=200 if ready else 503)


def liveness_check(request):
    """
    Liveness check endpoint: /health/live/
    
    Simple check that the application process is running.
    Used by orchestrators (Kubernetes, Docker) to know if app needs restart.
    """
    return JsonResponse({
        'alive': True,
        'timestamp': timezone.now().isoformat()
    })
