import os
import django
import csv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.profiles.models import UserProfile

def import_students_and_assign():
    """Import students from CSV and assign them to mentor1"""
    
    # Get the mentor
    try:
        mentor_user = User.objects.get(username='mentor1')
        print(f"✅ Found mentor: {mentor_user.username} ({mentor_user.email})")
    except User.DoesNotExist:
        print("❌ Error: mentor1 not found. Please create mentor first.")
        return
    
    # Student data from CSV
    students_data = [
        {
            'email': 'sudharsshana.r.cse.2024@snsce.ac.in',
            'username': 'sudharsshana.r',
            'full_name': 'Sudharsshana R',
            'password': 'pass123@'
        },
        {
            'email': 'alana.s.iot.2024@snsce.ac.in',
            'username': 'alana.s',
            'full_name': 'ALANA SEBASTIAN',
            'password': 'pass123@'
        },
        {
            'email': 'bsurya.n.it.2024@snsce.ac.in',
            'username': 'bsurya.n',
            'full_name': 'BALASURYA N',
            'password': 'pass123@'
        },
        {
            'email': 'gobinath.g.csd.2024@snsce.ac.in',
            'username': 'gobinath.g',
            'full_name': 'Gobinath.G',
            'password': 'pass123@'
        },
        {
            'email': 'santhosh.m.cse.2024@snsct.org',
            'username': 'santhosh.m',
            'full_name': 'SANTHOSH KRISHNAN M',
            'password': 'pass123@'
        },
        {
            'email': 'marlenesaranya.s.cse.2024@snsct.org',
            'username': 'marlenesaranya.s',
            'full_name': 'MARLENE SARANYA S',
            'password': 'pass123@'
        },
        {
            'email': 'mathi.t.cse.2024@snsce.ac.in',
            'username': 'mathi.t',
            'full_name': 'MATHIYAZHAGAN T',
            'password': 'pass123@'
        },
        {
            'email': 'pranethi.r.iot.2024@snsce.ac.in',
            'username': 'pranethi.r',
            'full_name': 'PRANETHI .R',
            'password': 'pass123@'
        },
        {
            'email': 'dayanithi.m.cse.2024@snsce.ac.in',
            'username': 'dayanithi.m',
            'full_name': 'Dayanithi M',
            'password': 'pass123@'
        },
        {
            'email': 'jabbastin.k.csd.2024@snsce.ac.in',
            'username': 'jabbastin.k',
            'full_name': 'JABBASTIN AKASH K',
            'password': 'pass123@'
        },
        {
            'email': 'vishnudharshan.s.csd.2024@snsce.ac.in',
            'username': 'vishnudharshan.s',
            'full_name': 'VISHNUDHARSHAN S',
            'password': 'pass123@'
        },
    ]
    
    print("\n" + "="*60)
    print("IMPORTING STUDENTS AND ASSIGNING TO MENTOR")
    print("="*60 + "\n")
    
    created_count = 0
    updated_count = 0
    assigned_count = 0
    
    for student_data in students_data:
        email = student_data['email']
        username = student_data['username']
        full_name = student_data['full_name']
        password = student_data['password']
        
        # Split full name
        name_parts = full_name.split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''
        
        # Check if user exists
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
            }
        )
        
        if created:
            user.set_password(password)
            user.save()
            created_count += 1
            print(f"✅ Created user: {username} ({email})")
        else:
            updated_count += 1
            print(f"ℹ️  User exists: {username} ({email})")
        
        # Update profile to student role
        profile = user.profile
        if profile.role != 'STUDENT':
            profile.role = 'STUDENT'
        profile.campus = 'TECH'
        profile.floor = 2  # Assign all to floor 2
        profile.assigned_mentor = mentor_user  # Assign mentor
        profile.save()
        
        if created:
            assigned_count += 1
            print(f"   └─ Assigned to mentor: {mentor_user.username}")
        else:
            if profile.assigned_mentor != mentor_user:
                assigned_count += 1
                print(f"   └─ Reassigned to mentor: {mentor_user.username}")
            else:
                print(f"   └─ Already assigned to mentor: {mentor_user.username}")
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"✅ New users created: {created_count}")
    print(f"ℹ️  Existing users: {updated_count}")
    print(f"👥 Students assigned to {mentor_user.username}: {assigned_count}")
    print(f"📊 Total students under {mentor_user.username}: {UserProfile.objects.filter(assigned_mentor=mentor_user, role='STUDENT').count()}")
    
    print("\n" + "="*60)
    print("STUDENT LOGIN CREDENTIALS")
    print("="*60)
    for student_data in students_data:
        print(f"\nUsername: {student_data['username']}")
        print(f"Email:    {student_data['email']}")
        print(f"Password: {student_data['password']}")
    
    print("\n" + "="*60)
    print("⚠️  All passwords are: pass123@")
    print("="*60)

if __name__ == '__main__':
    import_students_and_assign()
    print("\n✅ Done!")
