#!/usr/bin/env python3
"""
Test if users were synced to the live Render deployment
"""
import requests

API_URL = "https://cohort-37ur.onrender.com/api"

# Try to login with test credentials
print("🧪 Testing Render deployment...")
print("=" * 80)

# Test 1: Health check
print("\n1️⃣ Testing API health...")
try:
    response = requests.get(f"{API_URL}/health/")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 2: Try to fetch user profile (will fail if not logged in, but shows if endpoint exists)
print("\n2️⃣ Testing auth endpoint availability...")
try:
    # Try login with Supabase token
    test_email = "priya.k.iot.2024@snsce.ac.in"
    test_password = "pass123@"
    
    # Note: This won't work without proper Supabase integration on backend
    # But we can check if the endpoint exists
    response = requests.post(f"{API_URL}/auth/token/", json={
        "username": test_email,
        "password": test_password
    })
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✅ Login successful!")
        print(f"   Response keys: {list(response.json().keys())}")
    else:
        print(f"   Response: {response.text[:200]}")
except Exception as e:
    print(f"   Error: {e}")

print("\n" + "=" * 80)
print("\n💡 To fully test:")
print("   1. Open browser DevTools (F12)")
print("   2. Go to Console tab")
print("   3. Login at https://cohort-37ur.onrender.com")
print("   4. Check for any errors in console")
