"""Tests for caching functionality."""

import os
import tempfile
import pytest
from src.cache import compute_document_hash, get_cached_response, save_response_to_cache, cache


class TestDocumentHashing:
    """Test document hash computation."""

    def test_compute_hash_deterministic(self):
        """Test that same input produces same hash."""
        data = b"Test document content"
        hash1 = compute_document_hash(data)
        hash2 = compute_document_hash(data)

        assert hash1 == hash2

    def test_compute_hash_different_for_different_input(self):
        """Test that different inputs produce different hashes."""
        data1 = b"Document 1"
        data2 = b"Document 2"

        hash1 = compute_document_hash(data1)
        hash2 = compute_document_hash(data2)

        assert hash1 != hash2

    def test_compute_hash_format(self):
        """Test that hash is in correct format (SHA-256 hex)."""
        data = b"Test"
        hash_result = compute_document_hash(data)

        # SHA-256 produces 64 character hex string
        assert isinstance(hash_result, str)
        assert len(hash_result) == 64
        assert all(c in '0123456789abcdef' for c in hash_result)


class TestCacheOperations:
    """Test cache save and retrieve operations."""

    @pytest.fixture(autouse=True)
    def clear_cache(self):
        """Clear cache before each test."""
        cache.clear()
        yield
        cache.clear()

    def test_save_and_retrieve_response(self):
        """Test saving and retrieving cached response."""
        doc_hash = "test_hash_123"
        response = "Test response content"

        # Save to cache
        save_response_to_cache(doc_hash, response)

        # Retrieve from cache
        cached = get_cached_response(doc_hash)

        assert cached == response

    def test_get_nonexistent_response(self):
        """Test retrieving non-existent cache entry returns None."""
        cached = get_cached_response("nonexistent_hash")
        assert cached is None

    def test_cache_overwrite(self):
        """Test that saving with same hash overwrites previous value."""
        doc_hash = "test_hash_456"
        response1 = "First response"
        response2 = "Second response"

        # Save first response
        save_response_to_cache(doc_hash, response1)

        # Save second response with same hash
        save_response_to_cache(doc_hash, response2)

        # Should retrieve second response
        cached = get_cached_response(doc_hash)
        assert cached == response2

    def test_cache_with_real_pdf_hash(self):
        """Test cache with realistic PDF hash."""
        pdf_bytes = b"PDF content here"
        doc_hash = compute_document_hash(pdf_bytes)
        response = "Synopse markdown content"

        # Save and retrieve
        save_response_to_cache(doc_hash, response)
        cached = get_cached_response(doc_hash)

        assert cached == response

    def test_cache_with_unicode_content(self):
        """Test cache with German characters (unicode)."""
        doc_hash = "unicode_test"
        response = "§ 1 Änderung des Gesetzes\n\nÄnderungsvorschlag mit ä, ö, ü, ß"

        save_response_to_cache(doc_hash, response)
        cached = get_cached_response(doc_hash)

        assert cached == response
