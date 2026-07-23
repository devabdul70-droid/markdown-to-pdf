# Markdown to PDF Converter

A production-ready FastAPI backend service that converts Markdown (raw text or uploaded `.md` file) into beautifully styled PDFs with customizable themes, fonts, colors, and page settings.

## Features

- ✅ **Markdown to PDF Conversion** - Convert raw markdown text or uploaded `.md` files to PDF
- 🎨 **Multiple Themes** - 5 built-in themes: default, dark, academic, minimal, github
- 🎯 **Customizable Styling** - Override fonts, colors, background, page size, and margins
- 📄 **Advanced Markdown Support** - Tables, code highlighting, TOC, fenced code blocks
- 🔒 **Production Ready** - Comprehensive error handling, validation, logging, CORS
- 📊 **RESTful API** - Well-documented OpenAPI/Swagger docs at `/docs`
- 🐳 **Docker Ready** - Included Dockerfile for easy deployment

## Tech Stack

- **FastAPI** - Modern Python web framework
- **Pydantic v2** - Data validation and settings management
- **python-markdown** - Markdown to HTML conversion
- **WeasyPrint** - HTML/CSS to PDF rendering
- **Jinja2** - Template engine for HTML composition
- **uvicorn** - ASGI server

## Installation

### Prerequisites

- Python 3.11+
- System dependencies for WeasyPrint:
  - On Ubuntu/Debian: `libpango-1.0-0 libcairo2 libgdk-pixbuf2.0-0`
  - On macOS: `brew install libffi libssl`
  - On Windows: Pre-compiled wheels available

### Setup

1. **Clone or download the project:**
   ```bash
   cd markdown-to-pdf
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment (optional):**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Run the server:**
   ```bash
   uvicorn app.main:app --reload
   ```
   
   Server will be available at `http://localhost:8000`

### Docker Setup

**Production build:**
```bash
docker build -t markdown-to-pdf:latest .
docker run -p 8000:8000 markdown-to-pdf:latest
```

**Development build with hot reload:**
```bash
docker build -f Dockerfile-dev -t markdown-to-pdf:dev .
docker run -p 8000:8000 -v $(pwd)/app:/app/app markdown-to-pdf:dev
```

## Configuration

Environment variables can be set in `.env` file or passed to the application:

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `DEBUG` | bool | False | Enable debug mode |
| `MAX_FILE_SIZE` | int | 5242880 | Max upload file size in bytes (5MB) |
| `MAX_MARKDOWN_LENGTH` | int | 500000 | Max markdown text length in characters |
| `ALLOWED_ORIGINS` | str | "*" | CORS allowed origins (comma-separated) |
| `DEFAULT_PAGE_SIZE` | str | "A4" | Default PDF page size (A4, Letter, Legal) |
| `DEFAULT_MARGIN` | str | "2cm" | Default page margin (CSS format) |
| `DEFAULT_FONT_SIZE` | int | 12 | Default font size in points |
| `TEMP_DIR` | str | "/tmp" | Temporary directory for file processing |

## API Endpoints

### 1. Convert Markdown Text to PDF

**Endpoint:** `POST /convert/text`

**Request Body (JSON):**
```json
{
  "markdown": "# Hello World\n\nThis is a **markdown** document.",
  "theme": "default",
  "font_family": "Georgia",
  "font_size": 12,
  "font_color": "#1a1a1a",
  "background_color": "#ffffff",
  "page_size": "A4",
  "margin": "2cm",
  "title": "My Document"
}
```

**Response:** PDF file (application/pdf)

**Example with curl:**
```bash
curl -X POST http://localhost:8000/convert/text \
  -H "Content-Type: application/json" \
  -d '{
    "markdown": "# Hello\n\nThis is **bold** text.",
    "theme": "default",
    "title": "test_document"
  }' \
  --output output.pdf
```

### 2. Convert Markdown File to PDF

**Endpoint:** `POST /convert/file`

**Form Data:**
- `file` (required): `.md` or `.markdown` file
- `theme` (optional): Theme name (default: "default")
- `font_family` (optional): Font family name
- `font_size` (optional): Font size in pt
- `font_color` (optional): Hex color (e.g., "#1a1a1a")
- `background_color` (optional): Hex color
- `page_size` (optional): "A4", "Letter", or "Legal"
- `margin` (optional): CSS margin (e.g., "2cm")
- `title` (optional): PDF title

**Response:** PDF file (application/pdf)

**Example with curl:**
```bash
curl -X POST http://localhost:8000/convert/file \
  -F "file=@document.md" \
  -F "theme=academic" \
  -F "font_size=14" \
  --output output.pdf
```

### 3. List Available Themes

**Endpoint:** `GET /themes`

**Response:**
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
    }
  ]
}
```

**Example with curl:**
```bash
curl http://localhost:8000/themes | jq
```

### 4. Get Theme Details

**Endpoint:** `GET /themes/{theme_id}`

**Response:** Detailed theme metadata including CSS variables

**Example with curl:**
```bash
curl http://localhost:8000/themes/dark | jq
```

### 5. Health Check

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "app": "Markdown to PDF Converter",
  "version": "1.0.0"
}
```

## Available Themes

1. **default** - Clean, neutral design with blue accents
2. **dark** - Dark background with light text and blue accents
3. **academic** - Formal serif font, suitable for academic papers
4. **minimal** - Minimalist design with lots of whitespace
5. **github** - Inspired by GitHub's markdown rendering

## Field Specifications

### Markdown Content

- **Max length:** 500,000 characters (configurable)
- **Supported markdown:** Standard markdown + tables, fenced code blocks, syntax highlighting
- **Code highlighting:** Automatic syntax highlighting for code blocks

### Custom Styling

- **font_family:** Any CSS-compatible font name (e.g., "Roboto", "Georgia", "Courier New")
- **font_size:** Integer, 6-72 pt
- **font_color:** Hex color code (e.g., "#1a1a1a", "#fff")
- **background_color:** Hex color code
- **page_size:** "A4" (210×297mm), "Letter" (8.5×11in), "Legal" (8.5×14in)
- **margin:** CSS-compatible margin (e.g., "2cm", "1in", "20mm")

## Error Handling

The API returns structured error responses:

```json
{
  "error": "InvalidMarkdown",
  "detail": "Markdown exceeds maximum length of 500000 characters",
  "status_code": 400
}
```

### Common Errors

| Error | Status | Description |
|-------|--------|-------------|
| InvalidMarkdown | 400 | Markdown is empty or exceeds max length |
| UnsupportedTheme | 404 | Theme ID not found |
| FileTooLarge | 413 | Uploaded file exceeds 5MB |
| UnsupportedFileType | 415 | File is not .md or .markdown |
| PDFGenerationFailed | 500 | PDF rendering error |

## Documentation

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **OpenAPI JSON:** http://localhost:8000/openapi.json

## Performance & Limits

- **Request timeout:** 300 seconds
- **Max file size:** 5MB (configurable)
- **Max markdown length:** 500,000 characters (configurable)
- **Concurrent requests:** Limited by uvicorn workers

## Testing

Run tests with pytest:

```bash
pip install pytest pytest-asyncio httpx
pytest tests/ -v
```

## Logging

Application logs are output to stdout in the following format:

```
2024-01-15 10:30:45 - markdown_to_pdf - INFO - [main.py:42] - Starting Markdown to PDF Converter v1.0.0
```

For production, pipe logs to a logging service or file:

```bash
uvicorn app.main:app >> logs/app.log 2>&1
```

## Troubleshooting

### "No module named 'weasyprint'" on Mac/Linux

Install system dependencies:

```bash
# macOS
brew install libffi libssl
pip install --upgrade weasyprint

# Ubuntu/Debian
sudo apt-get install libpango-1.0-0 libcairo2 libgdk-pixbuf2.0-0
pip install --upgrade weasyprint
```

### "ImportError: cannot import name '_imaging_cffi'" on Windows

Download WeasyPrint pre-compiled wheels:

```bash
pip install --only-binary :all: weasyprint
```

### Generated PDFs missing styling

1. Verify the theme exists: `GET /themes`
2. Check theme CSS files exist in `app/themes/`
3. Try with `theme=default` to isolate issues
4. Check application logs for rendering errors

## Project Structure

```
markdown-to-pdf/
├── app/
│   ├── main.py                 # FastAPI app entry point
│   ├── core/
│   │   ├── config.py           # Configuration management
│   │   └── logging.py          # Logging setup
│   ├── api/
│   │   ├── routes/
│   │   │   ├── convert.py      # Conversion endpoints
│   │   │   └── themes.py       # Theme endpoints
│   │   └── deps.py             # Shared dependencies
│   ├── services/
│   │   ├── markdown_service.py # Markdown → HTML
│   │   ├── pdf_service.py      # HTML+CSS → PDF
│   │   └── theme_service.py    # Theme management
│   ├── models/
│   │   └── schemas.py          # Pydantic models
│   ├── utils/
│   │   ├── validators.py       # Input validation
│   │   └── exceptions.py       # Custom exceptions
│   ├── themes/
│   │   ├── default.css
│   │   ├── dark.css
│   │   ├── academic.css
│   │   ├── minimal.css
│   │   └── github.css
│   └── templates/
│       └── pdf_template.html   # Jinja2 template
├── tests/
│   ├── test_convert.py
│   └── test_themes.py
├── requirements.txt
├── Dockerfile
├── Dockerfile-dev
├── .env.example
└── README.md
```

## License

MIT License - feel free to use in your projects

## Support

For issues, questions, or suggestions, please check the documentation at `/docs` or review the structured logging output.
