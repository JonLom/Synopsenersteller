"""Tests for PDF generation functionality."""

import pytest
from src.pdf_generator import markdown_to_pdf


class TestMarkdownToPDF:
    """Test markdown to PDF conversion."""

    def test_generate_pdf_from_simple_markdown(self):
        """Test basic PDF generation from markdown."""
        markdown = """# Test Synopse

## Gesetzesänderung

| Abschnitt | Alte Fassung | Neue Fassung | Änderungstyp |
|-----------|--------------|--------------|--------------|
| § 1       | Alt          | Neu          | Ersetzen     |
"""
        pdf_bytes = markdown_to_pdf(markdown)

        # Basic checks
        assert isinstance(pdf_bytes, bytes)
        assert len(pdf_bytes) > 0
        assert pdf_bytes[:4] == b'%PDF'  # PDF file signature

    def test_generate_pdf_with_german_characters(self):
        """Test PDF generation with German special characters."""
        markdown = """# Synopse

| Abschnitt | Alte Fassung | Neue Fassung | Änderungstyp |
|-----------|--------------|--------------|--------------|
| § 1 Abs. 2| Änderung     | Löschung     | Ersetzen     |
| § 3       | für größere  | für größere Änderungen | Ergänzen |
"""
        pdf_bytes = markdown_to_pdf(markdown)

        assert isinstance(pdf_bytes, bytes)
        assert len(pdf_bytes) > 0
        assert pdf_bytes[:4] == b'%PDF'

    def test_generate_pdf_with_complex_table(self):
        """Test PDF generation with more complex table content."""
        markdown = """# Synopse

## Änderungsvorschlag zum Bundesgesetz

| Abschnitt | Alte Fassung | Neue Fassung | Änderungstyp |
|-----------|--------------|--------------|--------------|
| § 1 Abs. 1 | Der Betrag beträgt 100 Euro. | Der Betrag beträgt **200 Euro**. | Ersetzen |
| § 2 | ~~Dieser Paragraph wird gelöscht.~~ | | Löschen |
| § 3 | | Dieser Paragraph ist neu. | Einfügen |

## Weiterführende Informationen

- Relevant: Seiten 5-10
- Quelle: https://www.gesetze-im-internet.de
"""
        pdf_bytes = markdown_to_pdf(markdown)

        assert isinstance(pdf_bytes, bytes)
        assert len(pdf_bytes) > 0
        assert pdf_bytes[:4] == b'%PDF'

    def test_generate_pdf_with_long_content(self):
        """Test PDF generation with longer content."""
        # Create a table with multiple rows
        table_rows = "\n".join([
            f"| § {i} | Alte Fassung {i} | Neue Fassung {i} | Ersetzen |"
            for i in range(1, 11)
        ])

        markdown = f"""# Synopse

| Abschnitt | Alte Fassung | Neue Fassung | Änderungstyp |
|-----------|--------------|--------------|--------------|
{table_rows}

## Weiterführende Informationen

Test information.
"""
        pdf_bytes = markdown_to_pdf(markdown)

        assert isinstance(pdf_bytes, bytes)
        assert len(pdf_bytes) > 0
        assert pdf_bytes[:4] == b'%PDF'

    def test_generate_pdf_empty_markdown(self):
        """Test PDF generation with empty markdown."""
        markdown = ""
        pdf_bytes = markdown_to_pdf(markdown)

        # Should still generate a valid (empty) PDF
        assert isinstance(pdf_bytes, bytes)
        assert pdf_bytes[:4] == b'%PDF'

    def test_generate_pdf_with_special_formatting(self):
        """Test PDF with markdown formatting (bold, strikethrough)."""
        markdown = """# Test

| Column 1 | Column 2 |
|----------|----------|
| **Bold** | Normal   |
| ~~Strike~~ | Normal |
"""
        pdf_bytes = markdown_to_pdf(markdown)

        assert isinstance(pdf_bytes, bytes)
        assert len(pdf_bytes) > 0
        assert pdf_bytes[:4] == b'%PDF'
