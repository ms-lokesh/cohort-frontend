"""
Master script to import all users from both CSV files
Runs both import scripts in sequence
"""

import os
import sys

# Add backend to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print('=' * 80)
print('COHORT USER IMPORT - MASTER SCRIPT')
print('=' * 80)

print('\n📋 This will import users from:')
print('   1. dummy users - Sheet1.csv (11 users)')
print('   2. Untitled spreadsheet - Sheet1.csv (100+ users)')

print('\n⚠️  Make sure you have set these environment variables:')
print('   - SUPABASE_URL')
print('   - SUPABASE_SERVICE_ROLE_KEY')

response = input('\n🚀 Continue? (y/n): ').lower().strip()

if response != 'y':
    print('❌ Import cancelled')
    sys.exit(0)

print('\n' + '=' * 80)
print('PHASE 1: Importing dummy users (with passwords)')
print('=' * 80)

# Import phase 1
try:
    import import_dummy_users_supabase
    import_dummy_users_supabase.main()
except Exception as e:
    print(f'❌ Phase 1 failed: {e}')
    print('Continuing to phase 2...')

print('\n' + '=' * 80)
print('PHASE 2: Importing untitled spreadsheet users')
print('=' * 80)

# Import phase 2
try:
    import import_untitled_spreadsheet
    import_untitled_spreadsheet.main()
except Exception as e:
    print(f'❌ Phase 2 failed: {e}')

print('\n' + '=' * 80)
print('✨ ALL IMPORTS COMPLETE')
print('=' * 80)

print('\n📊 Check the terminal output above for detailed results')
print('📄 Credentials saved to: imported_users_credentials.txt')
print('\n✅ Setup complete! Users can now login to the application.')
