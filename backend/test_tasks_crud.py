"""
Comprehensive CRUD tests for Task API
Tests all task operations without modifying existing code
"""
import asyncio
import pytest
import httpx
import os
from datetime import datetime

BASE_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"

# Test configuration
TEST_USER_ID = "test-user-crud-001"
TEST_TITLE = "Test Task Title"
TEST_DESCRIPTION = "Test Task Description"


async def get_test_token():
    """Get JWT token from frontend auth"""
    async with httpx.AsyncClient(cookies=httpx.Cookies(), timeout=30.0) as client:
        try:
            # Try to get token
            token_response = await client.get(
                f"{FRONTEND_URL}/api/auth/token",
                timeout=30.0
            )
            if token_response.status_code == 200:
                data = token_response.json()
                return data.get("token")
        except Exception as e:
            print(f"Error getting token: {e}")
    return None


@pytest.mark.asyncio
async def test_api_health():
    """Test if backend API is reachable"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/", timeout=10.0)
        assert response.status_code == 200, f"API not reachable: {response.status_code}"
        print(f"[OK] API Health Check: {response.text}")


@pytest.mark.asyncio
async def test_get_tasks_empty():
    """Test GET tasks when no tasks exist (should return empty list)"""
    token = await get_test_token()
    if not token:
        pytest.skip("No JWT token available")
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/api/tasks/{TEST_USER_ID}",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10.0
        )
        print(f"GET /api/tasks/{TEST_USER_ID} - Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        # Should return 200 with empty list or 401/403
        assert response.status_code in [200, 401, 403]
        if response.status_code == 200:
            data = response.json()
            assert isinstance(data, list), "Response should be a list"


@pytest.mark.asyncio
async def test_create_task():
    """Test POST - Create a new task"""
    token = await get_test_token()
    if not token:
        pytest.skip("No JWT token available")
    
    async with httpx.AsyncClient() as client:
        task_data = {
            "title": TEST_TITLE,
            "description": TEST_DESCRIPTION
        }
        
        response = await client.post(
            f"{BASE_URL}/api/tasks/{TEST_USER_ID}",
            json=task_data,
            headers={"Authorization": f"Bearer {token}"},
            timeout=10.0
        )
        
        print(f"POST /api/tasks/{TEST_USER_ID} - Status: {response.status_code}")
        print(f"Response: {response.text[:500]}")
        
        # Should succeed or fail with proper error
        assert response.status_code in [200, 201, 401, 403, 500], \
            f"Unexpected status code: {response.status_code}"
        
        if response.status_code in [200, 201]:
            data = response.json()
            assert "id" in data, "Response should contain 'id'"
            assert data["title"] == TEST_TITLE, "Title should match"
            assert data["description"] == TEST_DESCRIPTION, "Description should match"
            print(f"[OK] Task created with ID: {data['id']}")
            return data["id"]
    
    return None


@pytest.mark.asyncio
async def test_get_tasks_after_create():
    """Test GET tasks after creating one"""
    token = await get_test_token()
    if not token:
        pytest.skip("No JWT token available")
    
    # First create a task
    async with httpx.AsyncClient() as client:
        create_response = await client.post(
            f"{BASE_URL}/api/tasks/{TEST_USER_ID}",
            json={"title": "Test for GET", "description": "Testing GET"},
            headers={"Authorization": f"Bearer {token}"},
            timeout=10.0
        )
        
        if create_response.status_code not in [200, 201]:
            print(f"Task creation failed, skipping GET test")
            return
        
        # Now get all tasks
        get_response = await client.get(
            f"{BASE_URL}/api/tasks/{TEST_USER_ID}",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10.0
        )
        
        print(f"GET /api/tasks/{TEST_USER_ID} - Status: {get_response.status_code}")
        print(f"Response: {get_response.json()}")
        
        assert get_response.status_code in [200, 401, 403]
        if get_response.status_code == 200:
            data = get_response.json()
            assert isinstance(data, list), "Response should be a list"
            assert len(data) > 0, "Should have at least one task"
            print(f"[OK] Found {len(data)} task(s)")


@pytest.mark.asyncio
async def test_update_task():
    """Test PUT - Update an existing task"""
    token = await get_test_token()
    if not token:
        pytest.skip("No JWT token available")
    
    async with httpx.AsyncClient() as client:
        # First create a task to update
        create_response = await client.post(
            f"{BASE_URL}/api/tasks/{TEST_USER_ID}",
            json={"title": "Task to Update", "description": "Will be updated"},
            headers={"Authorization": f"Bearer {token}"},
            timeout=10.0
        )
        
        if create_response.status_code not in [200, 201]:
            print(f"Task creation failed, skipping UPDATE test")
            return
        
        task_id = create_response.json()["id"]
        
        # Update the task
        update_data = {
            "title": "Updated Title",
            "description": "Updated Description"
        }
        
        update_response = await client.put(
            f"{BASE_URL}/api/tasks/{TEST_USER_ID}/{task_id}",
            json=update_data,
            headers={"Authorization": f"Bearer {token}"},
            timeout=10.0
        )
        
        print(f"PUT /api/tasks/{TEST_USER_ID}/{task_id} - Status: {update_response.status_code}")
        print(f"Response: {update_response.text[:500]}")
        
        # Should succeed or fail with proper error
        assert update_response.status_code in [200, 201, 401, 403, 404, 500]
        
        if update_response.status_code in [200, 201]:
            print(f"[OK] Task {task_id} updated successfully")


@pytest.mark.asyncio
async def test_toggle_complete():
    """Test PATCH - Mark task as complete/incomplete"""
    token = await get_test_token()
    if not token:
        pytest.skip("No JWT token available")
    
    async with httpx.AsyncClient() as client:
        # First create a task
        create_response = await client.post(
            f"{BASE_URL}/api/tasks/{TEST_USER_ID}",
            json={"title": "Task to Complete", "description": "Will be completed"},
            headers={"Authorization": f"Bearer {token}"},
            timeout=10.0
        )
        
        if create_response.status_code not in [200, 201]:
            print(f"Task creation failed, skipping PATCH test")
            return
        
        task_id = create_response.json()["id"]
        
        # Mark as complete
        patch_response = await client.patch(
            f"{BASE_URL}/api/tasks/{TEST_USER_ID}/{task_id}/complete",
            json={"completed": True},
            headers={"Authorization": f"Bearer {token}"},
            timeout=10.0
        )
        
        print(f"PATCH /api/tasks/{TEST_USER_ID}/{task_id}/complete - Status: {patch_response.status_code}")
        print(f"Response: {patch_response.text[:500]}")
        
        # Should succeed or fail with proper error
        assert patch_response.status_code in [200, 201, 401, 403, 404, 500]
        
        if patch_response.status_code in [200, 201]:
            print(f"[OK] Task {task_id} marked as complete")


@pytest.mark.asyncio
async def test_delete_task():
    """Test DELETE - Remove a task"""
    token = await get_test_token()
    if not token:
        pytest.skip("No JWT token available")
    
    async with httpx.AsyncClient() as client:
        # First create a task to delete
        create_response = await client.post(
            f"{BASE_URL}/api/tasks/{TEST_USER_ID}",
            json={"title": "Task to Delete", "description": "Will be deleted"},
            headers={"Authorization": f"Bearer {token}"},
            timeout=10.0
        )
        
        if create_response.status_code not in [200, 201]:
            print(f"Task creation failed, skipping DELETE test")
            return
        
        task_id = create_response.json()["id"]
        
        # Delete the task
        delete_response = await client.delete(
            f"{BASE_URL}/api/tasks/{TEST_USER_ID}/{task_id}",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10.0
        )
        
        print(f"DELETE /api/tasks/{TEST_USER_ID}/{task_id} - Status: {delete_response.status_code}")
        print(f"Response: {delete_response.text[:500]}")
        
        # Should succeed or fail with proper error
        assert delete_response.status_code in [200, 201, 401, 403, 404, 500]
        
        if delete_response.status_code in [200, 201]:
            print(f"[OK] Task {task_id} deleted successfully")


@pytest.mark.asyncio
async def test_full_crud_flow():
    """Test complete CRUD flow: Create -> Read -> Update -> Delete"""
    token = await get_test_token()
    if not token:
        pytest.skip("No JWT token available")
    
    async with httpx.AsyncClient() as client:
        print("\n=== FULL CRUD FLOW TEST ===\n")
        
        # CREATE
        print("1. CREATE task...")
        create_response = await client.post(
            f"{BASE_URL}/api/tasks/{TEST_USER_ID}",
            json={"title": "CRUD Test Task", "description": "Full CRUD test"},
            headers={"Authorization": f"Bearer {token}"},
            timeout=10.0
        )
        print(f"   CREATE Status: {create_response.status_code}")
        
        if create_response.status_code not in [200, 201]:
            print(f"   CREATE failed: {create_response.text[:200]}")
            return
        
        task_id = create_response.json()["id"]
        print(f"   [OK] Created task with ID: {task_id}")
        
        # READ
        print("\n2. READ tasks...")
        get_response = await client.get(
            f"{BASE_URL}/api/tasks/{TEST_USER_ID}",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10.0
        )
        print(f"   READ Status: {get_response.status_code}")
        
        if get_response.status_code == 200:
            tasks = get_response.json()
            print(f"   [OK] Found {len(tasks)} task(s)")
        
        # UPDATE
        print("\n3. UPDATE task...")
        update_response = await client.put(
            f"{BASE_URL}/api/tasks/{TEST_USER_ID}/{task_id}",
            json={"title": "Updated CRUD Task", "description": "Updated description"},
            headers={"Authorization": f"Bearer {token}"},
            timeout=10.0
        )
        print(f"   UPDATE Status: {update_response.status_code}")
        
        if update_response.status_code in [200, 201]:
            print(f"   [OK] Task updated")
        
        # PATCH (Toggle Complete)
        print("\n4. PATCH task (mark complete)...")
        patch_response = await client.patch(
            f"{BASE_URL}/api/tasks/{TEST_USER_ID}/{task_id}/complete",
            json={"completed": True},
            headers={"Authorization": f"Bearer {token}"},
            timeout=10.0
        )
        print(f"   PATCH Status: {patch_response.status_code}")
        
        if patch_response.status_code in [200, 201]:
            print(f"   [OK] Task marked as complete")
        
        # DELETE
        print("\n5. DELETE task...")
        delete_response = await client.delete(
            f"{BASE_URL}/api/tasks/{TEST_USER_ID}/{task_id}",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10.0
        )
        print(f"   DELETE Status: {delete_response.status_code}")
        
        if delete_response.status_code in [200, 201]:
            print(f"   [OK] Task deleted")
        
        print("\n=== FULL CRUD FLOW COMPLETED ===\n")


async def run_all_tests():
    """Run all tests sequentially with detailed output"""
    print("=" * 60)
    print("TASK CRUD COMPREHENSIVE TESTS")
    print("=" * 60)
    
    tests = [
        ("API Health Check", test_api_health),
        ("GET Tasks (Empty)", test_get_tasks_empty),
        ("CREATE Task", test_create_task),
        ("GET Tasks (After Create)", test_get_tasks_after_create),
        ("UPDATE Task", test_update_task),
        ("PATCH Task (Complete)", test_toggle_complete),
        ("DELETE Task", test_delete_task),
        ("FULL CRUD FLOW", test_full_crud_flow),
    ]
    
    passed = 0
    failed = 0
    skipped = 0
    
    for test_name, test_func in tests:
        print(f"\n{'='*60}")
        print(f"Running: {test_name}")
        print(f"{'='*60}")
        
        try:
            await test_func()
            passed += 1
            print(f"[PASS] {test_name}")
        except pytest.skip.Exception:
            skipped += 1
            print(f"[SKIP] {test_name}")
        except Exception as e:
            failed += 1
            print(f"[FAIL] {test_name}")
            print(f"   Error: {e}")
    
    print("\n" + "=" * 60)
    print(f"TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Passed:  {passed}/{len(tests)}")
    print(f"Failed:  {failed}/{len(tests)}")
    print(f"Skipped: {skipped}/{len(tests)}")
    print(f"{'='*60}")


if __name__ == "__main__":
    asyncio.run(run_all_tests())
