#!/usr/bin/env python3
"""
Check user details in Supabase including email confirmation status
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

# Check specific user
test_email = 'priya.k.iot.2024@snsce.ac.in'

print(f'🔍 Checking user: {test_email}\n')

response = supabase.auth.admin.list_users()

for user in response:
    if user.email and user.email.lower() == test_email.lower():
        print('✅ User found in Supabase!')
        print(f'   Email: {user.email}')
        print(f'   User ID: {user.id}')
        print(f'   Email Confirmed: {user.email_confirmed_at is not None}')
        print(f'   Email Confirmed At: {user.email_confirmed_at}')
        print(f'   Created At: {user.created_at}')
        print(f'   Last Sign In: {user.last_sign_in_at}')
        print(f'\n⚠️  Email Confirmation Status: {"CONFIRMED ✅" if user.email_confirmed_at else "NOT CONFIRMED ❌"}')
        
        if not user.email_confirmed_at:
            print('\n🔧 SOLUTION: Users need to confirm their email OR disable email confirmation in Supabase')
            print('\nOption 1: Manually confirm user in Supabase Dashboard')
            print('   → Go to Authentication → Users → Click user → Confirm Email')
            print('\nOption 2: Disable email confirmation (for dev/testing)')
            print('   → Go to Authentication → Settings → Email Auth')
            print('   → Disable "Enable email confirmations"')
        break
else:
    print(f'❌ User {test_email} not found in Supabase')
