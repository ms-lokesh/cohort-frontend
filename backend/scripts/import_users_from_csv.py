"""
Script to import multiple users from CSV file

CSV Format:
    email,username,first_name,last_name,is_staff,is_superuser
    john@example.com,john_doe,John,Doe,0,0
    admin@example.com,admin,Admin,User,1,1

Usage:
    python backend/scripts/import_users_from_csv.py --csv users.csv --send-email

Environment variables required:
    SUPABASE_URL: Your Supabase project URL
    SUPABASE_SERVICE_ROLE_KEY: Service role key (admin access)
"""

import os
import sys
import csv
import django
import argparse
import secrets
import string

# Add backend to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from create_supabase_users import create_user


def generate_random_password(length=16):
    """Generate a secure random password"""
    alphabet = string.ascii_letters + string.digits + '!@#$%^&*'
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def parse_bool(value):
    """Parse boolean from CSV (1, 0, true, false, yes, no)"""
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    value = str(value).lower().strip()
    return value in ('1', 'true', 'yes', 'y')


def import_users_from_csv(csv_path: str, send_email: bool = False, 
                          default_password: str = None):
    """
    Import multiple users from CSV file
    
    Args:
        csv_path: Path to CSV file
        send_email: Send password reset email to each user
        default_password: Default password for all users (if not sending email)
    """
    
    if not os.path.exists(csv_path):
        print(f'❌ CSV file not found: {csv_path}')
        return
    
    print(f'\n📁 Reading CSV: {csv_path}')
    
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        users = list(reader)
    
    print(f'📊 Found {len(users)} users to import\n')
    print('=' * 80)
    
    results = {
        'success': [],
        'failed': [],
    }
    
    for idx, user_data in enumerate(users, 1):
        print(f'\n[{idx}/{len(users)}] Processing {user_data.get("email")}')
        
        try:
            # Extract data
            email = user_data.get('email', '').strip()
            username = user_data.get('username', '').strip()
            first_name = user_data.get('first_name', '').strip()
            last_name = user_data.get('last_name', '').strip()
            is_staff = parse_bool(user_data.get('is_staff', False))
            is_superuser = parse_bool(user_data.get('is_superuser', False))
            
            # Validate required fields
            if not email or not username:
                print(f'   ❌ Missing required fields (email or username)')
                results['failed'].append({
                    'email': email,
                    'error': 'Missing required fields'
                })
                continue
            
            # Generate or use default password
            if send_email:
                # Password will be set via email reset link
                password = generate_random_password()
            elif default_password:
                password = default_password
            else:
                # Generate unique password for each user
                password = generate_random_password()
            
            # Create user
            result = create_user(
                email=email,
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                is_staff=is_staff,
                is_superuser=is_superuser,
                send_email=send_email,
            )
            
            if result:
                results['success'].append(result)
            else:
                results['failed'].append({
                    'email': email,
                    'error': 'Creation failed'
                })
        
        except Exception as e:
            print(f'   ❌ Unexpected error: {e}')
            results['failed'].append({
                'email': user_data.get('email', 'unknown'),
                'error': str(e)
            })
    
    # Print summary
    print('\n' + '=' * 80)
    print('\n📈 IMPORT SUMMARY')
    print('=' * 80)
    print(f'✅ Successful: {len(results["success"])}')
    print(f'❌ Failed: {len(results["failed"])}')
    
    if results['failed']:
        print('\n❌ Failed users:')
        for failed in results['failed']:
            print(f'   - {failed["email"]}: {failed["error"]}')
    
    if results['success'] and not send_email:
        print('\n🔑 Created users (save these credentials):')
        for user in results['success']:
            print(f'   - {user["email"]} ({user["username"]})')
    
    print('\n✨ Import complete!')


def main():
    parser = argparse.ArgumentParser(description='Import users from CSV')
    parser.add_argument('--csv', required=True, help='Path to CSV file')
    parser.add_argument('--send-email', action='store_true', 
                       help='Send password reset email to each user')
    parser.add_argument('--default-password', 
                       help='Use same password for all users (if not sending email)')
    
    args = parser.parse_args()
    
    import_users_from_csv(
        csv_path=args.csv,
        send_email=args.send_email,
        default_password=args.default_password,
    )


if __name__ == '__main__':
    main()
