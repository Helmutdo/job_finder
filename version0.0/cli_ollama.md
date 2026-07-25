# Prompt para Claude CLI — Copiloto de búsqueda de empleo (IA local con Ollama)

## Contexto rápido

Prototipo de un "copiloto de búsqueda de empleo asistido por IA", con
humano en el loop (nunca actúa de forma autónoma sobre plataformas
externas). El usuario sube su CV y pega el texto de una vacante. La
herramienta analiza la compatibilidad y genera documentos adaptados,
que el usuario siempre revisa antes de usar.

Cambio respecto a la versión anterior: en vez de llamar a una API de
IA en la nube (Claude o Gemini), esta fase usa un **modelo local
servido con Ollama**, pensando en portabilidad: el mismo backend debe
poder apuntar más adelante a un Ollama corriendo en un servidor
remoto, cambiando solo una variable de entorno.

---

## Prompt (copiar y pegar en Claude Code)

```
Vas a ayudarme a construir el prototipo mínimo de un "copiloto de
búsqueda de empleo asistido por IA". Es un proyecto personal en etapa
de validación, no una app en producción todavía.

CONTEXTO DEL PRODUCTO:
Es una herramienta con humano en el loop (nunca actúa de forma
autónoma sobre plataformas externas como LinkedIn). El usuario sube
su CV y pega el texto de una vacante concreta. La herramienta analiza
la compatibilidad entre ambos y genera documentos adaptados. El
usuario siempre revisa y aprueba antes de usar cualquier documento
generado.

REGLA CENTRAL, NO NEGOCIABLE:
El análisis y los documentos generados NUNCA pueden incorporar una
habilidad, experiencia, tecnología o logro que no esté ya presente en
el CV real del usuario. Si no hay evidencia de algo en el CV, no se
le puede atribuir en el CV adaptado ni en la carta de presentación.
Prioriza precisión y honestidad sobre "sonar mejor".

MODELO DE IA: LOCAL, VÍA OLLAMA (no uses APIs en la nube en este
prototipo)
  - El backend debe llamar a un modelo servido por Ollama, ya sea
    usando la librería oficial "ollama" de Python o peticiones HTTP
    directas al endpoint REST de Ollama (por defecto
    http://localhost:11434).
  - La URL del host de Ollama debe leerse de una variable de entorno
    OLLAMA_HOST (default "http://localhost:11434"), y el nombre del
    modelo de una variable OLLAMA_MODEL (default "llama3.1:8b").
    Esto es importante: en una etapa posterior este mismo backend se
    va a desplegar apuntando a un Ollama corriendo en un servidor
    remoto, y no debe requerir cambios de código, solo de variables
    de entorno.
  - Usa salida estructurada: Ollama soporta forzar JSON con el
    parámetro "format" (format="json" o, si el modelo lo soporta,
    un JSON schema). Aun así, valida siempre la respuesta del modelo
    contra un modelo Pydantic antes de devolverla, y maneja el caso
    en que el modelo local no devuelva JSON válido (reintento simple
    con el error incluido en el siguiente prompt, máximo 1 reintento).
  - Recomiéndame en el README qué modelos de Ollama probar para esta
    tarea (razonamiento sobre texto + generación de JSON confiable) y
    cómo descargarlos con "ollama pull", sin asumir que ya tengo uno
    instalado.

ALCANCE DE ESTE PROTOTIPO (fase 1, solo esto, nada más):
1. Backend en FastAPI con un único endpoint POST /analyze que reciba:
     - un archivo PDF (el CV)
     - un campo de texto (la descripción de la vacante, pegada tal
       cual)
2. El endpoint debe:
     - extraer el texto del PDF usando PyMuPDF
     - construir un prompt para el modelo local con el CV extraído +
       la descripción de la vacante, incluyendo explícitamente la
       regla de no inventar experiencia
     - pedirle al modelo que devuelva JSON con esta forma:
         {
           "compatibilidad_estimada": number (0-100),
           "criterios_evaluados": string[],
           "requisitos_cumplidos": string[],
           "requisitos_faltantes": string[],
           "evidencia_del_cv": string[],
           "recomendaciones": string[],
           "cv_adaptado": string,
           "carta_presentacion": string,
           "preguntas_entrevista_sugeridas": string[]
         }
     - devolver ese JSON validado como respuesta del endpoint
3. Validar el request y la respuesta con modelos Pydantic.
4. Manejo de errores razonable: PDF vacío o ilegible, campo de
   vacante vacío, Ollama no disponible (connection refused — dar un
   mensaje claro de que hay que correr "ollama serve" o revisar
   OLLAMA_HOST), respuesta del modelo que no es JSON válido tras el
   reintento.
5. Dockerfile para el backend, pensado para que MÁS ADELANTE se
   pueda desplegar en un servidor junto a (o apuntando a) un Ollama
   propio. En este prototipo no levantes Ollama dentro de Docker
   todavía, solo deja el backend containerizado y documentado.
6. Un archivo README.md corto explicando:
     - cómo instalar y correr Ollama localmente
     - qué modelo descargar y por qué
     - cómo correr el backend localmente (instalación, variables de
       entorno, cómo probar el endpoint con curl o con /docs)
     - una nota breve de qué cambiaría para apuntar a Ollama en
       un servidor remoto en la etapa posterior (solo cambiar
       OLLAMA_HOST)
7. Un test básico con pytest que verifique que el endpoint responde
   con la forma esperada de JSON (mockea la llamada a Ollama, no
   dependas de tener el modelo corriendo para que el test pase).

EXPLÍCITAMENTE FUERA DE ALCANCE PARA ESTE PROTOTIPO:
  - Login o autenticación de usuarios
  - Base de datos (ni SQL ni grafo)
  - Frontend
  - Integración con LinkedIn, Google Calendar u otras plataformas
  - Postulación o mensajería automática
  - LangGraph, MCP, o cualquier framework de orquestación de agentes
  - Levantar Ollama dentro del mismo contenedor Docker del backend

STACK A USAR:
FastAPI, Pydantic, PyMuPDF, librería "ollama" de Python (o requests
directo al endpoint REST), pytest, python-dotenv para las variables
de entorno. Python 3.11+.

Antes de escribir código, propone la estructura de carpetas del
proyecto y confírmame que te parece razonable. Después implementa
paso a paso, explicando brevemente cada archivo que crees.
```