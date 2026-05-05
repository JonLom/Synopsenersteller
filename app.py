"""Main Streamlit application for Synopsenersteller."""

import streamlit as st
from src.pdf_processor import extract_text_from_pdf, validate_pdf
from src.llm_client import process_amendment_with_llm
from src.pdf_generator import markdown_to_pdf
import config
import logging
import os

# Configure logging
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    filename='logs/synopsenersteller.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main application entry point."""

    st.set_page_config(
        page_title="Synopsenersteller",
        page_icon="📄",
        layout="centered"
    )

    logger.info("Application started")

    st.title("Synopsenersteller")
    st.subheader("Erstellt Synopsen aus PDF, KI und Online Gesetzestexten")

    st.divider()

    if not config.ANTHROPIC_API_KEY:
        st.error(
            "ANTHROPIC_API_KEY not configured. "
            "Please create a .env file with your API key."
        )
        st.stop()

    uploaded_file = st.file_uploader(
        "PDF-Datei hochladen",
        type=['pdf'],
        help="Laden Sie eine PDF-Datei mit einem Gesetzesänderungsvorschlag hoch"
    )

    if uploaded_file is not None:
        st.success(f"Datei hochgeladen: {uploaded_file.name}")
        logger.info(f"PDF uploaded: {uploaded_file.name}")

        pdf_bytes = uploaded_file.read()

        if not validate_pdf(pdf_bytes):
            logger.warning(f"Invalid PDF uploaded: {uploaded_file.name}")
            st.error("Die hochgeladene Datei ist keine gültige PDF-Datei.")
            st.stop()

        if st.button("Synopse erstellen", type="primary", use_container_width=True):
            logger.info(f"Synopsis creation requested for: {uploaded_file.name}")
            with st.spinner("Verarbeite PDF..."):
                try:
                    pdf_text = extract_text_from_pdf(pdf_bytes)
                    st.success("PDF erfolgreich verarbeitet")

                except Exception as e:
                    st.error(f"Fehler beim Verarbeiten der PDF: {str(e)}")
                    st.stop()

            with st.spinner("Analysiere Gesetzesänderungen mit KI..."):
                try:
                    synopsis_markdown, was_cached = process_amendment_with_llm(pdf_text, pdf_bytes)

                    if was_cached:
                        logger.info(f"Result retrieved from cache for: {uploaded_file.name}")
                        st.success("Ergebnis aus Cache geladen (keine API-Kosten)")
                    else:
                        logger.info(f"API call completed for: {uploaded_file.name}")
                        st.success("KI-Analyse abgeschlossen")

                    st.markdown("### Vorschau")
                    st.markdown(synopsis_markdown)

                except Exception as e:
                    logger.error(f"LLM processing failed for {uploaded_file.name}: {str(e)}")
                    st.error(f"Fehler bei der KI-Verarbeitung: {str(e)}")
                    st.stop()

            with st.spinner("Erstelle PDF-Ausgabe..."):
                try:
                    output_pdf = markdown_to_pdf(synopsis_markdown)
                    logger.info(f"PDF generated successfully for: {uploaded_file.name}")
                    st.success("PDF erfolgreich erstellt")

                    st.download_button(
                        label="Synopse als PDF herunterladen",
                        data=output_pdf,
                        file_name="synopse.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )

                except Exception as e:
                    logger.error(f"PDF generation failed for {uploaded_file.name}: {str(e)}")
                    st.error(f"Fehler beim Erstellen der PDF: {str(e)}")
                    st.stop()

    st.divider()

    with st.expander("Über diese Anwendung"):
        st.markdown("""
        Diese Anwendung verarbeitet Gesetzesänderungsvorschläge und erstellt
        strukturierte Synopsen, die die Änderungen im Vergleich zur aktuellen
        Gesetzeslage darstellen.

        **Funktionsweise:**
        1. PDF mit Gesetzesänderungsvorschlag hochladen
        2. KI analysiert den Vorschlag und holt aktuelle Gesetzestexte
        3. Synopse wird als strukturierte Tabelle erstellt
        4. Ausgabe als PDF zum Download

        **Datenquellen:**
        - gesetze-im-internet.de
        - recht.bund.de
        - bgbl.de
        - eur-lex.europa.eu
        """)


if __name__ == "__main__":
    main()
