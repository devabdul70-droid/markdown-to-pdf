"""
Tests for the themes endpoints.
Tests GET /themes and GET /themes/{theme_id}.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestThemesList:
    """Tests for GET /themes endpoint."""

    def test_list_themes_success(self):
        """Test listing all available themes."""
        response = client.get("/themes")
        assert response.status_code == 200
        data = response.json()
        assert "themes" in data
        assert isinstance(data["themes"], list)
        assert len(data["themes"]) > 0

    def test_list_themes_structure(self):
        """Test that theme list has correct structure."""
        response = client.get("/themes")
        data = response.json()
        
        for theme in data["themes"]:
            assert "id" in theme
            assert "name" in theme
            assert "description" in theme
            assert "default_font" in theme
            assert "colors" in theme
            
            # Check colors structure
            colors = theme["colors"]
            assert "primary_text" in colors
            assert "background" in colors
            assert "accent" in colors
            assert "code_background" in colors

    def test_list_themes_contains_default_theme(self):
        """Test that default theme is in the list."""
        response = client.get("/themes")
        data = response.json()
        theme_ids = [t["id"] for t in data["themes"]]
        assert "default" in theme_ids

    def test_list_themes_contains_all_themes(self):
        """Test that all expected themes are present."""
        response = client.get("/themes")
        data = response.json()
        theme_ids = [t["id"] for t in data["themes"]]
        
        expected_themes = ["default", "dark", "academic", "minimal", "github"]
        for expected in expected_themes:
            assert expected in theme_ids

    def test_list_themes_theme_info(self):
        """Test individual theme information in list."""
        response = client.get("/themes")
        data = response.json()
        
        default_theme = next(t for t in data["themes"] if t["id"] == "default")
        assert default_theme["name"] == "Default"
        assert len(default_theme["description"]) > 0
        assert "font" in default_theme["default_font"].lower() or "system" in default_theme["default_font"].lower()


class TestThemeDetail:
    """Tests for GET /themes/{theme_id} endpoint."""

    def test_get_default_theme(self):
        """Test retrieving default theme details."""
        response = client.get("/themes/default")
        assert response.status_code == 200
        data = response.json()
        
        assert data["id"] == "default"
        assert data["name"] == "Default"
        assert "description" in data
        assert "default_font" in data
        assert "colors" in data
        assert "css_variables" in data

    def test_get_dark_theme(self):
        """Test retrieving dark theme details."""
        response = client.get("/themes/dark")
        assert response.status_code == 200
        data = response.json()
        
        assert data["id"] == "dark"
        assert data["name"] == "Dark"

    def test_get_academic_theme(self):
        """Test retrieving academic theme details."""
        response = client.get("/themes/academic")
        assert response.status_code == 200
        data = response.json()
        
        assert data["id"] == "academic"
        assert data["name"] == "Academic"

    def test_get_minimal_theme(self):
        """Test retrieving minimal theme details."""
        response = client.get("/themes/minimal")
        assert response.status_code == 200
        data = response.json()
        
        assert data["id"] == "minimal"
        assert data["name"] == "Minimal"

    def test_get_github_theme(self):
        """Test retrieving github theme details."""
        response = client.get("/themes/github")
        assert response.status_code == 200
        data = response.json()
        
        assert data["id"] == "github"
        assert data["name"] == "GitHub"

    def test_theme_detail_structure(self):
        """Test detailed theme response structure."""
        response = client.get("/themes/default")
        data = response.json()
        
        # Basic info
        assert "id" in data
        assert "name" in data
        assert "description" in data
        assert "default_font" in data
        
        # Colors
        assert "colors" in data
        colors = data["colors"]
        assert "primary_text" in colors
        assert "background" in colors
        assert "accent" in colors
        assert "code_background" in colors
        
        # CSS variables
        assert "css_variables" in data
        assert isinstance(data["css_variables"], dict)

    def test_theme_css_variables(self):
        """Test that theme contains CSS variables."""
        response = client.get("/themes/default")
        data = response.json()
        css_vars = data["css_variables"]
        
        # Should have common CSS variables
        assert len(css_vars) > 0
        
        # Check for expected variables (may vary by theme)
        var_names = list(css_vars.keys())
        assert any("font" in name for name in var_names)
        assert any("color" in name for name in var_names)

    def test_invalid_theme_returns_404(self):
        """Test that invalid theme returns 404."""
        response = client.get("/themes/nonexistent_theme")
        assert response.status_code == 404

    def test_invalid_theme_error_message(self):
        """Test error message for invalid theme."""
        response = client.get("/themes/invalid")
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"]
        # Should suggest available themes
        assert "Available themes" in data["detail"]

    def test_theme_colors_are_valid_hex(self):
        """Test that theme colors are valid hex codes."""
        response = client.get("/themes/default")
        data = response.json()
        colors = data["colors"]
        
        import re
        hex_pattern = r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"
        
        for color_name, color_value in colors.items():
            assert re.match(hex_pattern, color_value), \
                f"Color {color_name}={color_value} is not valid hex"

    def test_all_themes_have_required_fields(self):
        """Test that all themes have required fields."""
        response = client.get("/themes")
        data = response.json()
        
        for theme_id in ["default", "dark", "academic", "minimal", "github"]:
            detail_response = client.get(f"/themes/{theme_id}")
            assert detail_response.status_code == 200
            detail_data = detail_response.json()
            
            # Check all required fields
            assert detail_data["id"] == theme_id
            assert "name" in detail_data
            assert "description" in detail_data
            assert "default_font" in detail_data
            assert "colors" in detail_data
            assert "css_variables" in detail_data

    def test_theme_case_sensitivity(self):
        """Test theme ID case sensitivity."""
        # Assuming theme IDs are lowercase
        response_lower = client.get("/themes/default")
        response_upper = client.get("/themes/DEFAULT")
        
        # Should handle lowercase correctly
        assert response_lower.status_code == 200
        
        # Upper case might fail (depending on implementation)
        # This test documents the expected behavior
        if response_upper.status_code != 200:
            assert response_upper.status_code == 404


class TestThemeConsistency:
    """Tests for consistency between list and detail endpoints."""

    def test_themes_in_list_match_detail(self):
        """Test that themes listed in /themes have matching /themes/{id}."""
        list_response = client.get("/themes")
        list_data = list_response.json()
        
        for theme in list_data["themes"]:
            theme_id = theme["id"]
            detail_response = client.get(f"/themes/{theme_id}")
            
            assert detail_response.status_code == 200
            detail_data = detail_response.json()
            
            # Basic fields should match
            assert detail_data["id"] == theme["id"]
            assert detail_data["name"] == theme["name"]
            assert detail_data["default_font"] == theme["default_font"]

    def test_theme_colors_consistency(self):
        """Test that colors are consistent between list and detail."""
        list_response = client.get("/themes")
        list_data = list_response.json()
        
        for theme in list_data["themes"]:
            theme_id = theme["id"]
            detail_response = client.get(f"/themes/{theme_id}")
            detail_data = detail_response.json()
            
            # Colors should match
            assert theme["colors"] == detail_data["colors"]
