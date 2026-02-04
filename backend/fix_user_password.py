"""
Fix user password - check if user exists and reset password with proper hashing
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

# The email you're trying to log in with
email = 'jabbastin.k.csd.2024@snsce.ac.in'
password = 'pass123#'

print(f"\n{'='*60}")
print(f"Checking user: {email}")
print(f"{'='*60}\n")

# Check if user exists
try:
    user = User.objects.get(email=email)
    print(f"✓ User found!")
    print(f"  Username: {user.username}")
    print(f"  Email: {user.email}")
    print(f"  Active: {user.is_active}")
    print(f"  Password hash: {user.password[:50]}...")
    
    # Check if password is properly hashed
    if not user.password.startswith('pbkdf2_sha256$') and not user.password.startswith('argon2'):
        print(f"\n⚠ WARNING: Password is NOT properly hashed!")
        print(f"  Current password field: {user.password}")
        print(f"\n  Fixing password...")
        user.set_password(password)
        user.save()
        print(f"✓ Password updated with proper hashing!")
    else:
        print(f"\n✓ Password is properly hashed")
        print(f"\n  Resetting password to: {password}")
        user.set_password(password)
        user.save()
        print(f"✓ Password reset successful!")
    
    # Test authentication
    from django.contrib.auth import authenticate
    test_user = authenticate(username=user.username, password=password)
    if test_user:
        print(f"\n✓ Authentication test PASSED!")
        print(f"\n{'='*60}")
        print(f"You can now login with:")
        print(f"  Email: {email}")
        print(f"  Password: {password}")
        print(f"{'='*60}\n")
    else:
        print(f"\n✗ Authentication test FAILED!")
        print(f"  Something is still wrong with the password")
        
except User.DoesNotExist:
    print(f"✗ User with email '{email}' does NOT exist!")
    print(f"\nCreating user...")
    
    username = email.split('@')[0]
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name='Jabbastin',
        last_name='K'
    )
    user.is_active = True
    user.save()
    
    print(f"✓ User created successfully!")
    print(f"\n{'='*60}")
    print(f"Login credentials:")
    print(f"  Email: {email}")
    print(f"  Password: {password}")
    print(f"{'='*60}\n")
