"""
Logging utility for Todo AI-Powered Chatbot
"""
import logging
import sys
from datetime import datetime
from enum import Enum
from typing import Any, Dict
import json


class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class Logger:
    """
    Custom logger class for the application
    """

    def __init__(self, name: str = "TodoChatbot", level: LogLevel = LogLevel.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.value))

        # Prevent adding handlers multiple times
        if not self.logger.handlers:
            # Create console handler
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(getattr(logging, level.value))

            # Create formatter
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            console_handler.setFormatter(formatter)

            # Add handler to logger
            self.logger.addHandler(console_handler)

    def _log(self, level: LogLevel, message: str, **kwargs):
        """
        Internal method to log messages
        """
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": level.value,
            "message": message,
        }

        if kwargs:
            log_data["extra"] = kwargs

        log_msg = json.dumps(log_data)
        getattr(self.logger, level.value.lower())(log_msg)

    def debug(self, message: str, **kwargs):
        """Log debug message"""
        self._log(LogLevel.DEBUG, message, **kwargs)

    def info(self, message: str, **kwargs):
        """Log info message"""
        self._log(LogLevel.INFO, message, **kwargs)

    def warning(self, message: str, **kwargs):
        """Log warning message"""
        self._log(LogLevel.WARNING, message, **kwargs)

    def error(self, message: str, **kwargs):
        """Log error message"""
        self._log(LogLevel.ERROR, message, **kwargs)

    def critical(self, message: str, **kwargs):
        """Log critical message"""
        self._log(LogLevel.CRITICAL, message, **kwargs)


# Global logger instance
app_logger = Logger()


def get_logger(name: str = "TodoChatbot") -> Logger:
    """
    Get a logger instance
    """
    return Logger(name=name)


# Convenience functions
def log_debug(message: str, **kwargs):
    app_logger.debug(message, **kwargs)


def log_info(message: str, **kwargs):
    app_logger.info(message, **kwargs)


def log_warning(message: str, **kwargs):
    app_logger.warning(message, **kwargs)


def log_error(message: str, **kwargs):
    app_logger.error(message, **kwargs)


def log_critical(message: str, **kwargs):
    app_logger.critical(message, **kwargs)