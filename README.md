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
cp .env .env
# Edit .env and add your ANTHROPIC_API_KEY
```

## Usage

Run the Streamlit app:
```bash
streamlit run app.py
```

## Project Structure

- `app.py`: Main Streamlit application
- `src/`: Backend modules
  - `pdf_processor.py`: PDF extraction and processing
  - `llm_client.py`: LLM integration with Anthropic Claude
  - `pdf_generator.py`: Markdown to PDF conversion
- `config.py`: Configuration settings
