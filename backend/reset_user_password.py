#!/usr/bin/env python3
"""
Reset password for a specific user in Supabase
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

# User to reset
test_email = 'priya.k.iot.2024@snsce.ac.in'
new_password = 'pass123@'

print(f'🔄 Resetting password for: {test_email}')
print(f'   New password: {new_password}\n')

# Get user ID
response = supabase.auth.admin.list_users()
user_id = None

for user in response:
    if user.email and user.email.lower() == test_email.lower():
        user_id = user.id
        break

if not user_id:
    print(f'❌ User not found: {test_email}')
    sys.exit(1)

print(f'✅ Found user ID: {user_id}')

# Update password using admin API
try:
    result = supabase.auth.admin.update_user_by_id(
        user_id,
        {
            'password': new_password
        }
    )
    print(f'✅ Password updated successfully!')
    print(f'\n🔐 Login credentials:')
    print(f'   Email: {test_email}')
    print(f'   Password: {new_password}')
    
except Exception as e:
    print(f'❌ Failed to update password: {e}')
