#!/usr/bin/env python3
"""
Get Supabase JWT Secret from project
"""
import os
from dotenv import load_dotenv

load_dotenv('/Users/user/Documents/GitHub/cohort/.env')

print("🔐 Your Supabase Configuration:")
print("=" * 80)
print(f"\nSUPABASE_URL: {os.getenv('SUPABASE_URL')}")
print(f"\nSUPABASE_ANON_KEY:\n{os.getenv('SUPABASE_ANON_KEY')}")
print(f"\nSUPABASE_SERVICE_ROLE_KEY:\n{os.getenv('SUPABASE_SERVICE_ROLE_KEY')}")

print("\n" + "=" * 80)
print("\n📝 To get your JWT Secret:")
print("   1. Go to: https://supabase.com/dashboard/project/yfoopcuwdyotlukbkoej/settings/api")
print("   2. Scroll to 'JWT Settings'")
print("   3. Copy the 'JWT Secret' value")
print("\n💡 The JWT Secret is used to verify JWT tokens issued by Supabase")
print("   It's different from the ANON_KEY and SERVICE_ROLE_KEY")
