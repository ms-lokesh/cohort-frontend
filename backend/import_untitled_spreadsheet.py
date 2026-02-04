"""
Script to import users from Untitled spreadsheet CSV file
This CSV has a different format with FullName, email, phone, reg number, etc.
Passwords will be auto-generated for security
"""

import os
import sys
import csv
import django
import secrets
import string

# Add backend to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from supabase import create_client
from django.contrib.auth.models import User
from apps.auth_supabase.models import SupabaseUserMapping


def get_supabase_admin_client():
    """Create Supabase client with service_role key"""
    url = os.environ.get('SUPABASE_URL')
    service_key = os.environ.get('SUPABASE_SERVICE_ROLE_KEY')
    
    if not url or not service_key:
        raise ValueError('SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in environment')
    
    return create_client(url, service_key)


def generate_username_from_email(email):
    """Extract username from email (part before @)"""
    return email.split('@')[0].replace('.', '_')


def create_user_in_both_systems(email, full_name, password='TempPass@2024', send_email=False):
    """Create user in both Supabase and Django"""
    
    username = generate_username_from_email(email)
    
    print(f'  📝 {email}')
    
    # 1. Create in Supabase
    supabase = get_supabase_admin_client()
    
    try:
        supabase_user = supabase.auth.admin.create_user({
            'email': email,
            'password': password,
            'email_confirm': True,  # Auto-confirm
            'user_metadata': {
                'full_name': full_name
            }
        })
        
        supabase_id = supabase_user.user.id
        print(f'     ✅ Supabase: {supabase_id[:8]}...')
        
    except Exception as e:
        if 'already been registered' in str(e):
            print(f'     ⚠️  Already exists in Supabase')
            return None
        print(f'     ❌ Supabase failed: {e}')
        return None
    
    # 2. Create in Django
    try:
        if User.objects.filter(username=username).exists():
            print(f'     ⚠️  Django user exists')
            django_user = User.objects.filter(username=username).first()
        elif User.objects.filter(email=email).exists():
            print(f'     ⚠️  Django email exists')
            django_user = User.objects.filter(email=email).first()
        else:
            # Split full name into first and last name
            name_parts = full_name.strip().split(maxsplit=1)
            first_name = name_parts[0] if name_parts else ''
            last_name = name_parts[1] if len(name_parts) > 1 else ''
            
            django_user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
            print(f'     ✅ Django: {username}')
    
    except Exception as e:
        print(f'     ❌ Django failed: {e}')
        try:
            supabase.auth.admin.delete_user(supabase_id)
        except:
            pass
        return None
    
    # 3. Create mapping
    try:
        if SupabaseUserMapping.objects.filter(supabase_id=supabase_id).exists():
            print(f'     ⚠️  Mapping exists')
            return None
            
        mapping = SupabaseUserMapping.create_mapping(
            django_user=django_user,
            supabase_id=supabase_id,
            supabase_email=email
        )
        print(f'     ✅ Mapped')
        return {
            'email': email,
            'username': username,
            'full_name': full_name,
            'password': password,
        }
    
    except Exception as e:
        print(f'     ❌ Mapping failed: {e}')
        return None


def main():
    csv_path = '/Users/user/Documents/GitHub/cohort/Untitled spreadsheet - Sheet1.csv'
    
    if not os.path.exists(csv_path):
        print(f'❌ CSV file not found: {csv_path}')
        return
    
    print(f'\n📁 Reading CSV: {csv_path}')
    
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        users = list(reader)
    
    print(f'📊 Found {len(users)} users to import\n')
    print('=' * 80)
    
    # Ask for password option
    print('\nPassword options:')
    print('1. Use default password for all users: TempPass@2024')
    print('2. Generate random passwords (will be saved to file)')
    
    choice = input('\nEnter choice (1 or 2, default=1): ').strip() or '1'
    
    use_random = choice == '2'
    default_password = 'TempPass@2024'
    
    results = {'success': [], 'failed': [], 'skipped': []}
    
    for idx, user_data in enumerate(users, 1):
        email = user_data.get('College Domain Mail ID', '').strip()
        full_name = user_data.get('FullName', '').strip()
        
        if not email or not full_name:
            continue
        
        # Clean email (remove spaces)
        email = email.replace(' ', '')
        
        # Skip invalid emails
        if '@' not in email or email.startswith('@'):
            print(f'  ⚠️  Invalid email: {email}')
            results['skipped'].append(email)
            continue
        
        print(f'\n[{idx}/{len(users)}]')
        
        # Generate or use default password
        if use_random:
            password = ''.join(secrets.choice(string.ascii_letters + string.digits + '!@#$') for _ in range(12))
        else:
            password = default_password
        
        result = create_user_in_both_systems(email, full_name, password)
        
        if result:
            results['success'].append(result)
        else:
            results['failed'].append({'email': email, 'name': full_name})
    
    # Summary
    print('\n' + '=' * 80)
    print('\n📈 IMPORT SUMMARY')
    print('=' * 80)
    print(f'✅ Successful: {len(results["success"])}')
    print(f'❌ Failed: {len(results["failed"])}')
    print(f'⏭️  Skipped: {len(results["skipped"])}')
    
    if results['failed']:
        print('\n❌ Failed users:')
        for failed in results['failed'][:10]:  # Show first 10
            print(f'   - {failed["email"]}')
        if len(results['failed']) > 10:
            print(f'   ... and {len(results["failed"]) - 10} more')
    
    # Save credentials to file
    if results['success']:
        creds_file = 'imported_users_credentials.txt'
        with open(creds_file, 'w') as f:
            f.write('=' * 80 + '\n')
            f.write('IMPORTED USER CREDENTIALS\n')
            f.write('=' * 80 + '\n\n')
            
            if use_random:
                f.write('⚠️  IMPORTANT: Random passwords generated - save this file securely!\n\n')
            else:
                f.write(f'Default password for all users: {default_password}\n\n')
            
            f.write(f'Total users created: {len(results["success"])}\n\n')
            f.write('-' * 80 + '\n\n')
            
            for user in results['success']:
                f.write(f"Email: {user['email']}\n")
                f.write(f"Name: {user['full_name']}\n")
                f.write(f"Username: {user['username']}\n")
                if use_random:
                    f.write(f"Password: {user['password']}\n")
                f.write('\n')
        
        print(f'\n📄 Credentials saved to: {creds_file}')
    
    print('\n✨ Import complete!')
    print('\nℹ️  Users can now login with their email and password')
    if not use_random:
        print(f'ℹ️  Default password: {default_password}')
        print('⚠️  Users should change their password after first login')


if __name__ == '__main__':
    main()
