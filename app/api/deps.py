"""
Shared dependencies for API endpoints.
"""

from typing import Optional
from fastapi import UploadFile, File, Form
from app.utils.validators import validate_file_upload
from app.core.logging import logger


async def validate_upload_file(file: UploadFile = File(...)) -> tuple[str, bytes]:
    """
    Dependency to validate and read uploaded file.
    
    Args:
        file: Uploaded file
        
    Returns:
        Tuple of (filename, file_content_bytes)
        
    Raises:
        UnsupportedFileTypeError: If file type is invalid
        FileTooLargeError: If file size exceeds limit
    """
    try:
        # Read file content
        content = await file.read()
        
        # Validate file
        validate_file_upload(file.filename, len(content))
        
        logger.info(f"File upload validated: {file.filename} ({len(content)} bytes)")
        return file.filename, content
        
    except Exception as e:
        logger.error(f"File validation failed: {e}")
        raise


async def extract_form_options(
    theme: Optional[str] = Form(default="default"),
    font_family: Optional[str] = Form(default=None),
    font_size: Optional[int] = Form(default=None),
    font_color: Optional[str] = Form(default=None),
    background_color: Optional[str] = Form(default=None),
    page_size: Optional[str] = Form(default="A4"),
    margin: Optional[str] = Form(default="2cm"),
    title: Optional[str] = Form(default=None),
) -> dict:
    """
    Dependency to extract and return form options.
    
    Returns:
        Dictionary of conversion options
    """
    return {
        "theme": theme,
        "font_family": font_family,
        "font_size": font_size,
        "font_color": font_color,
        "background_color": background_color,
        "page_size": page_size,
        "margin": margin,
        "title": title,
    }
