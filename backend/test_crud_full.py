"""
Full integration test with user signup and CRUD operations
"""
import asyncio
import httpx
import random
import string


BASE_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"

# Generate unique test user
TEST_EMAIL = f"test_{random.randint(10000, 99999)}@example.com"
TEST_PASSWORD = "Test123456!"
TEST_NAME = "Test User"


async def signup_and_get_token():
    """Sign up a new user and get JWT token"""
    async with httpx.AsyncClient(cookies=httpx.Cookies(), timeout=30.0) as client:
        try:
            print(f"Signing up user: {TEST_EMAIL}")
            
            # Sign up
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
            
            if sign_up_response.status_code not in [200, 201]:
                print(f"Sign up failed: {sign_up_response.text[:200]}")
                # Try to sign in instead
                print("Trying to sign in...")
                sign_in_response = await client.post(
                    f"{FRONTEND_URL}/api/auth/sign-in/email",
                    json={
                        "email": TEST_EMAIL,
                        "password": TEST_PASSWORD
                    },
                    timeout=30.0
                )
                print(f"Sign In Status: {sign_in_response.status_code}")
            
            # Get token
            token_response = await client.get(
                f"{FRONTEND_URL}/api/auth/token",
                timeout=30.0
            )
            print(f"Token Response Status: {token_response.status_code}")
            
            if token_response.status_code == 200:
                data = token_response.json()
                token = data.get("token")
                print(f"Got token: {token[:50] if token else 'None'}...")
                return token, client.cookies
            
            return None, client.cookies
            
        except Exception as e:
            print(f"Error: {e}")
            return None, httpx.Cookies()


async def test_full_crud_with_signup():
    """Test full CRUD flow after signing up"""
    print("=" * 60)
    print("FULL CRUD TEST WITH USER SIGNUP")
    print("=" * 60)
    
    # Get token
    token, cookies = await signup_and_get_token()
    
    if not token:
        print("\n[FAIL] Could not get JWT token")
        print("Make sure:")
        print("1. Frontend is running on http://localhost:3000")
        print("2. Backend is running on http://localhost:8000")
        print("3. Database is configured correctly")
        return
    
    print(f"\n[OK] Got JWT token for testing")
    
    # Use a test user ID
    user_id = "test-user-crud"
    
    async with httpx.AsyncClient(cookies=cookies, timeout=30.0) as client:
        headers = {"Authorization": f"Bearer {token}"}
        
        print("\n" + "=" * 60)
        print("TESTING CRUD OPERATIONS")
        print("=" * 60)
        
        # CREATE
        print("\n1. CREATE task...")
        create_response = await client.post(
            f"{BASE_URL}/api/tasks/{user_id}",
            json={"title": "Test Task", "description": "Test Description"},
            headers=headers,
            timeout=10.0
        )
        print(f"   Status: {create_response.status_code}")
        print(f"   Response: {create_response.text[:300]}")
        
        if create_response.status_code not in [200, 201]:
            print(f"   [FAIL] CREATE failed")
            return
        
        task_data = create_response.json()
        task_id = task_data.get("id")
        print(f"   [OK] Created task with ID: {task_id}")
        
        # READ
        print("\n2. READ tasks...")
        get_response = await client.get(
            f"{BASE_URL}/api/tasks/{user_id}",
            headers=headers,
            timeout=10.0
        )
        print(f"   Status: {get_response.status_code}")
        print(f"   Response: {get_response.json()}")
        
        if get_response.status_code == 200:
            tasks = get_response.json()
            print(f"   [OK] Found {len(tasks)} task(s)")
        else:
            print(f"   [FAIL] READ failed")
        
        # UPDATE
        print("\n3. UPDATE task...")
        update_response = await client.put(
            f"{BASE_URL}/api/tasks/{user_id}/{task_id}",
            json={"title": "Updated Title", "description": "Updated Description"},
            headers=headers,
            timeout=10.0
        )
        print(f"   Status: {update_response.status_code}")
        print(f"   Response: {update_response.text[:300]}")
        
        if update_response.status_code in [200, 201]:
            print(f"   [OK] Task updated successfully")
        else:
            print(f"   [FAIL] UPDATE failed")
        
        # PATCH (Toggle Complete)
        print("\n4. PATCH task (mark complete)...")
        patch_response = await client.patch(
            f"{BASE_URL}/api/tasks/{user_id}/{task_id}/complete",
            json={"completed": True},
            headers=headers,
            timeout=10.0
        )
        print(f"   Status: {patch_response.status_code}")
        print(f"   Response: {patch_response.text[:300]}")
        
        if patch_response.status_code in [200, 201]:
            print(f"   [OK] Task marked as complete")
        else:
            print(f"   [FAIL] PATCH failed")
        
        # DELETE
        print("\n5. DELETE task...")
        delete_response = await client.delete(
            f"{BASE_URL}/api/tasks/{user_id}/{task_id}",
            headers=headers,
            timeout=10.0
        )
        print(f"   Status: {delete_response.status_code}")
        print(f"   Response: {delete_response.text[:300]}")
        
        if delete_response.status_code in [200, 201]:
            print(f"   [OK] Task deleted successfully")
        else:
            print(f"   [FAIL] DELETE failed")
        
        print("\n" + "=" * 60)
        print("CRUD TEST COMPLETED")
        print("=" * 60)
        print("\nResults:")
        print("- CREATE: Tested")
        print("- READ: Tested")
        print("- UPDATE: Tested")
        print("- PATCH: Tested")
        print("- DELETE: Tested")


async def test_authorization_only():
    """Test that authentication is required"""
    print("\n" + "=" * 60)
    print("AUTHORIZATION TEST (No Token)")
    print("=" * 60)
    
    async with httpx.AsyncClient() as client:
        user_id = "test-user"
        
        # Try GET without token
        print("\n1. GET without token...")
        get_response = await client.get(
            f"{BASE_URL}/api/tasks/{user_id}",
            timeout=10.0
        )
        print(f"   Status: {get_response.status_code}")
        if get_response.status_code == 401:
            print(f"   [OK] Correctly rejected (401)")
        else:
            print(f"   [FAIL] Expected 401, got {get_response.status_code}")
        
        # Try POST without token
        print("\n2. POST without token...")
        post_response = await client.post(
            f"{BASE_URL}/api/tasks/{user_id}",
            json={"title": "Test", "description": "Test"},
            timeout=10.0
        )
        print(f"   Status: {post_response.status_code}")
        if post_response.status_code == 401:
            print(f"   [OK] Correctly rejected (401)")
        else:
            print(f"   [FAIL] Expected 401, got {post_response.status_code}")


async def main():
    # Test authorization
    await test_authorization_only()
    
    # Test full CRUD
    await test_full_crud_with_signup()


if __name__ == "__main__":
    asyncio.run(main())
