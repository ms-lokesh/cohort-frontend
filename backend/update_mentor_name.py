import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

# Update mentor1 with proper name
try:
    mentor = User.objects.get(username='mentor1')
    mentor.first_name = 'Test'
    mentor.last_name = 'Mentor'
    mentor.save()
    
    print("="*60)
    print("MENTOR NAME UPDATED")
    print("="*60)
    print(f"Username: {mentor.username}")
    print(f"First Name: {mentor.first_name}")
    print(f"Last Name: {mentor.last_name}")
    print(f"Email: {mentor.email}")
    print(f"Full Name: {mentor.first_name} {mentor.last_name}")
    print("="*60)
    print("✅ Mentor name has been updated!")
    print("The mentor dashboard will now show: 'Welcome back, Test!'")
    print("="*60)
    
except User.DoesNotExist:
    print("❌ Error: mentor1 user not found")
