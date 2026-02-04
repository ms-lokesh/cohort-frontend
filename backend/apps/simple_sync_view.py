"""
Simple API endpoint to sync Supabase mappings
"""
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from apps.auth_supabase.models import SupabaseUserMapping
from supabase import create_client
import os

@csrf_exempt
def simple_sync_mappings(request):
    """
    Sync Django users with Supabase - simple version
    GET /api/simple-sync-mappings/
    """
    try:
        # Get Supabase credentials
        url = os.environ.get('SUPABASE_URL')
        key = os.environ.get('SUPABASE_SERVICE_ROLE_KEY')
        
        if not url or not key:
            return JsonResponse({'error': 'Missing Supabase credentials'}, status=500)
        
        # Get unmapped users
        unmapped = User.objects.exclude(
            id__in=SupabaseUserMapping.objects.values_list('django_user_id', flat=True)
        )
        
        total_users = User.objects.count()
        already_mapped = SupabaseUserMapping.objects.count()
        
        if unmapped.count() == 0:
            return JsonResponse({
                'status': 'success',
                'message': 'All users already mapped',
                'total_users': total_users,
                'mapped': already_mapped
            })
        
        # Connect to Supabase
        supabase = create_client(url, key)
        response_data = supabase.auth.admin.list_users()
        supabase_users = {user.email.lower(): user.id for user in response_data if user.email}
        
        # Create mappings
        created = 0
        for user in unmapped:
            email = user.email.lower()
            if email in supabase_users:
                try:
                    SupabaseUserMapping.objects.create(
                        django_user=user,
                        supabase_id=supabase_users[email],
                        supabase_email=email
                    )
                    created += 1
                except:
                    pass
        
        # Final status
        total_mapped = SupabaseUserMapping.objects.count()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Sync completed',
            'created': created,
            'total_mapped': total_mapped,
            'remaining': total_users - total_mapped
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
