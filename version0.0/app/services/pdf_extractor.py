import fitz

from app.errors import PDFExtractionError


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    try:
        document = fitz.open(stream=pdf_bytes, filetype="pdf")
    except Exception as exc:
        raise PDFExtractionError(
            "No se pudo abrir el PDF. Verifica que el archivo no esté dañado."
        ) from exc

    try:
        text = "\n".join(page.get_text() for page in document)
    finally:
        document.close()

    text = text.strip()
    if not text:
        raise PDFExtractionError(
            "El PDF no contiene texto extraíble (¿es una imagen escaneada?)."
        )

    return text
