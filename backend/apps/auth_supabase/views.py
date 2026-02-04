"""
Example API views using Supabase authentication
"""
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .decorators import supabase_auth_required, supabase_admin_required


@require_http_methods(['GET'])
@supabase_auth_required
def get_current_user(request):
    """
    GET /api/me
    Returns current authenticated user info
    """
    user = request.user
    
    return JsonResponse({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'is_staff': user.is_staff,
        'is_superuser': user.is_superuser,
        'date_joined': user.date_joined.isoformat(),
    })


@require_http_methods(['GET'])
@supabase_auth_required
def protected_view(request):
    """
    GET /api/protected
    Example of a protected endpoint
    """
    return JsonResponse({
        'message': 'This is protected data',
        'user': request.user.username,
        'access_granted': True,
    })


@require_http_methods(['GET'])
@supabase_admin_required
def admin_only_view(request):
    """
    GET /api/admin/stats
    Example of an admin-only endpoint
    """
    return JsonResponse({
        'message': 'Admin access granted',
        'admin': request.user.username,
        'stats': {
            'total_users': 100,
            'active_sessions': 25,
        }
    })


@require_http_methods(['GET'])
def health_check(request):
    """
    GET /api/health
    Public health check endpoint
    """
    return JsonResponse({
        'status': 'ok',
        'service': 'django-supabase-auth'
    })


@require_http_methods(['GET'])
def echo_headers(request):
    """
    Debug endpoint to echo incoming Authorization header (safe preview).
    GET /api/supabase/echo-headers/
    """
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    try:
        preview = f"{auth_header[:40]}... (len={len(auth_header)})" if auth_header else ''
    except Exception:
        preview = 'unavailable'

    return JsonResponse({
        'authorization_header_present': bool(auth_header),
        'authorization_preview': preview,
    })
