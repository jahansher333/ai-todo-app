import os
import jwt
import sys
from pathlib import Path
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Add the parent directory to the Python path to import from src
sys.path.insert(0, str(Path(__file__).parent))

# Load environment variables
load_dotenv()

# Get secret key
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET") or os.getenv("JWT_SECRET") or os.getenv("SECRET_KEY", "fallback_secret_key_for_development")
ALGORITHM = "HS256"

# Test token from the latest request
fresh_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMzQwYTFjZWUtMzg1MS00OGRjLWIwNjItYmM0ZjhhOGFjYmZhIiwiZXhwIjoxNzY5NDEwODkxLjM1ODU0fQ.j-zaFDJ89tNrz15vjq3tRmwuRrduxs7ifWExqlIivLU"

print(f"Current time: {datetime.utcnow()}")
print(f"Current timestamp: {datetime.utcnow().timestamp()}")

try:
    # Decode without verification to see the payload
    unverified_payload = jwt.decode(fresh_token, options={"verify_signature": False})
    print(f"Token payload: {unverified_payload}")

    exp_timestamp = unverified_payload.get('exp')
    exp_datetime = datetime.fromtimestamp(exp_timestamp)
    current_datetime = datetime.utcnow()

    print(f"Token expires at: {exp_datetime}")
    print(f"Current time: {current_datetime}")
    print(f"Time difference: {(exp_datetime - current_datetime).total_seconds()} seconds")

    # Try to decode with different leeway values
    print("\nTrying to decode with various leeway values...")

    for leeway_val in [0, 10, 30, 60, 120]:
        try:
            verified_payload = jwt.decode(
                fresh_token,
                SECRET_KEY,
                algorithms=[ALGORITHM],
                options={"verify_exp": True},
                leeway=timedelta(seconds=leeway_val)
            )
            print(f"✅ Success with leeway {leeway_val}s: {verified_payload}")
            break
        except jwt.ExpiredSignatureError:
            print(f"❌ Still expired with leeway {leeway_val}s")
        except Exception as e:
            print(f"❌ Other error with leeway {leeway_val}s: {e}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()