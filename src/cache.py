"""Cache module for storing LLM responses using diskcache."""

import hashlib
from diskcache import Cache


# Initialize cache in ./cache directory
cache = Cache('./cache')


def compute_document_hash(pdf_bytes: bytes) -> str:
    """
    Compute SHA-256 hash of PDF document.

    Args:
        pdf_bytes: PDF file content as bytes

    Returns:
        Hexadecimal hash string
    """
    return hashlib.sha256(pdf_bytes).hexdigest()


def get_cached_response(document_hash: str) -> str:
    """
    Retrieve cached response for a document hash.

    Args:
        document_hash: SHA-256 hash of the document

    Returns:
        Cached response text or None if not found
    """
    return cache.get(document_hash)


def save_response_to_cache(document_hash: str, response: str):
    """
    Save LLM response to cache.

    Args:
        document_hash: SHA-256 hash of the document
        response: LLM response text
    """
    cache[document_hash] = response


def is_cached(document_hash: str) -> bool:
    """
    Check if document hash exists in cache.

    Args:
        document_hash: SHA-256 hash of the document

    Returns:
        True if cached, False otherwise
    """
    return document_hash in cache
