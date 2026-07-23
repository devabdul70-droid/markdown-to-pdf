# API Endpoint Documentation

## Base URL

```
http://localhost:8000
```

## Response Format

All responses include appropriate HTTP status codes and JSON bodies (except PDF responses).

### Error Response Format
```json
{
  "error": "ErrorType",
  "detail": "Detailed error message",
  "status_code": 400
}
```

---

## Endpoints

### 1. Convert Markdown Text to PDF

**Endpoint:** `POST /convert/text`

**Description:** Convert raw markdown text to a PDF document.

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "markdown": "string (required)",
  "theme": "string (optional, default: 'default')",
  "font_family": "string (optional)",
  "font_size": "integer (optional, 6-72)",
  "font_color": "string (optional, hex code)",
  "background_color": "string (optional, hex code)",
  "page_size": "string (optional, 'A4'|'Letter'|'Legal', default: 'A4')",
  "margin": "string (optional, default: '2cm')",
  "title": "string (optional)"
}
```

**Request Example:**
```bash
curl -X POST http://localhost:8000/convert/text \
  -H "Content-Type: application/json" \
  -d '{
    "markdown": "# Hello World\n\nThis is **bold** text.",
    "theme": "dark",
    "font_size": 14,
    "title": "My Document"
  }' \
  --output document.pdf
```

**Response:**
- **Status:** 200 OK
- **Content-Type:** application/pdf
- **Body:** PDF file bytes

**Response Headers:**
```
Content-Type: application/pdf
Content-Disposition: attachment; filename="document.pdf"
```

**Error Responses:**

| Status | Error | Description |
|--------|-------|-------------|
| 400 | InvalidMarkdown | Markdown is empty, too long, or invalid |
| 404 | UnsupportedTheme | Theme not found |
| 422 | ValidationError | Invalid request parameters |
| 500 | PDFGenerationFailed | PDF rendering error |

**Field Specifications:**

- **markdown**: 
  - Required field
  - Must be non-empty
  - Max 500,000 characters (configurable)
  - Supports standard Markdown + tables, code highlighting, TOC

- **theme**: 
  - Optional, defaults to "default"
  - Valid values: "default", "dark", "academic", "minimal", "github"
  - Case-sensitive

- **font_family**: 
  - Optional
  - Any CSS-compatible font name
  - Examples: "Roboto", "Georgia", "Courier New", "Arial"
  - Will override theme default

- **font_size**: 
  - Optional
  - Integer between 6 and 72 (points)
  - Will override theme default

- **font_color**: 
  - Optional
  - Must be valid hex color code
  - Format: "#RRGGBB" or "#RGB"
  - Examples: "#1a1a1a", "#fff", "#333"

- **background_color**: 
  - Optional
  - Must be valid hex color code
  - Format: "#RRGGBB" or "#RGB"

- **page_size**: 
  - Optional, defaults to "A4"
  - Valid values: "A4" (210×297mm), "Letter" (8.5×11in), "Legal" (8.5×14in)

- **margin**: 
  - Optional, defaults to "2cm"
  - Must include CSS unit: cm, mm, in, pt, px, em
  - Examples: "1cm", "0.5in", "20mm"

- **title**: 
  - Optional
  - Used for PDF metadata and default filename
  - If not provided, defaults to "Document"

---

### 2. Convert Markdown File to PDF

**Endpoint:** `POST /convert/file`

**Description:** Convert an uploaded markdown file to PDF.

**Request Headers:**
```
Content-Type: multipart/form-data
```

**Request Form Data:**
```
file: file (required, .md or .markdown, max 5MB)
theme: string (optional, default: "default")
font_family: string (optional)
font_size: integer (optional)
font_color: string (optional, hex code)
background_color: string (optional, hex code)
page_size: string (optional, 'A4'|'Letter'|'Legal')
margin: string (optional)
title: string (optional)
```

**Request Example:**
```bash
curl -X POST http://localhost:8000/convert/file \
  -F "file=@document.md" \
  -F "theme=academic" \
  -F "font_size=13" \
  -F "margin=2.5cm" \
  --output output.pdf
```

**Response:**
- **Status:** 200 OK
- **Content-Type:** application/pdf
- **Body:** PDF file bytes

**Error Responses:**

| Status | Error | Description |
|--------|-------|-------------|
| 413 | FileTooLarge | File exceeds 5MB limit |
| 415 | UnsupportedFileType | File is not .md or .markdown |
| 400 | InvalidMarkdown | File content is invalid or too long |
| 404 | UnsupportedTheme | Theme not found |
| 500 | PDFGenerationFailed | PDF rendering error |

**Field Specifications:**

- **file**:
  - Required
  - Accepted extensions: .md, .markdown
  - Max size: 5MB (5,242,880 bytes)
  - Must be UTF-8 encoded text

- **All other fields**: Same as /convert/text endpoint

---

### 3. List Available Themes

**Endpoint:** `GET /themes`

**Description:** Get list of all available themes with preview information.

**Request Example:**
```bash
curl http://localhost:8000/themes
```

**Response (200 OK):**
```json
{
  "themes": [
    {
      "id": "default",
      "name": "Default",
      "description": "Clean, neutral theme suitable for general documents",
      "default_font": "Segoe UI, sans-serif",
      "colors": {
        "primary_text": "#1a1a1a",
        "background": "#ffffff",
        "accent": "#0066cc",
        "code_background": "#f5f5f5"
      }
    },
    {
      "id": "dark",
      "name": "Dark",
      "description": "Dark background with light text for reading in low-light",
      "default_font": "Segoe UI, sans-serif",
      "colors": {
        "primary_text": "#e0e0e0",
        "background": "#1e1e1e",
        "accent": "#66b3ff",
        "code_background": "#2d2d2d"
      }
    }
  ]
}
```

**Available Themes:**

1. **default** - Clean, neutral design (Segoe UI, sans-serif)
2. **dark** - Dark background with light text (Segoe UI, sans-serif)
3. **academic** - Formal serif font (Georgia, serif)
4. **minimal** - Minimalist design (Helvetica, Arial, sans-serif)
5. **github** - GitHub-inspired style (System fonts, sans-serif)

---

### 4. Get Theme Details

**Endpoint:** `GET /themes/{theme_id}`

**Description:** Get detailed information about a specific theme, including all CSS variables.

**Path Parameters:**
- `theme_id` (required): Theme identifier (e.g., "default", "dark", "academic")

**Request Example:**
```bash
curl http://localhost:8000/themes/academic
```

**Response (200 OK):**
```json
{
  "id": "academic",
  "name": "Academic",
  "description": "Formal serif font, suitable for academic papers and articles",
  "default_font": "Georgia, 'Times New Roman', serif",
  "colors": {
    "primary_text": "#333333",
    "background": "#ffffff",
    "accent": "#2c5aa0",
    "code_background": "#fafafa"
  },
  "css_variables": {
    "font-family": "Georgia, 'Times New Roman', serif",
    "font-size": "12pt",
    "font-color": "#333333",
    "background-color": "#ffffff",
    "heading-color": "#1a1a1a",
    "code-bg": "#fafafa",
    "link-color": "#2c5aa0",
    "border-color": "#d0d0d0",
    "accent-color": "#2c5aa0"
  }
}
```

**Error Responses:**

| Status | Error | Description |
|--------|-------|-------------|
| 404 | Not Found | Theme not found. Response includes list of available themes |

**Error Response Example:**
```json
{
  "detail": "Theme 'invalid' not found. Available themes: default, dark, academic, minimal, github"
}
```

---

### 5. Health Check

**Endpoint:** `GET /health`

**Description:** Check if the API is running and healthy.

**Request Example:**
```bash
curl http://localhost:8000/health
```

**Response (200 OK):**
```json
{
  "status": "healthy",
  "app": "Markdown to PDF Converter",
  "version": "1.0.0"
}
```

---

### 6. API Root Information

**Endpoint:** `GET /`

**Description:** Get general API information and available endpoints.

**Request Example:**
```bash
curl http://localhost:8000/
```

**Response (200 OK):**
```json
{
  "app": "Markdown to PDF Converter",
  "version": "1.0.0",
  "description": "Convert Markdown to PDF",
  "endpoints": {
    "health": "/health",
    "docs": "/docs",
    "redoc": "/redoc",
    "convert_text": "POST /convert/text",
    "convert_file": "POST /convert/file",
    "list_themes": "GET /themes",
    "theme_detail": "GET /themes/{theme_id}"
  }
}
```

---

## HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 400 | Bad Request | Invalid request data (e.g., invalid markdown, color format) |
| 404 | Not Found | Theme not found |
| 413 | Payload Too Large | File exceeds size limit |
| 415 | Unsupported Media Type | Invalid file type |
| 422 | Unprocessable Entity | Validation error in request parameters |
| 500 | Internal Server Error | Server error during PDF generation |

---

## Common Use Cases

### Basic Text Conversion
```bash
curl -X POST http://localhost:8000/convert/text \
  -H "Content-Type: application/json" \
  -d '{"markdown": "# Title\n\nContent"}' \
  --output output.pdf
```

### Professional Academic PDF
```bash
curl -X POST http://localhost:8000/convert/text \
  -H "Content-Type: application/json" \
  -d '{
    "markdown": "# Research Paper\n\nContent...",
    "theme": "academic",
    "font_size": 12,
    "margin": "2.5cm",
    "page_size": "A4"
  }' \
  --output paper.pdf
```

### Dark Mode PDF for Night Reading
```bash
curl -X POST http://localhost:8000/convert/text \
  -H "Content-Type: application/json" \
  -d '{
    "markdown": "# Document\n\nContent...",
    "theme": "dark"
  }' \
  --output dark.pdf
```

### File Conversion with Custom Styling
```bash
curl -X POST http://localhost:8000/convert/file \
  -F "file=@README.md" \
  -F "font_family=Courier New" \
  -F "font_color=#333333" \
  -F "background_color=#f9f9f9" \
  --output README.pdf
```

### Get All Available Options
```bash
# List themes
curl http://localhost:8000/themes | jq

# Get specific theme details
curl http://localhost:8000/themes/github | jq '.css_variables'
```

---

## Rate Limiting

Currently no rate limiting is implemented. For production, consider adding:
- Per-IP rate limits
- Per-user rate limits
- Request size limits

---

## CORS

CORS is configured via the `ALLOWED_ORIGINS` environment variable.

Default: `*` (allow all origins)

To restrict:
```bash
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

---

## Authentication

Currently no authentication is implemented. For production, consider adding:
- API key authentication
- JWT tokens
- OAuth2

---

## Webhook Support

Not currently implemented. For future enhancement, consider:
- Async PDF generation with webhooks
- Polling endpoints
- WebSocket support for real-time conversion status

---

## API Documentation UIs

- **Swagger UI (Interactive):** http://localhost:8000/docs
- **ReDoc (Alternative):** http://localhost:8000/redoc
- **OpenAPI JSON Schema:** http://localhost:8000/openapi.json

---

## Support

For API issues:
1. Check the interactive documentation at `/docs`
2. Review error response details
3. Check application logs
4. Verify request format matches specification

---

## Version History

### v1.0.0 (Current)
- Initial release
- Text and file conversion
- 5 built-in themes
- Customizable fonts, colors, page sizes
- Complete error handling
- Comprehensive test suite
