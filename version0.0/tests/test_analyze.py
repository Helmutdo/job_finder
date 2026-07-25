import fitz
from fastapi.testclient import TestClient

from app.main import app
from app.schemas import AnalysisResult

client = TestClient(app)


def _build_sample_pdf_bytes() -> bytes:
    document = fitz.open()
    page = document.new_page()
    page.insert_text((72, 72), "Juan Perez\nIngeniero de Software\nPython, FastAPI, SQL")
    pdf_bytes = document.tobytes()
    document.close()
    return pdf_bytes


def test_analyze_returns_expected_json_shape(monkeypatch):
    fake_result = AnalysisResult(
        compatibilidad_estimada=72.5,
        criterios_evaluados=["habilidades", "experiencia"],
        requisitos_cumplidos=["Python"],
        requisitos_faltantes=["Kubernetes"],
        evidencia_del_cv=["Python, FastAPI, SQL"],
        recomendaciones=["Sumar experiencia con Kubernetes"],
        cv_adaptado="CV adaptado de prueba",
        carta_presentacion="Carta de prueba",
        preguntas_entrevista_sugeridas=["¿Cuéntame de tu experiencia con Python?"],
    )

    monkeypatch.setattr(
        "app.routers.analyze.analyze_cv_against_job",
        lambda cv_text, job_description: fake_result,
    )

    response = client.post(
        "/analyze",
        files={"cv": ("cv.pdf", _build_sample_pdf_bytes(), "application/pdf")},
        data={"job_description": "Se busca desarrollador Python con experiencia en FastAPI."},
    )

    assert response.status_code == 200
    body = response.json()
    assert set(body.keys()) == set(AnalysisResult.model_fields.keys())
    assert body["compatibilidad_estimada"] == 72.5
    assert body["evidencia_del_cv"] == ["Python, FastAPI, SQL"]


def test_analyze_rejects_empty_job_description():
    response = client.post(
        "/analyze",
        files={"cv": ("cv.pdf", _build_sample_pdf_bytes(), "application/pdf")},
        data={"job_description": "   "},
    )

    assert response.status_code == 400


def test_analyze_rejects_non_pdf_file():
    response = client.post(
        "/analyze",
        files={"cv": ("cv.txt", b"no es un pdf", "text/plain")},
        data={"job_description": "Se busca desarrollador Python."},
    )

    assert response.status_code == 400
