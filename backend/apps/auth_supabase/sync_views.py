"""
Admin-only API endpoint to sync Supabase user mappings
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.contrib.auth.models import User
from apps.auth_supabase.models import SupabaseUserMapping
from supabase import create_client
import os


@api_view(['POST'])
@permission_classes([IsAdminUser])
def sync_mappings_view(request):
    """
    Sync Django users with Supabase authentication users
    Only accessible to admin users
    """
    try:
        # Get Supabase credentials
        url = os.environ.get('SUPABASE_URL')
        key = os.environ.get('SUPABASE_SERVICE_ROLE_KEY')
        
        if not url or not key:
            return Response({
                'success': False,
                'error': 'Missing Supabase credentials'
            }, status=500)
        
        # Get unmapped users
        unmapped = User.objects.exclude(
            id__in=SupabaseUserMapping.objects.values_list('django_user_id', flat=True)
        )
        
        total_users = User.objects.count()
        already_mapped = SupabaseUserMapping.objects.count()
        
        if unmapped.count() == 0:
            return Response({
                'success': True,
                'message': 'All users already mapped',
                'total_users': total_users,
                'mapped': already_mapped,
                'created': 0
            })
        
        # Connect to Supabase
        supabase = create_client(url, key)
        response_data = supabase.auth.admin.list_users()
        supabase_users = {user.email.lower(): user.id for user in response_data if user.email}
        
        # Create mappings
        created = 0
        not_found = 0
        errors = []
        
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
                except Exception as e:
                    errors.append(f"{email}: {str(e)[:50]}")
            else:
                not_found += 1
        
        # Final status
        total_mapped = SupabaseUserMapping.objects.count()
        
        return Response({
            'success': True,
            'message': 'Sync completed',
            'total_users': total_users,
            'already_mapped': already_mapped,
            'created': created,
            'not_found': not_found,
            'errors': errors[:10],  # Limit to first 10 errors
            'final_mapped': total_mapped,
            'remaining': total_users - total_mapped
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=500)


@api_view(['GET'])
def sync_mappings_public(request):
    """
    Public endpoint to sync mappings (can be called without auth on first setup)
    Should be disabled after initial sync
    """
    # Check if this is initial setup (no mappings exist)
    if SupabaseUserMapping.objects.count() > 0:
        return Response({
            'success': False,
            'error': 'Sync already completed. Use admin endpoint for re-sync.'
        }, status=403)
    
    # Same logic as admin endpoint
    try:
        url = os.environ.get('SUPABASE_URL')
        key = os.environ.get('SUPABASE_SERVICE_ROLE_KEY')
        
        if not url or not key:
            return Response({'success': False, 'error': 'Missing credentials'}, status=500)
        
        unmapped = User.objects.exclude(
            id__in=SupabaseUserMapping.objects.values_list('django_user_id', flat=True)
        )
        
        supabase = create_client(url, key)
        response_data = supabase.auth.admin.list_users()
        supabase_users = {user.email.lower(): user.id for user in response_data if user.email}
        
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
        
        return Response({
            'success': True,
            'message': 'Initial sync completed',
            'created': created,
            'total_mapped': SupabaseUserMapping.objects.count()
        })
        
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=500)
