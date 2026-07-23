"""
Markdown to HTML conversion service using python-markdown.
"""

import markdown
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from app.core.logging import logger


class MarkdownService:
    """Service for converting Markdown to HTML."""

    # Markdown extensions to use
    EXTENSIONS = [
        "extra",           # Provides: abbreviations, attribute lists, definition lists, tables
        "codehilite",      # Syntax highlighting for code blocks
        "tables",          # Support for tables (redundant with 'extra', but explicit)
        "toc",             # Table of contents generation
        "fenced_code",     # Fenced code blocks
    ]

    EXTENSION_CONFIGS = {
        "codehilite": {
            "use_pygments": True,
            "linenums": False,
        },
        "toc": {
            "toc_depth": "2-3",
            "title": "Contents",
        }
    }

    @staticmethod
    def convert(markdown_text: str) -> str:
        """
        Convert markdown text to HTML.
        
        Args:
            markdown_text: Raw markdown text
            
        Returns:
            Rendered HTML string
        """
        try:
            html = markdown.markdown(
                markdown_text,
                extensions=MarkdownService.EXTENSIONS,
                extension_configs=MarkdownService.EXTENSION_CONFIGS,
            )
            logger.info("Markdown converted to HTML successfully")
            return html
        except Exception as e:
            logger.error(f"Markdown conversion failed: {e}")
            raise


# Singleton instance
markdown_service = MarkdownService()
