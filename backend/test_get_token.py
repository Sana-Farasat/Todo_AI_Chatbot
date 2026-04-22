"""
Test to get JWT token from frontend
"""
import asyncio
import httpx


async def test_token_endpoint():
    """Test getting JWT token from frontend"""
    async with httpx.AsyncClient(cookies=httpx.Cookies(), timeout=30.0) as client:
        try:
            # Check frontend
            print("1. Checking frontend...")
            ping = await client.get("http://localhost:3000/", timeout=5.0)
            print(f"   Frontend status: {ping.status_code}")
            
            # Get token
            print("\n2. Getting JWT token...")
            token_response = await client.get("http://localhost:3000/api/auth/token", timeout=30.0)
            print(f"   Token endpoint status: {token_response.status_code}")
            print(f"   Response: {token_response.text[:500]}")
            
            if token_response.status_code == 200:
                data = token_response.json()
                token = data.get("token")
                if token:
                    print(f"\n[OK] Got token: {token[:50]}...")
                    return token
                else:
                    print("\n[FAIL] No token in response")
            else:
                print(f"\n[FAIL] Token request failed with status {token_response.status_code}")
                
        except Exception as e:
            print(f"\n[ERROR] {e}")
            import traceback
            traceback.print_exc()
    
    return None


async def test_jwks_endpoint():
    """Test JWKS endpoint"""
    async with httpx.AsyncClient() as client:
        try:
            print("\n3. Testing JWKS endpoint...")
            response = await client.get("http://localhost:3000/api/auth/jwks", timeout=10.0)
            print(f"   JWKS status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"   Keys count: {len(data.get('keys', []))}")
                print(f"[OK] JWKS endpoint working")
            else:
                print(f"[FAIL] JWKS endpoint failed")
                
        except Exception as e:
            print(f"\n[ERROR] JWKS test failed: {e}")


async def test_signin_flow():
    """Test full sign-in flow to get token"""
    async with httpx.AsyncClient(cookies=httpx.Cookies(), timeout=30.0) as client:
        try:
            print("\n4. Testing sign-in flow...")
            
            # Try to sign in
            print("   Attempting sign in...")
            sign_in_response = await client.post(
                "http://localhost:3000/api/auth/sign-in/email",
                json={
                    "email": "test@example.com",
                    "password": "Test123456!"
                },
                timeout=30.0
            )
            print(f"   Sign-in status: {sign_in_response.status_code}")
            print(f"   Response: {sign_in_response.text[:300]}")
            
            # Get token after sign-in
            print("\n   Getting token after sign-in...")
            token_response = await client.get(
                "http://localhost:3000/api/auth/token",
                timeout=30.0
            )
            print(f"   Token status: {token_response.status_code}")
            print(f"   Response: {token_response.text[:300]}")
            
            if token_response.status_code == 200:
                data = token_response.json()
                token = data.get("token")
                if token:
                    print(f"\n[OK] Got token after sign-in: {token[:50]}...")
                    return token
                    
        except Exception as e:
            print(f"\n[ERROR] Sign-in flow failed: {e}")
    
    return None


async def main():
    print("=" * 60)
    print("TESTING FRONTEND AUTH ENDPOINTS")
    print("=" * 60)
    
    # Test token endpoint
    token = await test_token_endpoint()
    
    # Test JWKS
    await test_jwks_endpoint()
    
    # Test sign-in flow
    if not token:
        token = await test_signin_flow()
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    if token:
        print(f"[OK] Successfully got JWT token")
        print(f"Token: {token[:50]}...")
    else:
        print("[FAIL] Could not get JWT token")
        print("\nPossible reasons:")
        print("1. Not signed in")
        print("2. No user account exists")
        print("3. Auth session expired")
        print("\nSolution: Sign in through the frontend UI first")


if __name__ == "__main__":
    asyncio.run(main())
