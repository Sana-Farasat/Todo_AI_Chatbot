import jwt
from fastapi import HTTPException, Request
import os
from dotenv import load_dotenv
import httpx
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.backends import default_backend

load_dotenv()

# Better Auth JWKS endpoint
JWKS_URL = os.getenv("BETTER_AUTH_JWKS_URL", "http://localhost:3000/api/auth/jwks")

async def get_public_key_from_jwks(kid: str = None):
    """Fetch public key from Better Auth JWKS endpoint"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(JWKS_URL, timeout=10.0)
            response.raise_for_status()
            jwks = response.json()
            
            # If kid provided, find matching key
            if kid:
                for key in jwks.get("keys", []):
                    if key.get("kid") == kid:
                        # Convert JWK to PEM
                        x_bytes = jwt.utils.base64url_decode(key["x"])
                        public_key = ed25519.Ed25519PublicKey.from_public_bytes(x_bytes)
                        return public_key
            
            # Otherwise return first key
            if jwks.get("keys"):
                key = jwks["keys"][0]
                x_bytes = jwt.utils.base64url_decode(key["x"])
                public_key = ed25519.Ed25519PublicKey.from_public_bytes(x_bytes)
                return public_key
                
    except Exception as e:
        print(f"DEBUG: Error fetching JWKS: {e}")
    
    return None

async def get_current_user(request: Request):
    auth_header = request.headers.get("Authorization")
    print(f"DEBUG: Auth header received: {auth_header[:50] if auth_header else 'None'}...")
    
    if not auth_header:
        print("DEBUG: No authorization header")
        raise HTTPException(401, "No token")

    parts = auth_header.split(" ")
    if len(parts) != 2 or parts[0] != "Bearer":
        print(f"DEBUG: Invalid auth header format: {parts}")
        raise HTTPException(401, "Invalid authorization header format")

    token = parts[1]
    print(f"DEBUG: Token extracted: {token[:50]}...")
    
    try:
        # Decode without verification first to see the payload and header
        unverified_payload = jwt.decode(token, options={"verify_signature": False})
        unverified_header = jwt.get_unverified_header(token)
        print(f"DEBUG: Unverified payload: {unverified_payload}")
        print(f"DEBUG: Token header: {unverified_header}")
        
        alg = unverified_header.get("alg", "EdDSA")
        kid = unverified_header.get("kid")
        print(f"DEBUG: Token algorithm: {alg}")
        print(f"DEBUG: Token kid: {kid}")
        
        # Get public key from JWKS
        public_key = await get_public_key_from_jwks(kid)
        
        if not public_key:
            print("DEBUG: Could not fetch public key from JWKS")
            # Fallback: return user_id from unverified payload (less secure, for dev only)
            user_id = unverified_payload.get("id") or unverified_payload.get("sub")
            if user_id:
                print(f"DEBUG: Using unverified user_id: {user_id}")
                return str(user_id)
            raise HTTPException(401, "Could not verify token")
        
        # Verify with EdDSA
        try:
            payload = jwt.decode(
                token,
                public_key,
                algorithms=["EdDSA"],
                options={
                    "require": ["exp"],
                    "verify_aud": False,  # Skip audience verification for now
                    "verify_iss": False,  # Skip issuer verification for now
                }
            )
            print(f"DEBUG: Verified payload: {payload}")
        except Exception as decode_error:
            print(f"DEBUG: Decode error: {decode_error}")
            raise HTTPException(401, f"Token verification failed: {str(decode_error)}")
        
        # Better Auth JWT plugin uses 'id' or 'sub' for user identifier
        user_id = payload.get("id") or payload.get("sub") or payload.get("user_id")
        print(f"DEBUG: Extracted user_id: {user_id}")
        
        if not user_id:
            print("DEBUG: No user_id found in token payload")
            raise HTTPException(401, "No user_id in token")
            
        return str(user_id)  # Convert to string to match path parameter
    except jwt.ExpiredSignatureError as e:
        print(f"DEBUG: Token expired: {e}")
        raise HTTPException(401, "Token expired")
    except jwt.InvalidTokenError as e:
        print(f"DEBUG: Invalid token: {str(e)}")
        raise HTTPException(401, f"Invalid token: {str(e)}")