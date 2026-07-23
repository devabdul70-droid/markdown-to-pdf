"""
PDF rendering service using WeasyPrint.
Converts HTML+CSS to PDF bytes.
"""

from io import BytesIO
from weasyprint import HTML, CSS
from app.utils.exceptions import PDFGenerationError
from app.core.logging import logger


class PDFService:
    """Service for rendering HTML to PDF."""

    @staticmethod
    def render_to_pdf(
        html_content: str,
        css_content: str,
        title: str = "Document",
    ) -> bytes:
        """
        Render HTML with CSS to PDF bytes.
        
        Args:
            html_content: Complete HTML string (including doctype, html tags, etc.)
            css_content: CSS string to apply to the HTML
            title: PDF title for metadata
            
        Returns:
            PDF content as bytes
            
        Raises:
            PDFGenerationError: If PDF generation fails
        """
        try:
            logger.info(f"Starting PDF generation for '{title}'")

            # Create HTML object from string
            html_obj = HTML(string=html_content, base_url=None)

            # Create CSS object from string
            css_obj = CSS(string=css_content)

            # Render to PDF in memory
            pdf_bytes = BytesIO()
            html_obj.write_pdf(
                pdf_bytes,
                stylesheets=[css_obj],
            )

            pdf_content = pdf_bytes.getvalue()
            logger.info(f"PDF generated successfully ({len(pdf_content)} bytes)")

            return pdf_content

        except Exception as e:
            logger.error(f"PDF generation failed: {e}")
            raise PDFGenerationError(f"Failed to generate PDF: {str(e)}")


# Singleton instance
pdf_service = PDFService()
