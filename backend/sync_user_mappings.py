#!/usr/bin/env python3
"""
Sync User Mappings - Create missing SupabaseUserMapping entries
for Django users that already exist in Supabase
"""

import os
import sys
import django
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.auth_supabase.models import SupabaseUserMapping
from supabase import create_client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_supabase_client():
    """Initialize Supabase client"""
    url = os.environ.get('SUPABASE_URL')
    key = os.environ.get('SUPABASE_SERVICE_ROLE_KEY')
    
    if not url or not key:
        raise ValueError('SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in environment')
    
    return create_client(url, key)

def sync_mappings():
    """Sync mappings between Django users and Supabase users"""
    
    print("\n🔄 SYNCING USER MAPPINGS")
    print("=" * 80)
    
    # Get Django users without mappings
    unmapped_users = User.objects.exclude(
        id__in=SupabaseUserMapping.objects.values_list('django_user_id', flat=True)
    ).order_by('email')
    
    print(f"📊 Found {unmapped_users.count()} unmapped Django users\n")
    
    if unmapped_users.count() == 0:
        print("✅ All users are already mapped!")
        return
    
    # Initialize Supabase client
    try:
        supabase = get_supabase_client()
    except Exception as e:
        print(f"❌ Failed to connect to Supabase: {e}")
        return
    
    # Fetch all Supabase users
    print("📥 Fetching Supabase users...")
    try:
        response = supabase.auth.admin.list_users()
        supabase_users = {user.email.lower(): user.id for user in response if user.email}
        print(f"✅ Found {len(supabase_users)} Supabase users\n")
    except Exception as e:
        print(f"❌ Failed to fetch Supabase users: {e}")
        return
    
    # Match and create mappings
    created = 0
    not_found = 0
    errors = 0
    
    print("🔗 Creating mappings...\n")
    
    for i, user in enumerate(unmapped_users, 1):
        email = user.email.lower()
        print(f"[{i}/{unmapped_users.count()}] {user.email}")
        
        if email in supabase_users:
            supabase_id = supabase_users[email]
            try:
                # Create mapping
                SupabaseUserMapping.objects.create(
                    django_user=user,
                    supabase_id=supabase_id,
                    supabase_email=email
                )
                print(f"   ✅ Created mapping: {supabase_id[:12]}...")
                created += 1
            except Exception as e:
                print(f"   ❌ Error creating mapping: {e}")
                errors += 1
        else:
            print(f"   ⚠️  Not found in Supabase")
            not_found += 1
        
        print()
    
    # Summary
    print("=" * 80)
    print("📊 SYNC SUMMARY")
    print("=" * 80)
    print(f"✅ Mappings created: {created}")
    print(f"⚠️  Users not found in Supabase: {not_found}")
    print(f"❌ Errors: {errors}")
    print("=" * 80)
    
    # Final count
    total_users = User.objects.count()
    total_mapped = SupabaseUserMapping.objects.count()
    remaining = total_users - total_mapped
    
    print(f"\n📈 FINAL STATUS")
    print(f"   Total Django users: {total_users}")
    print(f"   Users with mappings: {total_mapped}")
    print(f"   Users without mappings: {remaining}")
    
    if remaining == 0:
        print("\n🎉 All users are now mapped!")
    else:
        print(f"\n⚠️  {remaining} users still need Supabase accounts")

if __name__ == '__main__':
    try:
        sync_mappings()
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
