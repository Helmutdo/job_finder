class PDFExtractionError(Exception):
    """El PDF no se pudo abrir o no contiene texto extraíble."""


class OllamaError(Exception):
    """Ollama no está disponible o devolvió una respuesta inválida."""
