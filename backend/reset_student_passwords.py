#!/usr/bin/env python
"""Reset student passwords to match CSV"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

print("\n🔑 Resetting Student Passwords\n")
print("="*60)

# Get all students
students = User.objects.filter(profile__role='STUDENT', profile__campus='TECH', profile__floor=2)

count = 0
for student in students:
    student.set_password('pass123@')
    student.save()
    print(f"✓ Reset password for: {student.get_full_name()} ({student.email})")
    count += 1

print("\n" + "="*60)
print(f"✅ Reset {count} student passwords to 'pass123@'")
print("\n💡 You can now login with:")
print("   Email: sudharsshana.r.cse.2024@snsce.ac.in")
print("   Password: pass123@")
print()
