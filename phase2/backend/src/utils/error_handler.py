"""
Comprehensive Error Handler for Todo AI-Powered Chatbot
"""
from typing import Union, Dict, Any
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
import logging
import traceback


class AppError(Exception):
    """
    Base application error class
    """
    def __init__(self, message: str, error_code: str = "APP_ERROR", status_code: int = 500):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        super().__init__(self.message)


class ValidationError(AppError):
    """
    Error for validation failures
    """
    def __init__(self, message: str):
        super().__init__(message, "VALIDATION_ERROR", status.HTTP_422_UNPROCESSABLE_ENTITY)


class AuthenticationError(AppError):
    """
    Error for authentication failures
    """
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, "AUTH_ERROR", status.HTTP_401_UNAUTHORIZED)


class AuthorizationError(AppError):
    """
    Error for authorization failures
    """
    def __init__(self, message: str = "Not authorized"):
        super().__init__(message, "AUTHORIZATION_ERROR", status.HTTP_403_FORBIDDEN)


class ResourceNotFoundError(AppError):
    """
    Error for when a requested resource is not found
    """
    def __init__(self, resource_type: str, resource_id: str = None):
        message = f"{resource_type} not found"
        if resource_id:
            message += f" with ID: {resource_id}"
        super().__init__(message, "RESOURCE_NOT_FOUND", status.HTTP_404_NOT_FOUND)


class RateLimitError(AppError):
    """
    Error for rate limit exceeded
    """
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(message, "RATE_LIMIT_ERROR", status.HTTP_429_TOO_MANY_REQUESTS)


def handle_error(error: Exception) -> Dict[str, Any]:
    """
    Handle different types of errors and return appropriate response
    """
    if isinstance(error, AppError):
        # Log the error
        logging.error(f"{error.error_code}: {error.message}")
        return {
            "error": error.error_code,
            "message": error.message,
            "status_code": error.status_code
        }

    elif isinstance(error, HTTPException):
        # Log the error
        logging.error(f"HTTP {error.status_code}: {error.detail}")
        return {
            "error": "HTTP_ERROR",
            "message": str(error.detail),
            "status_code": error.status_code
        }

    else:
        # Log the error with traceback
        logging.error(f"Unexpected error: {str(error)}")
        logging.error(traceback.format_exc())
        return {
            "error": "INTERNAL_ERROR",
            "message": "An internal error occurred",
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR
        }


def create_error_response(error: Exception) -> JSONResponse:
    """
    Create a standardized error response
    """
    error_details = handle_error(error)
    return JSONResponse(
        status_code=error_details["status_code"],
        content=error_details
    )


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def log_error(error: Exception, context: str = ""):
    """
    Log error with context
    """
    logger.error(f"Error in {context}: {str(error)}")
    logger.error(f"Traceback: {traceback.format_exc()}")


def log_info(message: str, context: str = ""):
    """
    Log info message
    """
    logger.info(f"[{context}] {message}")


def log_warning(message: str, context: str = ""):
    """
    Log warning message
    """
    logger.warning(f"[{context}] {message}")


# Global error handler decorator
def error_handler(func):
    """
    Decorator to handle errors in functions
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            log_error(e, func.__name__)
            raise
    return wrapper