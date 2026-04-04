# 🚀 Goodman Tech — Generador Automático de Landing Pages SEO

## El problema que resuelve

Antes: generar 1 landing page = 1 sesión de Claude Desktop + miles de tokens + 2 horas de trabajo manual.

Ahora: generar 20 landing pages = `python generar_lote.py` + ~20,000 tokens (Haiku) + 5 minutos.

---

## Arquitectura del sistema

```
detectar_tendencias.py   →  Encuentra keywords trending en México
        ↓
keywords.txt             →  Lista de keywords a generar
        ↓
generar_lote.py          →  Procesa todas en paralelo
        ↓
generar_landing.py       →  Por cada keyword genera:
        ↓
┌─────────────────────────────────────────────────────┐
│  PYTHON (0 tokens):                                  │
│  • Schema JSON-LD completo (WebPage + FAQ + Local)   │
│  • Open Graph + Twitter Cards + Geo meta tags        │
│  • BreadcrumbList Schema                             │
│  • Estructura TSX completa con colores Goodman Tech  │
│  • Registros para App.tsx, Header.tsx, sitemap.xml   │
│  • Entrada para llms.txt                             │
│                                                      │
│  CLAUDE API HAIKU (~1,000 tokens):                   │
│  • Meta title y meta description                     │
│  • H1, subtítulo, párrafos hero                      │
│  • Answer-First paragraphs para cada H2              │
│  • 5 FAQs con respuestas SEO-ready                   │
│  • Beneficios y pasos del proceso                    │
└─────────────────────────────────────────────────────┘
        ↓
output/[keyword-slug]/
  ├── EmpresasNombreComponente.tsx  ← Copiar a src/pages/
  └── REGISTROS.md                  ← Instrucciones de integración
```

---

## Instalación

```bash
pip install anthropic pytrends
export ANTHROPIC_API_KEY="tu-api-key-aqui"
```

---

## Uso

### Opción 1 — Una sola landing page

```bash
python generar_landing.py "Como aplicar la IA en mi empresa"
python generar_landing.py "automatizacion de ventas con inteligencia artificial"
python generar_landing.py "reducir costos operativos con IA en manufactura"
```

**Output:**
```
output/como-aplicar-la-ia-en-mi-empresa/
  ├── EmpresasComoAplicarLaIAEnMiEmpresa.tsx
  └── REGISTROS.md
```

### Opción 2 — Lote de keywords (20+ páginas de una vez)

1. Edita `keywords.txt` con una keyword por línea
2. Corre:
```bash
python generar_lote.py
```

### Opción 3 — Detección automática de tendencias

```bash
python detectar_tendencias.py
```

El script detecta qué keywords sobre IA empresarial están subiendo en México
y ofrece generarlas automáticamente.

**Flujo recomendado para cada lunes:**
```
python detectar_tendencias.py
→ Selecciona [1] para generar las trending
→ En 10 minutos tienes 20 nuevas landing pages listas
```

---

## Integración al proyecto React

Después de generar, para cada landing:

### 1. Copiar el .tsx
```bash
cp output/como-aplicar-la-ia-en-mi-empresa/EmpresasComoAplicarLaIAEnMiEmpresa.tsx \
   /ruta/a/tu/proyecto/src/pages/
```

### 2. Abrir REGISTROS.md y pegar en:
- `src/App.tsx` → importación + ruta
- `src/components/Header.tsx` → menú desktop + móvil
- `public/sitemap.xml` → entrada nueva

### 3. Build y deploy
```bash
npm run build
# o si usas Vite:
npm run preview
```

---

## Consumo de tokens estimado

| Acción | Tokens Claude | Costo estimado |
|--------|-------------|----------------|
| 1 landing page | ~1,000 (Haiku) | ~$0.001 USD |
| 20 landing pages | ~20,000 (Haiku) | ~$0.02 USD |
| 100 landing pages | ~100,000 (Haiku) | ~$0.10 USD |

**Comparado con el proceso anterior con Claude Desktop:**
- Antes: ~50,000 tokens por landing (lectura de agentes + ejecución + verificación)
- Ahora: ~1,000 tokens por landing (solo copy creativo)
- **Ahorro: 98% de tokens**

---

## Estructura de archivos generados

### EmpresasXxx.tsx incluye:
- ✅ Helmet con meta title, description, canonical
- ✅ Open Graph completo (title, description, url, image, locale, site_name)
- ✅ Twitter Cards
- ✅ Geo meta tags (geo.region, geo.placename, geo.position)
- ✅ Schema JSON-LD: WebPage + ProfessionalService + FAQPage + BreadcrumbList
- ✅ Hero con H1 + keyword + stat + CTAs
- ✅ Sección problema con Answer-First paragraph (citable por IA)
- ✅ Sección solución con beneficios y proceso
- ✅ FAQ con 5 preguntas + respuestas Answer-First
- ✅ CTA final con WhatsApp + datos de contacto
- ✅ Colores y fuentes de identidad Goodman Tech
- ✅ Material Symbols Outlined
- ✅ Plus Jakarta Sans + Inter

### REGISTROS.md incluye:
- ✅ Línea de importación para App.tsx
- ✅ Bloque `<Route>` para App.tsx
- ✅ `<DropdownMenuItem>` para Header.tsx desktop
- ✅ `<Link>` para Header.tsx mobile
- ✅ Entrada `<url>` para sitemap.xml
- ✅ Línea para llms.txt

---

## Personalización

Para ajustar el generador a otros clientes, edita `generar_landing.py`:

```python
BRAND = {
    "nombre":    "Nombre del Cliente",
    "ciudad":    "Ciudad, Estado",
    "dominio":   "https://www.clientedominio.com",
    "whatsapp":  "521234567890",
    "email":     "info@cliente.com",
    "telefono":  "+52 XX XXXX XXXX",
    "contacto":  "Nombre Contacto",
    "propuesta": "Propuesta única de valor del cliente",
    ...
}
```

El sistema es **agnóstico al cliente** — los colores y la propuesta de valor
se pueden parametrizar para generar landings para cualquier cliente.

---

## Próximas mejoras sugeridas

- [ ] Integración con Google Search Console API para detectar keywords emergentes propias
- [ ] Auto-deploy a Vercel via GitHub Actions al generar nuevas páginas
- [ ] Generación de imágenes OG automática con Pillow
- [ ] Monitoreo de posicionamiento mensual con GSC API
- [ ] Subida automática a Modal para ejecución programada cada lunes
