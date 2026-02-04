import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.profiles.models import UserProfile

# Get mentor
mentor = User.objects.get(username='mentor1')

# Get all students assigned to this mentor
students = User.objects.filter(
    profile__assigned_mentor=mentor,
    profile__role='STUDENT'
).select_related('profile')

print("="*60)
print(f"STUDENTS ASSIGNED TO MENTOR: {mentor.username}")
print("="*60)
print(f"Total Students: {students.count()}\n")

for student in students:
    print(f"✅ {student.username}")
    print(f"   Name: {student.first_name} {student.last_name}")
    print(f"   Email: {student.email}")
    print(f"   Campus: {student.profile.campus}")
    print(f"   Floor: {student.profile.floor}")
    print()

print("="*60)
print("✅ Backend connection verified!")
print("="*60)
