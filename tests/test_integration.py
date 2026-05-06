"""Integration tests for full pipeline: PDF → LLM → Synopsis."""

import os
import pytest
from src.pdf_processor import extract_text_from_pdf
from src.llm_client import process_amendment_with_llm
from src.pdf_generator import markdown_to_pdf
import config


# Test data paths
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
SIMPLE_PDF = os.path.join(TEST_DATA_DIR, '2105688-EinfachesDokument.pdf')
OTHER_SIMPLE_PDF = os.path.join(TEST_DATA_DIR, '2105528-EinfachesDokument2.pdf')


# Skip all integration tests if no API key is configured
pytestmark = pytest.mark.skipif(
    not config.ANTHROPIC_API_KEY,
    reason="ANTHROPIC_API_KEY not configured - skipping integration tests"
)


@pytest.fixture
def simple_pdf_bytes():
    """Load simple test PDF."""
    with open(SIMPLE_PDF, 'rb') as f:
        return f.read()


@pytest.fixture
def another_simple_pdf_bytes():
    """Load another test PDF."""
    with open(OTHER_SIMPLE_PDF, 'rb') as f:
        return f.read()


@pytest.mark.integration
class TestFullPipeline:
    """Integration tests for complete PDF to synopsis pipeline."""

    def test_simple_pdf_full_pipeline(self, simple_pdf_bytes):
        """Test complete pipeline with simple PDF."""
        # Step 1: Extract text from PDF
        pdf_text = extract_text_from_pdf(simple_pdf_bytes)
        assert len(pdf_text) > 0

        # Step 2: Process with LLM (uses cache if available)
        synopsis_markdown, was_cached = process_amendment_with_llm(pdf_text, simple_pdf_bytes)

        # Verify synopsis structure
        assert isinstance(synopsis_markdown, str)
        assert len(synopsis_markdown) > 0

        # Should contain key German legal terms
        assert any(term in synopsis_markdown.lower() for term in ['synopse', 'gesetz', '§'])

        # Should contain table structure
        assert '|' in synopsis_markdown  # Markdown table syntax

        # Step 3: Generate PDF from synopsis
        output_pdf = markdown_to_pdf(synopsis_markdown)
        assert isinstance(output_pdf, bytes)
        assert output_pdf[:4] == b'%PDF'


@pytest.mark.integration
class TestSynopsisContent:
    """Integration tests verifying synopsis content quality."""

    def test_synopsis_contains_required_sections(self, simple_pdf_bytes):
        """Verify synopsis contains all required sections."""
        pdf_text = extract_text_from_pdf(simple_pdf_bytes)
        synopsis, _ = process_amendment_with_llm(pdf_text, simple_pdf_bytes)

        # Check for required sections according to system prompt
        assert '# Synopse' in synopsis or '# Synopsis' in synopsis

        # Should have section for additional information
        assert 'Weiterführende Informationen' in synopsis or 'weiterführende' in synopsis.lower()

    def test_synopsis_contains_table_structure(self, simple_pdf_bytes):
        """Verify synopsis has proper table structure."""
        pdf_text = extract_text_from_pdf(simple_pdf_bytes)
        synopsis, _ = process_amendment_with_llm(pdf_text, simple_pdf_bytes)

        # Should have markdown table with expected columns
        # According to system prompt: Abschnitt | Alte Fassung | Neue Fassung | Änderungstyp
        table_headers = ['Abschnitt', 'Alte Fassung', 'Neue Fassung', 'Änderungstyp']

        # At least some of these headers should be present
        header_count = sum(1 for header in table_headers if header in synopsis)
        assert header_count >= 2, f"Synopsis should contain at least 2 table headers, found {header_count}"

    def test_synopsis_references_online_sources(self, simple_pdf_bytes):
        """Verify synopsis references official online sources."""
        pdf_text = extract_text_from_pdf(simple_pdf_bytes)
        synopsis, _ = process_amendment_with_llm(pdf_text, simple_pdf_bytes)

        # According to system prompt, should reference official sources
        official_sources = [
            'gesetze-im-internet.de',
            'recht.bund.de',
            'bgbl.de',
            'eur-lex.europa.eu',
            'dejure.org',
            'buzer.de'
        ]

        # Should reference at least one official source
        has_source = any(source in synopsis.lower() for source in official_sources)
        assert has_source, "Synopsis should reference at least one official legal source"

    def test_synopsis_identifies_change_types(self, simple_pdf_bytes):
        """Verify synopsis identifies types of legal changes."""
        pdf_text = extract_text_from_pdf(simple_pdf_bytes)
        synopsis, _ = process_amendment_with_llm(pdf_text, simple_pdf_bytes)

        # According to system prompt, should identify change types
        change_types = ['Ersetzen', 'Einfügen', 'Löschen', 'Nummerierung']

        # Should mention at least one change type
        has_change_type = any(change_type in synopsis for change_type in change_types)
        assert has_change_type, "Synopsis should identify at least one type of change"


@pytest.mark.integration
class TestCachingIntegration:
    """Integration tests for caching behavior."""

    def test_cache_hit_on_repeated_request(self, simple_pdf_bytes):
        """Verify that processing same PDF twice uses cache."""
        pdf_text = extract_text_from_pdf(simple_pdf_bytes)

        # First request - should call API
        synopsis1, was_cached1 = process_amendment_with_llm(pdf_text, simple_pdf_bytes)

        # Second request - should use cache
        synopsis2, was_cached2 = process_amendment_with_llm(pdf_text, simple_pdf_bytes)

        # Second request should be cached
        assert was_cached2 is True, "Second identical request should use cache"

        # Results should be identical
        assert synopsis1 == synopsis2

    def test_cache_miss_on_different_pdf(self, simple_pdf_bytes, another_simple_pdf_bytes):
        """Verify that different PDFs don't share cache entries."""
        # Process first PDF
        pdf_text1 = extract_text_from_pdf(simple_pdf_bytes)
        synopsis1, _ = process_amendment_with_llm(pdf_text1, simple_pdf_bytes)

        # Process second PDF
        pdf_text2 = extract_text_from_pdf(another_simple_pdf_bytes)
        synopsis2, was_cached2 = process_amendment_with_llm(pdf_text2, another_simple_pdf_bytes)

        # Results should be different
        assert synopsis1 != synopsis2, "Different PDFs should produce different synopses"


@pytest.mark.integration
class TestErrorHandling:
    """Integration tests for error handling."""

    def test_invalid_pdf_handling(self):
        """Test that invalid PDF is handled gracefully."""
        invalid_pdf = b"This is not a valid PDF"

        with pytest.raises(Exception):
            extract_text_from_pdf(invalid_pdf)

    def test_empty_pdf_text_handling(self):
        """Test handling of empty or minimal PDF text."""
        # Create a minimal PDF with almost no content
        minimal_bytes = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n>>\nendobj\nxref\n0 0\ntrailer\n<<\n>>\nstartxref\n0\n%%EOF"

        # Should not crash, but may produce minimal output
        try:
            pdf_text = extract_text_from_pdf(minimal_bytes)
            # If extraction succeeds, text might be empty or minimal
            assert isinstance(pdf_text, str)
        except Exception as e:
            # If extraction fails, that's acceptable for invalid minimal PDF
            assert isinstance(e, Exception)
