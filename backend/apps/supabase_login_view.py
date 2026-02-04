"""
Hybrid authentication view that uses Supabase for auth and returns Django JWT
"""
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from apps.auth_supabase.models import SupabaseUserMapping
from supabase import create_client
import json
import os


@csrf_exempt
def supabase_login(request):
    """
    Authenticate with Supabase and return Django JWT tokens
    POST /api/auth/supabase-login/
    Body: {"email": "user@example.com", "password": "password"}
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return JsonResponse({
                'detail': 'Email and password required',
                'code': 'validation_error'
            }, status=400)
        
        # Get Supabase credentials
        url = os.environ.get('SUPABASE_URL')
        key = os.environ.get('SUPABASE_ANON_KEY')
        
        if not url or not key:
            return JsonResponse({
                'detail': 'Authentication service not configured',
                'code': 'server_error'
            }, status=500)
        
        # Authenticate with Supabase
        try:
            supabase = create_client(url, key)
            auth_response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            if not auth_response or not auth_response.user:
                return JsonResponse({
                    'detail': 'No active account found with the given credentials',
                    'code': 'authentication_failed'
                }, status=401)
            
            supabase_user = auth_response.user
            
        except Exception as e:
            error_msg = str(e)
            if 'Invalid login credentials' in error_msg or 'invalid' in error_msg.lower():
                return JsonResponse({
                    'detail': 'No active account found with the given credentials',
                    'code': 'authentication_failed'
                }, status=401)
            return JsonResponse({
                'detail': f'Authentication error: {error_msg}',
                'code': 'authentication_error'
            }, status=401)
        
        # Find or create Django user
        try:
            mapping = SupabaseUserMapping.objects.get(supabase_id=supabase_user.id)
            user = mapping.django_user
        except SupabaseUserMapping.DoesNotExist:
            # Try to find user by email
            user = User.objects.filter(email=email).first()
            if not user:
                # Create Django user
                username = email.split('@')[0].replace('.', '_')[:150]
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password  # This won't be used for auth
                )
            
            # Create mapping
            SupabaseUserMapping.objects.create(
                django_user=user,
                supabase_id=supabase_user.id,
                supabase_email=email
            )
        
        # Generate Django JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return JsonResponse({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'detail': 'Invalid JSON',
            'code': 'parse_error'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'detail': f'Server error: {str(e)}',
            'code': 'server_error'
        }, status=500)
