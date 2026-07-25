from pydantic import BaseModel, Field


class AnalysisResult(BaseModel):
    compatibilidad_estimada: float = Field(..., ge=0, le=100)
    criterios_evaluados: list[str]
    requisitos_cumplidos: list[str]
    requisitos_faltantes: list[str]
    evidencia_del_cv: list[str]
    recomendaciones: list[str]
    cv_adaptado: str
    carta_presentacion: str
    preguntas_entrevista_sugeridas: list[str]
