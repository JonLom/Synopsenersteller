"""Main Streamlit application for Synopsenersteller."""

import streamlit as st
from src.pdf_processor import extract_text_from_pdf, validate_pdf
from src.llm_client import process_amendment_with_llm
from src.pdf_generator import markdown_to_pdf
import config
import logging
import os

# Configure logging for both local and Streamlit Cloud
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Logs to stdout (captured by Streamlit Cloud)
    ]
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

    st.warning("""⚠️ Testversion! Muss noch verifiziert werden. 
                Wir freuen uns über Feedback und Ideen! Siehe Kontakt unten.
                """)

    st.divider()

    if not config.ANTHROPIC_API_KEY:
        logger.error("API key missing. Please create a .env file with your API key.")

        st.error( "Kein KI-Zugang. Abburch."
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

        # Check if we need to reset state for new file
        if 'last_filename' not in st.session_state or st.session_state.last_filename != uploaded_file.name:
            st.session_state.last_filename = uploaded_file.name
            st.session_state.synopsis_markdown = None
            st.session_state.output_pdf = None

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
                    else:
                        logger.info(f"API call completed for: {uploaded_file.name}")

                    st.success("KI-Analyse abgeschlossen")

                except Exception as e:
                    logger.error(f"LLM processing failed for {uploaded_file.name}: {str(e)}")
                    st.error(f"Fehler bei der KI-Verarbeitung: {str(e)}")
                    st.stop()

            with st.spinner("Erstelle PDF-Ausgabe..."):
                try:
                    output_pdf = markdown_to_pdf(synopsis_markdown)
                    logger.info(f"PDF generated successfully for: {uploaded_file.name}")
                    st.success("PDF erfolgreich erstellt")

                    # Store in session state
                    st.session_state.synopsis_markdown = synopsis_markdown
                    st.session_state.output_pdf = output_pdf

                except Exception as e:
                    logger.error(f"PDF generation failed for {uploaded_file.name}: {str(e)}")
                    st.error(f"Fehler beim Erstellen der PDF: {str(e)}")
                    st.stop()

        # Display results if available in session state
        if st.session_state.get('synopsis_markdown') and st.session_state.get('output_pdf'):
            st.download_button(
                label="Synopse als PDF herunterladen",
                data=st.session_state.output_pdf,
                file_name="synopse.pdf",
                mime="application/pdf",
                use_container_width=True
            )

            st.markdown(st.session_state.synopsis_markdown)

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

        **Inspiriert durch:**
        - [Lage der Gesetze - Forum Thread](https://talk.lagedernation.org/t/lage-der-gesetze-gesetzesaenderungen-als-pull-requests-sichtbar-machen/32799)

        **Repository:**
        - [GitHub: JonLom/Synopsenersteller](https://github.com/JonLom/Synopsenersteller)
        """)


if __name__ == "__main__":
    main()
