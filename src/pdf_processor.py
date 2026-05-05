"""PDF processing module for extracting text from uploaded PDFs."""

import fitz
from typing import Optional


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """
    Extract text content from a PDF file.

    Args:
        pdf_bytes: PDF file as bytes

    Returns:
        Extracted text as string

    Raises:
        Exception: If PDF processing fails
    """
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        text_content = []

        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            text_content.append(f"--- Page {page_num + 1} ---\n{text}")

        doc.close()

        return "\n\n".join(text_content)

    except Exception as e:
        raise Exception(f"Failed to extract text from PDF: {str(e)}")


def validate_pdf(pdf_bytes: bytes) -> bool:
    """
    Validate that the uploaded file is a valid PDF.

    Args:
        pdf_bytes: File bytes to validate

    Returns:
        True if valid PDF, False otherwise
    """
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        is_valid = len(doc) > 0
        doc.close()
        return is_valid
    except:
        return False
