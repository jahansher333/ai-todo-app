"""
Input Validation and Sanitization Utilities
"""
import re
from typing import Any, Dict, Optional, List
from pydantic import BaseModel, validator, ValidationError
import html
import bleach


class InputValidator:
    """
    Class to handle input validation and sanitization
    """

    @staticmethod
    def sanitize_text(text: str) -> str:
        """
        Sanitize text input by removing potentially harmful content
        """
        if not isinstance(text, str):
            raise ValueError("Input must be a string")

        # Remove HTML tags and sanitize content
        sanitized = bleach.clean(text, strip=True)

        # Decode any HTML entities
        sanitized = html.unescape(sanitized)

        # Remove any remaining potentially harmful patterns
        sanitized = re.sub(r'<script[^>]*>.*?</script>', '', sanitized, flags=re.IGNORECASE)
        sanitized = re.sub(r'javascript:', '', sanitized, flags=re.IGNORECASE)
        sanitized = re.sub(r'on\w+\s*=', '', sanitized, flags=re.IGNORECASE)

        return sanitized.strip()

    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validate email format
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    @staticmethod
    def validate_username(username: str) -> bool:
        """
        Validate username (alphanumeric, underscore, hyphen, 3-30 chars)
        """
        if len(username) < 3 or len(username) > 30:
            return False
        pattern = r'^[a-zA-Z0-9_-]+$'
        return bool(re.match(pattern, username))

    @staticmethod
    def validate_task_title(title: str) -> tuple[bool, Optional[str]]:
        """
        Validate task title
        Returns: (is_valid, error_message)
        """
        if not title or len(title.strip()) == 0:
            return False, "Task title cannot be empty"

        if len(title) > 200:
            return False, "Task title cannot exceed 200 characters"

        # Check for potentially harmful content
        try:
            sanitized = InputValidator.sanitize_text(title)
            if sanitized != title:
                return False, "Task title contains invalid characters or markup"
        except Exception:
            return False, "Task title contains invalid content"

        return True, None

    @staticmethod
    def validate_task_description(description: str) -> tuple[bool, Optional[str]]:
        """
        Validate task description
        Returns: (is_valid, error_message)
        """
        if description and len(description) > 1000:
            return False, "Task description cannot exceed 1000 characters"

        # Sanitize the description
        try:
            sanitized = InputValidator.sanitize_text(description or "")
            if description and sanitized != description:
                return False, "Task description contains invalid characters or markup"
        except Exception:
            return False, "Task description contains invalid content"

        return True, None

    @staticmethod
    def validate_user_input(input_text: str) -> tuple[bool, Optional[str]]:
        """
        Validate general user input
        Returns: (is_valid, error_message)
        """
        if not input_text or len(input_text.strip()) == 0:
            return False, "Input cannot be empty"

        if len(input_text) > 10000:  # 10KB limit
            return False, "Input is too long"

        # Check for potentially harmful content
        try:
            sanitized = InputValidator.sanitize_text(input_text)
            if sanitized != input_text:
                return False, "Input contains invalid characters or markup"
        except Exception:
            return False, "Input contains invalid content"

        return True, None

    @staticmethod
    def validate_uuid(uuid_string: str) -> bool:
        """
        Validate UUID format
        """
        import uuid
        try:
            uuid.UUID(uuid_string)
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_priority(priority: str) -> bool:
        """
        Validate task priority
        """
        return priority.lower() in ['low', 'medium', 'high']

    @staticmethod
    def validate_status(status: str) -> bool:
        """
        Validate task status
        """
        return status.lower() in ['pending', 'completed']


# Pydantic models for validation
class TaskValidationModel(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Optional[str] = "medium"
    status: Optional[str] = "pending"

    @validator('title')
    def validate_task_title(cls, v):
        is_valid, error_msg = InputValidator.validate_task_title(v)
        if not is_valid:
            raise ValueError(error_msg)
        return v

    @validator('description')
    def validate_task_description(cls, v):
        if v is not None:
            is_valid, error_msg = InputValidator.validate_task_description(v)
            if not is_valid:
                raise ValueError(error_msg)
        return v

    @validator('priority')
    def validate_priority(cls, v):
        if v and not InputValidator.validate_priority(v):
            raise ValueError(f"Invalid priority: {v}. Must be low, medium, or high.")
        return v.lower()

    @validator('status')
    def validate_status(cls, v):
        if v and not InputValidator.validate_status(v):
            raise ValueError(f"Invalid status: {v}. Must be pending or completed.")
        return v.lower()


class UserValidationModel(BaseModel):
    email: str
    username: Optional[str] = None

    @validator('email')
    def validate_email(cls, v):
        if not InputValidator.validate_email(v):
            raise ValueError(f"Invalid email format: {v}")
        return v

    @validator('username')
    def validate_username(cls, v):
        if v and not InputValidator.validate_username(v):
            raise ValueError(f"Invalid username format: {v}")
        return v


def validate_and_sanitize_task_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and sanitize task data
    """
    try:
        # Validate using Pydantic model
        task_model = TaskValidationModel(**data)

        # Sanitize the title and description
        sanitized_data = data.copy()
        sanitized_data['title'] = InputValidator.sanitize_text(task_model.title)
        if task_model.description:
            sanitized_data['description'] = InputValidator.sanitize_text(task_model.description)

        return sanitized_data
    except ValidationError as e:
        raise ValueError(f"Validation error: {e}")


def validate_and_sanitize_user_input(input_text: str) -> str:
    """
    Validate and sanitize user input text
    """
    is_valid, error_msg = InputValidator.validate_user_input(input_text)
    if not is_valid:
        raise ValueError(error_msg)

    return InputValidator.sanitize_text(input_text)


def validate_and_sanitize_conversation_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and sanitize conversation data
    """
    sanitized_data = data.copy()

    if 'title' in sanitized_data and sanitized_data['title']:
        is_valid, error_msg = InputValidator.validate_task_title(sanitized_data['title'])
        if not is_valid:
            raise ValueError(error_msg)
        sanitized_data['title'] = InputValidator.sanitize_text(sanitized_data['title'])

    return sanitized_data


# Global validator instance
validator = InputValidator()