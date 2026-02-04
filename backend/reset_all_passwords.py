#!/usr/bin/env python3
"""
Reset passwords for ALL users in Supabase to a standard password
"""
import os
import sys
from pathlib import Path
from supabase import create_client
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

url = os.environ.get('SUPABASE_URL')
key = os.environ.get('SUPABASE_SERVICE_ROLE_KEY')

supabase = create_client(url, key)

# Standard password for all users
STANDARD_PASSWORD = 'pass123@'

print('🔄 RESETTING ALL USER PASSWORDS')
print('=' * 80)
print(f'   New password for all users: {STANDARD_PASSWORD}\n')

# Get all users
response = supabase.auth.admin.list_users()

print(f'📊 Found {len(response)} users to update\n')

success = 0
failed = 0

for i, user in enumerate(response, 1):
    email = user.email if user.email else 'No email'
    user_id = user.id
    
    print(f'[{i}/{len(response)}] {email:<45}', end=' ')
    
    try:
        supabase.auth.admin.update_user_by_id(
            user_id,
            {'password': STANDARD_PASSWORD}
        )
        print('✅')
        success += 1
    except Exception as e:
        print(f'❌ {str(e)[:30]}')
        failed += 1

print('\n' + '=' * 80)
print('📈 SUMMARY')
print('=' * 80)
print(f'✅ Successfully updated: {success}')
print(f'❌ Failed: {failed}')
print(f'\n🔐 All users can now login with password: {STANDARD_PASSWORD}')
