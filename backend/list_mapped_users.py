#!/usr/bin/env python3
"""
List all users with Supabase mappings - ready to login
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

def list_mapped_users():
    """List all users with Supabase mappings"""
    
    print("\n✅ USERS READY TO LOGIN")
    print("=" * 80)
    
    mappings = SupabaseUserMapping.objects.select_related('django_user').order_by('django_user__email')
    
    print(f"Total users with mappings: {mappings.count()}\n")
    
    for i, mapping in enumerate(mappings, 1):
        user = mapping.django_user
        print(f"{i:3d}. {user.email}")
        print(f"     Django ID: {user.id} | Supabase ID: {mapping.supabase_id[:12]}...")
        print(f"     Last login: {user.last_login or 'Never'}")
        print()
    
    print("=" * 80)
    print("\n💡 TIP: If users don't know their passwords, you can:")
    print("   1. Check what password was used in the original import")
    print("   2. Use Supabase dashboard to reset passwords")
    print("   3. Create a password reset script")

if __name__ == '__main__':
    list_mapped_users()
