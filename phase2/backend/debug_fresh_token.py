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

# Fresh token from the latest request
fresh_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMzQwYTFjZWUtMzg1MS00OGRjLWIwNjItYmM0ZjhhOGFjYmZhIiwiZXhwIjoxNzY5NDEwODkxLjM1ODU0fQ.j-zaFDJ89tNrz15vjq3tRmwuRrduxs7ifWExqlIivLU"

print(f"Fresh token: {fresh_token}")

try:
    # Decode without verification to see the payload
    unverified_payload = jwt.decode(fresh_token, options={"verify_signature": False})
    print(f"Unverified payload: {unverified_payload}")

    # Check the expiration timestamp
    exp_timestamp = unverified_payload.get('exp')
    print(f"Expiration timestamp: {exp_timestamp}")
    print(f"Expiration datetime: {datetime.fromtimestamp(exp_timestamp)}")
    print(f"Current datetime: {datetime.utcnow()}")
    print(f"Time until expiration: {(datetime.fromtimestamp(exp_timestamp) - datetime.utcnow()).total_seconds() / 60:.2f} minutes")

    # Now try to decode with verification
    verified_payload = jwt.decode(fresh_token, SECRET_KEY, algorithms=[ALGORITHM])
    print(f"✅ Successfully verified payload: {verified_payload}")

except jwt.ExpiredSignatureError as e:
    print(f"❌ ExpiredSignatureError: {e}")
except jwt.InvalidSignatureError as e:
    print(f"❌ InvalidSignatureError: {e}")
except jwt.InvalidTokenError as e:
    print(f"❌ InvalidTokenError: {e}")
except Exception as e:
    print(f"❌ Other error: {e}")
    import traceback
    traceback.print_exc()