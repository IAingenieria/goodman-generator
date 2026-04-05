 Resumen: Goodman Tech — Generador Automático de Landing Pages SEO
¿Qué hace esta app?
Es un sistema automatizado de marketing SEO que genera landing pages y artículos de blog para posicionar a Goodman Tech (empresa de IA en Monterrey) en Google sin trabajo manual.

🎯 Objetivo
Posicionar decenas de keywords sobre IA empresarial en México automáticamente, usando Claude API para generar contenido SEO optimizado.

🔧 Componentes principales
1️⃣ Detector de Keywords (detectar_keywords_ambassador.py)
Qué hace: Encuentra automáticamente las mejores keywords para posicionar

7 fuentes de datos:

Google Search Console API
Google Suggest
Google Trends
SerpApi Autocomplete (keywords reales de Google México)
SerpApi Related Searches
SerpApi People Also Ask
Claude API (análisis estratégico de gaps y clusters)
Output: keywords.txt, keywords_blog.txt, keywords_ambassador.csv

2️⃣ Generador de Landings (generar_landing.py)
Qué hace: Recibe una keyword y genera una landing page completa en React/TypeScript

Proceso:

Llama a Claude API con la keyword
Claude genera el copy SEO optimizado
Crea archivo .tsx completo con React + Tailwind CSS
Registra la ruta en App.tsx
Valida que no tenga errores de sintaxis
Output: Archivo listo para compilar en src/pages/Empresas*.tsx

3️⃣ Generador en Lote (generar_lote.py)
Qué hace: Genera múltiples landings automáticamente

Ejemplo:

bash
python generar_lote.py --limite 5  # Genera 5 landings
Al terminar:

Actualiza sitemap.xml automáticamente
Notifica a Google Search Console
4️⃣ Bot Telegram (bot_goodman.py)
Qué hace: Control SEO desde el celular

Comandos principales:

/keywords → Detecta keywords nuevas
/siguiente → Aprobar/rechazar keywords una por una
/estado → Ver indexación del sitio en Google
/alertas → Problemas críticos de SEO
/generadas → Páginas ya creadas
Beneficio: Puedes aprobar keywords y generar landings desde el celular

5️⃣ Analizador GSC (gsc_indexacion.py)
Qué hace: Lee datos de Google Search Console y genera alertas

Output: reporte_indexacion.json con:

Páginas indexadas vs no indexadas
Problemas críticos
Recomendaciones automáticas
6️⃣ Actualizador de Sitemap (actualizar_sitemap.py)
Qué hace: Lee App.tsx, genera sitemap.xml actualizado y notifica a Google

Se ejecuta automáticamente después de cada generación en lote.

📊 Resultados actuales (04/04/2026)
Métrica	Valor
Landings generadas	~41 páginas
Páginas indexadas en Google	8 (36.4%)
Impresiones últimos 7 días	74
Sitemap enviado a GSC	✅
🚀 Flujo completo
1. Detector encuentra keywords → keywords.txt
2. Bot Telegram te notifica → apruebas desde celular
3. Generador crea landing page → archivo .tsx
4. Sitemap se actualiza automáticamente
5. Google recibe notificación
6. Página se indexa en Google
7. Empieza a recibir tráfico orgánico
💡 Lo más importante
Todo es automático excepto la aprobación de keywords, que haces desde Telegram para mantener control de calidad.

Stack:

Python (backend/scripts)
React + TypeScript (frontend)
Claude API (generación de contenido)
Google Search Console API (datos SEO)
SerpApi (keywords reales)
Telegram Bot (control remoto)
Resultado: Escalas tu SEO sin contratar copywriters ni hacer trabajo manual repetitivo.