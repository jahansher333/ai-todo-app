import os
import jwt
import sys
from pathlib import Path
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Add the parent directory to the Python path to import from src
sys.path.insert(0, str(Path(__file__).parent))

from src.middleware.jwt_middleware import encode_token

# Load environment variables
load_dotenv()

# Get secret key
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET") or os.getenv("JWT_SECRET") or os.getenv("SECRET_KEY", "fallback_secret_key_for_development")
ALGORITHM = "HS256"

print(f"Current time: {datetime.utcnow()}")
print(f"Current timestamp: {datetime.utcnow().timestamp()}")

# Create a new token using the actual function
user_id = "test-user-id-123"
new_token = encode_token(user_id)
print(f"New token: {new_token}")

# Decode the new token to see what's inside
try:
    unverified_payload = jwt.decode(new_token, options={"verify_signature": False})
    print(f"New token payload: {unverified_payload}")

    # Decode with verification
    verified_payload = jwt.decode(new_token, SECRET_KEY, algorithms=[ALGORITHM])
    print(f"✅ New token verified successfully: {verified_payload}")
except Exception as e:
    print(f"❌ Error with new token: {e}")

# Test with the problematic fresh token
fresh_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMzQwYTFjZWUtMzg1MS00OGRjLWIwNjItYmM0ZjhhOGFjYmZhIiwiZXhwIjoxNzY5NDEwODkxLjM1ODU0fQ.j-zaFDJ89tNrz15vjq3tRmwuRrduxs7ifWExqlIivLU"

try:
    # Decode without verification to see the payload
    unverified_payload = jwt.decode(fresh_token, options={"verify_signature": False})
    print(f"Problematic token payload: {unverified_payload}")

    # Check the time
    exp_time = datetime.fromtimestamp(unverified_payload['exp'])
    current_time = datetime.utcnow()
    print(f"Token expires at: {exp_time}")
    print(f"Current time: {current_time}")
    print(f"Time difference: {(exp_time - current_time).total_seconds()} seconds")

    # Try to verify
    verified_payload = jwt.decode(fresh_token, SECRET_KEY, algorithms=[ALGORITHM])
    print(f"✅ Problematic token verified successfully: {verified_payload}")
except Exception as e:
    print(f"❌ Error with problematic token: {e}")