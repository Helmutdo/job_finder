# Copiloto de búsqueda de empleo — Prototipo (fase 1, IA local con Ollama)

Prototipo mínimo del flujo principal: sube un CV en PDF, pega el texto de
una vacante, y obtén un análisis de compatibilidad generado con un modelo
de IA **local**, servido con [Ollama](https://ollama.com) (evidencia citada
del CV, requisitos cumplidos/faltantes, recomendaciones, CV adaptado, carta
de presentación y preguntas de entrevista sugeridas).

Herramienta con humano en el loop: no postula ni envía nada de forma
automática. Solo analiza y prepara documentos para que el usuario los
revise y apruebe.

Fuera de alcance en esta fase: login, base de datos, frontend, integración
con LinkedIn/Calendar, postulación o mensajería automática, correr Ollama
dentro del contenedor Docker del backend.

## 1. Instalar y correr Ollama

Instala Ollama siguiendo [ollama.com/download](https://ollama.com/download)
(en Linux: `curl -fsSL https://ollama.com/install.sh | sh`).

Arranca el daemon (si no se inició solo al instalar):

```bash
ollama serve
```

Descarga un modelo. Para esta tarea (razonamiento sobre texto + generación
de JSON confiable) se recomienda, de más a menos liviano:

- `llama3.1:8b` (default de este proyecto) — buen equilibrio entre calidad
  de razonamiento y velocidad en CPU/GPU modesta. ~4.7 GB.
- `qwen2.5:14b` — mejor siguiendo instrucciones y generando JSON
  estructurado si tienes más VRAM/RAM disponible. ~9 GB.
- `mistral:7b` — alternativa más liviana si `llama3.1:8b` es muy lento en
  tu máquina. ~4.1 GB.

```bash
ollama pull llama3.1:8b
```

## 2. Instalar el backend

Requiere Python 3.11+.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 3. Configuración

Copia `.env.example` a `.env`:

```bash
cp .env.example .env
```

```
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
```

`OLLAMA_HOST` es la única variable que cambiarías para apuntar a un Ollama
corriendo en un servidor remoto más adelante (por ejemplo
`http://mi-servidor:11434`) — no requiere cambios de código.

## 4. Ejecutar el servidor

```bash
uvicorn app.main:app --reload
```

La API queda disponible en `http://127.0.0.1:8000`. Documentación
interactiva (Swagger UI) en `http://127.0.0.1:8000/docs`.

## 5. Probar el endpoint

### Con la documentación automática

Abre `http://127.0.0.1:8000/docs`, expande `POST /analyze`, sube un PDF y
pega el texto de una vacante en `job_description`.

### Con curl

```bash
curl -X POST http://127.0.0.1:8000/analyze \
  -F "cv=@/ruta/a/tu_cv.pdf" \
  -F "job_description=Se busca desarrollador backend con experiencia en Python, FastAPI y SQL. Inglés intermedio."
```

Respuesta esperada (JSON):

```json
{
  "compatibilidad_estimada": 78,
  "criterios_evaluados": ["..."],
  "requisitos_cumplidos": ["..."],
  "requisitos_faltantes": ["..."],
  "evidencia_del_cv": ["..."],
  "recomendaciones": ["..."],
  "cv_adaptado": "...",
  "carta_presentacion": "...",
  "preguntas_entrevista_sugeridas": ["..."]
}
```

Si Ollama no está corriendo, el endpoint responde `502` con un mensaje
indicando que revises `ollama serve` o la variable `OLLAMA_HOST`. Si el
modelo no está descargado, el mensaje sugiere el `ollama pull` necesario.

## 6. Tests

```bash
pytest
```

Los tests mockean la llamada a Ollama, por lo que no requieren tener el
modelo descargado ni el daemon corriendo.

## 7. Docker

El `Dockerfile` empaqueta solo el backend (no incluye Ollama). Se espera
que `OLLAMA_HOST` apunte a un Ollama accesible desde el contenedor:

```bash
docker build -t job-applier-backend .
docker run -p 8000:8000 -e OLLAMA_HOST=http://host.docker.internal:11434 job-applier-backend
```

En un despliegue posterior, `OLLAMA_HOST` apuntaría a un servidor remoto
con Ollama (o a un contenedor de Ollama en la misma red) — sin tocar el
código del backend.
