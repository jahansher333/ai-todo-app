import os
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get secret key
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET") or os.getenv("JWT_SECRET") or os.getenv("SECRET_KEY", "fallback_secret_key_for_development")
ALGORITHM = "HS256"

print(f"Using SECRET_KEY: {SECRET_KEY}")

# Test token from the previous request
test_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMzY5MWZkNTEtZDY2ZC00MWVlLTg5ZDgtZjU3NDQ5ZDdjNjY0IiwiZXhwIjoxNzY5NDEwNTQ3Ljg5OTIyMn0.1lKWO7rSb-nJ9N9G49NK9zOayvd8upapP_tr-cHqOio"

print(f"Test token: {test_token[:50]}...")

# Try to decode the token
try:
    # First, let's decode without verification to see the payload
    unverified_payload = jwt.decode(test_token, options={"verify_signature": False})
    print(f"Unverified payload: {unverified_payload}")

    # Check the expiration timestamp
    exp_timestamp = unverified_payload.get('exp')
    print(f"Expiration timestamp: {exp_timestamp}")
    print(f"Expiration datetime: {datetime.fromtimestamp(exp_timestamp)}")
    print(f"Current datetime: {datetime.utcnow()}")
    print(f"Is token expired? {exp_timestamp < datetime.utcnow().timestamp()}")

    # Now try to decode with verification
    verified_payload = jwt.decode(test_token, SECRET_KEY, algorithms=[ALGORITHM])
    print(f"Verified payload: {verified_payload}")

except jwt.ExpiredSignatureError as e:
    print(f"ExpiredSignatureError: {e}")
except jwt.InvalidSignatureError as e:
    print(f"InvalidSignatureError: {e}")
except Exception as e:
    print(f"Other error: {e}")