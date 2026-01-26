#!/usr/bin/env python3
"""
Simple test to verify JWT middleware functionality after the fix.
"""

import sys
import os
from unittest.mock import Mock

# Add the backend src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

# Import the JWT functions after adding the path
from middleware.jwt_middleware import encode_token, decode_token

def test_basic_jwt():
    """Test basic JWT encoding and decoding"""
    print("Testing basic JWT functionality...")

    # Set environment variable for the test
    os.environ['BETTER_AUTH_SECRET'] = 'dev_secret_key_for_local_testing'

    # Reload the module to pick up the environment variable
    import importlib
    import middleware.jwt_middleware
    importlib.reload(middleware.jwt_middleware)

    # Re-import the functions
    from middleware.jwt_middleware import encode_token, decode_token

    # Test encoding
    user_id = "test-user-id-123"
    token = encode_token(user_id)
    print(f"Generated token: {token[:20]}...")

    # Test decoding
    decoded = decode_token(token)
    if decoded is not None:
        print(f"SUCCESS: Token decoded successfully")
        print(f"User ID from token: {decoded.get('user_id')}")
        if decoded.get('user_id') == user_id:
            print("SUCCESS: User ID matches!")
        else:
            print(f"ERROR: Expected {user_id}, got {decoded.get('user_id')}")
    else:
        print("ERROR: Token could not be decoded")

    # Test the actual middleware function
    from middleware.jwt_middleware import get_current_user

    # Mock a request with proper Authorization header
    mock_request = Mock()
    token = encode_token(user_id)
    mock_request.headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        result = get_current_user(mock_request)
        print(f"SUCCESS: get_current_user returned: {type(result)}")
        print(f"User ID in result: {result.get('user_id')}")

        if result.get('user_id') == user_id:
            print("SUCCESS: JWT authentication flow works correctly!")
            print("\nThe fix is working:")
            print("- get_current_user now properly extracts token from request")
            print("- Token is decoded and validated correctly")
            print("- Returns the decoded payload instead of Depends object")
            return True
        else:
            print("ERROR: User ID mismatch in get_current_user result")
            return False

    except Exception as e:
        print(f"ERROR: get_current_user failed with: {e}")
        return False

if __name__ == "__main__":
    print("Testing JWT Authentication Fix")
    print("=" * 50)

    success = test_basic_jwt()

    print("\n" + "=" * 50)
    if success:
        print("OVERALL: SUCCESS - JWT authentication fix is working!")
        print("\nSUMMARY OF FIXES MADE:")
        print("1. Fixed get_current_user function in jwt_middleware.py to properly extract")
        print("   token from Authorization header instead of receiving Depends object")
        print("2. Updated tasks.py to expect decoded token payload instead of raw token")
        print("3. Removed redundant decode_token calls in tasks endpoints")
        print("4. Maintained proper authentication flow and error handling")
    else:
        print("OVERALL: FAILED - There are still issues with the JWT implementation")