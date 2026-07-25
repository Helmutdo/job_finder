CONTEXTO DEL PROYECTO
======================================================================

NOMBRE DE TRABAJO
Copiloto de búsqueda de empleo asistido por IA

FECHA DE ORIGEN DE LA IDEA
20 de julio de 2026

METODOLOGÍA DE ORIGEN
Desglose de idea (15 min) -> generar 3 ideas -> relacionarlas ->
dedicar una tarde a desarrollar y lanzar -> repetir.

----------------------------------------------------------------------
1. PROBLEMA
----------------------------------------------------------------------
Buscar trabajo es lento y repetitivo: adaptar el CV a cada vacante,
evaluar si realmente calzas con los requisitos, redactar cartas de
presentación y llevar registro de a qué postulaste y en qué estado
está cada proceso. La mayoría de las personas lo hace a mano, sin
evidencia clara de por qué encajan (o no) con una oferta.

----------------------------------------------------------------------
2. IDEA ORIGINAL (BRAINSTORM COMPLETO)
----------------------------------------------------------------------
La idea inicial era un "postulador automático a trabajos asistido por
IA" con seis capacidades:
  1. Recoger CV/LinkedIn/GitHub del usuario, calibrar contra ATS y
     optimizar el perfil.
  2. Postular a trabajos según cargo y mercado objetivo (elegido por
     el usuario o recomendado por IA).
  3. Contactar reclutadores y mantener conversaciones (mensajes en
     LinkedIn, postulación directa, otras plataformas).
  4. Agendar entrevistas en Google Calendar / Outlook.
  5. Recomendaciones sobre remuneración (aceptar/rechazar ofertas).
  6. Registro de trabajos postulados en una tabla.

----------------------------------------------------------------------
3. DECISIÓN DE ALCANCE (POR QUÉ SE ACOTÓ EL MVP)
----------------------------------------------------------------------
Automatizar mensajes y postulaciones directas en LinkedIn viola sus
Términos de Servicio (prohíbe bots, scraping y automatización de
mensajes/acciones) y expone al usuario a que le restrinjan o baneen
la cuenta. Por eso el punto 3 del brainstorm original queda FUERA del
producto, al menos en esta fase.

El producto se reposiciona como un "copiloto" con humano en el loop,
no un bot que actúa de forma autónoma:
  - La IA analiza y prepara.
  - El usuario revisa.
  - El usuario aprueba y envía manualmente.
  - La aplicación registra el resultado.

Este modelo es más defendible técnica, ética y comercialmente, y
además evita el riesgo de cuentas baneadas que mataría el producto
el día 1.

Segunda ronda de revisión (comparando dos propuestas de IA, Gemini y
Claude, evaluadas por un tercer modelo) corrigió además:
  - No usar LangGraph para un flujo de pocos pasos secuenciales;
    basta con funciones normales. LangGraph se reserva para cuando
    haya que pausar, guardar estado y reanudar procesos.
  - No usar MCP para crear eventos de calendario; la API directa de
    Google Calendar con OAuth es más simple y suficiente.
  - No usar una base de datos de grafos en el MVP; un esquema
    relacional (SQLite) modela perfectamente usuarios, CVs, vacantes,
    postulaciones, documentos y contactos. El grafo puede tener
    sentido más adelante para recomendaciones (empresas similares,
    redes de contactos), no para validar el problema inicial.
  - No llamar al resultado del análisis "score ATS" (no existe un
    algoritmo ATS universal); llamarlo "compatibilidad estimada" y
    explicar los criterios (habilidades obligatorias, experiencia,
    tecnologías, idioma, ubicación, autorización laboral).
  - No poner el agendamiento de entrevistas como núcleo del MVP: eso
    ocurre después de conseguir respuestas, y al principio habrá
    pocas entrevistas, por lo que esa función no valida el problema
    principal (compatibilidad + adaptación de candidatura).

REGLA CENTRAL DEL PRODUCTO (no negociable):
La IA nunca puede incorporar en el CV o la carta una habilidad,
experiencia o resultado que no aparezca ya en el perfil real del
usuario. Cero invención de logros o experiencia.

----------------------------------------------------------------------
4. MVP DEFINITIVO
----------------------------------------------------------------------
Flujo principal:
  1. El usuario sube su CV (PDF).
  2. Selecciona país, cargo e idioma objetivo.
  3. Pega el texto de una descripción de vacante concreta.
  4. La aplicación devuelve:
       - Compatibilidad estimada (con evidencia citada del CV, nunca
         inventada).
       - Requisitos cumplidos.
       - Requisitos faltantes.
       - Recomendaciones de mejora sin inventar experiencia.
       - CV adaptado a esa vacante.
       - Carta de presentación.
       - Respuestas sugeridas a preguntas frecuentes de entrevista.
  5. El usuario revisa, edita y aprueba los documentos generados.
  6. La postulación queda registrada con estado:
       descubierta -> preparada -> postulada -> entrevista ->
       rechazada -> oferta.

Fuera del alcance del MVP (deliberadamente pospuesto):
  - Postulación automática en LinkedIn u otras plataformas.
  - Envío/recepción automática de mensajes a reclutadores.
  - Agendamiento autónomo de entrevistas.
  - Base de datos de grafos.
  - Orquestación con LangGraph.
  - Integración vía MCP.

----------------------------------------------------------------------
5. STACK TÉCNICO DEL MVP
----------------------------------------------------------------------
  Backend:            FastAPI
  Validación/schemas:  Pydantic
  Base de datos:       SQLite (migrable a PostgreSQL después)
  ORM:                 SQLModel o SQLAlchemy
  Extracción de PDF:   PyMuPDF
  IA (análisis):       API de Claude (Sonnet) con salida estructurada
                       en JSON, o alternativamente Gemini con salida
                       estructurada
  Pruebas:             pytest
  Despliegue:          contenedor Docker (VPS)
  Frontend (fase 2):   Next.js o React (el MVP puede validarse primero
                       solo con API + Swagger UI o un frontend mínimo)

Modelo de datos relacional sugerido (tablas):
  users
  profiles
  jobs
  applications
  documents
  contacts
  interviews

----------------------------------------------------------------------
6. ROLES / CONTEXTO DEL EQUIPO (si aplica al mismo autor)
----------------------------------------------------------------------
Este proyecto es una iniciativa personal/lateral de Helmut Schweitzer
González, estudiante de Ingeniería Informática en INACAP, con
experiencia previa en desarrollo web, soporte TI, y trabajo con
agentes de IA (incluye participación en un hackathon de agentes SRE).
No tiene relación formal con las asignaturas de INACAP; es un
proyecto propio para validar y eventualmente lanzar.

----------------------------------------------------------------------
7. PRÓXIMO PASO ACORDADO
----------------------------------------------------------------------
Construir un prototipo mínimo del flujo principal en una sola tarde:
extracción de texto del CV + comparación contra una vacante pegada
como texto plano + salida de compatibilidad estimada. Sin login, sin
base de datos todavía, para validar el análisis antes de construir
el resto.


======================================================================
PROMPT PARA CLAUDE CLI (Claude Code)
======================================================================
Copia y pega el siguiente prompt en Claude Code para iniciar el
desarrollo del prototipo.

----------------------------------------------------------------------

Vas a ayudarme a construir el prototipo mínimo de un "copiloto de
búsqueda de empleo asistido por IA". Este es un proyecto personal en
etapa de validación, no una app en producción todavía.

CONTEXTO DEL PRODUCTO:
Es una herramienta con humano en el loop (nunca actúa de forma
autónoma sobre plataformas externas). El usuario sube su CV y pega el
texto de una vacante concreta. La herramienta analiza la
compatibilidad entre ambos y genera documentos adaptados. El usuario
siempre revisa y aprueba antes de usar cualquier documento generado.

REGLA CENTRAL, NO NEGOCIABLE:
El análisis y los documentos generados NUNCA pueden incorporar una
habilidad, experiencia, tecnología o logro que no esté ya presente en
el CV real del usuario. Si el usuario no tiene evidencia de algo en
su CV, no se le puede atribuir en el CV adaptado ni en la carta de
presentación. Prioriza precisión y honestidad sobre "sonar mejor".

ALCANCE DE ESTE PROTOTIPO (fase 1, solo esto, nada más):
1. Un backend en FastAPI con un único endpoint POST /analyze que
   reciba:
     - un archivo PDF (el CV)
     - un campo de texto (la descripción de la vacante, pegada tal
       cual)
2. El endpoint debe:
     - extraer el texto del PDF usando PyMuPDF
     - enviar el CV extraído + la descripción de la vacante a la API
       de Claude (usar la Anthropic Python SDK, modelo
       claude-sonnet-4-6, con salida estructurada vía JSON schema)
     - pedirle al modelo que devuelva un JSON con esta forma:
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
     - el prompt al modelo debe incluir explícitamente la regla de no
       inventar experiencia, y pedirle que cite en "evidencia_del_cv"
       fragmentos reales del CV que respalden la compatibilidad
     - devolver ese JSON como respuesta del endpoint
3. Validar el request y la respuesta con modelos Pydantic.
4. Manejo de errores razonable (PDF vacío o ilegible, campo de
   vacante vacío, error de la API de Claude).
5. Un archivo README.md corto explicando cómo correr el proyecto
   localmente (instalación, variables de entorno para la API key,
   cómo probar el endpoint con curl o con la documentación
   automática de FastAPI en /docs).
6. Un test básico con pytest que verifique que el endpoint responde
   con la forma esperada de JSON (puedes mockear la llamada a la API
   de Claude).

EXPLÍCITAMENTE FUERA DE ALCANCE PARA ESTE PROTOTIPO (no lo
implementes todavía, ni dejes código a medio hacer para esto):
  - Login o autenticación de usuarios
  - Base de datos (ni SQL ni grafo)
  - Frontend
  - Integración con LinkedIn, Google Calendar u otras plataformas
  - Postulación o mensajería automática
  - LangGraph, MCP, o cualquier framework de orquestación de agentes

STACK A USAR:
FastAPI, Pydantic, PyMuPDF, Anthropic Python SDK, pytest, python-dotenv
para la API key. Python 3.11+.

Antes de escribir código, propone la estructura de carpetas del
proyecto y confírmame que te parece razonable. Después implementa
paso a paso, explicando brevemente cada archivo que crees.

----------------------------------------------------------------------
FIN DEL PROMPT
======================================================================