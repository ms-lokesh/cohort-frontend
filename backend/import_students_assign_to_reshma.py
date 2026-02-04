"""
Import students from CSV and assign them to mentor 'Reshma'.

Also sets/updates each student's password to 'pass123#'.

Run:
    python import_students_assign_to_reshma.py
"""
import os
import django
import csv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.profiles.models import UserProfile


def get_or_create_mentor_reshma():
    """Find a mentor named Reshma; create if not found."""
    # Try by first name, username, or email
    mentor = (
        User.objects.filter(first_name__iexact='Reshma').first()
        or User.objects.filter(username__iexact='reshma').first()
        or User.objects.filter(email__iexact='reshma@cohort.com').first()
    )

    if mentor:
        # Ensure profile indicates mentor role
        profile = mentor.profile
        changed = False
        if profile.role != 'MENTOR':
            profile.role = 'MENTOR'
            changed = True
        if not profile.campus:
            profile.campus = 'TECH'
            changed = True
        if not profile.floor:
            profile.floor = 2
            changed = True
        if changed:
            profile.save()
        if not mentor.is_staff:
            mentor.is_staff = True
            mentor.save()
        return mentor

    # Create mentor user
    mentor = User.objects.create_user(
        username='reshma',
        email='reshma@cohort.com',
        first_name='Reshma',
        last_name='Raj',
    )
    mentor.set_password('mentor123')
    mentor.is_staff = True
    mentor.save()

    profile = mentor.profile
    profile.role = 'MENTOR'
    profile.campus = 'TECH'
    profile.floor = 2
    profile.save()

    return mentor


def import_students(password_override='pass123#'):
    """Import students from the repository CSV and assign to Reshma."""
    # CSV is located one directory above backend
    csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'dummy users - Sheet1.csv')
    if not os.path.exists(csv_path):
        print(f"❌ CSV not found at: {csv_path}")
        return

    mentor = get_or_create_mentor_reshma()
    print(f"✅ Using mentor: {mentor.get_full_name() or mentor.username} ({mentor.email})\n")

    created, updated, assigned = 0, 0, 0

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            email = row['email'].strip()
            full_name = row['username'].strip()  # column contains full name
            # Use email prefix as username (safer than full name field)
            base_username = email.split('@')[0]

            # Ensure unique username if clashes
            username = base_username
            suffix = 1
            while User.objects.filter(username=username).exclude(email=email).exists():
                username = f"{base_username}{suffix}"
                suffix += 1

            # Split full name
            parts = full_name.split()
            first_name = parts[0] if parts else base_username
            last_name = ' '.join(parts[1:]) if len(parts) > 1 else ''

            user = User.objects.filter(email=email).first()
            if user:
                # Update name fields if empty
                changed = False
                if not user.first_name and first_name:
                    user.first_name = first_name
                    changed = True
                if not user.last_name and last_name:
                    user.last_name = last_name
                    changed = True
                # Always set password to override
                user.set_password(password_override)
                changed = True
                if changed:
                    user.save()
                updated += 1
                print(f"ℹ️  Updated existing: {email}")
            else:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                )
                user.set_password(password_override)
                user.save()
                created += 1
                print(f"✅ Created: {email} (username: {user.username})")

            # Ensure profile fields and assignment
            profile = user.profile
            profile.role = 'STUDENT'
            profile.campus = 'TECH'
            # Default all to floor 2 for this cohort
            profile.floor = 2
            if profile.assigned_mentor_id != mentor.id:
                profile.assigned_mentor = mentor
                assigned += 1
            profile.save()

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"New users created: {created}")
    print(f"Existing users updated: {updated}")
    print(f"Students assigned/reassigned to Reshma: {assigned}")
    total_under_mentor = UserProfile.objects.filter(role='STUDENT', assigned_mentor=mentor).count()
    print(f"Total students under Reshma: {total_under_mentor}")
    print("=" * 60)
    print("\nAll student passwords set to: pass123#")


if __name__ == '__main__':
    import_students()
    print("\n✅ Done!")
