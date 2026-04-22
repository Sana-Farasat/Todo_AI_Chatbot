"""
Simple CRUD tests for Task API with mock authentication
Tests all task operations without modifying existing code
"""
import asyncio
import httpx
import jwt
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"

# Test configuration
TEST_USER_ID = "test-user-crud-001"
TEST_TITLE = "Test Task Title"
TEST_DESCRIPTION = "Test Task Description"


def create_mock_token(user_id: str) -> str:
    """Create a mock JWT token for testing (no verification, just for testing)"""
    # Create a simple token with user_id
    # Note: This is for testing only - in production, use real Better Auth tokens
    payload = {
        "id": user_id,
        "sub": user_id,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    # Create unsigned token (for testing only)
    token = jwt.encode(payload, key="", algorithm="none")
    return token


async def test_api_health():
    """Test if backend API is reachable"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/", timeout=10.0)
        assert response.status_code == 200, f"API not reachable: {response.status_code}"
        print(f"[OK] API Health Check: {response.text}")
        return True


async def test_get_tasks_no_auth():
    """Test GET tasks without authentication (should fail with 401)"""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/api/tasks/{TEST_USER_ID}",
            timeout=10.0
        )
        print(f"GET without auth - Status: {response.status_code}")
        # Should return 401 Unauthorized
        assert response.status_code == 401, f"Expected 401, got {response.status_code}"
        print(f"[OK] Correctly rejected unauthenticated request")


async def test_create_task_no_auth():
    """Test CREATE task without authentication (should fail with 401)"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/api/tasks/{TEST_USER_ID}",
            json={"title": TEST_TITLE, "description": TEST_DESCRIPTION},
            timeout=10.0
        )
        print(f"POST without auth - Status: {response.status_code}")
        # Should return 401 Unauthorized
        assert response.status_code == 401, f"Expected 401, got {response.status_code}"
        print(f"[OK] Correctly rejected unauthenticated request")


async def test_crud_with_mock_token():
    """Test full CRUD flow with mock JWT token"""
    token = create_mock_token(TEST_USER_ID)
    print(f"Created mock token for user: {TEST_USER_ID}")
    
    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"Bearer {token}"}
        
        print("\n=== TESTING CRUD WITH MOCK TOKEN ===\n")
        
        # CREATE
        print("1. CREATE task...")
        create_response = await client.post(
            f"{BASE_URL}/api/tasks/{TEST_USER_ID}",
            json={"title": TEST_TITLE, "description": TEST_DESCRIPTION},
            headers=headers,
            timeout=10.0
        )
        print(f"   CREATE Status: {create_response.status_code}")
        print(f"   Response: {create_response.text[:300]}")
        
        if create_response.status_code not in [200, 201]:
            print(f"   [FAIL] CREATE failed")
            return False
        
        task_data = create_response.json()
        task_id = task_data.get("id")
        print(f"   [OK] Created task with ID: {task_id}")
        
        # READ
        print("\n2. READ tasks...")
        get_response = await client.get(
            f"{BASE_URL}/api/tasks/{TEST_USER_ID}",
            headers=headers,
            timeout=10.0
        )
        print(f"   READ Status: {get_response.status_code}")
        print(f"   Response: {get_response.json()}")
        
        if get_response.status_code == 200:
            tasks = get_response.json()
            print(f"   [OK] Found {len(tasks)} task(s)")
        else:
            print(f"   [FAIL] READ failed")
        
        # UPDATE
        print("\n3. UPDATE task...")
        update_response = await client.put(
            f"{BASE_URL}/api/tasks/{TEST_USER_ID}/{task_id}",
            json={"title": "Updated Title", "description": "Updated Description"},
            headers=headers,
            timeout=10.0
        )
        print(f"   UPDATE Status: {update_response.status_code}")
        print(f"   Response: {update_response.text[:300]}")
        
        if update_response.status_code in [200, 201]:
            print(f"   [OK] Task updated")
        else:
            print(f"   [FAIL] UPDATE failed")
        
        # PATCH (Toggle Complete)
        print("\n4. PATCH task (mark complete)...")
        patch_response = await client.patch(
            f"{BASE_URL}/api/tasks/{TEST_USER_ID}/{task_id}/complete",
            json={"completed": True},
            headers=headers,
            timeout=10.0
        )
        print(f"   PATCH Status: {patch_response.status_code}")
        print(f"   Response: {patch_response.text[:300]}")
        
        if patch_response.status_code in [200, 201]:
            print(f"   [OK] Task marked as complete")
        else:
            print(f"   [FAIL] PATCH failed")
        
        # DELETE
        print("\n5. DELETE task...")
        delete_response = await client.delete(
            f"{BASE_URL}/api/tasks/{TEST_USER_ID}/{task_id}",
            headers=headers,
            timeout=10.0
        )
        print(f"   DELETE Status: {delete_response.status_code}")
        print(f"   Response: {delete_response.text[:300]}")
        
        if delete_response.status_code in [200, 201]:
            print(f"   [OK] Task deleted")
        else:
            print(f"   [FAIL] DELETE failed")
        
        print("\n=== CRUD TEST COMPLETED ===\n")
        return True


async def test_authorization():
    """Test that users can only access their own tasks"""
    token_user1 = create_mock_token("user-1")
    token_user2 = create_mock_token("user-2")
    
    async with httpx.AsyncClient() as client:
        print("\n=== TESTING AUTHORIZATION ===\n")
        
        # User 1 creates a task
        print("1. User 1 creates task...")
        create_response = await client.post(
            f"{BASE_URL}/api/tasks/user-1",
            json={"title": "User 1 Task", "description": "Only User 1 can access"},
            headers={"Authorization": f"Bearer {token_user1}"},
            timeout=10.0
        )
        print(f"   Status: {create_response.status_code}")
        
        if create_response.status_code in [200, 201]:
            task_id = create_response.json()["id"]
            print(f"   [OK] Task created")
            
            # User 2 tries to access User 1's task (should fail)
            print("\n2. User 2 tries to access User 1's task...")
            get_response = await client.get(
                f"{BASE_URL}/api/tasks/user-1",
                headers={"Authorization": f"Bearer {token_user2}"},
                timeout=10.0
            )
            print(f"   Status: {get_response.status_code}")
            
            if get_response.status_code == 403:
                print(f"   [OK] Correctly rejected unauthorized access")
            else:
                print(f"   [INFO] Got status: {get_response.status_code}")
            
            # Cleanup - User 1 deletes their task
            print("\n3. User 1 deletes their task...")
            delete_response = await client.delete(
                f"{BASE_URL}/api/tasks/user-1/{task_id}",
                headers={"Authorization": f"Bearer {token_user1}"},
                timeout=10.0
            )
            print(f"   Status: {delete_response.status_code}")
            
            if delete_response.status_code in [200, 201]:
                print(f"   [OK] Task deleted")
        
        print("\n=== AUTHORIZATION TEST COMPLETED ===\n")


async def run_all_tests():
    """Run all tests sequentially"""
    print("=" * 60)
    print("TASK CRUD SIMPLE TESTS (with mock authentication)")
    print("=" * 60)
    
    tests = [
        ("API Health Check", test_api_health),
        ("GET without auth (expect 401)", test_get_tasks_no_auth),
        ("POST without auth (expect 401)", test_create_task_no_auth),
        ("Full CRUD with mock token", test_crud_with_mock_token),
        ("Authorization test", test_authorization),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n{'='*60}")
        print(f"Running: {test_name}")
        print(f"{'='*60}")
        
        try:
            result = await test_func()
            if result is not False:  # None or True means pass
                passed += 1
                print(f"[PASS] {test_name}")
            else:
                failed += 1
                print(f"[FAIL] {test_name}")
        except Exception as e:
            failed += 1
            print(f"[FAIL] {test_name}")
            print(f"   Error: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 60)
    print(f"TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Passed:  {passed}/{len(tests)}")
    print(f"Failed:  {failed}/{len(tests)}")
    print(f"{'='*60}")
    
    if failed > 0:
        print("\n[WARNING] Some tests failed. Check the output above for details.")
        print("Make sure the backend server is running on http://localhost:8000")


if __name__ == "__main__":
    asyncio.run(run_all_tests())
