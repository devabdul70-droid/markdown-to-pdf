"""
API routes for theme management endpoints.
"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import ThemesListResponse, ThemeDetailResponse, ThemeInfo, ThemeColorPalette
from app.services.theme_service import theme_service
from app.utils.exceptions import UnsupportedThemeError
from app.core.logging import logger

router = APIRouter(prefix="/themes", tags=["themes"])


@router.get("", response_model=ThemesListResponse)
async def list_themes() -> ThemesListResponse:
    """
    Get list of all available themes.
    
    Returns:
        ThemesListResponse containing list of available themes with basic info
    """
    try:
        themes_data = theme_service.get_themes_list()
        
        themes = [
            ThemeInfo(
                id=t["id"],
                name=t["name"],
                description=t["description"],
                default_font=t["default_font"],
                colors=ThemeColorPalette(**t["colors"]),
            )
            for t in themes_data
        ]
        
        logger.info(f"Listed {len(themes)} themes")
        return ThemesListResponse(themes=themes)
        
    except Exception as e:
        logger.error(f"Failed to list themes: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve themes")


@router.get("/{theme_id}", response_model=ThemeDetailResponse)
async def get_theme_detail(theme_id: str) -> ThemeDetailResponse:
    """
    Get detailed information about a specific theme, including CSS variables.
    
    Args:
        theme_id: Theme identifier
        
    Returns:
        ThemeDetailResponse with full theme metadata and CSS variables
        
    Raises:
        HTTPException: 404 if theme not found
    """
    try:
        theme_info = theme_service.get_theme_info(theme_id)
        
        response = ThemeDetailResponse(
            id=theme_info["id"],
            name=theme_info["name"],
            description=theme_info["description"],
            default_font=theme_info["default_font"],
            colors=ThemeColorPalette(**theme_info["colors"]),
            css_variables=theme_info["css_variables"],
        )
        
        logger.info(f"Retrieved theme detail: {theme_id}")
        return response
        
    except UnsupportedThemeError as e:
        logger.warning(f"Theme not found: {theme_id}")
        # Return available themes in error detail
        available_themes = theme_service.get_available_themes()
        raise HTTPException(
            status_code=404,
            detail=f"Theme '{theme_id}' not found. Available themes: {', '.join(available_themes)}"
        )
    except Exception as e:
        logger.error(f"Failed to retrieve theme '{theme_id}': {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve theme")
