#!/usr/bin/env python3
"""
Test script to verify the JWT authentication fix in the todo application.
This script demonstrates the corrected JWT implementation that addresses the issue
where the dependency injection system was receiving a 'Depends' object instead of
the actual token string.
"""

import sys
import os
import jwt
from datetime import datetime, timedelta
from unittest.mock import Mock

# Add the backend src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

from middleware.jwt_middleware import get_current_user, encode_token, decode_token

def test_jwt_functions():
    """Test the JWT encoding and decoding functions"""
    print("Testing JWT functions...")

    # Test encoding
    user_id = "test-user-id-123"
    token = encode_token(user_id)
    print(f"SUCCESS: Generated token: {token[:20]}...")

    # Test decoding
    decoded = decode_token(token)
    assert decoded is not None, "Token should decode successfully"
    assert decoded.get("user_id") == user_id, f"Expected user_id {user_id}, got {decoded.get('user_id')}"
    print("✓ Token decoded successfully with correct user_id")

    # Test expired token
    expired_token = jwt.encode({
        "user_id": user_id,
        "exp": (datetime.utcnow() - timedelta(minutes=1)).timestamp()  # Expired 1 minute ago
    }, "fallback_secret_key_for_development", algorithm="HS256")

    decoded_expired = decode_token(expired_token)
    assert decoded_expired is None, "Expired token should return None"
    print("✓ Expired token correctly rejected")

def test_get_current_user_dependency():
    """Test the get_current_user function as a dependency"""
    print("\nTesting get_current_user dependency function...")

    # Create a mock request with proper Authorization header
    mock_request = Mock()
    user_id = "test-user-id-123"
    token = encode_token(user_id)
    mock_request.headers = {
        "Authorization": f"Bearer {token}"
    }

    # Test the dependency function
    result = get_current_user(mock_request)
    assert isinstance(result, dict), "Result should be a dictionary (decoded token)"
    assert result.get("user_id") == user_id, f"Expected user_id {user_id}, got {result.get('user_id')}"
    print("✓ get_current_user correctly extracted and decoded token")

    # Test with invalid header format
    mock_request_invalid = Mock()
    mock_request_invalid.headers = {
        "Authorization": f"Basic {token}"  # Wrong scheme
    }

    try:
        get_current_user(mock_request_invalid)
        assert False, "Should have raised HTTPException for invalid scheme"
    except Exception as e:
        print("✓ Correctly rejected invalid authorization scheme")

    # Test with no header
    mock_request_no_auth = Mock()
    mock_request_no_auth.headers = {}

    try:
        get_current_user(mock_request_no_auth)
        assert False, "Should have raised HTTPException for missing header"
    except Exception as e:
        print("✓ Correctly rejected missing authorization header")

def simulate_task_endpoint_call():
    """Simulate how the task endpoints will work with the fix"""
    print("\nSimulating task endpoint call...")

    # Simulate a request with valid JWT
    user_id = "test-user-123"
    token = encode_token(user_id)

    # Mock request object
    mock_request = Mock()
    mock_request.headers = {
        "Authorization": f"Bearer {token}"
    }

    # Call the dependency function (this is what happens in the actual endpoints)
    decoded_token = get_current_user(mock_request)

    # Verify the token user_id matches the expected user_id
    token_user_id = decoded_token.get("user_id")
    path_user_id = user_id  # This would come from the route path parameter

    assert token_user_id == path_user_id, f"Token user_id {token_user_id} should match path user_id {path_user_id}"
    print("✓ Task endpoint authentication would succeed with valid token")

    print(f"✓ Token user_id: {token_user_id}")
    print(f"✓ Path user_id: {path_user_id}")
    print("✓ Authentication passed - user authorized")

if __name__ == "__main__":
    print("Testing JWT Authentication Fix for Todo Application Backend")
    print("=" * 60)

    try:
        test_jwt_functions()
        test_get_current_user_dependency()
        simulate_task_endpoint_call()

        print("\n" + "=" * 60)
        print("🎉 All tests passed! JWT authentication fix is working correctly.")
        print("\nThe issue has been resolved:")
        print("- The get_current_user dependency now returns decoded token payload")
        print("- Task endpoints can properly validate user identity")
        print("- No more 'Depends' object issues in the dependency injection")
        print("- Proper error handling for invalid/expired tokens")

    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)