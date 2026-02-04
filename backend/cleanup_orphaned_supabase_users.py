"""
Cleanup orphaned Supabase users that don't have Django mappings
This will delete Supabase users that were created but failed to map to Django users
"""

import os
import sys
import django

# Add backend to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from supabase import create_client
from apps.auth_supabase.models import SupabaseUserMapping


def get_supabase_admin_client():
    """Create Supabase client with service_role key"""
    url = os.environ.get('SUPABASE_URL')
    service_key = os.environ.get('SUPABASE_SERVICE_ROLE_KEY')
    
    if not url or not service_key:
        raise ValueError('SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set')
    
    return create_client(url, service_key)


def main():
    print('\n🧹 SUPABASE USER CLEANUP')
    print('=' * 80)
    print('\nThis will delete Supabase users that are NOT mapped to Django users.')
    print('⚠️  This action cannot be undone!')
    
    response = input('\nContinue? (y/n): ').lower().strip()
    if response != 'y':
        print('❌ Cleanup cancelled')
        return
    
    supabase = get_supabase_admin_client()
    
    # Get all Supabase users
    print('\n📊 Fetching all Supabase users...')
    result = supabase.auth.admin.list_users()
    all_supabase_users = result.users if hasattr(result, 'users') else []
    
    print(f'   Found {len(all_supabase_users)} users in Supabase')
    
    # Get all mapped Supabase IDs
    mapped_ids = set(SupabaseUserMapping.objects.values_list('supabase_id', flat=True))
    print(f'   Found {len(mapped_ids)} mapped users in Django')
    
    # Find orphaned users
    orphaned_users = [
        user for user in all_supabase_users 
        if user.id not in mapped_ids
    ]
    
    print(f'\n🗑️  Found {len(orphaned_users)} orphaned Supabase users')
    
    if not orphaned_users:
        print('✅ No cleanup needed!')
        return
    
    print('\nOrphaned users:')
    for user in orphaned_users[:20]:  # Show first 20
        print(f'   - {user.email} ({user.id[:8]}...)')
    if len(orphaned_users) > 20:
        print(f'   ... and {len(orphaned_users) - 20} more')
    
    response = input(f'\n⚠️  Delete these {len(orphaned_users)} orphaned users? (y/n): ').lower().strip()
    if response != 'y':
        print('❌ Cleanup cancelled')
        return
    
    # Delete orphaned users
    print('\n🗑️  Deleting orphaned users...')
    deleted = 0
    failed = 0
    
    for user in orphaned_users:
        try:
            supabase.auth.admin.delete_user(user.id)
            deleted += 1
            print(f'   ✅ Deleted: {user.email}')
        except Exception as e:
            failed += 1
            print(f'   ❌ Failed to delete {user.email}: {e}')
    
    print('\n' + '=' * 80)
    print('📈 CLEANUP SUMMARY')
    print('=' * 80)
    print(f'✅ Deleted: {deleted}')
    print(f'❌ Failed: {failed}')
    print('\n✨ Cleanup complete!')


if __name__ == '__main__':
    main()
