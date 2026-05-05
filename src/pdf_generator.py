"""PDF generation module for converting markdown output to PDF."""

import os
import tempfile

from markdown_pdf import MarkdownPdf, Section


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

        # Create temporary file for PDF output
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.pdf', delete=False) as tmp_file:
            tmp_path = tmp_file.name

        try:
            # Create PDF with custom CSS for better table formatting
            pdf = MarkdownPdf(toc_level=0)

            # Add custom CSS for table styling with proper borders
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
            table, th, td {
                border: 1px solid #333;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
                font-size: 9pt;
            }
            th, td {
                padding: 10px;
                text-align: left;
                vertical-align: top;
            }
            th {
                background-color: #f2f2f2;
                font-weight: bold;
                border: 1px solid #666;
            }
            tr:nth-child(even) {
                background-color: #f9f9f9;
            }
            """

            # Add section with markdown content, pass CSS to add_section()
            pdf.add_section(Section(markdown_text), user_css=css)
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
