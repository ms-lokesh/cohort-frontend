"""
Script to clean up duplicate Django User records
Keeps the most recent user for each email and removes older duplicates
"""

import os
import sys
import django
from collections import defaultdict

# Add backend to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.auth_supabase.models import SupabaseUserMapping


def find_duplicate_users():
    """Find all email addresses that have multiple User records"""
    email_counts = defaultdict(list)
    
    for user in User.objects.all().order_by('email', '-date_joined'):
        email_counts[user.email].append(user)
    
    duplicates = {email: users for email, users in email_counts.items() if len(users) > 1}
    return duplicates


def cleanup_duplicates(dry_run=True):
    """Remove duplicate users, keeping the most recent one"""
    
    print("\n🔍 DUPLICATE DJANGO USER CLEANUP")
    print("=" * 80)
    
    duplicates = find_duplicate_users()
    
    if not duplicates:
        print("✅ No duplicate users found!")
        return
    
    print(f"\n📊 Found {len(duplicates)} emails with duplicate users:\n")
    
    total_to_delete = 0
    
    for email, users in duplicates.items():
        print(f"📧 {email}: {len(users)} duplicates")
        
        # Sort by date_joined (most recent first)
        users_sorted = sorted(users, key=lambda u: u.date_joined, reverse=True)
        keeper = users_sorted[0]
        to_delete = users_sorted[1:]
        
        print(f"   ✅ Keep: User #{keeper.id} (joined: {keeper.date_joined})")
        
        # Check if keeper has Supabase mapping
        has_mapping = SupabaseUserMapping.objects.filter(django_user=keeper).exists()
        if has_mapping:
            mapping = SupabaseUserMapping.objects.get(django_user=keeper)
            print(f"      🔗 Has Supabase mapping: {mapping.supabase_id[:8]}...")
        else:
            print(f"      ⚠️  No Supabase mapping")
        
        for user in to_delete:
            print(f"   🗑️  Delete: User #{user.id} (joined: {user.date_joined})")
            
            # Check if this user has any important data
            has_mapping = SupabaseUserMapping.objects.filter(django_user=user).exists()
            if has_mapping:
                mapping = SupabaseUserMapping.objects.get(django_user=user)
                print(f"      ⚠️  Has Supabase mapping: {mapping.supabase_id[:8]}... (will be deleted)")
            
            total_to_delete += 1
        
        print()
    
    print("=" * 80)
    print(f"📊 SUMMARY:")
    print(f"   Total emails with duplicates: {len(duplicates)}")
    print(f"   Total users to delete: {total_to_delete}")
    print("=" * 80)
    
    if dry_run:
        print("\n⚠️  DRY RUN MODE - No changes made")
        print("Run with dry_run=False to actually delete duplicates")
        return
    
    # Confirm before deletion
    print("\n⚠️  WARNING: This will permanently delete duplicate user records!")
    response = input("Continue? (yes/no): ")
    
    if response.lower() != 'yes':
        print("❌ Cancelled")
        return
    
    # Perform deletion
    deleted_count = 0
    for email, users in duplicates.items():
        users_sorted = sorted(users, key=lambda u: u.date_joined, reverse=True)
        to_delete = users_sorted[1:]
        
        for user in to_delete:
            # Delete Supabase mapping if exists
            SupabaseUserMapping.objects.filter(django_user=user).delete()
            # Delete user
            user.delete()
            deleted_count += 1
    
    print(f"\n✅ Deleted {deleted_count} duplicate users!")
    print("✅ Cleanup complete!")


if __name__ == '__main__':
    import sys
    
    # Check if --execute flag is passed
    execute = '--execute' in sys.argv
    
    if execute:
        print("🚀 EXECUTING CLEANUP (will delete duplicates)\n")
        cleanup_duplicates(dry_run=False)
    else:
        print("🔍 DRY RUN MODE (no changes will be made)")
        print("   Run with --execute flag to actually delete duplicates\n")
        cleanup_duplicates(dry_run=True)
