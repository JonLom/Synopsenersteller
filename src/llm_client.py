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


def process_amendment_with_llm(pdf_text: str, pdf_bytes: bytes, status_callback=None) -> tuple[str, bool]:
    """
    Process legislative amendment proposal using Claude LLM with caching.

    Args:
        pdf_text: Extracted text from the amendment PDF
        pdf_bytes: Original PDF bytes for cache hashing
        status_callback: Optional callback function for streaming status updates

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

        if config.ENABLE_STREAMING:
            # Streaming mode: show real-time progress
            response_text = _process_with_streaming(
                client, system_prompt, pdf_text, status_callback
            )
        else:
            # Non-streaming mode: simple placeholder
            if status_callback:
                status_callback("Analysiere ...")

            message = client.messages.create(
                model=config.MODEL_NAME,
                max_tokens=config.MAX_TOKENS,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": f"Hier ist der Änderungsvorschlag:\n\n{pdf_text}"
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


def _process_with_streaming(client, system_prompt: str, pdf_text: str, status_callback) -> str:
    """
    Process amendment with streaming to show real-time progress.

    Args:
        client: Anthropic client instance
        system_prompt: System prompt text
        pdf_text: PDF content text
        status_callback: Callback function for status updates

    Returns:
        Complete response text
    """
    full_response = ""
    thinking_text = ""

    stream_params = {
        "model": config.MODEL_NAME,
        "max_tokens": config.MAX_TOKENS,
        "system": system_prompt,
        "messages": [
            {
                "role": "user",
                "content": f"Hier der Änderungsvorschlag:\n\n{pdf_text}"
            }
        ]
    }

    # Add thinking parameters if enabled (summary is included automatically)
    if config.ENABLE_THINKING:
        stream_params["thinking"] = {
            "type": "enabled",
            "budget_tokens": config.THINKING_BUDGET
        }

    with client.messages.stream(**stream_params) as stream:
        for event in stream:
            if status_callback:
                # Handle different event types
                if event.type == "content_block_start":
                    status_callback("Analysiere:...")

                elif event.type == "content_block_delta":
                    if hasattr(event.delta, 'type'):
                        if event.delta.type == "thinking_delta":
                            # Show thinking process if enabled
                            if config.ENABLE_THINKING:
                                if hasattr(event.delta, 'thinking'):
                                    thinking_text += event.delta.thinking
                                    status_callback(f"Analysiere: ...{thinking_text}")
                        elif event.delta.type == "text_delta":
                            # Show response being generated
                            if hasattr(event.delta, 'text'):
                                full_response += event.delta.text
                                status_callback(f"Erstelle Synopse: ...{full_response}")

        # Get final message
        final_message = stream.get_final_message()

        # Extract text content from final message
        for block in final_message.content:
            if block.type == "text":
                full_response = block.text
                break

    return full_response
