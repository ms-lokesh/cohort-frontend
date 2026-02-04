import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import authenticate

credentials = [
    ('admin', 'admin123'),
    ('mentor1', 'mentor123'),
    ('student1', 'student123'),
    ('floorwing1', 'floorwing123'),
]

print("="*60)
print("TESTING LOGIN CREDENTIALS")
print("="*60)

for username, password in credentials:
    user = authenticate(username=username, password=password)
    if user:
        profile = user.profile
        print(f"\n✅ {username}: WORKS")
        print(f"   Password: {password}")
        print(f"   Role: {profile.role}")
        print(f"   Email: {user.email}")
    else:
        print(f"\n❌ {username}: FAILED")
        print(f"   Tried password: {password}")

print("\n" + "="*60)
