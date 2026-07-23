"""
Custom exception classes for the application.
"""


class MarkdownToPDFException(Exception):
    """Base exception for all application errors."""
    def __init__(self, error: str, detail: str, status_code: int = 500):
        self.error = error
        self.detail = detail
        self.status_code = status_code
        super().__init__(f"{error}: {detail}")


class InvalidMarkdownError(MarkdownToPDFException):
    """Raised when markdown input is invalid or too large."""
    def __init__(self, detail: str):
        super().__init__("InvalidMarkdown", detail, 400)


class UnsupportedThemeError(MarkdownToPDFException):
    """Raised when requested theme is not found."""
    def __init__(self, theme_id: str, available_themes: list[str]):
        detail = (
            f"Theme '{theme_id}' not found. "
            f"Available themes: {', '.join(available_themes)}"
        )
        super().__init__("UnsupportedTheme", detail, 404)


class FileTooLargeError(MarkdownToPDFException):
    """Raised when uploaded file exceeds size limit."""
    def __init__(self, file_size: int, max_size: int):
        detail = f"File size ({file_size} bytes) exceeds maximum ({max_size} bytes)"
        super().__init__("FileTooLarge", detail, 413)


class UnsupportedFileTypeError(MarkdownToPDFException):
    """Raised when uploaded file has unsupported extension."""
    def __init__(self, filename: str, allowed_extensions: list[str]):
        detail = (
            f"File '{filename}' has unsupported type. "
            f"Allowed: {', '.join(allowed_extensions)}"
        )
        super().__init__("UnsupportedFileType", detail, 415)


class PDFGenerationError(MarkdownToPDFException):
    """Raised when PDF generation fails."""
    def __init__(self, detail: str):
        super().__init__("PDFGenerationFailed", detail, 500)


class TemplateRenderError(MarkdownToPDFException):
    """Raised when template rendering fails."""
    def __init__(self, detail: str):
        super().__init__("TemplateRenderFailed", detail, 500)
