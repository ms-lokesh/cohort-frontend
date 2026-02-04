import requests

# Test CORS with the exact same setup as frontend
BASE_URL = "http://127.0.0.1:8000"
LOGIN_URL = f"{BASE_URL}/api/auth/token/"

headers = {
    "Origin": "http://localhost:5176",
    "Content-Type": "application/json",
}

test_data = {
    "username": "jabbastin.k.csd.2024@snsce.ac.in",
    "password": "pass123@"
}

print("="*80)
print("Testing CORS and Login from Frontend Perspective")
print("="*80)
print(f"\nOrigin: {headers['Origin']}")
print(f"Target: {LOGIN_URL}")
print(f"Email: {test_data['username']}")
print(f"Password: {test_data['password']}")
print("\n" + "="*80)

try:
    response = requests.post(LOGIN_URL, json=test_data, headers=headers)
    print(f"\nStatus Code: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ LOGIN SUCCESS!")
        data = response.json()
        print(f"Access Token: {data.get('access', '')[:50]}...")
    else:
        print("❌ LOGIN FAILED!")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"❌ ERROR: {str(e)}")

print("\n" + "="*80)
