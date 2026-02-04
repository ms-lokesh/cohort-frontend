"""
Create a production user for testing
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.profiles.models import StudentProfile

# Create the user you tried to log in with
email = 'jabbastin.k.csd.2024@snsce.ac.in'
username = email.split('@')[0]  # jabbastin.k.csd.2024
password = 'pass123#'

if User.objects.filter(email=email).exists():
    print(f"✓ User '{email}' already exists")
    user = User.objects.get(email=email)
else:
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name='Jabbastin',
        last_name='K'
    )
    print(f"✓ Created user '{email}'")
    
    # Create student profile
    try:
        profile = StudentProfile.objects.create(
            user=user,
            register_number='CSD2024001',
            department='Computer Science'
        )
        print(f"✓ Created student profile for {email}")
    except Exception as e:
        print(f"⚠ Could not create profile: {e}")

print(f"\n{'='*50}")
print(f"User Created Successfully!")
print(f"{'='*50}")
print(f"Email: {email}")
print(f"Password: {password}")
print(f"\nYou can now login at: https://cohort-37ur.onrender.com")
print(f"{'='*50}\n")
