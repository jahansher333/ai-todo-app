import os
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get secret key
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET") or os.getenv("JWT_SECRET") or os.getenv("SECRET_KEY", "fallback_secret_key_for_development")
ALGORITHM = "HS256"

# Function to decode token (same as in middleware)
def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Check if token is expired
        exp = payload.get("exp")
        print(f"Token expiration timestamp: {exp}")
        print(f"Current UTC time timestamp: {datetime.utcnow().timestamp()}")

        if exp and datetime.fromtimestamp(exp) < datetime.utcnow():
            print("Token is expired!")
            return None
        print("Token is valid!")
        return payload
    except jwt.PyJWTError as e:
        print(f"JWT Error: {e}")
        return None

# Test token from the previous request
test_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMzY5MWZkNTEtZDY2ZC00MWVlLTg5ZDgtZjU3NDQ5ZDdjNjY0IiwiZXhwIjoxNzY5NDEwNTQ3Ljg5OTIyMn0.1lKWO7rSb-nJ9N9G49NK9zOayvd8upapP_tr-cHqOio"

print("Testing token decoding...")
decoded = decode_token(test_token)
print(f"Decoded token: {decoded}")

if decoded:
    print(f"User ID from token: {decoded.get('user_id')}")
else:
    print("Failed to decode token!")