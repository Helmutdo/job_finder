from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers.analyze import router as analyze_router

app = FastAPI(
    title="Copiloto de búsqueda de empleo — Prototipo",
    description=(
        "Analiza la compatibilidad entre un CV y una vacante concreta "
        "usando un modelo de IA local servido con Ollama. Humano en el "
        "loop: nunca postula ni actúa de forma autónoma."
    ),
    version="0.1.0",
)

app.include_router(analyze_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


STATIC_DIR = Path(__file__).resolve().parent.parent / "static"
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")
