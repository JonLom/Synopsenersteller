# Synopsenersteller

Erstellt Synopsen aus PDF, KI und Online Gesetzestexten

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file with your API key:
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

## Configuration

The application supports several configuration options via environment variables in the `.env` file:

### Required
- `ANTHROPIC_API_KEY`: Your Anthropic API key

### Optional - Streaming Settings
- `ENABLE_STREAMING`: Set to `true` to show real-time progress updates during AI analysis (default: `false`)
- `ENABLE_THINKING`: Set to `true` to show the agent's thought process with Claude's extended thinking feature (requires `ENABLE_STREAMING=true`, default: `false`)
- `THINKING_BUDGET`: Maximum tokens for thinking process (default: `10000`)

**Example:**
```bash
# Enable streaming with extended thinking
ENABLE_STREAMING=true
ENABLE_THINKING=true
THINKING_BUDGET=10000
```

**What you'll see:**

When streaming is disabled:
- Simple "KI analysiert..." placeholder

When streaming is enabled:
- 🧠 Analysiere Gesetzesänderung...
- ✍️ Erstelle Synopse...
- Real-time response preview

When extended thinking is enabled (requires streaming):
- 🧠 Denkt nach: ...[abbreviated thinking process]
- 💭 Zusammenfassung: [Claude's thinking summary]
- Shows the AI's reasoning process in real-time

## Usage

Run the Streamlit app:
```bash
streamlit run app.py
```

## Testing

### Unit Tests (fast, no API required)

Run unit tests only:
```bash
pytest tests/test_pdf_processor.py tests/test_cache.py tests/test_pdf_generator.py -v
```

### Integration Tests (requires API key, may incur costs)

Run integration tests:
```bash
pytest -m integration -v
```

Integration tests verify the complete pipeline:
- PDF → Text extraction → LLM processing → Synopsis generation → PDF output
- Verification of synopsis structure and content quality
- Online source referencing (gesetze-im-internet.de, etc.)
- Legal change type identification (Ersetzen, Einfügen, Löschen)
- Cache behavior with real API calls

### Run All Tests

```bash
pytest -v
```

### Test Coverage

Run tests with coverage report:
```bash
# Terminal coverage report (unit tests only, fast)
pytest --cov=src --cov=. --cov-report=term-missing -m "not integration"

# Terminal coverage with all tests (includes API calls)
pytest --cov=src --cov=. --cov-report=term-missing

# Generate HTML coverage report
pytest --cov=src --cov=. --cov-report=html

# View HTML report (opens in browser)
open htmlcov/index.html
```

Coverage configuration in `.coveragerc`:
- Target: 70% coverage
- Excludes test files, virtual env, and site-packages
- Shows missing lines in report

**Test Coverage:**
- **Unit tests (21)**: PDF processing, caching, PDF generation
- **Integration tests (10)**: Full pipeline, content quality, error handling
- **Total: 31 tests**

Test data includes both simple and complex PDF examples in `tests/data/`.

**Note:** Integration tests require `ANTHROPIC_API_KEY` to be configured and will make real API calls.

## Project Structure

- `app.py`: Main Streamlit application
- `src/`: Backend modules
  - `pdf_processor.py`: PDF extraction and processing
  - `llm_client.py`: LLM integration with Anthropic Claude
  - `pdf_generator.py`: Markdown to PDF conversion
- `config.py`: Configuration settings
