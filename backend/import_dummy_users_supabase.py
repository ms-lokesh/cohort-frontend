"""
Script to import users from dummy users CSV file
This version is adapted for the cohort project structure
"""

import os
import sys
import csv
import django

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


def create_user_in_both_systems(email, username, password, send_email=False):
    """Create user in both Supabase and Django"""
    
    print(f'\n📝 Creating user: {email}')
    
    # 1. Create in Supabase
    print('  1️⃣ Creating Supabase user...')
    supabase = get_supabase_admin_client()
    
    try:
        supabase_user = supabase.auth.admin.create_user({
            'email': email,
            'password': password,
            'email_confirm': True,  # Auto-confirm
        })
        
        supabase_id = supabase_user.user.id
        print(f'     ✅ Supabase user created: {supabase_id[:8]}...')
        
    except Exception as e:
        print(f'     ❌ Failed: {e}')
        return None
    
    # 2. Create in Django
    print('  2️⃣ Creating Django user...')
    
    try:
        if User.objects.filter(username=username).exists():
            print(f'     ⚠️  User {username} already exists, using existing')
            django_user = User.objects.filter(username=username).first()
        else:
            django_user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
            )
            print(f'     ✅ Django user created: {username}')
    
    except Exception as e:
        print(f'     ❌ Failed: {e}')
        try:
            supabase.auth.admin.delete_user(supabase_id)
        except:
            pass
        return None
    
    # 3. Create mapping
    print('  3️⃣ Creating mapping...')
    
    try:
        mapping = SupabaseUserMapping.create_mapping(
            django_user=django_user,
            supabase_id=supabase_id,
            supabase_email=email
        )
        print(f'     ✅ Mapping created')
        return {
            'email': email,
            'username': username,
            'supabase_id': supabase_id,
            'django_id': django_user.id,
        }
    
    except Exception as e:
        print(f'     ❌ Failed to create mapping: {e}')
        return None


def main():
    csv_path = '/Users/user/Documents/GitHub/cohort/dummy users - Sheet1.csv'
    
    if not os.path.exists(csv_path):
        print(f'❌ CSV file not found: {csv_path}')
        return
    
    print(f'\n📁 Reading CSV: {csv_path}')
    
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        users = list(reader)
    
    print(f'📊 Found {len(users)} users to import\n')
    print('=' * 80)
    
    results = {'success': [], 'failed': []}
    
    for idx, user_data in enumerate(users, 1):
        email = user_data.get('email', '').strip()
        username = user_data.get('username', '').strip()
        password = user_data.get('password', '').strip()
        
        print(f'\n[{idx}/{len(users)}] {email}')
        
        if not email or not username or not password:
            print('  ❌ Missing required fields')
            results['failed'].append({'email': email, 'error': 'Missing fields'})
            continue
        
        result = create_user_in_both_systems(email, username, password)
        
        if result:
            results['success'].append(result)
        else:
            results['failed'].append({'email': email, 'error': 'Creation failed'})
    
    # Summary
    print('\n' + '=' * 80)
    print('\n📈 IMPORT SUMMARY')
    print('=' * 80)
    print(f'✅ Successful: {len(results["success"])}')
    print(f'❌ Failed: {len(results["failed"])}')
    
    if results['failed']:
        print('\n❌ Failed users:')
        for failed in results['failed']:
            print(f'   - {failed["email"]}: {failed.get("error", "Unknown error")}')
    
    print('\n✨ Import complete!')
    print('\nℹ️  Users can now login with their email and password')


if __name__ == '__main__':
    main()
