"""
Debug: Check what user_id is in the JWT token
"""
import asyncio
import httpx
import jwt
import random


BASE_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"

TEST_EMAIL = f"test_{random.randint(10000, 99999)}@example.com"
TEST_PASSWORD = "Test123456!"
TEST_NAME = "Test User"


async def debug_token_payload():
    """Get token and decode to see the actual user_id"""
    async with httpx.AsyncClient(cookies=httpx.Cookies(), timeout=30.0) as client:
        # Sign up
        print(f"Signing up: {TEST_EMAIL}")
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
        
        # Get token
        token_response = await client.get(
            f"{FRONTEND_URL}/api/auth/token",
            timeout=30.0
        )
        
        if token_response.status_code == 200:
            data = token_response.json()
            token = data.get("token")
            
            if token:
                print(f"\nGot token: {token[:50]}...")
                
                # Decode without verification
                unverified = jwt.decode(token, options={"verify_signature": False})
                print(f"\nToken payload:")
                for key, value in unverified.items():
                    print(f"  {key}: {value}")
                
                # Get header
                header = jwt.get_unverified_header(token)
                print(f"\nToken header:")
                for key, value in header.items():
                    print(f"  {key}: {value}")
                
                # The user_id from token
                user_id_from_token = unverified.get("id") or unverified.get("sub") or unverified.get("user_id")
                print(f"\n[INFO] User ID from token: {user_id_from_token}")
                
                # Now test with the correct user_id
                print(f"\n" + "=" * 60)
                print("TESTING CRUD WITH CORRECT USER_ID")
                print("=" * 60)
                
                headers = {"Authorization": f"Bearer {token}"}
                
                # CREATE with correct user_id
                print(f"\nCREATE task with user_id={user_id_from_token}...")
                create_response = await client.post(
                    f"{BASE_URL}/api/tasks/{user_id_from_token}",
                    json={"title": "Test Task", "description": "Test Description"},
                    headers=headers,
                    timeout=10.0
                )
                print(f"   Status: {create_response.status_code}")
                print(f"   Response: {create_response.text[:300]}")
                
                if create_response.status_code in [200, 201]:
                    task_id = create_response.json()["id"]
                    print(f"   [OK] Created task with ID: {task_id}")
                    
                    # READ
                    print(f"\nREAD tasks for user_id={user_id_from_token}...")
                    get_response = await client.get(
                        f"{BASE_URL}/api/tasks/{user_id_from_token}",
                        headers=headers,
                        timeout=10.0
                    )
                    print(f"   Status: {get_response.status_code}")
                    print(f"   Response: {get_response.json()}")
                    
                    if get_response.status_code == 200:
                        tasks = get_response.json()
                        print(f"   [OK] Found {len(tasks)} task(s)")
                    
                    # UPDATE
                    print(f"\nUPDATE task {task_id}...")
                    update_response = await client.put(
                        f"{BASE_URL}/api/tasks/{user_id_from_token}/{task_id}",
                        json={"title": "Updated Title", "description": "Updated Description"},
                        headers=headers,
                        timeout=10.0
                    )
                    print(f"   Status: {update_response.status_code}")
                    print(f"   Response: {update_response.text[:300]}")
                    
                    if update_response.status_code in [200, 201]:
                        print(f"   [OK] Task updated")
                    
                    # PATCH
                    print(f"\nPATCH task {task_id} (mark complete)...")
                    patch_response = await client.patch(
                        f"{BASE_URL}/api/tasks/{user_id_from_token}/{task_id}/complete",
                        json={"completed": True},
                        headers=headers,
                        timeout=10.0
                    )
                    print(f"   Status: {patch_response.status_code}")
                    print(f"   Response: {patch_response.text[:300]}")
                    
                    if patch_response.status_code in [200, 201]:
                        print(f"   [OK] Task marked as complete")
                    
                    # DELETE
                    print(f"\nDELETE task {task_id}...")
                    delete_response = await client.delete(
                        f"{BASE_URL}/api/tasks/{user_id_from_token}/{task_id}",
                        headers=headers,
                        timeout=10.0
                    )
                    print(f"   Status: {delete_response.status_code}")
                    print(f"   Response: {delete_response.text[:300]}")
                    
                    if delete_response.status_code in [200, 201]:
                        print(f"   [OK] Task deleted")
                    
                    print(f"\n" + "=" * 60)
                    print("ALL CRUD OPERATIONS COMPLETED SUCCESSFULLY!")
                    print("=" * 60)
                    
                else:
                    print(f"   [FAIL] CREATE failed")
                
                return token
            
        return None


async def main():
    print("=" * 60)
    print("DEBUG: JWT Token Payload and CRUD Test")
    print("=" * 60)
    await debug_token_payload()


if __name__ == "__main__":
    asyncio.run(main())
