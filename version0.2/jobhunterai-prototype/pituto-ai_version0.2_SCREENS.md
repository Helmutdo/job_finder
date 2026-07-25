# Pituto-AI — Pantallas de version0.2

Prototipo estilo SaaS ejecutivo con navegación lateral fija (sidebar) presente en las 6 pantallas: **Profile · AI Recommendations · CV Builder · Automation Engine · History · Settings**, más el botón "New Application" que siempre vuelve a `index.html`. A diferencia de version0.1 (layout de barra superior), version0.2 usa un layout de sidebar fijo a la izquierda y, en la mayoría de las pantallas, tema oscuro ("Executive Automation").

---

## 1. Profile (`index.html`)

Pantalla de entrada del flujo: calibración del perfil profesional antes de que la IA empiece a buscar y postular.

- **Identity Details**: Nombre, Apellido, Nacionalidad (select), enlace de Portfolio/GitHub y perfil de LinkedIn.
- **Career Target**: Rol de TI deseado (select) y aspiración salarial (USD/año).
- **Market Target**: chips de países/regiones donde buscar trabajo (ej. Chile, Remote LATAM), con input + botón "Add" para agregar nuevas ubicaciones dinámicamente (JS funcional, soporta Enter).
- **Role Target**: filtros de modalidad de trabajo (Remote / Onsite / Hybrid, pills multi-selección) y nivel de experiencia requerido (select).
- **CV Architecture** (columna derecha): zona de drag & drop para subir el CV en PDF, con barra de progreso animada de "AI Calibration Status" que simula el análisis y muestra una insignia "Profile Calibrated for IT" al completarse.
- **Optimization Engine**: barra inferior tipo bento con el % de perfil completado y botón "Finalize Calibration" → navega a `recomendaciones-mercado.html`.

---

## 2. AI Recommendations (`recomendaciones-mercado.html`)

Análisis de mercado: compara el rol que el usuario busca contra lo que la IA recomienda según su perfil técnico.

- **Featured Recommendation**: tarjeta destacada con el rol alternativo sugerido (ej. Infrastructure Engineer / SRE), justificación basada en habilidades (Kubernetes, CI/CD) y aumento estimado de salario.
- **Strategic Pivot**: comparación visual "Job You Seek" vs. "Job AI Recommends" con indicadores de competencia/demanda.
- **Market Hiring Velocity**: gráfico de barras mock comparando velocidad de contratación entre roles (SRE vs Backend).
- **Mandatory IT Keywords**: lista de palabras clave requeridas por ATS, marcando cuáles ya tiene el usuario y cuáles faltan.
- Botones de acción: "View Gap Analysis" y "Add to CV Builder" → ambos navegan a `fabrica-cv-optimizado.html`.
- Insight con efecto de "escritura" que rota entre distintos mensajes de la IA cada pocos segundos.

---

## 3. CV Builder (`fabrica-cv-optimizado.html`)

Editor/visor donde la IA optimiza el CV del usuario para una vacante específica.

- **Raw Input Extract** (panel izquierdo): resumen original del CV extraído del PDF, historial laboral y notas de la IA sobre keywords faltantes detectadas.
- **AI Enhanced CV Preview** (panel derecho): mockup del CV en formato A4 ya optimizado, con keywords resaltadas, y un widget flotante "AI Strategy" con la probabilidad estimada de ser llamado a entrevista.
- Toolbar superior: "Copy Text", "Download PDF", indicador "98% ATS MATCH" y un toggle "Approve for automatic application" (activa/desactiva el envío automático de la postulación, con feedback visual al activarse).

---

## 4. Automation Engine (`motor-automatizacion.html`)

Panel de control del bot que scrapea plataformas de empleo y postula automáticamente.

- **Target Platforms**: tarjetas de LinkedIn, Getonbrd y Wellfound con switches para activar/desactivar el scraping por plataforma y su estado de conexión.
- Configuración de límites: máximo de postulaciones por día y países/regiones objetivo (chips).
- **Engine Status**: barras de progreso de precisión del scraper y de match rate de la IA, más el botón "Start Scraper & Automated Postulation" que inicia/detiene el motor (cambia a estado "Stop Engine Now").
- **Engine Logs**: consola en vivo estilo terminal que va agregando logs simulados (scraping, matcheo de IA, postulaciones exitosas) mientras el motor está "corriendo".

---

## 5. History (`historial-aplicaciones.html`)

Registro histórico de todas las postulaciones realizadas por el sistema.

- Barra de stats: Success Rate, Active Interviews, AI Match Avg, Time to Offer.
- Tabla de "Recent Activities" con empresa, cargo, plataforma, fecha y estado (Interview, Offer, Auto-applied, Rejected, Discovered), con buscador y filtros.
- Al hacer clic en una fila se abre un panel lateral ("Application Details") con el detalle de esa postulación: documentos enviados (CV, carta de presentación, portafolio) e insights de la IA sobre esa postulación puntual.

---

## 6. Settings (`configuracion.html`)

Configuración general de la cuenta y del motor de automatización.

- **Platform Integration**: gestión segura de credenciales (cookie de sesión de LinkedIn, API Key de OpenAI) con botón para mostrar/ocultar el valor.
- **Automation Logic**: switches para "Dynamic Tailoring" (ajuste automático del CV según la vacante) y "AI Negotiation Proxy" (respuesta automática a reclutadores sobre pretensión salarial).
- **System Notifications**: checkboxes para resumen diario por email, alertas SMS de entrevistas y reporte semanal "Market Pulse".
- **Engine Status**: estado operativo del motor y próxima corrida programada.
- Acciones globales: "Discard Changes" y "Save Global Settings".

---

## Flujo de navegación

```
index.html (Profile)
   └─ "Finalize Calibration" → recomendaciones-mercado.html (AI Recommendations)
        └─ "View Gap Analysis" / "Add to CV Builder" → fabrica-cv-optimizado.html (CV Builder)

Sidebar (todas las pantallas): Profile · AI Recommendations · CV Builder · Automation Engine · History · Settings
"New Application" (todas las pantallas): → index.html
```
