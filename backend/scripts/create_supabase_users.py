"""
Script to create users in both Django and Supabase

Usage:
    python backend/scripts/create_supabase_users.py --email user@example.com --username john_doe --password SecurePass123

Environment variables required:
    SUPABASE_URL: Your Supabase project URL
    SUPABASE_SERVICE_ROLE_KEY: Service role key (admin access) - NEVER use in frontend!
"""

import os
import sys
import django
import argparse
from supabase import create_client, Client

# Add backend to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.auth_supabase.models import SupabaseUserMapping


def get_supabase_admin_client() -> Client:
    """
    Create Supabase client with service_role key (admin access)
    WARNING: This key has admin privileges - NEVER expose in frontend!
    """
    url = os.environ.get('SUPABASE_URL')
    service_key = os.environ.get('SUPABASE_SERVICE_ROLE_KEY')
    
    if not url or not service_key:
        raise ValueError('SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set')
    
    return create_client(url, service_key)


def create_user(email: str, username: str, password: str, 
                first_name: str = '', last_name: str = '', 
                is_staff: bool = False, is_superuser: bool = False,
                send_email: bool = False):
    """
    Create user in both Django and Supabase
    
    Args:
        email: User email address
        username: Django username
        password: Initial password
        first_name: User first name (optional)
        last_name: User last name (optional)
        is_staff: Django staff status
        is_superuser: Django superuser status
        send_email: Send password reset email instead of setting password
    
    Returns:
        dict: Created user info
    """
    
    print(f'\n📝 Creating user: {email}')
    
    # 1. Create user in Supabase
    print('1️⃣ Creating Supabase user...')
    supabase = get_supabase_admin_client()
    
    try:
        # Create auth user in Supabase
        supabase_user = supabase.auth.admin.create_user({
            'email': email,
            'password': password,
            'email_confirm': not send_email,  # Auto-confirm if not sending email
        })
        
        supabase_id = supabase_user.user.id
        print(f'   ✅ Supabase user created: {supabase_id}')
        
    except Exception as e:
        print(f'   ❌ Failed to create Supabase user: {e}')
        return None
    
    # 2. Create user in Django
    print('2️⃣ Creating Django user...')
    
    try:
        # Check if user exists
        if User.objects.filter(username=username).exists():
            print(f'   ⚠️  User {username} already exists in Django')
            django_user = User.objects.get(username=username)
        else:
            django_user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                is_staff=is_staff,
                is_superuser=is_superuser,
            )
            print(f'   ✅ Django user created: {username}')
    
    except Exception as e:
        print(f'   ❌ Failed to create Django user: {e}')
        # Cleanup: Delete Supabase user
        try:
            supabase.auth.admin.delete_user(supabase_id)
            print('   🧹 Cleaned up Supabase user')
        except:
            pass
        return None
    
    # 3. Create mapping
    print('3️⃣ Creating user mapping...')
    
    try:
        mapping = SupabaseUserMapping.create_mapping(
            django_user=django_user,
            supabase_id=supabase_id,
            supabase_email=email
        )
        print(f'   ✅ Mapping created')
    
    except Exception as e:
        print(f'   ❌ Failed to create mapping: {e}')
        # Cleanup
        try:
            django_user.delete()
            supabase.auth.admin.delete_user(supabase_id)
            print('   🧹 Cleaned up both users')
        except:
            pass
        return None
    
    # 4. Send password reset email (optional)
    if send_email:
        print('4️⃣ Sending password reset email...')
        try:
            supabase.auth.admin.generate_link({
                'type': 'recovery',
                'email': email,
            })
            print(f'   ✅ Password reset email sent to {email}')
        except Exception as e:
            print(f'   ⚠️  Failed to send email: {e}')
    
    print(f'\n✨ User created successfully!')
    print(f'   Email: {email}')
    print(f'   Username: {username}')
    print(f'   Supabase ID: {supabase_id}')
    print(f'   Django ID: {django_user.id}')
    
    if send_email:
        print(f'   📧 Password reset email sent')
    else:
        print(f'   🔑 Password: {password}')
    
    return {
        'email': email,
        'username': username,
        'supabase_id': supabase_id,
        'django_id': django_user.id,
    }


def main():
    parser = argparse.ArgumentParser(description='Create user in Django and Supabase')
    parser.add_argument('--email', required=True, help='User email address')
    parser.add_argument('--username', required=True, help='Django username')
    parser.add_argument('--password', required=True, help='Initial password')
    parser.add_argument('--first-name', default='', help='First name')
    parser.add_argument('--last-name', default='', help='Last name')
    parser.add_argument('--staff', action='store_true', help='Make user staff')
    parser.add_argument('--superuser', action='store_true', help='Make user superuser')
    parser.add_argument('--send-email', action='store_true', 
                       help='Send password reset email instead of setting password')
    
    args = parser.parse_args()
    
    result = create_user(
        email=args.email,
        username=args.username,
        password=args.password,
        first_name=args.first_name,
        last_name=args.last_name,
        is_staff=args.staff,
        is_superuser=args.superuser,
        send_email=args.send_email,
    )
    
    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
