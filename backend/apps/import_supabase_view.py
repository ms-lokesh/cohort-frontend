"""
Simple API endpoint to import users from Supabase to Django
"""
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from apps.auth_supabase.models import SupabaseUserMapping
from supabase import create_client
import os

@csrf_exempt
def import_from_supabase(request):
    """
    Import all Supabase users to Django and create mappings
    GET /api/import-from-supabase/
    """
    try:
        # Get Supabase credentials
        url = os.environ.get('SUPABASE_URL')
        key = os.environ.get('SUPABASE_SERVICE_ROLE_KEY')
        
        if not url or not key:
            return JsonResponse({'error': 'Missing Supabase credentials'}, status=500)
        
        # Connect to Supabase
        supabase = create_client(url, key)
        response_data = supabase.auth.admin.list_users()
        supabase_users = [(user.email, user.id) for user in response_data if user.email]
        
        created_users = 0
        created_mappings = 0
        skipped = 0
        
        default_password = "TempPass@2024"
        
        for email, supabase_id in supabase_users:
            # Check if Django user exists
            user = User.objects.filter(email=email).first()
            
            if not user:
                # Create Django user
                username = email.split('@')[0].replace('.', '_')[:150]
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=default_password
                )
                created_users += 1
            
            # Check if mapping exists
            if not SupabaseUserMapping.objects.filter(django_user=user).exists():
                # Create mapping
                try:
                    SupabaseUserMapping.objects.create(
                        django_user=user,
                        supabase_id=supabase_id,
                        supabase_email=email
                    )
                    created_mappings += 1
                except:
                    pass
            else:
                skipped += 1
        
        return JsonResponse({
            'status': 'success',
            'message': 'Import completed',
            'supabase_users_found': len(supabase_users),
            'created_users': created_users,
            'created_mappings': created_mappings,
            'skipped': skipped,
            'total_users': User.objects.count(),
            'total_mappings': SupabaseUserMapping.objects.count()
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
