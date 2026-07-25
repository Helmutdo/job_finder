from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status

from app.errors import OllamaError, PDFExtractionError
from app.schemas import AnalysisResult
from app.services.ollama_client import analyze_cv_against_job
from app.services.pdf_extractor import extract_text_from_pdf

router = APIRouter()


@router.post("/analyze", response_model=AnalysisResult)
async def analyze(
    cv: UploadFile = File(..., description="CV del candidato en formato PDF."),
    job_description: str = Form(..., description="Texto de la descripción de la vacante."),
) -> AnalysisResult:
    if cv.content_type not in ("application/pdf", "application/x-pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El archivo debe ser un PDF.",
        )

    if not job_description or not job_description.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La descripción de la vacante no puede estar vacía.",
        )

    pdf_bytes = await cv.read()
    if not pdf_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El archivo PDF está vacío.",
        )

    try:
        cv_text = extract_text_from_pdf(pdf_bytes)
    except PDFExtractionError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc

    try:
        return analyze_cv_against_job(cv_text=cv_text, job_description=job_description)
    except OllamaError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        ) from exc
