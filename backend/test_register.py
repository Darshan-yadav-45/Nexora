import urllib.request
import urllib.error
import json
import traceback

data = json.dumps({
    "email": "test7@example.com",
    "password": "testpassword",
    "first_name": "Test",
    "last_name": "User"
}).encode('utf-8')

req = urllib.request.Request(
    "http://localhost:8000/api/auth/register",
    data=data,
    headers={'Content-Type': 'application/json'},
    method='POST'
)

try:
    with urllib.request.urlopen(req) as response:
        print(f"Status: {response.getcode()}")
        print(f"Response: {response.read().decode('utf-8')}")
except urllib.error.HTTPError as e:
    print(f"HTTPError: {e.code}")
    print(f"Response: {e.read().decode('utf-8')}")
except Exception as e:
    print("Exception occurred!")
    traceback.print_exc()
