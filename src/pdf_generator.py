"""PDF generation module for converting markdown output to PDF."""

from io import BytesIO
from markdown_pdf import MarkdownPdf, Section
import tempfile
import os


def markdown_to_pdf(markdown_text: str) -> bytes:
    """
    Convert markdown text to PDF format using markdown-pdf library.

    Args:
        markdown_text: Markdown formatted text (typically synopsis table)

    Returns:
        PDF file as bytes

    Raises:
        Exception: If PDF generation fails
    """
    try:
        # Add title to markdown
        full_markdown = f"# Synopse\n\n{markdown_text}"

        # Create temporary file for PDF output
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.pdf', delete=False) as tmp_file:
            tmp_path = tmp_file.name

        try:
            # Create PDF with custom CSS for better table formatting
            pdf = MarkdownPdf(toc_level=0)

            # Add custom CSS for table styling
            css = """
            body {
                font-family: Arial, sans-serif;
                font-size: 10pt;
                line-height: 1.4;
            }
            h1 {
                color: #2c3e50;
                border-bottom: 2px solid #3498db;
                padding-bottom: 10px;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
                font-size: 9pt;
            }
            th, td {
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
                vertical-align: top;
            }
            th {
                background-color: #f2f2f2;
                font-weight: bold;
            }
            tr:nth-child(even) {
                background-color: #f9f9f9;
            }
            """

            # Add section with markdown content
            section = Section(full_markdown)
            section.css = css
            pdf.add_section(section)
            pdf.save(tmp_path)

            # Read the generated PDF
            with open(tmp_path, 'rb') as f:
                pdf_bytes = f.read()

            return pdf_bytes

        finally:
            # Clean up temporary file
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    except Exception as e:
        raise Exception(f"Failed to generate PDF from markdown: {str(e)}")


def save_pdf(pdf_bytes: bytes, output_path: str) -> None:
    """
    Save PDF bytes to a file.

    Args:
        pdf_bytes: PDF content as bytes
        output_path: Path where PDF should be saved

    Raises:
        Exception: If saving fails
    """
    try:
        with open(output_path, 'wb') as f:
            f.write(pdf_bytes)
    except Exception as e:
        raise Exception(f"Failed to save PDF: {str(e)}")
