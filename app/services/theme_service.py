"""
Theme management service.
Loads theme CSS files, merges with user overrides.
"""

import re
from pathlib import Path
from typing import Optional, Dict
from app.utils.exceptions import UnsupportedThemeError
from app.core.logging import logger


class ThemeService:
    """Service for managing themes and CSS customization."""

    # Path to themes directory (relative to this file)
    THEMES_DIR = Path(__file__).parent.parent / "themes"

    # Predefined theme metadata
    THEME_METADATA = {
        "default": {
            "name": "Default",
            "description": "Clean, neutral theme suitable for general documents",
            "default_font": "Segoe UI, sans-serif",
            "preview_colors": {
                "primary_text": "#1a1a1a",
                "background": "#ffffff",
                "accent": "#0066cc",
                "code_background": "#f5f5f5",
            }
        },
        "dark": {
            "name": "Dark",
            "description": "Dark background with light text for reading in low-light",
            "default_font": "Segoe UI, sans-serif",
            "preview_colors": {
                "primary_text": "#e0e0e0",
                "background": "#1e1e1e",
                "accent": "#66b3ff",
                "code_background": "#2d2d2d",
            }
        },
        "academic": {
            "name": "Academic",
            "description": "Formal serif font, suitable for academic papers and articles",
            "default_font": "Georgia, serif",
            "preview_colors": {
                "primary_text": "#333333",
                "background": "#ffffff",
                "accent": "#2c5aa0",
                "code_background": "#fafafa",
            }
        },
        "minimal": {
            "name": "Minimal",
            "description": "Minimalist design with lots of whitespace and clean typography",
            "default_font": "Helvetica, Arial, sans-serif",
            "preview_colors": {
                "primary_text": "#000000",
                "background": "#ffffff",
                "accent": "#555555",
                "code_background": "#efefef",
            }
        },
        "github": {
            "name": "GitHub",
            "description": "Inspired by GitHub's markdown rendering style",
            "default_font": "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
            "preview_colors": {
                "primary_text": "#24292e",
                "background": "#ffffff",
                "accent": "#0366d6",
                "code_background": "#f6f8fa",
            }
        }
    }

    @classmethod
    def get_available_themes(cls) -> list[str]:
        """Get list of available theme IDs."""
        return list(cls.THEME_METADATA.keys())

    @classmethod
    def load_theme_css(cls, theme_id: str) -> str:
        """
        Load raw CSS from theme file.
        
        Args:
            theme_id: Theme identifier
            
        Returns:
            CSS content as string
            
        Raises:
            UnsupportedThemeError: If theme not found
        """
        available_themes = cls.get_available_themes()
        
        if theme_id not in available_themes:
            raise UnsupportedThemeError(theme_id, available_themes)

        theme_file = cls.THEMES_DIR / f"{theme_id}.css"
        
        if not theme_file.exists():
            raise UnsupportedThemeError(theme_id, available_themes)

        try:
            css_content = theme_file.read_text(encoding="utf-8")
            logger.info(f"Loaded theme: {theme_id}")
            return css_content
        except Exception as e:
            logger.error(f"Failed to load theme '{theme_id}': {e}")
            raise UnsupportedThemeError(theme_id, available_themes)

    @classmethod
    def extract_css_variables(cls, css_content: str) -> Dict[str, str]:
        """
        Extract CSS custom property definitions from CSS content.
        
        Args:
            css_content: CSS string
            
        Returns:
            Dictionary of variable names to values
        """
        variables = {}
        
        # Match CSS custom properties in :root block
        pattern = r"--([a-z-]+):\s*([^;]+);"
        matches = re.finditer(pattern, css_content, re.IGNORECASE)
        
        for match in matches:
            var_name = match.group(1)
            var_value = match.group(2).strip()
            variables[var_name] = var_value

        return variables

    @classmethod
    def merge_theme_with_overrides(
        cls,
        theme_id: str,
        font_family: Optional[str] = None,
        font_size: Optional[int] = None,
        font_color: Optional[str] = None,
        background_color: Optional[str] = None,
    ) -> str:
        """
        Load theme CSS and override specific variables with user-supplied values.
        
        Args:
            theme_id: Theme identifier
            font_family: Optional font family override
            font_size: Optional font size override (in pt)
            font_color: Optional text color override (hex)
            background_color: Optional background color override (hex)
            
        Returns:
            Complete CSS with merged overrides
            
        Raises:
            UnsupportedThemeError: If theme not found
        """
        # Load base theme CSS
        css_content = cls.load_theme_css(theme_id)

        # Extract existing variables
        variables = cls.extract_css_variables(css_content)

        # Apply user overrides
        if font_family:
            variables["font-family"] = font_family
        if font_size:
            variables["font-size"] = f"{font_size}pt"
        if font_color:
            variables["font-color"] = font_color
        if background_color:
            variables["background-color"] = background_color

        # Rebuild CSS with overridden variables
        override_css = ":root {\n"
        for var_name, var_value in variables.items():
            override_css += f"  --{var_name}: {var_value};\n"
        override_css += "}\n"

        # Append remaining CSS (everything after :root block)
        remaining_css = re.sub(r":root\s*\{[^}]*\}", "", css_content)
        final_css = override_css + remaining_css

        logger.info(
            f"Theme '{theme_id}' merged with overrides: "
            f"font_family={font_family}, font_size={font_size}, "
            f"font_color={font_color}, background_color={background_color}"
        )

        return final_css

    @classmethod
    def get_theme_info(cls, theme_id: str) -> dict:
        """
        Get metadata and CSS variables for a specific theme.
        
        Args:
            theme_id: Theme identifier
            
        Returns:
            Dictionary with theme info and CSS variables
            
        Raises:
            UnsupportedThemeError: If theme not found
        """
        available_themes = cls.get_available_themes()
        
        if theme_id not in available_themes:
            raise UnsupportedThemeError(theme_id, available_themes)

        metadata = cls.THEME_METADATA[theme_id]
        css_content = cls.load_theme_css(theme_id)
        variables = cls.extract_css_variables(css_content)

        return {
            "id": theme_id,
            "name": metadata["name"],
            "description": metadata["description"],
            "default_font": metadata["default_font"],
            "colors": {
                "primary_text": metadata["preview_colors"]["primary_text"],
                "background": metadata["preview_colors"]["background"],
                "accent": metadata["preview_colors"]["accent"],
                "code_background": metadata["preview_colors"]["code_background"],
            },
            "css_variables": variables,
        }

    @classmethod
    def get_themes_list(cls) -> list[dict]:
        """
        Get list of all available themes with basic info.
        
        Returns:
            List of theme info dictionaries
        """
        themes = []
        for theme_id in cls.get_available_themes():
            metadata = cls.THEME_METADATA[theme_id]
            themes.append({
                "id": theme_id,
                "name": metadata["name"],
                "description": metadata["description"],
                "default_font": metadata["default_font"],
                "colors": {
                    "primary_text": metadata["preview_colors"]["primary_text"],
                    "background": metadata["preview_colors"]["background"],
                    "accent": metadata["preview_colors"]["accent"],
                    "code_background": metadata["preview_colors"]["code_background"],
                },
            })
        return themes


# Singleton instance
theme_service = ThemeService()
