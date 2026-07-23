"""
API routes for markdown conversion endpoints.
"""

from fastapi import APIRouter, Body, Depends
from fastapi.responses import FileResponse, StreamingResponse
from io import BytesIO
from jinja2 import Template
import time

from app.models.schemas import ConvertTextRequest, ConvertOptions
from app.services.markdown_service import markdown_service
from app.services.pdf_service import pdf_service
from app.services.theme_service import theme_service
from app.utils.validators import validate_markdown_input, sanitize_markdown
from app.core.logging import logger
from app.api.deps import validate_upload_file, extract_form_options
from pathlib import Path

router = APIRouter(prefix="/convert", tags=["conversion"])

# Path to Jinja2 template
TEMPLATE_PATH = Path(__file__).parent.parent / "templates" / "pdf_template.html"


def _load_template() -> Template:
    """Load the PDF template from file."""
    template_content = TEMPLATE_PATH.read_text(encoding="utf-8")
    return Template(template_content)


@router.post("/text", response_class=StreamingResponse)
async def convert_text(request: ConvertTextRequest) -> StreamingResponse:
    """
    Convert markdown text to PDF.
    
    Args:
        request: ConvertTextRequest with markdown and optional customizations
        
    Returns:
        PDF file as streaming response
    """
    start_time = time.time()
    
    try:
        # Validate markdown input
        validate_markdown_input(request.markdown)
        
        # Sanitize markdown
        markdown_text = sanitize_markdown(request.markdown)
        
        logger.info(f"Processing text conversion: theme={request.theme}, length={len(markdown_text)}")
        
        # Convert markdown to HTML
        html_content = markdown_service.convert(markdown_text)
        
        # Merge theme with user overrides
        css_content = theme_service.merge_theme_with_overrides(
            theme_id=request.theme,
            font_family=request.font_family,
            font_size=request.font_size,
            font_color=request.font_color,
            background_color=request.background_color,
        )
        
        # Load and render template
        template = _load_template()
        full_html = template.render(
            content=html_content,
            custom_css=css_content,
            page_size=request.page_size.value,
            margin=request.margin,
        )
        
        # Generate PDF
        pdf_bytes = pdf_service.render_to_pdf(
            html_content=full_html,
            css_content=css_content,
            title=request.title or "Document",
        )
        
        # Create filename
        filename = (request.title or "document").replace(" ", "_").lower()
        if not filename.endswith(".pdf"):
            filename += ".pdf"
        
        duration = time.time() - start_time
        logger.info(
            f"Text conversion completed: theme={request.theme}, "
            f"size={len(pdf_bytes)} bytes, duration={duration:.2f}s"
        )
        
        # Return as streaming response
        return StreamingResponse(
            iter([pdf_bytes]),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )
        
    except Exception as e:
        logger.error(f"Text conversion failed: {e}")
        raise


@router.post("/file", response_class=StreamingResponse)
async def convert_file(
    file_data: tuple[str, bytes] = Depends(validate_upload_file),
    options: dict = Depends(extract_form_options),
) -> StreamingResponse:
    """
    Convert uploaded markdown file to PDF.
    
    Args:
        file_data: Tuple of (filename, content) from validate_upload_file
        options: Form options from extract_form_options
        
    Returns:
        PDF file as streaming response
    """
    start_time = time.time()
    filename, file_content = file_data
    
    try:
        # Decode file content to string
        markdown_text = file_content.decode("utf-8")
        
        # Validate markdown input
        validate_markdown_input(markdown_text)
        
        # Sanitize markdown
        markdown_text = sanitize_markdown(markdown_text)
        
        logger.info(
            f"Processing file conversion: file={filename}, "
            f"theme={options['theme']}, length={len(markdown_text)}"
        )
        
        # Convert markdown to HTML
        html_content = markdown_service.convert(markdown_text)
        
        # Merge theme with user overrides
        css_content = theme_service.merge_theme_with_overrides(
            theme_id=options["theme"],
            font_family=options.get("font_family"),
            font_size=options.get("font_size"),
            font_color=options.get("font_color"),
            background_color=options.get("background_color"),
        )
        
        # Load and render template
        template = _load_template()
        full_html = template.render(
            content=html_content,
            custom_css=css_content,
            page_size=options.get("page_size", "A4"),
            margin=options.get("margin", "2cm"),
        )
        
        # Generate PDF
        pdf_bytes = pdf_service.render_to_pdf(
            html_content=full_html,
            css_content=css_content,
            title=options.get("title") or filename,
        )
        
        # Create output filename
        output_filename = (options.get("title") or filename).replace(" ", "_").lower()
        if not output_filename.endswith(".pdf"):
            output_filename = output_filename.replace(".md", "").replace(".markdown", "") + ".pdf"
        
        duration = time.time() - start_time
        logger.info(
            f"File conversion completed: file={filename}, "
            f"theme={options['theme']}, size={len(pdf_bytes)} bytes, duration={duration:.2f}s"
        )
        
        # Return as streaming response
        return StreamingResponse(
            iter([pdf_bytes]),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={output_filename}"},
        )
        
    except Exception as e:
        logger.error(f"File conversion failed: {e}")
        raise
