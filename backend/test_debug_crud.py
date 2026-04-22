"""
Debug test to understand the exact CRUD errors
"""
import asyncio
import httpx
import jwt
from datetime import datetime, timedelta, timezone

BASE_URL = "http://localhost:8000"
TEST_USER_ID = "test-user-001"


def create_test_token(user_id: str):
    """Create a proper EdDSA-signed token for testing"""
    # For testing with the actual backend, we need to understand what the backend expects
    # The backend uses Better Auth with EdDSA
    # Since we can't sign without the private key, let's create an unsigned token
    # and rely on the fallback in jwt.py
    
    payload = {
        "id": user_id,
        "sub": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }
    
    # Create unsigned token (alg=none)
    # The backend should fall back to unverified payload when JWKS is unavailable
    token = jwt.encode(payload, key="", algorithm="none")
    return token


async def debug_auth_flow():
    """Debug the authentication flow step by step"""
    print("=" * 60)
    print("DEBUG: Testing Authentication Flow")
    print("=" * 60)
    
    token = create_test_token(TEST_USER_ID)
    print(f"\n1. Created token: {token[:50]}...")
    
    # Decode without verification to see payload
    unverified = jwt.decode(token, options={"verify_signature": False})
    print(f"2. Unverified payload: {unverified}")
    
    header = jwt.get_unverified_header(token)
    print(f"3. Token header: {header}")
    
    # Try to make a request
    async with httpx.AsyncClient() as client:
        print(f"\n4. Making GET request to /api/tasks/{TEST_USER_ID}")
        response = await client.get(
            f"{BASE_URL}/api/tasks/{TEST_USER_ID}",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10.0
        )
        
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        
        # Check if it's the fallback behavior
        if response.status_code == 401:
            print("\n[INFO] Backend rejected the token")
            print("This means the fallback is not working or backend is strict about verification")
        elif response.status_code == 200:
            print("\n[OK] Backend accepted the token via fallback")
        else:
            print(f"\n[INFO] Unexpected status: {response.status_code}")


async def debug_route_paths():
    """Test different route path variations"""
    print("\n" + "=" * 60)
    print("DEBUG: Testing Route Path Variations")
    print("=" * 60)
    
    token = create_test_token(TEST_USER_ID)
    
    paths_to_test = [
        f"/api/tasks/{TEST_USER_ID}",
        f"/api/{TEST_USER_ID}/tasks",
        f"/api/tasks/{TEST_USER_ID}/",
        f"/api/{TEST_USER_ID}/tasks/",
    ]
    
    async with httpx.AsyncClient() as client:
        for path in paths_to_test:
            print(f"\nTesting: GET {path}")
            try:
                response = await client.get(
                    f"{BASE_URL}{path}",
                    headers={"Authorization": f"Bearer {token}"},
                    timeout=10.0
                )
                print(f"   Status: {response.status_code}")
                if response.status_code != 404:
                    print(f"   Response: {response.text[:200]}")
            except Exception as e:
                print(f"   Error: {e}")


async def debug_create_task():
    """Debug task creation with detailed error output"""
    print("\n" + "=" * 60)
    print("DEBUG: Testing Task Creation")
    print("=" * 60)
    
    token = create_test_token(TEST_USER_ID)
    
    async with httpx.AsyncClient() as client:
        task_data = {
            "title": "Test Task",
            "description": "Test Description",
            "completed": False
        }
        
        print(f"\nPOST /api/tasks/{TEST_USER_ID}")
        print(f"Body: {task_data}")
        
        response = await client.post(
            f"{BASE_URL}/api/tasks/{TEST_USER_ID}",
            json=task_data,
            headers={"Authorization": f"Bearer {token}"},
            timeout=10.0
        )
        
        print(f"\nStatus: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        print(f"Response: {response.text}")
        
        # Try to parse as JSON
        try:
            error_data = response.json()
            print(f"Parsed JSON: {error_data}")
        except:
            pass


async def main():
    await debug_auth_flow()
    await debug_route_paths()
    await debug_create_task()
    
    print("\n" + "=" * 60)
    print("DEBUG SESSION COMPLETE")
    print("=" * 60)
    print("\nKey findings:")
    print("1. Check if backend accepts unsigned tokens (fallback)")
    print("2. Verify route paths match between frontend and backend")
    print("3. Check JWT middleware logs for detailed error messages")


if __name__ == "__main__":
    asyncio.run(main())
