#!/usr/bin/env python3
"""
List all users in Supabase Auth database
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

if not url or not key:
    print('❌ Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY')
    sys.exit(1)

print('🔐 Connecting to Supabase...')
print(f'URL: {url}\n')

supabase = create_client(url, key)

print('📥 Fetching all users from Supabase Auth...\n')
response = supabase.auth.admin.list_users()

print(f'✅ Found {len(response)} users\n')
print('=' * 100)
print(f'{"#":<5} {"EMAIL":<45} {"USER ID":<40}')
print('=' * 100)

for i, user in enumerate(response, 1):
    email = user.email if user.email else 'No email'
    user_id = user.id if user.id else 'No ID'
    created = user.created_at if hasattr(user, 'created_at') else 'Unknown'
    print(f'{i:<5} {email:<45} {user_id}')

print('=' * 100)
print(f'\n📊 Total users in Supabase Auth: {len(response)}')
print('\n⚠️  Note: Passwords are hashed (bcrypt) and cannot be displayed')
print('💡 To reset a password, users must use "Forgot Password" or you can reset via Supabase dashboard')
print('\n🔍 To check if a user can login, try the credentials that were used during import')
