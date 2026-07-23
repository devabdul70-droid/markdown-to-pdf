"""
Tests for the conversion endpoints.
Tests /convert/text and /convert/file with various scenarios.
"""

import pytest
from fastapi.testclient import TestClient
from io import BytesIO

from app.main import app

client = TestClient(app)


class TestConvertText:
    """Tests for POST /convert/text endpoint."""

    def test_convert_text_minimal(self):
        """Test basic text conversion with minimal parameters."""
        response = client.post(
            "/convert/text",
            json={
                "markdown": "# Hello\n\nThis is a test document."
            }
        )
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/pdf"
        assert len(response.content) > 0

    def test_convert_text_with_default_theme(self):
        """Test text conversion with explicit default theme."""
        response = client.post(
            "/convert/text",
            json={
                "markdown": "# Test\n\n**Bold** and *italic* text.",
                "theme": "default"
            }
        )
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/pdf"

    def test_convert_text_with_dark_theme(self):
        """Test text conversion with dark theme."""
        response = client.post(
            "/convert/text",
            json={
                "markdown": "# Dark Theme\n\nTest content",
                "theme": "dark"
            }
        )
        assert response.status_code == 200

    def test_convert_text_with_academic_theme(self):
        """Test text conversion with academic theme."""
        response = client.post(
            "/convert/text",
            json={
                "markdown": "# Academic\n\nFormal document.",
                "theme": "academic"
            }
        )
        assert response.status_code == 200

    def test_convert_text_with_minimal_theme(self):
        """Test text conversion with minimal theme."""
        response = client.post(
            "/convert/text",
            json={
                "markdown": "# Minimal\n\nClean design.",
                "theme": "minimal"
            }
        )
        assert response.status_code == 200

    def test_convert_text_with_github_theme(self):
        """Test text conversion with github theme."""
        response = client.post(
            "/convert/text",
            json={
                "markdown": "# GitHub Style\n\n```python\nprint('hello')\n```",
                "theme": "github"
            }
        )
        assert response.status_code == 200

    def test_convert_text_with_custom_font_family(self):
        """Test text conversion with custom font family override."""
        response = client.post(
            "/convert/text",
            json={
                "markdown": "# Custom Font\n\nGeorgia serif font.",
                "theme": "default",
                "font_family": "Georgia"
            }
        )
        assert response.status_code == 200

    def test_convert_text_with_custom_font_size(self):
        """Test text conversion with custom font size override."""
        response = client.post(
            "/convert/text",
            json={
                "markdown": "# Large Font\n\nThis is bigger.",
                "theme": "default",
                "font_size": 16
            }
        )
        assert response.status_code == 200

    def test_convert_text_with_custom_colors(self):
        """Test text conversion with custom color overrides."""
        response = client.post(
            "/convert/text",
            json={
                "markdown": "# Colored Text",
                "theme": "default",
                "font_color": "#333333",
                "background_color": "#f9f9f9"
            }
        )
        assert response.status_code == 200

    def test_convert_text_with_title(self):
        """Test text conversion with custom title."""
        response = client.post(
            "/convert/text",
            json={
                "markdown": "# Document",
                "title": "My Custom Title"
            }
        )
        assert response.status_code == 200
        assert "attachment" in response.headers.get("content-disposition", "")

    def test_convert_text_with_page_size_letter(self):
        """Test text conversion with Letter page size."""
        response = client.post(
            "/convert/text",
            json={
                "markdown": "# Letter Size",
                "page_size": "Letter"
            }
        )
        assert response.status_code == 200

    def test_convert_text_with_page_size_legal(self):
        """Test text conversion with Legal page size."""
        response = client.post(
            "/convert/text",
            json={
                "markdown": "# Legal Size",
                "page_size": "Legal"
            }
        )
        assert response.status_code == 200

    def test_convert_text_with_custom_margin(self):
        """Test text conversion with custom margin."""
        response = client.post(
            "/convert/text",
            json={
                "markdown": "# Custom Margin",
                "margin": "1in"
            }
        )
        assert response.status_code == 200

    def test_convert_text_with_all_options(self):
        """Test text conversion with all customization options."""
        response = client.post(
            "/convert/text",
            json={
                "markdown": "# Complete\n\n**Bold**, *italic*, and `code`.",
                "theme": "academic",
                "font_family": "Georgia",
                "font_size": 14,
                "font_color": "#222222",
                "background_color": "#f5f5f5",
                "page_size": "A4",
                "margin": "2.5cm",
                "title": "Complete Test"
            }
        )
        assert response.status_code == 200

    def test_convert_text_with_markdown_features(self):
        """Test conversion with various markdown features."""
        markdown_content = """# Heading 1

## Heading 2

This is a paragraph with **bold**, *italic*, and `inline code`.

### Lists

- Item 1
- Item 2
- Nested item

1. First
2. Second

### Code Block

```python
def hello():
    print("Hello, World!")
```

### Table

| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell 2   |

### Blockquote

> This is a blockquote with multiple lines.
> It should be styled appropriately.

### Links and Images

[Link text](https://example.com)
"""
        response = client.post(
            "/convert/text",
            json={"markdown": markdown_content}
        )
        assert response.status_code == 200

    def test_convert_text_empty_markdown(self):
        """Test conversion fails with empty markdown."""
        response = client.post(
            "/convert/text",
            json={"markdown": ""}
        )
        assert response.status_code == 400
        assert "error" in response.json()

    def test_convert_text_whitespace_only(self):
        """Test conversion fails with whitespace-only markdown."""
        response = client.post(
            "/convert/text",
            json={"markdown": "   \n\t\n  "}
        )
        assert response.status_code == 400

    def test_convert_text_oversized_markdown(self):
        """Test conversion fails when markdown exceeds max length."""
        huge_markdown = "x" * 600_000  # Exceeds default 500,000 limit
        response = client.post(
            "/convert/text",
            json={"markdown": huge_markdown}
        )
        assert response.status_code == 400
        assert "exceeds" in response.json()["detail"]

    def test_convert_text_invalid_theme(self):
        """Test conversion fails with invalid theme."""
        response = client.post(
            "/convert/text",
            json={
                "markdown": "# Test",
                "theme": "nonexistent_theme"
            }
        )
        assert response.status_code == 404
        assert "error" in response.json()

    def test_convert_text_invalid_hex_color(self):
        """Test conversion fails with invalid hex color."""
        response = client.post(
            "/convert/text",
            json={
                "markdown": "# Test",
                "font_color": "not_a_hex_color"
            }
        )
        assert response.status_code == 422  # Validation error

    def test_convert_text_invalid_font_size(self):
        """Test conversion fails with invalid font size."""
        response = client.post(
            "/convert/text",
            json={
                "markdown": "# Test",
                "font_size": -5
            }
        )
        assert response.status_code == 422

    def test_convert_text_invalid_page_size(self):
        """Test conversion with invalid page size defaults to A4."""
        response = client.post(
            "/convert/text",
            json={
                "markdown": "# Test",
                "page_size": "InvalidSize"
            }
        )
        # Should either fail or default to A4 depending on validation
        assert response.status_code in [200, 422]


class TestConvertFile:
    """Tests for POST /convert/file endpoint."""

    def test_convert_file_markdown(self):
        """Test basic file conversion with .md file."""
        markdown_content = b"# Test\n\nThis is a test."
        response = client.post(
            "/convert/file",
            data={},
            files={"file": ("test.md", BytesIO(markdown_content), "text/markdown")}
        )
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/pdf"

    def test_convert_file_markdown_extension(self):
        """Test file conversion with .markdown extension."""
        markdown_content = b"# Test\n\nContent."
        response = client.post(
            "/convert/file",
            data={},
            files={"file": ("test.markdown", BytesIO(markdown_content), "text/markdown")}
        )
        assert response.status_code == 200

    def test_convert_file_with_theme(self):
        """Test file conversion with theme selection."""
        markdown_content = b"# Dark Theme\n\nUsing dark theme."
        response = client.post(
            "/convert/file",
            data={"theme": "dark"},
            files={"file": ("test.md", BytesIO(markdown_content), "text/markdown")}
        )
        assert response.status_code == 200

    def test_convert_file_with_custom_options(self):
        """Test file conversion with custom styling options."""
        markdown_content = b"# Styled\n\nCustom styling."
        response = client.post(
            "/convert/file",
            data={
                "theme": "academic",
                "font_size": "14",
                "font_color": "#333333",
                "page_size": "Letter"
            },
            files={"file": ("test.md", BytesIO(markdown_content), "text/markdown")}
        )
        assert response.status_code == 200

    def test_convert_file_with_title(self):
        """Test file conversion with custom title."""
        markdown_content = b"# Document"
        response = client.post(
            "/convert/file",
            data={"title": "Custom PDF Title"},
            files={"file": ("test.md", BytesIO(markdown_content), "text/markdown")}
        )
        assert response.status_code == 200

    def test_convert_file_invalid_extension(self):
        """Test file conversion fails with invalid file extension."""
        content = b"# Test"
        response = client.post(
            "/convert/file",
            data={},
            files={"file": ("test.txt", BytesIO(content), "text/plain")}
        )
        assert response.status_code == 415

    def test_convert_file_oversized(self):
        """Test file conversion fails when file exceeds size limit."""
        # Create a file larger than 5MB
        oversized_content = b"x" * (6 * 1024 * 1024)
        response = client.post(
            "/convert/file",
            data={},
            files={"file": ("large.md", BytesIO(oversized_content), "text/markdown")}
        )
        assert response.status_code == 413

    def test_convert_file_invalid_theme(self):
        """Test file conversion fails with invalid theme."""
        markdown_content = b"# Test"
        response = client.post(
            "/convert/file",
            data={"theme": "invalid_theme"},
            files={"file": ("test.md", BytesIO(markdown_content), "text/markdown")}
        )
        assert response.status_code == 404
