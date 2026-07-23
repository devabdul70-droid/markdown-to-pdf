"""
Validation utilities for file uploads and markdown input.
"""

import re
from pathlib import Path
from app.core.config import settings
from app.utils.exceptions import (
    FileTooLargeError,
    UnsupportedFileTypeError,
    InvalidMarkdownError,
)


def validate_file_upload(filename: str, file_size: int) -> None:
    """
    Validate uploaded file type and size.
    
    Args:
        filename: Name of the uploaded file
        file_size: Size of the file in bytes
        
    Raises:
        UnsupportedFileTypeError: If file extension is not allowed
        FileTooLargeError: If file size exceeds limit
    """
    # Check extension
    file_ext = Path(filename).suffix.lower()
    if file_ext not in settings.allowed_extensions:
        raise UnsupportedFileTypeError(filename, settings.allowed_extensions)
    
    # Check file size
    if file_size > settings.max_file_size:
        raise FileTooLargeError(file_size, settings.max_file_size)


def validate_markdown_input(markdown: str) -> None:
    """
    Validate markdown input.
    
    Args:
        markdown: Raw markdown text
        
    Raises:
        InvalidMarkdownError: If markdown is invalid or too long
    """
    if not markdown or not markdown.strip():
        raise InvalidMarkdownError("Markdown content cannot be empty")
    
    if len(markdown) > settings.max_markdown_length:
        raise InvalidMarkdownError(
            f"Markdown exceeds maximum length of {settings.max_markdown_length} characters"
        )


def sanitize_markdown(markdown: str) -> str:
    """
    Basic sanitization of markdown input.
    
    Args:
        markdown: Raw markdown text
        
    Returns:
        Sanitized markdown string
    """
    # Remove null bytes and control characters
    sanitized = "".join(char for char in markdown if ord(char) >= 32 or char in "\t\n\r")
    return sanitized.strip()


def is_valid_hex_color(color: str) -> bool:
    """
    Validate hex color format.
    
    Args:
        color: Color string to validate (e.g., '#1a1a1a')
        
    Returns:
        True if valid hex color, False otherwise
    """
    pattern = r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"
    return bool(re.match(pattern, color))
