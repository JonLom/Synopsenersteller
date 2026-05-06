"""Unit tests for LLM client focusing on error paths and edge cases."""

import os
import pytest
from unittest.mock import Mock, patch
from src.llm_client import load_system_prompt, process_amendment_with_llm
import anthropic


class TestLoadSystemPrompt:
    """Test system prompt loading error paths."""

    def test_load_system_prompt_success(self):
        """Test successful prompt loading (smoke test)."""
        prompt = load_system_prompt()
        assert isinstance(prompt, str)
        assert len(prompt) > 100

    def test_load_system_prompt_file_not_found(self, monkeypatch, tmp_path):
        """Test FileNotFoundError path."""
        # Point to non-existent directory
        fake_path = str(tmp_path / "nonexistent" / "prompts" / "system_prompt_de.md")
        monkeypatch.setattr('os.path.join', lambda *args: fake_path)

        with pytest.raises(Exception) as exc_info:
            load_system_prompt()

        assert "not found" in str(exc_info.value).lower()

    def test_load_system_prompt_read_error(self, monkeypatch):
        """Test general Exception path when file can't be read."""
        def mock_open(*args, **kwargs):
            raise PermissionError("Access denied")

        monkeypatch.setattr('builtins.open', mock_open)

        with pytest.raises(Exception) as exc_info:
            load_system_prompt()

        assert "Failed to load" in str(exc_info.value)


class TestAPIKeyValidation:
    """Test API key validation."""

    def test_missing_api_key_error(self, monkeypatch):
        """Test error when API key not configured."""
        # Mock empty API key
        monkeypatch.setattr('config.ANTHROPIC_API_KEY', None)

        with pytest.raises(Exception) as exc_info:
            process_amendment_with_llm("test text", b"test bytes")

        assert "ANTHROPIC_API_KEY not configured" in str(exc_info.value)


class TestErrorHandling:
    """Test API error handling paths."""

    @patch('src.llm_client.anthropic.Anthropic')
    @patch('src.llm_client.get_cached_response')
    def test_anthropic_api_error(self, mock_cache, mock_anthropic_class, monkeypatch):
        """Test APIError handling."""
        # Setup
        monkeypatch.setattr('config.ANTHROPIC_API_KEY', 'test-key')
        monkeypatch.setattr('config.ENABLE_STREAMING', False)
        mock_cache.return_value = None  # Cache miss

        # Mock client to raise a generic exception (simpler than creating proper APIError)
        mock_client = Mock()
        mock_client.messages.create.side_effect = Exception("API Error: Rate limit exceeded")
        mock_anthropic_class.return_value = mock_client

        # Test
        with pytest.raises(Exception) as exc_info:
            process_amendment_with_llm("text", b"bytes")

        assert "Failed to process" in str(exc_info.value)

    @patch('src.llm_client.load_system_prompt')
    @patch('src.llm_client.get_cached_response')
    def test_general_exception_handling(self, mock_cache, mock_load_prompt, monkeypatch):
        """Test general Exception handling."""
        monkeypatch.setattr('config.ANTHROPIC_API_KEY', 'test-key')
        mock_cache.return_value = None
        mock_load_prompt.side_effect = RuntimeError("Unexpected error")

        with pytest.raises(Exception) as exc_info:
            process_amendment_with_llm("text", b"bytes")

        assert "Failed to process" in str(exc_info.value)


class TestStatusCallback:
    """Test status callback functionality."""

    @patch('src.llm_client.anthropic.Anthropic')
    @patch('src.llm_client.get_cached_response')
    @patch('src.llm_client.save_response_to_cache')
    def test_status_callback_called_non_streaming(
        self, mock_save, mock_cache, mock_anthropic_class, monkeypatch
    ):
        """Test that status callback is invoked in non-streaming mode."""
        # Setup
        monkeypatch.setattr('config.ANTHROPIC_API_KEY', 'test-key')
        monkeypatch.setattr('config.ENABLE_STREAMING', False)
        monkeypatch.setattr('config.MODEL_NAME', 'claude-3')
        monkeypatch.setattr('config.MAX_TOKENS', 1000)
        monkeypatch.setattr('config.TEMPERATURE', 0.0)

        mock_cache.return_value = None

        # Mock successful API response
        mock_client = Mock()
        mock_message = Mock()
        mock_message.content = [Mock(text="Test response")]
        mock_client.messages.create.return_value = mock_message
        mock_anthropic_class.return_value = mock_client

        # Test with callback
        callback = Mock()
        result, cached = process_amendment_with_llm(
            "test text",
            b"test bytes",
            status_callback=callback
        )

        # Verify callback was called
        callback.assert_called()
        assert "Analysiere" in callback.call_args[0][0]
        assert result == "Test response"
        assert cached is False
