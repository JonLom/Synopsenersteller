"""Tests for PDF processing functionality."""

import os
import pytest
from src.pdf_processor import extract_text_from_pdf, validate_pdf


# Test data paths
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
SIMPLE_PDF = os.path.join(TEST_DATA_DIR, '2105688-EinfachesDokument.pdf')
COMPLEX_PDF = os.path.join(TEST_DATA_DIR, '2101934-KompliziertesDokument.pdf')


@pytest.fixture
def simple_pdf_bytes():
    """Load simple test PDF."""
    with open(SIMPLE_PDF, 'rb') as f:
        return f.read()


@pytest.fixture
def complex_pdf_bytes():
    """Load complex test PDF."""
    with open(COMPLEX_PDF, 'rb') as f:
        return f.read()


class TestPDFValidation:
    """Test PDF validation functionality."""

    def test_validate_valid_pdf(self, simple_pdf_bytes):
        """Test that valid PDF is recognized."""
        assert validate_pdf(simple_pdf_bytes) is True

    def test_validate_invalid_pdf(self):
        """Test that invalid data is rejected."""
        invalid_data = b"This is not a PDF file"
        assert validate_pdf(invalid_data) is False

    def test_validate_empty_pdf(self):
        """Test that empty data is rejected."""
        assert validate_pdf(b"") is False


class TestPDFTextExtraction:
    """Test PDF text extraction functionality."""

    def test_extract_text_from_simple_pdf(self, simple_pdf_bytes):
        """Test text extraction from simple PDF."""
        text = extract_text_from_pdf(simple_pdf_bytes)

        # Basic checks
        assert isinstance(text, str)
        assert len(text) > 0
        assert "Page 1" in text  # Should contain page markers

    def test_extract_text_from_complex_pdf(self, complex_pdf_bytes):
        """Test text extraction from complex PDF."""
        text = extract_text_from_pdf(complex_pdf_bytes)

        # Basic checks
        assert isinstance(text, str)
        assert len(text) > 0
        assert "Page 1" in text

    def test_extract_text_contains_page_numbers(self, simple_pdf_bytes):
        """Test that extracted text includes page number markers."""
        text = extract_text_from_pdf(simple_pdf_bytes)

        # Should contain page markers
        assert "--- Page" in text

    def test_extract_text_from_invalid_pdf(self):
        """Test that invalid PDF raises appropriate error."""
        invalid_data = b"Not a PDF"

        with pytest.raises(Exception):
            extract_text_from_pdf(invalid_data)
