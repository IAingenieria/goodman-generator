# 🤖 Goodman Tech — Generador Automático de Landing Pages SEO
## README de contexto para Claude

> **Propósito de este archivo:** Dar contexto completo al asistente en conversaciones nuevas.
> Comparte este archivo al inicio de cada sesión.

---

## ¿Qué es este proyecto?

Sistema para generar landing pages SEO y artículos de blog de forma automática para **Goodman Tech**, empresa de consultoría de IA con sede en Monterrey, NL. El objetivo es posicionar decenas de keywords sobre IA empresarial en México sin trabajo manual.

**Stack:**
- Backend: Python 3.12+
- Frontend: React + Vite + TypeScript (.tsx)
- IA: Claude API (modelo claude-sonnet-4-6)
- Proyecto React en: C:\Users\Dell\CascadeProjects\Godman_Webpage\Godman_Webpage
- Generador en: C:\Users\Dell\Documents\goodman_generator
- IDE: Windsurf (Cascade)
- OS: Windows 11

---

## Repositorios GitHub

- Sitio web: https://github.com/IAingenieria/Godman_Webpage
- Generador: https://github.com/IAingenieria/goodman-generator

---

## ⚠️ REGLAS CRÍTICAS DE SEGURIDAD — LEER OBLIGATORIO

### 🔒 PROHIBIDO HACER PUSH SIN VERIFICAR API KEYS

**ES INADMISIBLE EXPONER API KEYS EN EL CÓDIGO FUENTE**

Antes de CUALQUIER `git push`, SIEMPRE verificar:

```powershell
# Buscar API keys hardcodeadas en el código
Select-String -Path "*.py" -Pattern "sk-proj-|sk-ant-|SERPAPI_KEY.*=.*\"[a-f0-9]{40}|ANTHROPIC.*=.*\"sk-"
```

**NUNCA hacer:**
```python
# ❌ PROHIBIDO - API key hardcodeada
SERPAPI_KEY = os.environ.get("SERPAPI_KEY", "4b12977c0516981972...")
ANTHROPIC_KEY = os.environ.get("ANTHROPIC_API_KEY", "sk-ant-api03-...")
```

**SIEMPRE hacer:**
```python
# ✅ CORRECTO - Solo variables de entorno
SERPAPI_KEY = os.environ.get("SERPAPI_KEY")
ANTHROPIC_KEY = os.environ.get("ANTHROPIC_API_KEY")

if not SERPAPI_KEY:
    raise ValueError("SERPAPI_KEY no configurada en variables de entorno")
```

**Archivos que NUNCA deben subirse a Git:**
- `.env`
- `*_credentials.json`
- `*_token.json`
- Cualquier archivo con API keys

**Si se expone una API key:**
1. Rotar INMEDIATAMENTE la key en el servicio
2. Eliminar del código
3. Hacer commit de corrección
4. Verificar historial de Git (puede requerir git filter-branch)

---

## Estado al 05/04/2026 — LEER ANTES DE CUALQUIER SESIÓN

### Qué funciona HOY

| Sistema | Estado | Comando |
|---------|--------|---------|
| Bot Telegram | ✅ | python bot_goodman.py |
| Generador landings | ✅ **+GEO** | python generar_landing.py "keyword" |
| Generador blog | ✅ **NUEVO** | python generar_blog.py "¿cuánto cuesta implementar ia?" |
| Detector keywords | ✅ | python detectar_keywords_ambassador.py --auto --top 15 --csv |
| Analizador GSC | ✅ | python gsc_indexacion.py |
| Actualizador sitemap | ✅ | python actualizar_sitemap.py --ping |
| SEO Pipeline scorer | ✅ | python ../CLAUDE\ AGENTES\ DE\ SEO/seo_pipeline.py |
| SEO Pipeline + Claude | ✅ | python ../CLAUDE\ AGENTES\ DE\ SEO/seo_pipeline.py --advise |
| Sitio React | ✅ | npm run dev en Godman_Webpage |

### ⚠️ ADVERTENCIA: actualizar_sitemap.py SOBREESCRIBE sitemap.xml
`actualizar_sitemap.py` regenera el sitemap completo desde App.tsx — pierde prioridades manuales.
**Fix pendiente:** integrar las prioridades del dict PRIORIDADES con las entradas existentes.

### Variables de entorno SIEMPRE necesarias
```powershell
$env:TELEGRAM_TOKEN = "TU_TOKEN_AQUI"  # Obtener de @BotFather
$env:SERPAPI_KEY = "TU_KEY_AQUI"      # Obtener de serpapi.com
$env:ANTHROPIC_API_KEY = "TU_KEY_AQUI" # Obtener de console.anthropic.com
$env:OPENAI_API_KEY = "TU_KEY_AQUI"    # Para generar_blog_openai_v2.py
$env:PYTHONIOENCODING = "utf-8"
```

**⚠️ NUNCA hardcodear estas keys en el código**

### Arranque rápido próxima sesión
```powershell
cd C:\Users\Dell\Documents\goodman_generator
$env:PYTHONIOENCODING = "utf-8"
# Configurar API keys desde variables de entorno seguras
$env:TELEGRAM_TOKEN = "TU_TOKEN"
$env:SERPAPI_KEY = "TU_KEY"
$env:ANTHROPIC_API_KEY = "TU_KEY"
$env:OPENAI_API_KEY = "TU_KEY"
python bot_goodman.py
```

---

## Archivos del sistema

### generar_landing.py ✅ FUNCIONANDO
Motor principal. Recibe keyword y genera landing page completa.
```bash
python generar_landing.py "Como aplicar la IA en mi empresa"
```

**REGLAS CRÍTICAS en el prompt de Claude (línea ~126):**
- NUNCA usar {% %} — usar .map() para listas
- SIEMPRE declarar constantes: DARK, CARD, BLUE, YELLOW, GREEN, SLATE5, SLATE3, SLATE4
- NUNCA clip-path mayor al 5%
- Todo TSX debe compilar en Vite + React + TypeScript

**Validación anti-placeholder (línea ~695):**
```python
if "{%" in tsx_content or "%}" in tsx_content:
    print("⚠️ Claude generó sintaxis inválida. Abortando.")
    return False
```

**Contexto de marca Claude/Anthropic agregado:**
- Goodman Tech = único partner Claude en noreste de México
- Mencionar Claude, Claude Code, Anthropic naturalmente
- NUNCA mencionar ChatGPT/Gemini positivamente

---

### detectar_keywords_ambassador.py ✅ FUNCIONANDO (v3)

7 fuentes de keywords reales:
1. Google Search Console API (gsc_credentials.json + gsc_token.json)
2. Google Suggest público
3. Google Trends (pytrends)
4. SerpApi Autocomplete — keywords reales Google MX
5. SerpApi Related Searches
6. SerpApi People Also Ask
7. Claude API — gaps, clusters, ángulos estratégicos
```bash
python detectar_keywords_ambassador.py --auto --top 15 --csv
python detectar_keywords_ambassador.py --solo-serpapi  # sin GSC
```

**Seeds de Claude/Anthropic para agregar (PENDIENTE):**
```python
"claude ia empresas",
"claude anthropic méxico",
"claude code automatización",
"claude vs chatgpt empresas",
"implementar claude empresa",
"claude api monterrey",
```

---

### bot_goodman.py ✅ FUNCIONANDO (v2)

Bot Telegram con control SEO desde celular.

**Token:** variable de entorno TELEGRAM_TOKEN

**Comandos:**
- /start — menú principal
- /estado — indexación del sitio
- /alertas — problemas críticos GSC
- /keywords — detectar y cargar keywords
- /siguiente — aprobar/rechazar keywords
- /pendientes — lista en cola
- /generadas — páginas creadas
- /agregar — keyword manual

**Botones inline:** ✅ Landing | 📝 Blog | ✏️ Editar | ❌ Rechazar | ⏭️ Siguiente

**Fix Python 3.14 aplicado:**
```python
asyncio.set_event_loop(asyncio.new_event_loop())
```

**IMPORTANTE:** Las keywords se pierden al reiniciar el bot. Usar /keywords para recargar desde keywords.txt.

---

### gsc_indexacion.py ✅ FUNCIONANDO

Lee CSVs exportados de GSC y genera reporte con alertas.
```bash
python gsc_indexacion.py          # usa CSVs locales
python gsc_indexacion.py --api    # usa GSC API
```

**GSC API configurada:**
- Credenciales: gsc_credentials.json (NO en git)
- Token: gsc_token.json (NO en git)
- Usuario autorizado: info@goodmantech.com.mx
- Sitio: https://www.goodmantech.com.mx

---

### actualizar_sitemap.py ✅ NUEVO

Actualiza sitemap.xml automáticamente leyendo App.tsx.
```bash
python actualizar_sitemap.py           # solo actualizar
python actualizar_sitemap.py --ping    # actualizar + notificar Google
```

Integrado en generar_lote.py — se ejecuta automáticamente al terminar.

---

### generar_lote.py ✅ FUNCIONANDO
```bash
python generar_lote.py --limite 5
python generar_lote.py --blog --limite 3
python generar_lote.py --auto-detectar --limite 5
```

Al terminar: actualiza sitemap y notifica Google automáticamente.

---

## Estado del sitio goodmantech.com.mx

| Métrica | Valor al 04/04/2026 |
|---------|---------------------|
| Páginas indexadas | 8 (36.4%) |
| Páginas sin indexar | 14 |
| Tendencia | 📉 bajando |
| Impresiones 7 días | 74 |
| Sitemap enviado GSC | ✅ |
| noindex eliminado | ✅ 15 páginas |
| Landings generadas | ~41 en src/pages/Empresas*.tsx |

---

## Problemas conocidos y fixes

| Problema | Fix |
|----------|-----|
| UnicodeEncodeError emojis | $env:PYTHONIOENCODING = "utf-8" |
| Bot pierde keywords al reiniciar | /keywords en Telegram |
| {% for each stat %} en tsx | PowerShell: Select-String para buscar, luego fix manual |
| Bot asyncio Python 3.14 | Ya corregido |
| Git push bloqueado por secrets | Usar .gitignore — nunca commitear gsc_credentials.json ni gsc_token.json |

---

## Fix de emergencia para {% for each stat %} en tsx

Si aparece el error en Vite, ejecutar en PowerShell:
```powershell
# Verificar cuáles archivos tienen el problema
Select-String -Path "C:\Users\Dell\CascadeProjects\Godman_Webpage\Godman_Webpage\src\pages\Empresas*.tsx" -Pattern "\{%" | Select-Object Filename, LineNumber

# Ver líneas exactas del archivo afectado
$lines = Get-Content "RUTA_DEL_ARCHIVO" -Encoding UTF8
$lines[244..275] | ForEach-Object -Begin {$i=245} -Process { "$i: $_"; $i++ }

# Luego pedir a Windsurf que corrija ese archivo específico
```

**NUNCA usar PowerShell regex para reemplazar bloques JSX complejos** — deja código duplicado. Usar Windsurf archivo por archivo.

---

## Sesión 05/04/2026 — Cambios aplicados

### generar_landing.py — ACTUALIZADO
- ✅ **Bug corregido:** eliminado `{% for each stat %}` del template TSX (rompía Vite)
- ✅ **Sección GEO agregada:** entre FAQ y CTA en cada landing generada
  - Claude genera 3 campos nuevos en el mismo JSON: `geo_terminos`, `geo_definiciones`, `geo_enlaces_*`
  - Python ensambla cajas de definición con `id="def-{slug}"` (RAG-citable, apunta Speakable Schema)
  - Costo adicional: ~150 tokens por landing (mínimo overhead)
- ✅ **OG, Twitter Cards, geo.region ya estaban** — no se tocaron

### Agente 05 GEO — COMPLETADO en Godman_Webpage
- ✅ robots.txt: 14 crawlers IA + sitemap URL corregida a www
- ✅ llms.txt: actualizado con 26+ páginas + guía fan-out
- ✅ llms-full.txt: creado con 12 definiciones RAG-citables
- ✅ Artículo fan-out: `/empresas/guia-automatizacion-ia-pymes` (2,500+ palabras, 8 secciones)
- ✅ Citability Score promedio: 71.8/100 (21/27 páginas publicables)
- ⚠️ 6 páginas en rojo (score 33-49): EmpresasFinanzas, Operaciones, Ventas, Dirección, RRHH, TI

### seo_pipeline.py — NUEVO en CLAUDE AGENTES DE SEO/
Orquestador Python que:
1. Escanea Empresas*.tsx (Python puro, 0 tokens)
2. Calcula Citability Score 0-100 (Python puro, 0 tokens)
3. Llama a Claude UNA vez en batch para páginas < 70pts (--advise)
4. Inyecta FAQs mejoradas directo al TSX
5. Genera reporte JSON

```powershell
python seo_pipeline.py              # Solo scan + score
python seo_pipeline.py --advise     # + Claude mejora páginas < 70pts
python seo_pipeline.py --page EmpresasDireccion.tsx --advise  # 1 página
```

Requiere: `ANTHROPIC_API_KEY` en Godman_Webpage/.env

## Sesión 05/04/2026 (tarde) — Cambios adicionales

### generar_blog.py — NUEVO
- ✅ **Creado** como generador dedicado para artículos de blog
- URL: `/blog/{slug}` (no `/empresas/`)
- Componente: `Blog{PascalCase}` (no `Empresas{PascalCase}`)
- Schema: `BlogPosting` + `FAQPage` JSON-LD (no `ProfessionalService`)
- Prompt Claude: informacional — responde preguntas directamente (intención del usuario)
- Secciones: Breadcrumb → Answer-first → 3 H2 → Tips → GEO → FAQ → CTA suave
- Misma sección GEO (cajas RAG-citables con `id="def-{slug}"`)
- Uso: `python generar_blog.py "cuánto cuesta implementar ia en una empresa"`

### bot_goodman.py — FIX CRÍTICO
- ✅ **Bug corregido:** `generar_landing_sync()` ahora llama `generar_blog.py` cuando `tipo="blog"`
- Antes: `subprocess.run(["python", str(script), keyword])` — `tipo` nunca llegaba al script
- Ahora: elige el script correcto según tipo y lo llama correctamente
- Botón `📝 Blog` del Telegram ahora sí genera artículos de blog

---

## Sesión 05/04/2026 (noche) — SISTEMA DE BLOGS COMPLETO

### 🎉 SISTEMA DE BLOGS IMPLEMENTADO CON OPENAI GPT-4

**15 blogs generados automáticamente vinculando todas las landing pages**

#### generar_blog_openai_v2.py — NUEVO ✅
- ✅ **Creado** como generador de blogs usando OpenAI GPT-4
- ✅ **Genera contenido en formato JSON estructurado** (no Markdown)
- ✅ **Usa componentes React existentes:** `BlogLayout` + `BlogCTA`
- ✅ **JSX 100% válido garantizado** (sin errores de sintaxis)
- ✅ **Costo:** ~$0.10 USD por blog (2000-3000 palabras)
- ✅ **Tiempo:** 30-60 segundos por blog

**Uso:**
```powershell
$env:OPENAI_API_KEY = "sk-proj-..."
python generar_blog_openai_v2.py "Título del blog" ia-empresas
```

**Output:**
- `output_blogs/{slug}/Blog{ComponentName}.tsx` - Componente React
- `output_blogs/{slug}/contenido.json` - JSON original de OpenAI

#### Componentes de Blog Creados — NUEVO ✅

**8 componentes reutilizables en `src/components/blog/`:**

1. **BlogCard.tsx** - Tarjeta de preview de artículo
2. **BlogLayout.tsx** - Layout completo con breadcrumbs, TOC, sidebars
3. **BlogHero.tsx** - Hero section con categoría y metadata
4. **BlogTableOfContents.tsx** - Tabla de contenidos sticky
5. **BlogRelated.tsx** - Artículos relacionados en sidebar
6. **BlogCTA.tsx** - CTAs intermedios y finales
7. **BlogTags.tsx** - Tags SEO del artículo
8. **BlogShare.tsx** - Botones de compartir en redes

**Exportados desde:** `src/components/blog/index.ts`

#### 15 Blogs Generados — COMPLETADO ✅

**Todos los blogs vinculan estratégicamente a las landing pages de /empresas/**

1. ✅ Inteligencia Artificial para Empresas de Servicios
2. ✅ 5 Formas de Usar IA en tu Empresa de Servicios
3. ✅ Guía Completa: Cómo Implementar IA en tu Empresa en 2026
4. ✅ IA en Operaciones: Casos Reales de Reducción de Costos en México
5. ✅ Transformación Digital en RRHH: De la Contratación a la Retención con IA
6. ✅ IA en Ventas: Cómo Aumentar tu Pipeline en 90 Días
7. ✅ El Rol del CTO: Implementar IA sin Cambiar tu Stack Tecnológico
8. ✅ ROI de IA: Cómo Medir Resultados en Operaciones y Ventas
9. ✅ Servicios de IA vs Software de IA: Qué Necesita tu Empresa
10. ✅ IA para PyMEs en México: Por Dónde Empezar en 2026
11. ✅ Claude AI para Empresas en México: Guía Completa 2026
12. ✅ IA en Manufactura: Casos de Éxito en Monterrey
13. ✅ Comparativa: Las Mejores IA para Empresas Mexicanas en 2026
14. ✅ IA en Marketing Digital: De la Teoría a Resultados en 90 Días
15. ✅ Inteligencia de Manufactura: Transformando la Industria 4.0 en México

**URLs:**
```
https://www.goodmantech.com.mx/blog (índice con grid de 15 artículos)
https://www.goodmantech.com.mx/blog/ia-empresas/{slug}
```

#### BlogIndex.tsx — Página Índice ✅
- ✅ **Creada** en `src/pages/BlogIndex.tsx`
- ✅ **Grid responsive** con 15 BlogCards
- ✅ **Hero section** con descripción del blog
- ✅ **CTA final** para diagnóstico gratuito
- ✅ **Ruta registrada:** `/blog`

#### Sitemap XML — SEO ✅
- ✅ **Creado** `public/sitemap-blogs.xml` con 15 URLs
- ✅ **Desplegado** en producción
- ✅ **URL:** `https://www.goodmantech.com.mx/sitemap-blogs.xml`
- ✅ **Listo** para Google Search Console

#### Estrategia de Vinculación — IMPLEMENTADA ✅

**Cada blog vincula a landing pages relevantes:**
- `/empresas/inteligencia-artificial-en-las-empresas-pdf`
- `/empresas/inteligencia-artificial-para-empresas-de-servicios`
- `/empresas/operaciones`
- `/empresas/reducir-costos-operativos-con-ia`
- `/empresas/rrhh`
- `/empresas/servicios-de-ia-para-empresas`
- `/empresas/software-de-inteligencia-artificial-para-empresas`
- `/empresas/ti`
- `/empresas/ventas`
- `/empresas/agencia-de-ia-mexico`
- `/empresas/claude-para-empresas-mexico`
- `/empresas/como-se-utiliza-la-ia-en-la-manufactura`
- `/empresas/cual-es-la-mejor-ia-para-empresas`
- `/empresas/ia-en-marketing-digital-blog`
- `/empresas/que-es-la-inteligencia-de-manufactura`

#### Correcciones de Seguridad — CRÍTICO ✅

**⚠️ PROBLEMA DETECTADO Y CORREGIDO:**
- ❌ **API keys expuestas** en `detectar_keywords_ambassador.py`
- ✅ **Corregido:** Eliminadas API keys hardcodeadas del código
- ✅ **Ahora usa solo variables de entorno** sin valores por defecto
- ✅ **Commit de seguridad** subido a GitHub

**Archivos corregidos:**
- `detectar_keywords_ambassador.py` - Eliminado SerpAPI key hardcodeada

**LECCIÓN APRENDIDA:**
- **NUNCA** hacer push sin verificar API keys en el código
- **SIEMPRE** usar `os.environ.get()` sin valores por defecto
- **VERIFICAR** con grep antes de cada commit

#### Estado del Deployment — PRODUCCIÓN ✅
- ✅ **Build exitoso** en Vercel
- ✅ **15 blogs desplegados** y funcionando
- ✅ **Página índice** en `/blog` activa
- ✅ **Sitemap XML** disponible
- ✅ **Sin errores de sintaxis** en ningún archivo

**Métricas del sistema de blogs:**
- **Total de blogs:** 15
- **Palabras totales:** ~30,000+
- **Inversión OpenAI:** ~$1.50 USD
- **Tiempo total:** ~15 minutos
- **Componentes creados:** 8
- **Rutas registradas:** 16 (15 blogs + 1 índice)

---

## Pendientes próxima sesión

- [x] **CRÍTICO:** Rotar API keys expuestas en Git:
  - SerpAPI key: ✅ ROTADA el 05/04/2026
  - Nueva key configurada en variables de entorno
  - Ver: CONFIGURAR_API_KEYS.md para instrucciones
- [ ] **ALTA PRIORIDAD:** Agregar 15 URLs de blogs a Google Search Console:
  - Usar sitemap: `https://www.goodmantech.com.mx/sitemap-blogs.xml`
  - O inspección manual de cada URL
- [ ] Agregar seeds Claude/Anthropic al detector de keywords:
  ```python
  "claude ia empresas", "claude anthropic méxico", "claude code automatización",
  "claude vs chatgpt empresas", "implementar claude empresa", "claude api monterrey"
  ```
- [ ] Generar landings: claude-para-empresas-mexico, claude-code-monterrey, implementar-claude-en-mi-empresa
- [ ] Mejorar páginas departamento (score 33-49): Dirección, RRHH, TI, Ventas, Operaciones, Finanzas
  → Opción A: manual (editar TSX)  Opción B: `python seo_pipeline.py --advise` con ANTHROPIC_API_KEY
- [ ] Fix actualizar_sitemap.py: preservar prioridades manuales al regenerar
- [ ] Verificar en GSC cuántas páginas nuevas se indexaron (revisar 48h después)
- [ ] Generar más blogs con generar_blog_openai_v2.py según keywords detectadas
- [ ] Crear sistema de blogs relacionados automático (actualmente muestra placeholder)

---

## Marca Goodman Tech
```python
BRAND = {
    "nombre":    "Goodman Tech",
    "ciudad":    "Monterrey, Nuevo León",
    "dominio":   "https://www.goodmantech.com.mx",
    "whatsapp":  "528126350902",
    "email":     "info@goodmantech.com.mx",
    "telefono":  "+52 81 2635 0902",
    "contacto":  "Zenon Vilchis",
    "propuesta": "Implementamos IA en tu empresa con resultados medibles en 90 días",
    "diferenciador": "Único partner especializado en Claude de Anthropic en el noreste de México",
}
```

**Colores:**
```
Dark bg:  #0F172A   Card: #1e293b   Card2: #162032
Blue:     #2463eb   Yellow: #FACC15  Green: #4ade80
Slate3:   #cbd5e1   Slate4: #94a3b8  Slate5: #64748b
```

**Fuentes:** Plus Jakarta Sans (títulos) + Inter (cuerpo)
