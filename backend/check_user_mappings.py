"""
Check Django users and Supabase mappings
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.auth_supabase.models import SupabaseUserMapping

total = User.objects.count()
mapped = SupabaseUserMapping.objects.count()
unmapped = total - mapped

print(f'\n📊 USER MAPPING STATUS')
print('=' * 50)
print(f'Total Django users:         {total}')
print(f'Users with Supabase mapping: {mapped}')
print(f'Users WITHOUT mapping:       {unmapped}')
print('=' * 50)

if unmapped > 0:
    print(f'\n⚠️  {unmapped} users need to be mapped to Supabase!')
    print('\nUsers without mapping:')
    for user in User.objects.all():
        if not hasattr(user, 'supabase_mapping'):
            print(f'  - {user.email} (ID: {user.id})')
else:
    print('\n✅ All users are properly mapped!')
