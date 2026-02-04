#!/usr/bin/env python3
"""
Test login flow from terminal
"""
import requests
from supabase import create_client

# Configuration
SUPABASE_URL = "https://yfoopcuwdyotlukbkoej.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlmb29wY3V3ZHlvdGx1a2Jrb2VqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njk4MDA4NDEsImV4cCI6MjA4NTM3Njg0MX0.YK5uw24Grhc2TPYnF98i0eORgZHNHLJMdd5akenvKRs"
API_BASE_URL = "https://cohort-37ur.onrender.com/api"

# Test credentials
test_email = "priya.k.iot.2024@snsce.ac.in"
test_password = "pass123@"

print("🧪 Testing Login Flow")
print("=" * 80)

# Step 1: Login to Supabase
print("\n1️⃣ Logging into Supabase...")
supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

try:
    response = supabase.auth.sign_in_with_password({
        "email": test_email,
        "password": test_password
    })
    
    print(f"   ✅ Supabase login successful!")
    print(f"   User ID: {response.user.id}")
    print(f"   Email: {response.user.email}")
    
    access_token = response.session.access_token
    print(f"   Access Token: {access_token[:50]}...")
    
except Exception as e:
    print(f"   ❌ Supabase login failed: {e}")
    exit(1)

# Step 2: Test Django API with token
print("\n2️⃣ Testing Django API with Supabase token...")

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# Test dashboard endpoint
try:
    response = requests.get(f"{API_BASE_URL}/dashboard/stats/", headers=headers)
    print(f"   Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print(f"   ✅ API call successful!")
        data = response.json()
        print(f"   Response keys: {list(data.keys())}")
    else:
        print(f"   ❌ API call failed")
        print(f"   Response: {response.text[:200]}")
        
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 80)
print("✅ Login test complete!")
