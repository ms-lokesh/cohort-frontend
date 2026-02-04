"""
Decorators for Supabase authentication
"""
from functools import wraps
from django.http import JsonResponse


def supabase_auth_required(view_func):
    """
    Decorator to require Supabase authentication
    Returns 401 if user is not authenticated via Supabase
    
    Usage:
        @supabase_auth_required
        def my_view(request):
            # request.user is authenticated Django user
            return JsonResponse({'user': request.user.username})
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse(
                {'error': 'Authentication required'},
                status=401
            )
        
        if not getattr(request, 'supabase_token_valid', False):
            return JsonResponse(
                {'error': 'Invalid Supabase token'},
                status=401
            )
        
        return view_func(request, *args, **kwargs)
    
    return wrapper


def supabase_admin_required(view_func):
    """
    Decorator to require Supabase authentication + Django admin/staff status
    
    Usage:
        @supabase_admin_required
        def admin_view(request):
            # request.user is authenticated admin
            return JsonResponse({'admin': True})
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse(
                {'error': 'Authentication required'},
                status=401
            )
        
        if not getattr(request, 'supabase_token_valid', False):
            return JsonResponse(
                {'error': 'Invalid Supabase token'},
                status=401
            )
        
        if not (request.user.is_staff or request.user.is_superuser):
            return JsonResponse(
                {'error': 'Admin access required'},
                status=403
            )
        
        return view_func(request, *args, **kwargs)
    
    return wrapper
