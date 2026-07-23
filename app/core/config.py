"""
Configuration settings for the Markdown-to-PDF converter application.
Uses pydantic-settings to load configuration from environment variables.
"""

from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application info
    app_name: str = "Markdown to PDF Converter"
    app_version: str = "1.0.0"
    debug: bool = False

    # File upload constraints
    max_file_size: int = 5 * 1024 * 1024  # 5MB in bytes
    max_markdown_length: int = 500_000  # characters
    allowed_extensions: list[str] = [".md", ".markdown"]

    # Server configuration
    allowed_origins: Optional[str] = None  # comma-separated list of origins
    temp_dir: str = "/tmp"

    # PDF defaults
    default_page_size: str = "A4"
    default_margin: str = "2cm"
    default_font_size: int = 12

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    @property
    def cors_origins(self) -> list[str]:
        """Parse comma-separated ALLOWED_ORIGINS into a list."""
        if not self.allowed_origins:
            return ["*"]  # Allow all in development
        return [origin.strip() for origin in self.allowed_origins.split(",")]


# Global settings instance
settings = Settings()
