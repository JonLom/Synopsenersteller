"""LLM client module for processing legislative amendments with Claude."""

import logging
import os

import anthropic

import config
from .cache import compute_document_hash, get_cached_response, save_response_to_cache

logger = logging.getLogger(__name__)


def load_system_prompt() -> str:
    """
    Load the system prompt from the prompts directory.

    Returns:
        System prompt text

    Raises:
        Exception: If prompt file cannot be loaded
    """
    prompt_path = os.path.join(os.path.dirname(__file__), 'prompts', 'system_prompt_de.md')
    try:
        with open(prompt_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        raise Exception(f"System prompt file not found at: {prompt_path}")
    except Exception as e:
        raise Exception(f"Failed to load system prompt: {str(e)}")


def process_amendment_with_llm(pdf_text: str, pdf_bytes: bytes) -> tuple[str, bool]:
    """
    Process legislative amendment proposal using Claude LLM with caching.

    Args:
        pdf_text: Extracted text from the amendment PDF
        pdf_bytes: Original PDF bytes for cache hashing

    Returns:
        Tuple of (markdown formatted synopsis table, was_cached boolean)

    Raises:
        Exception: If LLM processing fails
    """
    if not config.ANTHROPIC_API_KEY:
        raise Exception("ANTHROPIC_API_KEY not configured. Please set it in your .env file.")

    # Compute document hash
    document_hash = compute_document_hash(pdf_bytes)

    # Check cache first
    cached_response = get_cached_response(document_hash)
    if cached_response:
        logger.info(f"Cache HIT for document hash: {document_hash[:16]}...")
        return cached_response, True

    # Cache miss - call API
    logger.info(f"Cache MISS for document hash: {document_hash[:16]}... - calling API")
    try:
        system_prompt = load_system_prompt()
        client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)

        message = client.messages.create(
            model=config.MODEL_NAME,
            max_tokens=config.MAX_TOKENS,
            temperature=config.TEMPERATURE,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": f"Here is the legislative amendment proposal:\n\n{pdf_text}"
                }
            ]
        )

        response_text = message.content[0].text

        # Save to cache
        save_response_to_cache(document_hash, response_text)

        return response_text, False

    except anthropic.APIError as e:
        raise Exception(f"Anthropic API error: {str(e)}")
    except Exception as e:
        raise Exception(f"Failed to process amendment with LLM: {str(e)}")
