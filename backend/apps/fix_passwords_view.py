"""
API endpoint to fix user passwords
"""
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import json

@csrf_exempt
def fix_user_password(request):
    """
    Fix password for a user - rehash if needed
    Usage: POST /api/fix-password/
    Body: {"email": "user@example.com", "password": "newpassword"}
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return JsonResponse({'error': 'Email and password required'}, status=400)
        
        # Find user
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({
                'error': 'User not found',
                'message': f'No user with email {email}'
            }, status=404)
        
        # Check current password hash
        old_hash = user.password[:50] if len(user.password) > 50 else user.password
        is_properly_hashed = user.password.startswith('pbkdf2_sha256$') or user.password.startswith('argon2')
        
        # Reset password with proper hashing
        user.set_password(password)
        user.is_active = True
        user.save()
        
        # Test authentication
        test_user = authenticate(username=user.username, password=password)
        auth_works = test_user is not None
        
        return JsonResponse({
            'success': True,
            'message': 'Password updated successfully',
            'user': {
                'username': user.username,
                'email': user.email,
                'is_active': user.is_active
            },
            'debug': {
                'old_hash_preview': old_hash,
                'was_properly_hashed': is_properly_hashed,
                'new_hash_preview': user.password[:50],
                'authentication_test': 'PASSED' if auth_works else 'FAILED'
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'error': 'Server error',
            'message': str(e)
        }, status=500)
