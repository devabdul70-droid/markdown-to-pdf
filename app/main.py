"""
Main FastAPI application.
Includes router setup, CORS configuration, exception handlers, and middleware.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.logging import logger, setup_logging
from app.utils.exceptions import MarkdownToPDFException
from app.api.routes import convert, themes
from app.models.schemas import ErrorResponse

# Set up logging
setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for application startup and shutdown.
    """
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    yield
    logger.info(f"Shutting down {settings.app_name}")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "Convert Markdown to beautifully styled PDFs with customizable themes, "
        "fonts, colors, and page settings."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Only add lifespan if not in a serverless environment that might choke on it
# (Vercel typically handles this, but some environments have issues)
# For now, we'll keep it simple to troubleshoot crashes.
# app.router.lifespan_context = lifespan

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers
@app.exception_handler(MarkdownToPDFException)
async def markdown_to_pdf_exception_handler(
    request: Request,
    exc: MarkdownToPDFException
) -> JSONResponse:
    """Handle custom application exceptions."""
    logger.error(f"Application error: {exc.error} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.error,
            "detail": exc.detail,
            "status_code": exc.status_code,
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(
    request: Request,
    exc: Exception
) -> JSONResponse:
    """Handle unexpected exceptions."""
    logger.error(f"Unexpected error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "InternalServerError",
            "detail": "An unexpected error occurred",
            "status_code": 500,
        },
    )


# Include routers
app.include_router(convert.router)
app.include_router(themes.router)


# Health check endpoint
@app.get("/health")
async def health_check() -> dict:
    """
    Health check endpoint.
    
    Returns:
        Dictionary with status information
    """
    return {
        "status": "healthy",
        "app": settings.app_name,
        "version": settings.app_version,
    }


@app.get("/", tags=["info"])
async def root() -> dict:
    """
    Root endpoint with API information.
    
    Returns:
        Dictionary with API info and available endpoints
    """
    return {
        "app": settings.app_name,
        "version": settings.app_version,
        "description": "Convert Markdown to PDF",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "redoc": "/redoc",
            "convert_text": "POST /convert/text",
            "convert_file": "POST /convert/file",
            "list_themes": "GET /themes",
            "theme_detail": "GET /themes/{theme_id}",
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
    )
