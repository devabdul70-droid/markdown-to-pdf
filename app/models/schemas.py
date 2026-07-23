"""
Pydantic v2 models for request/response schemas.
"""

from typing import Optional, List
from enum import Enum
from pydantic import BaseModel, Field, field_validator


class PageSizeEnum(str, Enum):
    """Supported page sizes for PDF generation."""
    A4 = "A4"
    LETTER = "Letter"
    LEGAL = "Legal"


class ConvertOptions(BaseModel):
    """Optional customization options for PDF conversion."""
    theme: str = Field(
        default="default",
        description="Theme to apply (e.g., 'default', 'dark', 'academic', 'minimal')"
    )
    font_family: Optional[str] = Field(
        default=None,
        description="Font family override (e.g., 'Roboto', 'Georgia', 'Courier New')"
    )
    font_size: Optional[int] = Field(
        default=None,
        description="Font size in points (pt)"
    )
    font_color: Optional[str] = Field(
        default=None,
        description="Hex color code for text (e.g., '#1a1a1a')",
        examples=["#1a1a1a"]
    )
    background_color: Optional[str] = Field(
        default=None,
        description="Hex color code for background (e.g., '#ffffff')",
        examples=["#ffffff"]
    )
    page_size: PageSizeEnum = Field(
        default=PageSizeEnum.A4,
        description="Page size for the PDF"
    )
    margin: str = Field(
        default="2cm",
        description="Page margin (CSS-compatible, e.g., '2cm', '1in')"
    )
    title: Optional[str] = Field(
        default=None,
        description="PDF title (used in metadata)"
    )

    @field_validator("font_color", "background_color", mode="before")
    @classmethod
    def validate_hex_color(cls, v: Optional[str]) -> Optional[str]:
        """Validate hex color format."""
        if v is None:
            return None
        if not _is_valid_hex_color(v):
            raise ValueError(f"Invalid hex color: {v}. Expected format: #RRGGBB or #RGB")
        return v

    @field_validator("font_size")
    @classmethod
    def validate_font_size(cls, v: Optional[int]) -> Optional[int]:
        """Validate font size is positive."""
        if v is not None and v <= 0:
            raise ValueError("Font size must be positive")
        return v

    @field_validator("margin")
    @classmethod
    def validate_margin(cls, v: str) -> str:
        """Validate margin format (basic check)."""
        if not v or not any(unit in v for unit in ["cm", "mm", "in", "pt", "px", "em"]):
            raise ValueError("Margin must include a valid CSS unit (cm, mm, in, pt, px, em)")
        return v


class ConvertTextRequest(ConvertOptions):
    """Request body for POST /convert/text endpoint."""
    markdown: str = Field(
        ...,
        description="Raw Markdown text to convert to PDF",
        min_length=1
    )


class ThemeColorPalette(BaseModel):
    """Color palette preview for a theme."""
    primary_text: str
    background: str
    accent: str
    code_background: str


class ThemeInfo(BaseModel):
    """Information about an available theme."""
    id: str = Field(description="Theme identifier")
    name: str = Field(description="Human-readable theme name")
    description: str = Field(description="Brief description of the theme")
    default_font: str = Field(description="Default font family for this theme")
    colors: ThemeColorPalette = Field(description="Color palette preview")


class ThemeDetailResponse(ThemeInfo):
    """Detailed theme response including raw CSS variables."""
    css_variables: dict[str, str] = Field(description="CSS variable definitions")


class ThemesListResponse(BaseModel):
    """Response for GET /themes endpoint."""
    themes: List[ThemeInfo] = Field(description="List of available themes")


class ErrorResponse(BaseModel):
    """Consistent error response schema."""
    error: str = Field(description="Error type/code")
    detail: str = Field(description="Detailed error message")
    status_code: int = Field(description="HTTP status code")


def _is_valid_hex_color(color: str) -> bool:
    """Validate hex color format."""
    import re
    pattern = r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"
    return bool(re.match(pattern, color))
