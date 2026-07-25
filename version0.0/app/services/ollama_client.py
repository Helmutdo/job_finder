import json
from functools import lru_cache

import httpx
import ollama

from app.config import get_settings
from app.errors import OllamaError
from app.schemas import AnalysisResult

SYSTEM_PROMPT = """Eres un asistente experto en reclutamiento que evalúa la \
compatibilidad entre el CV de un candidato y una vacante concreta.

REGLA NO NEGOCIABLE: nunca incorpores, en ningún campo de tu respuesta \
(incluyendo cv_adaptado y carta_presentacion), una habilidad, tecnología, \
experiencia o logro que no esté ya presente de forma explícita en el CV \
proporcionado. Si el candidato no tiene evidencia de algo en su CV, no se le \
puede atribuir bajo ninguna circunstancia. Prioriza precisión y honestidad \
sobre "sonar mejor". Si no hay evidencia suficiente para justificar una \
afirmación, no la hagas.

Para cada elemento de "evidencia_del_cv" cita un fragmento textual real del \
CV que respalde la compatibilidad estimada. No inventes citas.

Evalúa la compatibilidad usando criterios explícitos: habilidades \
obligatorias, experiencia relevante, tecnologías, idioma requerido, \
ubicación y autorización laboral, entre los que apliquen según la vacante.

Responde ÚNICAMENTE con un objeto JSON válido que cumpla el schema \
proporcionado. No agregues texto antes ni después del JSON."""

RESULT_SCHEMA = {
    "type": "object",
    "properties": {
        "compatibilidad_estimada": {
            "type": "number",
            "minimum": 0,
            "maximum": 100,
            "description": "Porcentaje estimado de compatibilidad entre el CV y la vacante.",
        },
        "criterios_evaluados": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Criterios usados para evaluar la compatibilidad.",
        },
        "requisitos_cumplidos": {
            "type": "array",
            "items": {"type": "string"},
        },
        "requisitos_faltantes": {
            "type": "array",
            "items": {"type": "string"},
        },
        "evidencia_del_cv": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Fragmentos textuales reales del CV. Nunca inventados.",
        },
        "recomendaciones": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Sugerencias de mejora que no atribuyan experiencia inexistente.",
        },
        "cv_adaptado": {"type": "string"},
        "carta_presentacion": {"type": "string"},
        "preguntas_entrevista_sugeridas": {
            "type": "array",
            "items": {"type": "string"},
        },
    },
    "required": [
        "compatibilidad_estimada",
        "criterios_evaluados",
        "requisitos_cumplidos",
        "requisitos_faltantes",
        "evidencia_del_cv",
        "recomendaciones",
        "cv_adaptado",
        "carta_presentacion",
        "preguntas_entrevista_sugeridas",
    ],
}

MAX_RETRIES = 1


@lru_cache
def _get_client() -> ollama.Client:
    return ollama.Client(host=get_settings().ollama_host)


def _build_user_message(cv_text: str, job_description: str) -> str:
    return (
        "CV DEL CANDIDATO:\n"
        f"{cv_text}\n\n"
        "DESCRIPCIÓN DE LA VACANTE:\n"
        f"{job_description}"
    )


def analyze_cv_against_job(cv_text: str, job_description: str) -> AnalysisResult:
    settings = get_settings()
    client = _get_client()

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": _build_user_message(cv_text, job_description)},
    ]

    last_error: str | None = None

    for attempt in range(MAX_RETRIES + 1):
        if last_error is not None:
            messages.append(
                {
                    "role": "user",
                    "content": (
                        "Tu respuesta anterior no era JSON válido o no cumplía el "
                        f"schema esperado. Error: {last_error}\n"
                        "Responde de nuevo ÚNICAMENTE con el JSON correcto."
                    ),
                }
            )

        try:
            response = client.chat(
                model=settings.ollama_model,
                messages=messages,
                format=RESULT_SCHEMA,
                options={"temperature": 0.2},
            )
        except httpx.ConnectError as exc:
            raise OllamaError(
                f"No se pudo conectar a Ollama en {settings.ollama_host}. "
                "¿Está corriendo? Prueba con 'ollama serve' o revisa la "
                "variable de entorno OLLAMA_HOST."
            ) from exc
        except ollama.ResponseError as exc:
            raise OllamaError(
                f"Ollama devolvió un error (¿descargaste el modelo "
                f"'{settings.ollama_model}' con 'ollama pull {settings.ollama_model}'?): {exc}"
            ) from exc

        raw_content = response["message"]["content"]

        try:
            parsed = json.loads(raw_content)
            return AnalysisResult.model_validate(parsed)
        except Exception as exc:
            last_error = str(exc)
            continue

    raise OllamaError(
        f"El modelo '{settings.ollama_model}' no devolvió un JSON válido tras "
        f"{MAX_RETRIES + 1} intento(s). Último error: {last_error}"
    )
