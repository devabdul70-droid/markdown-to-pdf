"""
Simple Markdown to PDF Converter API using FastAPI and fpdf2.
"""
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from fpdf import FPDF
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


def create_pdf_from_markdown(markdown_text: str, title: str = "Document") -> bytes:
    """
    Convert markdown text to PDF using fpdf2.
    
    Args:
        markdown_text: Markdown content
        title: PDF document title
    
    Returns:
        PDF as bytes
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=11)
    
    # Set document title
    pdf.set_title(title)
    
    # Add content with margins
    pdf.set_margins(10, 10, 10)
    
    # Split content into lines and render
    for line in markdown_text.split('\n'):
        line = line.strip()
        
        # Skip empty lines
        if not line:
            pdf.ln(5)
            continue
        
        # Handle headings
        if line.startswith('# '):
            pdf.set_font("Helvetica", style="B", size=18)
            pdf.cell(0, 10, line[2:].strip(), ln=True)
            pdf.set_font("Helvetica", size=11)
            pdf.ln(3)
        elif line.startswith('## '):
            pdf.set_font("Helvetica", style="B", size=14)
            pdf.cell(0, 10, line[3:].strip(), ln=True)
            pdf.set_font("Helvetica", size=11)
            pdf.ln(2)
        elif line.startswith('### '):
            pdf.set_font("Helvetica", style="B", size=12)
            pdf.cell(0, 10, line[4:].strip(), ln=True)
            pdf.set_font("Helvetica", size=11)
            pdf.ln(1)
        # Handle bold and italic (simple replacement)
        elif '**' in line or '__' in line:
            # Simple approach: just remove markdown syntax and render
            text = line.replace('**', '').replace('__', '').replace('`', '')
            pdf.multi_cell(0, 7, text)
        else:
            # Regular paragraph
            pdf.multi_cell(0, 7, line)
    
    # Return PDF as bytes
    pdf_bytes = BytesIO()
    pdf.output(pdf_bytes)
    pdf_bytes.seek(0)
    return pdf_bytes.getvalue()


@app.post("/convert/text")
async def convert_text(request: MarkdownRequest):
    """Convert markdown text to PDF."""
    try:
        if not request.markdown.strip():
            return {"error": "Markdown text is empty"}, 400
        
        # Generate PDF
        pdf_bytes = create_pdf_from_markdown(
            request.markdown,
            title="Document"
        )
        
        # Return PDF as stream download
        return StreamingResponse(
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
        # Validate file extension
        if not file.filename.endswith(('.md', '.markdown')):
            return {"error": "Only .md and .markdown files are supported"}, 415
        
        # Read file content
        content = await file.read()
        markdown_text = content.decode('utf-8')
        
        if not markdown_text.strip():
            return {"error": "File is empty"}, 400
        
        # Extract filename without extension for PDF title
        filename = file.filename.rsplit('.', 1)[0]
        
        # Generate PDF
        pdf_bytes = create_pdf_from_markdown(
            markdown_text,
            title=filename
        )
        
        # Return PDF as stream download
        return StreamingResponse(
            BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}.pdf"}
        )
    except UnicodeDecodeError:
        return {"error": "File is not a valid UTF-8 text file"}, 400
    except Exception as e:
        return {"error": str(e)}, 500


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
