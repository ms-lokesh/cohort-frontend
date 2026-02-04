#!/usr/bin/env python
"""Check student credentials"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

# Check a few students
emails = [
    'sudharsshana.r.cse.2024@snsce.ac.in',
    'alana.s.iot.2024@snsce.ac.in',
    'mentor1.floor2tech@snsce.ac.in'
]

print("\n🔍 Checking User Credentials\n")
print("="*60)

for email in emails:
    try:
        user = User.objects.get(email=email)
        password_valid = user.check_password('pass123@')
        mentor_password_valid = user.check_password('mentor123@')
        
        print(f"\n✓ Found: {email}")
        print(f"  Username: {user.username}")
        print(f"  Email: {user.email}")
        print(f"  Has usable password: {user.has_usable_password()}")
        print(f"  Password 'pass123@' valid: {password_valid}")
        print(f"  Password 'mentor123@' valid: {mentor_password_valid}")
        print(f"  Is active: {user.is_active}")
        print(f"  Role: {user.profile.role if hasattr(user, 'profile') else 'No profile'}")
        
    except User.DoesNotExist:
        print(f"\n✗ Not found: {email}")

print("\n" + "="*60)
print("\n💡 To login, use:")
print("   - Email: sudharsshana.r.cse.2024@snsce.ac.in")
print("   - Password: pass123@")
print("\n   OR")
print("   - Username: sudharsshana.r.cse.2024")
print("   - Password: pass123@")
print()
