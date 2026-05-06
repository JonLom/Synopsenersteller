import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODEL_NAME = "claude-sonnet-4-5-20250929"
MAX_TOKENS = 16000
TEMPERATURE = 0.0

# Streaming configuration
ENABLE_STREAMING = "true"
ENABLE_THINKING =  "true"
THINKING_BUDGET = 10000
