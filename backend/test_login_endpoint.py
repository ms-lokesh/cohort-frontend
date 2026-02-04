import requests
import json

BASE_URL = "http://127.0.0.1:8000"
LOGIN_URL = f"{BASE_URL}/api/auth/token/"

test_accounts = [
    ("admin@cohort.edu", "admin123", "ADMIN"),
    ("mentor@cohort.edu", "mentor123", "MENTOR"),
    ("student@cohort.edu", "student123", "STUDENT"),
    ("floorwing@cohort.edu", "floorwing123", "FLOOR_WING"),
    ("sudharsshana.r.cse.2024@snsce.ac.in", "pass123@", "STUDENT"),
]

print("="*80)
print("TESTING LOGIN API ENDPOINT")
print("="*80)

for email, password, expected_role in test_accounts:
    print(f"\n{'='*80}")
    print(f"Testing: {email}")
    print(f"Password: {password}")
    print(f"Expected Role: {expected_role}")
    print('-'*80)
    
    try:
        response = requests.post(
            LOGIN_URL,
            json={"username": email, "password": password},
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ LOGIN SUCCESSFUL!")
            print(f"Access Token: {data.get('access', '')[:50]}...")
            print(f"Refresh Token: {data.get('refresh', '')[:50]}...")
            
            # Try to get user info
            if 'access' in data:
                user_url = f"{BASE_URL}/api/auth/user/"
                headers = {"Authorization": f"Bearer {data['access']}"}
                user_response = requests.get(user_url, headers=headers)
                
                if user_response.status_code == 200:
                    user_data = user_response.json()
                    print(f"\nUser Info:")
                    print(f"  Email: {user_data.get('email')}")
                    print(f"  Name: {user_data.get('first_name')} {user_data.get('last_name')}")
                    print(f"  Role: {user_data.get('profile', {}).get('role')}")
                else:
                    print(f"❌ Failed to get user info: {user_response.status_code}")
        else:
            print("❌ LOGIN FAILED!")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

print("\n" + "="*80)
print("\nIf all tests show ✅, the login system is working correctly.")
print("If you see errors, check:")
print("  1. Backend server is running on http://127.0.0.1:8000")
print("  2. JWT authentication is properly configured")
print("  3. CORS settings allow frontend requests")
print("="*80 + "\n")
