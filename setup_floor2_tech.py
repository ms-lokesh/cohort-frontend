#!/usr/bin/env python
"""
Setup script for creating students, mentors, and floorwing hierarchy
- Creates students from CSV
- Creates 3 mentors
- Assigns students evenly to mentors
- Creates Floor 2 Tech floorwing
- Connects mentors to floorwing
- Creates admin and assigns floorwing
"""

import os
import sys
import django
import csv
from pathlib import Path

# Setup Django
sys.path.append(str(Path(__file__).parent / 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.profiles.models import UserProfile
from django.db import transaction

User = get_user_model()

def create_students_from_csv():
    """Create students from CSV file"""
    csv_path = Path(__file__).parent / 'dummy users - Sheet1.csv'
    
    students = []
    print("\n📚 Creating students from CSV...")
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            email = row['email'].strip()
            username = row['username'].strip()
            password = row['password'].strip()
            
            # Create user
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'username': email.split('@')[0],
                    'first_name': username.split()[0] if username else '',
                    'last_name': ' '.join(username.split()[1:]) if len(username.split()) > 1 else '',
                }
            )
            
            if created:
                user.set_password(password)
                user.save()
                print(f"  ✓ Created user: {username} ({email})")
            
            # Get or create profile with role=STUDENT
            profile = user.profile
            profile.role = 'STUDENT'
            profile.campus = 'TECH'
            profile.floor = 2
            profile.save()
            
            students.append(user)
            
    print(f"\n✅ Total students created: {len(students)}")
    return students


def create_mentors():
    """Create 3 mentors"""
    print("\n👨‍🏫 Creating mentors...")
    
    mentors_data = [
        {
            'email': 'mentor1.floor2tech@snsce.ac.in',
            'username': 'mentor1_floor2tech',
            'first_name': 'Rajesh',
            'last_name': 'Kumar',
            'password': 'mentor123@',
        },
        {
            'email': 'mentor2.floor2tech@snsce.ac.in',
            'username': 'mentor2_floor2tech',
            'first_name': 'Priya',
            'last_name': 'Sharma',
            'password': 'mentor123@',
        },
        {
            'email': 'mentor3.floor2tech@snsce.ac.in',
            'username': 'mentor3_floor2tech',
            'first_name': 'Arun',
            'last_name': 'Patel',
            'password': 'mentor123@',
        }
    ]
    
    mentors = []
    for data in mentors_data:
        # Create user
        user, created = User.objects.get_or_create(
            email=data['email'],
            defaults={
                'username': data['username'],
                'first_name': data['first_name'],
                'last_name': data['last_name'],
            }
        )
        
        if created:
            user.set_password(data['password'])
            user.save()
            print(f"  ✓ Created user: {data['first_name']} {data['last_name']} ({data['email']})")
        
        # Set profile as mentor
        profile = user.profile
        profile.role = 'MENTOR'
        profile.campus = 'TECH'
        profile.floor = 2
        profile.save()
        
        mentors.append(user)
    
    print(f"\n✅ Total mentors created: {len(mentors)}")
    return mentors


def create_floorwing_and_admin():
    """Create Floor 2 Tech floorwing and admin"""
    print("\n🏢 Creating Floor 2 Tech floorwing and admin...")
    
    # Create floorwing user
    floorwing_user, created = User.objects.get_or_create(
        email='floorwing.floor2tech@snsce.ac.in',
        defaults={
            'username': 'floorwing_floor2tech',
            'first_name': 'Floor Wing',
            'last_name': 'Tech Floor 2',
        }
    )
    
    if created:
        floorwing_user.set_password('floorwing123@')
        floorwing_user.save()
        print(f"  ✓ Created floorwing user: {floorwing_user.get_full_name()} ({floorwing_user.email})")
    
    # Set profile as floor wing
    profile = floorwing_user.profile
    profile.role = 'FLOOR_WING'
    profile.campus = 'TECH'
    profile.floor = 2
    profile.save()
    
    # Create admin user
    admin_user, created = User.objects.get_or_create(
        email='admin.floor2tech@snsce.ac.in',
        defaults={
            'username': 'admin_floor2tech',
            'first_name': 'Admin',
            'last_name': 'Tech Campus',
            'is_staff': True,
            'is_superuser': True,
        }
    )
    
    if created:
        admin_user.set_password('admin123@')
        admin_user.save()
        print(f"  ✓ Created admin user: {admin_user.get_full_name()} ({admin_user.email})")
    
    # Set admin profile
    admin_profile = admin_user.profile
    admin_profile.role = 'ADMIN'
    admin_profile.campus = 'TECH'
    admin_profile.save()
    
    return floorwing_user, admin_user


def assign_students_to_mentors(students, mentors):
    """Assign students evenly to mentors"""
    print("\n🔗 Assigning students to mentors...")
    
    # Calculate students per mentor
    total_students = len(students)
    students_per_mentor = total_students // len(mentors)
    remainder = total_students % len(mentors)
    
    start_idx = 0
    for i, mentor in enumerate(mentors):
        # Add one extra student to first 'remainder' mentors
        count = students_per_mentor + (1 if i < remainder else 0)
        end_idx = start_idx + count
        
        assigned_students = students[start_idx:end_idx]
        
        for student in assigned_students:
            student_profile = student.profile
            student_profile.assigned_mentor = mentor
            student_profile.save()
        
        print(f"  ✓ Assigned {count} students to {mentor.get_full_name()}")
        start_idx = end_idx


def assign_mentors_to_floorwing(mentors, floorwing):
    """Assign mentors to floorwing - already done via campus and floor"""
    print("\n🔗 All mentors assigned to Floor 2 Tech via campus and floor settings")


def print_summary(students, mentors, floorwing, admin):
    """Print summary of setup"""
    print("\n" + "="*60)
    print("📊 SETUP SUMMARY")
    print("="*60)
    
    print(f"\n🏢 Floor 2 Tech Campus")
    print(f"   Admin: {admin.get_full_name()} ({admin.email})")
    print(f"   Password: admin123@")
    
    print(f"\n👤 Floor Wing: {floorwing.get_full_name()} ({floorwing.email})")
    print(f"   Password: floorwing123@")
    
    print(f"\n👨‍🏫 Mentors (Total: {len(mentors)})")
    for mentor in mentors:
        student_count = User.objects.filter(
            profile__role='STUDENT',
            profile__assigned_mentor=mentor
        ).count()
        print(f"   • {mentor.get_full_name()} ({mentor.email})")
        print(f"     Password: mentor123@")
        print(f"     Students: {student_count}")
    
    print(f"\n📚 Students (Total: {len(students)})")
    for mentor in mentors:
        mentor_students = User.objects.filter(
            profile__role='STUDENT',
            profile__assigned_mentor=mentor
        )
        if mentor_students.exists():
            print(f"\n   Under {mentor.get_full_name()}:")
            for student in mentor_students:
                print(f"     • {student.get_full_name()} ({student.email})")
    
    print("\n" + "="*60)
    print("✅ SETUP COMPLETED SUCCESSFULLY!")
    print("="*60)
    
    print("\n📋 Login Credentials Summary:")
    print(f"\nAdmin:")
    print(f"  Email: admin.floor2tech@snsce.ac.in")
    print(f"  Password: admin123@")
    print(f"\nFloor Wing:")
    print(f"  Email: floorwing.floor2tech@snsce.ac.in")
    print(f"  Password: floorwing123@")
    print(f"\nMentors:")
    print(f"  mentor1.floor2tech@snsce.ac.in / mentor123@")
    print(f"  mentor2.floor2tech@snsce.ac.in / mentor123@")
    print(f"  mentor3.floor2tech@snsce.ac.in / mentor123@")
    print(f"\nStudents: Use credentials from CSV (password: pass123@)")
    print()


@transaction.atomic
def main():
    """Main setup function"""
    print("\n" + "="*60)
    print("🚀 COHORT SETUP SCRIPT")
    print("="*60)
    
    # Create all entities
    students = create_students_from_csv()
    mentors = create_mentors()
    floorwing, admin = create_floorwing_and_admin()
    
    # Assign relationships
    assign_students_to_mentors(students, mentors)
    assign_mentors_to_floorwing(mentors, floorwing)
    
    # Print summary
    print_summary(students, mentors, floorwing, admin)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
