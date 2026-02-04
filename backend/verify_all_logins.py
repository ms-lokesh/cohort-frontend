import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import authenticate

# Test credentials from CSV file
dummy_students = [
    ('sudharsshana.r.cse.2024@snsce.ac.in', 'pass123@'),
    ('alana.s.iot.2024@snsce.ac.in', 'pass123@'),
    ('bsurya.n.it.2024@snsce.ac.in', 'pass123@'),
    ('gobinath.g.csd.2024@snsce.ac.in', 'pass123@'),
    ('santhosh.m.cse.2024@snsct.org', 'pass123@'),
    ('marlenesaranya.s.cse.2024@snsct.org', 'pass123@'),
    ('mathi.t.cse.2024@snsce.ac.in', 'pass123@'),
    ('pranethi.r.iot.2024@snsce.ac.in', 'pass123@'),
    ('dayanithi.m.cse.2024@snsce.ac.in', 'pass123@'),
    ('jabbastin.k.csd.2024@snsce.ac.in', 'pass123@'),
    ('vishnudharshan.s.csd.2024@snsce.ac.in', 'pass123@'),
]

# Standard test accounts
standard_accounts = [
    ('admin@cohort.edu', 'admin123'),
    ('mentor@cohort.edu', 'mentor123'),
    ('student@cohort.edu', 'student123'),
    ('floorwing@cohort.edu', 'floorwing123'),
]

print("="*80)
print("TESTING ALL LOGIN CREDENTIALS")
print("="*80)

print("\n" + "="*80)
print("STANDARD TEST ACCOUNTS")
print("="*80)

for email, password in standard_accounts:
    user = authenticate(username=email, password=password)
    if user:
        profile = user.profile
        print(f"\n✅ {email}")
        print(f"   Password: {password}")
        print(f"   Role: {profile.role}")
        print(f"   Name: {user.first_name} {user.last_name}")
    else:
        print(f"\n❌ {email} - FAILED")
        print(f"   Password tried: {password}")

print("\n" + "="*80)
print("DUMMY STUDENTS (from CSV)")
print("="*80)

for email, password in dummy_students:
    user = authenticate(username=email, password=password)
    if user:
        profile = user.profile
        print(f"\n✅ {email}")
        print(f"   Password: {password}")
        print(f"   Name: {user.first_name} {user.last_name}")
    else:
        print(f"\n❌ {email} - FAILED")
        print(f"   Password tried: {password}")

print("\n" + "="*80)
print("\nSUMMARY:")
print("If any accounts show FAILED, their passwords may need to be reset.")
print("Run the import script again or manually reset passwords.")
print("="*80 + "\n")
