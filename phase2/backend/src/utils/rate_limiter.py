"""
Rate Limiter Utility
"""
import time
from typing import Dict
from collections import defaultdict
import threading
from datetime import datetime, timedelta


class RateLimiter:
    """
    Simple rate limiter to prevent abuse of the AI agent
    """

    def __init__(self, requests: int = 100, window: int = 60):
        """
        Initialize rate limiter
        :param requests: Number of requests allowed per window
        :param window: Time window in seconds
        """
        self.requests = requests
        self.window = window
        self.requests_log: Dict[str, list] = defaultdict(list)  # user_id -> list of request timestamps
        self.lock = threading.Lock()

    def is_allowed(self, user_id: str) -> bool:
        """
        Check if a request from user_id is allowed
        :param user_id: The user's ID
        :return: True if allowed, False otherwise
        """
        with self.lock:
            now = time.time()
            # Clean up old requests outside the window
            self.requests_log[user_id] = [
                req_time for req_time in self.requests_log[user_id]
                if now - req_time < self.window
            ]

            # Check if the user is within the rate limit
            if len(self.requests_log[user_id]) < self.requests:
                # Add the current request to the log
                self.requests_log[user_id].append(now)
                return True

            return False

    def get_reset_time(self, user_id: str) -> float:
        """
        Get the time when the rate limit will reset for the user
        :param user_id: The user's ID
        :return: Unix timestamp when the rate limit resets
        """
        with self.lock:
            if user_id in self.requests_log:
                oldest_req = min(self.requests_log[user_id])
                return oldest_req + self.window
            return time.time()


# Global rate limiter instance
rate_limiter = RateLimiter()


def get_rate_limiter() -> RateLimiter:
    """
    Get the global rate limiter instance
    """
    return rate_limiter