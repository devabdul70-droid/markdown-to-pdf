"""
Simple Markdown to PDF Converter API using FastAPI.
"""
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from pydantic import BaseModel
import markdown2
import pdfkit
from io import BytesIO

app = FastAPI(
    title="Markdown to PDF Converter",
    version="1.0.0",
    description="Convert Markdown text or files to PDF easily.",
)


class MarkdownRequest(BaseModel):
    markdown: str


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Markdown to PDF Converter API", "version": "1.0.0"}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/convert/text")
async def convert_text(request: MarkdownRequest):
    """Convert markdown text to PDF."""
    try:
        # Convert markdown to HTML
        html = markdown2.markdown(request.markdown)
        
        # Wrap in basic HTML template
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    margin: 20px;
                    color: #333;
                }}
                h1, h2, h3 {{
                    color: #0066cc;
                }}
                code {{
                    background-color: #f4f4f4;
                    padding: 2px 5px;
                    border-radius: 3px;
                }}
                pre {{
                    background-color: #f4f4f4;
                    padding: 10px;
                    border-radius: 5px;
                    overflow-x: auto;
                }}
                a {{
                    color: #0066cc;
                    text-decoration: none;
                }}
                a:hover {{
                    text-decoration: underline;
                }}
            </style>
        </head>
        <body>
            {html}
        </body>
        </html>
        """
        
        # Convert HTML to PDF
        pdf_bytes = pdfkit.from_string(html_content, False, options={
            'page-size': 'A4',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
        })
        
        # Return PDF as file download
        return FileResponse(
            BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=document.pdf"}
        )
    except Exception as e:
        return {"error": str(e)}, 500


@app.post("/convert/file")
async def convert_file(file: UploadFile = File(...)):
    """Convert markdown file to PDF."""
    try:
        # Read file content
        content = await file.read()
        markdown_text = content.decode('utf-8')
        
        # Convert markdown to HTML
        html = markdown2.markdown(markdown_text)
        
        # Wrap in basic HTML template
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    margin: 20px;
                    color: #333;
                }}
                h1, h2, h3 {{
                    color: #0066cc;
                }}
                code {{
                    background-color: #f4f4f4;
                    padding: 2px 5px;
                    border-radius: 3px;
                }}
                pre {{
                    background-color: #f4f4f4;
                    padding: 10px;
                    border-radius: 5px;
                    overflow-x: auto;
                }}
                a {{
                    color: #0066cc;
                    text-decoration: none;
                }}
                a:hover {{
                    text-decoration: underline;
                }}
            </style>
        </head>
        <body>
            {html}
        </body>
        </html>
        """
        
        # Convert HTML to PDF
        pdf_bytes = pdfkit.from_string(html_content, False, options={
            'page-size': 'A4',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
        })
        
        # Get filename without extension
        filename = file.filename.rsplit('.', 1)[0] if file.filename else "document"
        
        # Return PDF as file download
        return FileResponse(
            BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}.pdf"}
        )
    except Exception as e:
        return {"error": str(e)}, 500


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
