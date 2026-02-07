from fastapi import Request, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from jwt import PyJWTError
from datetime import datetime, timedelta
import os
from typing import Dict, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get secret from environment - check multiple possible variable names
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET") or os.getenv("JWT_SECRET") or os.getenv("SECRET_KEY", "fallback_secret_key_for_development")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

security = HTTPBearer()

# Simple function-based dependency that extracts and validates token from request
async def get_current_user(request: Request):
    # Extract the Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No authorization header provided"
        )

    # Check if it's Bearer token
    if not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format"
        )

    # Extract the token
    token = auth_header[len("Bearer "):]

    # Decode and validate the token
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token."
        )

    # Return the decoded token payload (which contains user_id)
    return payload

class JWTBearer:
    def __call__(self):
        return Depends(get_current_user)

    def verify_jwt(self, token: str) -> bool:
        try:
            payload = decode_token(token)
            return payload is not None
        except PyJWTError:
            return False

def decode_token(token: str) -> Optional[Dict]:
    try:
        # Decode without expiration verification first
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"verify_exp": False}  # Skip automatic exp verification
        )

        # Manually check expiration with more tolerance
        exp = payload.get("exp")
        if exp:
            # Convert to datetime and check with tolerance
            exp_dt = datetime.fromtimestamp(exp)
            current_dt = datetime.utcnow()

            # Allow for some clock differences by checking if it's more than 1 minute in the past
            if exp_dt < current_dt - timedelta(minutes=1):
                return None

        return payload
    except PyJWTError:
        return None

def encode_token(user_id: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "user_id": user_id,
        "exp": expire.timestamp()
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt