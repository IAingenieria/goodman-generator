# Goodman Tech — Contexto del Proyecto

---

## Sesión 04/04/2026 — SEO Ambassador v3 + Bot Telegram

### Lo que se construyó esta sesión

**Módulo SEO Ambassador v3** (`detectar_keywords_ambassador.py`)
- Fuente 1: Google Search Console API
- Fuente 2: Google Suggest público
- Fuente 3: Google Trends (pytrends)
- Fuente 4: SerpApi Autocomplete — keywords reales de Google MX
- Fuente 5/6: SerpApi Related Searches + People Also Ask
- Fuente 7: Claude API — gaps, clusters, ángulos estratégicos
- Output: `keywords.txt`, `keywords_blog.txt`, `analisis_claude.json` 

**Bot Telegram Ambassador** (`bot_goodman.py` v2)
- Comandos: /estado, /alertas, /keywords, /siguiente, /pendientes, /generadas, /agregar
- Botones: ✅ Landing, 📝 Blog, ✏️ Editar, ❌ Rechazar, ⏭️ Siguiente
- Monitor automático de indexación cada 24h
- Resumen diario a las 9am
- Fix Python 3.14: asyncio.set_event_loop(asyncio.new_event_loop())
- Token: variable de entorno TELEGRAM_TOKEN

**Analizador de indexación** (`gsc_indexacion.py`)
- Lee CSVs exportados de GSC sin necesidad de API
- Genera alertas y recomendaciones automáticas
- Output: `reporte_indexacion.json` 

**26 landing pages generadas y desplegadas**
- Todas en `src/pages/Empresas*.tsx` 
- Rutas registradas en `App.tsx` 
- Commit y push a GitHub: hash `69747aa` 

### Errores corregidos en generar_landing.py

**Error 1 — Placeholder inválido `{% for each stat %}`**
- Afectó 7 archivos tsx
- Fix: reemplazar con array + `.map()` 
- Prevenido en prompt de Claude con reglas explícitas

**Error 2 — Constante SLATE5 no definida**
- Fix: declarar todas las constantes al inicio
- Constantes obligatorias agregadas al prompt:
```
  const DARK   = '#0F172A';
  const CARD   = '#1e293b';
  const BLUE   = '#2463eb';
  const YELLOW = '#FACC15';
  const GREEN  = '#4ade80';
  const SLATE5 = '#64748b';
  const SLATE3 = '#cbd5e1';
  const SLATE4 = '#94a3b8';
```

**Error 3 — CSS clip-path cortando títulos**
- Fix: reducir de 10% a 5% en `.cnp-diagonal-top` 
- Archivo: `src/index.css` línea 299

**Error 4 — UnicodeEncodeError en Windows**
- Fix permanente:
```powershell
  [System.Environment]::SetEnvironmentVariable("PYTHONIOENCODING", "utf-8", "User")
```

### Configuraciones completadas

- `gsc_credentials.json` configurado en goodman_generator
- Google Search Console API habilitada en Google Cloud
- Sitemap enviado a GSC con 26+ URLs
- 15 páginas con noindex eliminado y desbloqueadas para Google

### Pendientes próxima sesión

- [ ] Crear `actualizar_sitemap.py` — actualización automática tras cada generación
- [ ] Agregar seeds de Claude/Anthropic al detector de keywords:
```python
  "claude ia empresas",
  "claude anthropic méxico",
  "claude code automatización",
  "claude vs chatgpt empresas",
  "implementar claude empresa",
  "claude api monterrey",
  "anthropic claude español",
  "claude para manufactura",
```
- [ ] Generar landing pages específicas de Claude:
  - `claude-para-empresas-mexico` 
  - `claude-code-monterrey` 
  - `implementar-claude-en-mi-empresa` 
- [ ] Verificar en GSC en 48h cuántas páginas nuevas se indexaron
- [ ] Integrar `actualizar_sitemap.py` en `generar_lote.py` 

### Comandos clave para arrancar la próxima sesión
```powershell
# Iniciar bot
cd C:\Users\Dell\Documents\goodman_generator
$env:TELEGRAM_TOKEN = "8743817840:AAG4o964NuLUxFgbLn_aYfYbWbEQfMXa08s"
$env:SERPAPI_KEY = "4b12977c0516981972e98be6d02f960068883a24a6cd05de84026ae3a4671930"
$env:ANTHROPIC_API_KEY = "sk-ant-api03-..."
python bot_goodman.py

# Detectar keywords nuevas
python detectar_keywords_ambassador.py --auto --top 15 --csv

# Ver estado de indexación
python gsc_indexacion.py
```

### Estado del sitio al cierre de sesión
- Páginas indexadas: 8 (36.4%)
- Páginas sin indexar: 14
- Tendencia: 📉 bajando (esperamos mejora en 7 días)
- Impresiones 7 días: 74
- Sitemap enviado: ✅ confirmado por Google

---

## Estado al 04/04/2026 13:40 — LEER ANTES DE CUALQUIER SESIÓN

### Qué funciona HOY

| Sistema | Estado | Comando para iniciar |
|---------|--------|---------------------|
| Bot Telegram | ✅ | `python bot_goodman.py` |
| Generador de landings | ✅ | `python generar_landing.py "keyword"` |
| Detector de keywords | ✅ | `python detectar_keywords_ambassador.py --auto --top 15 --csv` |
| Analizador GSC | ✅ | `python gsc_indexacion.py` |
| Sitio web React | ✅ | `npm run dev` en Godman_Webpage |

### Variables de entorno SIEMPRE necesarias
```powershell
$env:TELEGRAM_TOKEN = "8743817840:AAG4o964NuLUxFgbLn_aYfYbWbEQfMXa08s"
$env:SERPAPI_KEY = "4b12977c0516981972e98be6d02f960068883a24a6cd05de84026ae3a4671930"
$env:ANTHROPIC_API_KEY = "sk-ant-api03-..."
$env:PYTHONIOENCODING = "utf-8"
```

### Rutas críticas
```
Generador:  C:\Users\Dell\Documents\goodman_generator\
Proyecto React: C:\Users\Dell\CascadeProjects\Godman_Webpage\Godman_Webpage\
Landings en: src\pages\Empresas*.tsx
Bot: bot_goodman.py
Detector: detectar_keywords_ambassador.py
```

### Lo que se construyó esta sesión completa

1. **SEO Ambassador v3** — 7 fuentes de keywords reales
   - GSC API + Google Suggest + Trends + SerpApi Autocomplete + Related + PAA + Claude API
   
2. **Bot Telegram** — control desde celular
   - /keywords → detecta y carga keywords
   - /siguiente → aprobar una por una
   - /estado → ver indexación
   - /alertas → problemas GSC

3. **41 landings generadas** en src/pages/Empresas*.tsx

4. **Errores corregidos en generar_landing.py**
   - Sin más `{% for each stat %}` — usa `.map()` 
   - Constantes de color siempre declaradas
   - UTF-8 encoding forzado

5. **15 páginas con noindex eliminado** — desbloqueadas para Google

6. **Sitemap enviado a GSC** — Google notificado

7. **GSC API configurada**
   - Credenciales: `gsc_credentials.json` 
   - Token guardado: `gsc_token.json` 
   - Usuario autorizado: `info@goodmantech.com.mx` 

### Problemas conocidos y sus fixes

| Problema | Fix |
|---------|-----|
| UnicodeEncodeError emojis | `$env:PYTHONIOENCODING = "utf-8"` |
| Bot pierde keywords al reiniciar | Usar `/keywords` en Telegram para recargar |
| `{% for each stat %}` en tsx | Windsurf: buscar en Empresas*.tsx y reemplazar |
| Bot asyncio Python 3.14 | Ya corregido con `asyncio.set_event_loop()` |

### Próxima sesión — hacer esto primero
```powershell
# 1. Ir a la carpeta
cd C:\Users\Dell\Documents\goodman_generator

# 2. Variables de entorno
$env:PYTHONIOENCODING = "utf-8"
$env:TELEGRAM_TOKEN = "8743817840:AAG4o964NuLUxFgbLn_aYfYbWbEQfMXa08s"
$env:SERPAPI_KEY = "4b12977c0516981972e98be6d02f960068883a24a6cd05de84026ae3a4671930"
$env:ANTHROPIC_API_KEY = "sk-ant-api03-..."

# 3. Iniciar bot
python bot_goodman.py
```

### Pendientes prioritarios próxima sesión

- [ ] Crear `actualizar_sitemap.py` automático
- [ ] Agregar keywords de Claude/Anthropic al detector
- [ ] Generar landings: `claude-para-empresas-mexico`, `claude-code-monterrey` 
- [ ] Verificar en GSC cuántas páginas nuevas se indexaron
- [ ] Corregir archivos tsx que aún tengan `{% for each stat %}` 
- [ ] Integrar sitemap en `generar_lote.py`
