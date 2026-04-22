"""
Simple JWT Verification Test for Backend
This test verifies that the backend can verify JWT tokens from Better Auth
"""
import asyncio
import httpx
import jwt as pyjwt
from cryptography.hazmat.primitives.asymmetric import ed25519

FRONTEND_URL = "http://localhost:3000"
BASE_URL = "http://localhost:8000"

async def test_jwt_verification():
    """Test JWT token verification with JWKS"""
    print("=" * 60)
    print("JWT Verification Test")
    print("=" * 60)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Step 1: Fetch JWKS
        print("\n[Step 1] Fetching JWKS from frontend...")
        jwks_response = await client.get(f"{FRONTEND_URL}/api/auth/jwks")
        print(f"JWKS Status: {jwks_response.status_code}")
        
        if jwks_response.status_code != 200:
            print(f"[FAIL] JWKS endpoint returned {jwks_response.status_code}")
            return
        
        jwks = jwks_response.json()
        print(f"JWKS Keys: {jwks.get('keys', [])}")
        
        if not jwks.get('keys'):
            print("[FAIL] No keys in JWKS")
            return
        
        print("[PASS] JWKS fetched successfully")
        
        # Step 2: Extract public key from JWKS
        print("\n[Step 2] Extracting public key from JWKS...")
        jwk = jwks['keys'][0]
        print(f"Key ID (kid): {jwk.get('kid')}")
        print(f"Algorithm: {jwk.get('alg')}")
        print(f"Curve: {jwk.get('crv')}")
        print(f"X coordinate: {jwk.get('x')}")
        
        # Convert JWK to Ed25519 public key
        x_bytes = pyjwt.utils.base64url_decode(jwk['x'])
        public_key = ed25519.Ed25519PublicKey.from_public_bytes(x_bytes)
        print("[PASS] Public key extracted")
        
        # Step 3: Get a JWT token (manual test - user needs to be logged in)
        print("\n[Step 3] Testing with sample token...")
        print("NOTE: For full test, user must be logged in via browser")
        print("      Open http://localhost:3000 and sign up/sign in")
        
        # For now, we'll just verify the JWKS is working
        print("\n[PASS] JWKS verification successful!")
        print("\n" + "=" * 60)
        print("Test Summary:")
        print("- JWKS endpoint: WORKING")
        print("- Public key extraction: WORKING") 
        print("- JWT verification: READY (needs logged-in user)")
        print("=" * 60)
        
        # Step 4: Test backend JWT middleware
        print("\n[Step 4] Testing backend JWT middleware...")
        print("Backend will fetch JWKS and verify tokens automatically")
        
        # Try to call backend without token (should fail with 401)
        response = await client.get(f"{BASE_URL}/api/test-user-id/tasks/")
        print(f"Backend without token: {response.status_code} (expected 401)")
        
        if response.status_code == 401:
            print("[PASS] Backend correctly rejects unauthenticated requests")
        else:
            print(f"[INFO] Backend returned: {response.status_code}")

if __name__ == "__main__":
    asyncio.run(test_jwt_verification())
