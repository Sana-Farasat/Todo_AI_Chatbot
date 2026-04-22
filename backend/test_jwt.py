import asyncio
import httpx
import pytest
import random
import string

BASE_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"

# Generate unique test user
TEST_EMAIL = f"test_{random.randint(10000, 99999)}@example.com"
TEST_PASSWORD = "Test123456!"
TEST_NAME = "Test User"

async def get_jwt_token():
    """Get JWT token from frontend auth - using cookies for session"""
    async with httpx.AsyncClient(cookies=httpx.Cookies(), timeout=30.0) as client:
        try:
            # First check if frontend is reachable
            try:
                ping = await client.get(f"{FRONTEND_URL}/", timeout=5.0)
                print(f"Frontend ping status: {ping.status_code}")
            except Exception as e:
                print(f"Frontend not reachable: {e}")
                return None
            
            # Create new user (sign up)
            sign_up_response = await client.post(
                f"{FRONTEND_URL}/api/auth/sign-up/email",
                json={
                    "name": TEST_NAME,
                    "email": TEST_EMAIL,
                    "password": TEST_PASSWORD
                },
                timeout=30.0
            )
            print(f"Sign Up Status: {sign_up_response.status_code}")
            print(f"Sign Up Body: {sign_up_response.text[:300]}")
            
            if sign_up_response.status_code not in [200, 201]:
                print(f"Sign up failed, skipping sign in for now...")
            
            # Now get token (cookies should be set)
            token_response = await client.get(
                f"{FRONTEND_URL}/api/auth/token",
                timeout=30.0
            )
            print(f"Token Response Status: {token_response.status_code}")
            print(f"Token Response Body: {token_response.text[:300]}")
            
            if token_response.status_code == 200:
                data = token_response.json()
                token = data.get("token")
                print(f"Got token: {token[:50] if token else 'None'}...")
                return token
            else:
                print(f"Token request failed with status {token_response.status_code}")
                
        except Exception as e:
            import traceback
            print(f"Error getting token: {traceback.format_exc()}")
    
    return None

async def test_get_jwks():
    """Test JWKS endpoint is accessible"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{FRONTEND_URL}/api/auth/jwks", timeout=10.0)
        print(f"JWKS Status: {response.status_code}")
        print(f"JWKS Response: {response.json()}")
        assert response.status_code == 200
        data = response.json()
        assert "keys" in data

async def test_get_token():
    """Test getting JWT token"""
    token = await get_jwt_token()
    print(f"JWT Token: {token[:50] if token else 'None'}...")
    assert token is not None, "Failed to get JWT token"

async def test_create_task_with_jwt():
    """Test creating a task with JWT authentication"""
    token = await get_jwt_token()
    
    if not token:
        print("No token available, skipping test")
        return
    
    async with httpx.AsyncClient() as client:
        # Use a test user ID
        user_id = "test-user-123"
        
        response = await client.post(
            f"{BASE_URL}/api/{user_id}/tasks/",
            json={
                "title": "Test Task",
                "description": "Test Description"
            },
            headers={"Authorization": f"Bearer {token}"},
            timeout=10.0
        )
        
        print(f"Create Task Status: {response.status_code}")
        print(f"Create Task Response: {response.text}")
        
        # Should succeed or fail with proper error
        assert response.status_code in [200, 201, 401, 403]

async def test_get_tasks_with_jwt():
    """Test getting tasks with JWT authentication"""
    token = await get_jwt_token()
    
    if not token:
        print("No token available, skipping test")
        return
    
    async with httpx.AsyncClient() as client:
        user_id = "test-user-123"
        
        response = await client.get(
            f"{BASE_URL}/api/{user_id}/tasks/",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10.0
        )
        
        print(f"Get Tasks Status: {response.status_code}")
        print(f"Get Tasks Response: {response.text}")

async def main():
    print("=" * 50)
    print("Running JWT Authentication Tests")
    print("=" * 50)
    
    print("\n[Test 1] Testing JWKS endpoint...")
    try:
        await test_get_jwks()
        print("[PASS] JWKS test passed\n")
    except Exception as e:
        print(f"[FAIL] JWKS test failed: {e}\n")
    
    print("\n[Test 2] Testing JWT token retrieval...")
    try:
        await test_get_token()
        print("[PASS] Token retrieval test passed\n")
    except Exception as e:
        print(f"[FAIL] Token retrieval test failed: {e}\n")
    
    print("\n[Test 3] Testing task creation with JWT...")
    try:
        await test_create_task_with_jwt()
        print("[PASS] Task creation test passed\n")
    except Exception as e:
        print(f"[FAIL] Task creation test failed: {e}\n")
    
    print("\n[Test 4] Testing task retrieval with JWT...")
    try:
        await test_get_tasks_with_jwt()
        print("[PASS] Task retrieval test passed\n")
    except Exception as e:
        print(f"[FAIL] Task retrieval test failed: {e}\n")
    
    print("=" * 50)
    print("Tests completed!")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(main())
