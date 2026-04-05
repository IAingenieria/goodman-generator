#!/usr/bin/env python3
"""
GOODMAN TECH — Generador Automático de Landing Pages SEO
=========================================================
Uso:  python generar_landing.py "Como aplicar la IA en mi empresa"
      python generar_landing.py "automatizacion de procesos con IA"

Genera sin consumir tokens:
  - src/pages/EmpresasXxx.tsx  (completo, listo para deploy)
  - registros para App.tsx y Header.tsx
  - entrada de sitemap.xml

Usa API de Claude SOLO para el copy creativo (H1, subtítulo, párrafos,
FAQ) — todo lo estructural (Schema, OG, meta tags, colores, código TSX)
se genera localmente en Python.
"""

import sys
import re
import json
import os
import textwrap
import unicodedata
from datetime import date
import anthropic   # pip install anthropic

# ── CONFIGURACIÓN DE MARCA ────────────────────────────────────────────────────
BRAND = {
    "nombre":    "Goodman Tech",
    "ciudad":    "Monterrey, Nuevo León",
    "dominio":   "https://www.goodmantech.com.mx",
    "whatsapp":  "528126350902",
    "email":     "info@goodmantech.com.mx",
    "telefono":  "+52 81 2635 0902",
    "contacto":  "Zenon Vilchis",
    "anio":      "2026",
    "cliente_ideal": "directores, gerentes y dueños de empresa en México",
    "propuesta": "Implementamos IA en tu empresa con resultados medibles en 90 días",
    "wa_base":   "https://wa.me/528126350902?text=",
}

# ── PALETA GOODMAN TECH ───────────────────────────────────────────────────────
COLORS = {
    "DARK":   "0F172A",
    "CARD":   "1e293b",
    "CARD2":  "162032",
    "BLUE":   "2463eb",
    "YELLOW": "FACC15",
    "GREEN":  "4ade80",
    "RED":    "f87171",
    "SLATE3": "cbd5e1",
    "SLATE4": "94a3b8",
    "SLATE5": "64748b",
}

# ── ESTADÍSTICAS SEO PREDEFINIDAS (sin consumir tokens) ──────────────────────
STATS = [
    ("El 75% de los usuarios nunca pasa de la primera página de Google",
     "Backlinko, 2025"),
    ("Las empresas que implementan IA reportan un aumento promedio del 40% en productividad",
     "McKinsey Global Institute, 2025"),
    ("El 68% de los negocios en México no tienen procesos automatizados con IA",
     "INEGI Encuesta Digital, 2025"),
    ("En promedio, una empresa de 50 empleados pierde 340 horas al mes en tareas repetitivas",
     "Goodman Tech, análisis interno 2026"),
    ("El ROI promedio de implementaciones de IA en PyMEs es del 280% en el primer año",
     "Deloitte AI Survey, 2025"),
]

FAQ_BASE = [
    "¿Cuánto tiempo tarda en verse resultados con IA en una empresa?",
    "¿Necesito cambiar mi ERP o sistema actual para implementar IA?",
    "¿Mis empleados necesitan saber programar para usar las soluciones de IA?",
    "¿Cuánto cuesta implementar IA en una empresa mediana en México?",
    "¿Cómo sé si la IA está funcionando en mi empresa?",
    "¿La IA puede integrarse con SAP, Oracle o cualquier ERP?",
    "¿Qué pasa si la IA comete errores en procesos críticos?",
]

# ─────────────────────────────────────────────────────────────────────────────
# UTILIDADES
# ─────────────────────────────────────────────────────────────────────────────

def slugify(text: str) -> str:
    """'Como aplicar la IA en mi empresa' → 'como-aplicar-la-ia-en-mi-empresa'"""
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    return text

def component_name(text: str) -> str:
    """'Como aplicar la IA en mi empresa' → 'EmpresasComoAplicarLaIAEnMiEmpresa'"""
    slug = slugify(text)
    parts = slug.split("-")
    pascal = "".join(p.capitalize() for p in parts)
    return f"Empresas{pascal}"

def url_path(text: str) -> str:
    """Retorna '/empresas/como-aplicar-la-ia-en-mi-empresa'"""
    return f"/empresas/{slugify(text)}"

def canonical(text: str) -> str:
    return f"{BRAND['dominio']}{url_path(text)}"

def wa_link(keyword: str) -> str:
    msg = f"Hola, quiero información sobre {keyword} para mi empresa"
    encoded = msg.replace(" ", "%20").replace(",", "%2C")
    return f"{BRAND['wa_base']}{encoded}"

# ─────────────────────────────────────────────────────────────────────────────
# PASO 1 — LLAMADA A CLAUDE API (SOLO COPY CREATIVO)
# ─────────────────────────────────────────────────────────────────────────────

def generar_copy_con_claude(keyword: str) -> dict:
    """
    Llama a Claude API con un prompt muy comprimido.
    Retorna un dict con SOLO el contenido creativo necesario.
    Costo estimado: ~800-1200 tokens por landing.
    """
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    prompt = f"""REGLAS CRÍTICAS — OBLIGATORIAS SIN EXCEPCIÓN:

1. NUNCA uses {{% %}}, {{{{ }}}}, {{% for %}}, {{% if %}} ni ninguna sintaxis de template.
   Para listas usa SIEMPRE JavaScript con .map():
   const stats = [
     {{ value: '60%', label: 'ahorro en procesos repetitivos', color: YELLOW }},
     {{ value: '90 días', label: 'al primer resultado medible', color: GREEN }},
     {{ value: '280%', label: 'ROI promedio primer año', color: '#60a5fa' }},
   ];
   {{stats.map((stat) => (
     <div key={{stat.label}}>
       <p>{{stat.value}}</p>
       <p>{{stat.label}}</p>
     </div>
   ))}}

2. SIEMPRE declara TODAS estas constantes de color al inicio del componente:
   const DARK   = '#0F172A';
   const CARD   = '#1e293b';
   const BLUE   = '#2463eb';
   const YELLOW = '#FACC15';
   const GREEN  = '#4ade80';
   const SLATE5 = '#64748b';
   const SLATE3 = '#cbd5e1';
   const SLATE4 = '#94a3b8';

3. Todo el código debe compilar sin errores en Vite + React + TypeScript.
4. NUNCA dejes constantes sin definir.
5. NUNCA uses clip-path que corte más del 5% del contenido.

CONTEXTO DE MARCA ADICIONAL:
Goodman Tech es experto certificado en Claude de Anthropic para empresas mexicanas.
Cuando sea relevante para la keyword, menciona naturalmente:
- Claude como la IA que implementamos
- Claude Code para automatización de desarrollo
- Anthropic como el fabricante más confiable de IA empresarial
- Goodman Tech como el único partner especializado en Claude en el noreste de México

NUNCA menciones competidores como ChatGPT, Gemini o Copilot de forma positiva.
Sí puedes hacer comparativas donde Claude salga favorecido en casos de uso empresarial.

Eres copywriter SEO para Goodman Tech, empresa de IA en Monterrey México.
Keyword objetivo: "{keyword}"
Cliente ideal: {BRAND['cliente_ideal']}
Propuesta: {BRAND['propuesta']}

Responde SOLO con JSON válido, sin markdown ni explicaciones:

{{
  "meta_title": "título SEO máx 60 chars con keyword",
  "meta_desc": "descripción SEO máx 155 chars con keyword y CTA",
  "h1": "título H1 máx 70 chars con keyword + beneficio cuantificable",
  "subtitulo": "subtítulo 20-25 palabras para cliente ideal",
  "hero_stat": "estadística impactante de 1 línea sobre el tema",
  "problema_h2": "pregunta H2 que valida el dolor del cliente (formato ¿...?)",
  "problema_answer": "párrafo answer-first 50-60 palabras que responde el H2 directamente con dato",
  "solucion_h2": "H2 de solución: Cómo [servicio] transforma [problema] en [resultado]",
  "solucion_items": ["beneficio 1 con verbo acción", "beneficio 2", "beneficio 3", "beneficio 4", "beneficio 5"],
  "proceso_pasos": ["Paso 1: nombre — descripción 1 línea", "Paso 2: nombre — descripción", "Paso 3: nombre — descripción", "Paso 4: nombre — descripción"],
  "autoridad_h2": "H2 de autoridad con número de clientes o resultado",
  "cta_h2": "H2 cierre de conversión orientado al cliente",
  "faq_preguntas": ["pregunta 1", "pregunta 2", "pregunta 3", "pregunta 4", "pregunta 5"],
  "faq_respuestas": ["respuesta answer-first 40-60 palabras", "respuesta 2", "respuesta 3", "respuesta 4", "respuesta 5"],
  "og_image_alt": "texto alt para imagen OG relacionado con keyword",
  "geo_terminos": ["Término clave 1 relacionado a la keyword", "Término clave 2", "Término clave 3"],
  "geo_definiciones": [
    "Definición directa de 40-60 palabras del término 1. Sin primera persona. Neutral y citable como fuente.",
    "Definición directa de 40-60 palabras del término 2. Autocontenida, sin contexto previo requerido.",
    "Definición directa de 40-60 palabras del término 3. Con dato clave que la contextualiza."
  ],
  "geo_enlaces_texto": ["texto del enlace 1", "texto del enlace 2", "texto del enlace 3"],
  "geo_enlaces_url": ["/empresas/ruta-1", "/empresas/ruta-2", "/contact"]
}}"""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = message.content[0].text.strip()
    # Limpiar posibles bloques markdown
    raw = re.sub(r"```json\s*", "", raw)
    raw = re.sub(r"```\s*", "", raw)

    return json.loads(raw)


# ─────────────────────────────────────────────────────────────────────────────
# PASO 2 — GENERAR SCHEMA JSON-LD (100% Python, cero tokens)
# ─────────────────────────────────────────────────────────────────────────────

def generar_schema(keyword: str, copy: dict) -> str:
    today = date.today().isoformat()
    can = canonical(keyword)
    faqs = []
    for q, a in zip(copy["faq_preguntas"], copy["faq_respuestas"]):
        faqs.append({"@type": "Question",
                     "name": q,
                     "acceptedAnswer": {"@type": "Answer", "text": a}})

    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebPage",
                "@id": can,
                "url": can,
                "name": copy["meta_title"],
                "description": copy["meta_desc"],
                "dateModified": today,
                "inLanguage": "es-MX",
                "breadcrumb": {
                    "@type": "BreadcrumbList",
                    "itemListElement": [
                        {"@type": "ListItem", "position": 1,
                         "name": "Inicio", "item": BRAND["dominio"]},
                        {"@type": "ListItem", "position": 2,
                         "name": "Empresas",
                         "item": f"{BRAND['dominio']}/empresas"},
                        {"@type": "ListItem", "position": 3,
                         "name": keyword, "item": can},
                    ]
                }
            },
            {
                "@type": "ProfessionalService",
                "name": BRAND["nombre"],
                "url": BRAND["dominio"],
                "telephone": BRAND["telefono"],
                "email": BRAND["email"],
                "address": {
                    "@type": "PostalAddress",
                    "addressLocality": "Monterrey",
                    "addressRegion": "Nuevo León",
                    "addressCountry": "MX"
                },
                "geo": {
                    "@type": "GeoCoordinates",
                    "latitude": "25.6866",
                    "longitude": "-100.3161"
                },
                "areaServed": "México",
                "sameAs": [
                    f"https://wa.me/{BRAND['whatsapp']}",
                ]
            },
            {
                "@type": "FAQPage",
                "mainEntity": faqs
            }
        ]
    }

    return json.dumps(schema, ensure_ascii=False, indent=2)


# ─────────────────────────────────────────────────────────────────────────────
# PASO 3 — GENERAR ARCHIVO .TSX COMPLETO (100% Python, cero tokens)
# ─────────────────────────────────────────────────────────────────────────────

def generar_tsx(keyword: str, copy: dict, schema_str: str) -> str:
    comp   = component_name(keyword)
    slug   = slugify(keyword)
    can    = canonical(keyword)
    wa     = wa_link(keyword)
    today  = date.today().strftime("%d/%m/%Y")
    stat1  = STATS[0]
    stat2  = STATS[2]

    # Serializar schema para embed en JSX
    schema_escaped = schema_str.replace("`", "\\`").replace("${", "\\${")

    # Generar items de beneficios
    beneficios_jsx = "\n".join(
        f'                <div key="{i}" style={{{{display:"flex",gap:"10px",alignItems:"flex-start",marginBottom:"10px"}}}}>'
        f'<span style={{{{color:"#{COLORS["GREEN"]}",marginTop:"2px",flexShrink:0}}}}>✓</span>'
        f'<span style={{{{fontSize:"14px",color:"#{COLORS["SLATE3"]}",lineHeight:"1.5"}}}}>{item}</span></div>'
        for i, item in enumerate(copy["solucion_items"])
    )

    # Generar pasos del proceso
    pasos_jsx = "\n".join(
        f'                <div key="{i}" style={{{{background:"#{COLORS["CARD2"]}",border:"1px solid #2463eb33",'
        f'borderRadius:"12px",padding:"1rem",marginBottom:"8px"}}}}>'
        f'<span style={{{{color:"#{COLORS["YELLOW"]}",fontWeight:700,fontSize:"13px"}}}}>{paso}</span></div>'
        for i, paso in enumerate(copy["proceso_pasos"])
    )

    # Generar cajas de definición GEO (RAG-citable assets)
    slug_base = slugify(keyword)
    geo_terminos    = copy.get("geo_terminos", [])
    geo_defs        = copy.get("geo_definiciones", [])
    geo_links_txt   = copy.get("geo_enlaces_texto", ["Agentes de IA", "Automatización con IA", "Diagnóstico Gratuito"])
    geo_links_url   = copy.get("geo_enlaces_url",   ["/agentes-ia", "/empresas/automatizacion-con-ia-para-empresas", "/contact"])

    geo_def_jsx = "\n".join(
        f'          <div id="def-{slugify(term)}" style={{{{background:"#{COLORS["CARD2"]}",border:"1px solid #2463eb44",'
        f'borderRadius:"12px",padding:"1.2rem 1.4rem",marginBottom:"1rem",'
        f'borderLeft:"4px solid #{COLORS["BLUE"]}"}}}}>\n'
        f'            <p style={{{{fontFamily:\'"Plus Jakarta Sans",sans-serif\',fontWeight:700,'
        f'fontSize:"14px",color:"#{COLORS["YELLOW"]}",marginBottom:"0.5rem"}}}}>¿Qué es {term}?</p>\n'
        f'            <p style={{{{fontSize:"14px",color:"#{COLORS["SLATE3"]}",lineHeight:1.65,margin:0}}}}>{defn}</p>\n'
        f'            <cite style={{{{fontSize:"11px",color:"#{COLORS["SLATE5"]}",marginTop:"0.5rem",display:"block"}}}}>'
        f'Fuente: Goodman Tech — goodmantech.com.mx</cite>\n'
        f'          </div>'
        for term, defn in zip(geo_terminos, geo_defs)
        if term and defn
    ) or f'          <div id="def-{slug_base}" style={{{{background:"#{COLORS["CARD2"]}",border:"1px solid #2463eb44",borderRadius:"12px",padding:"1.2rem 1.4rem",marginBottom:"1rem",borderLeft:"4px solid #{COLORS["BLUE"]}"}}}}><p style={{{{fontFamily:\'"Plus Jakarta Sans",sans-serif\',fontWeight:700,fontSize:"14px",color:"#{COLORS["YELLOW"]}",marginBottom:"0.5rem"}}}}>¿Qué es {keyword}?</p><p style={{{{fontSize:"14px",color:"#{COLORS["SLATE3"]}",lineHeight:1.65,margin:0}}}}>La automatización con IA para empresas utiliza algoritmos de inteligencia artificial para ejecutar tareas repetitivas o complejas sin intervención humana constante, reduciendo costos operativos hasta un 70% y eliminando errores manuales.</p><cite style={{{{fontSize:"11px",color:"#{COLORS["SLATE5"]}",marginTop:"0.5rem",display:"block"}}}}>Fuente: Goodman Tech — goodmantech.com.mx</cite></div>'

    geo_links_jsx = " ".join(
        f'<a href="{url}" style={{{{fontSize:"12px",color:"#60a5fa",textDecoration:"none",'
        f'background:"#2463eb11",border:"1px solid #2463eb33",'
        f'padding:"5px 12px",borderRadius:"100px"}}}}>{txt}</a>'
        for txt, url in zip(geo_links_txt, geo_links_url)
        if txt and url
    )

    # Generar FAQ items
    faq_jsx = "\n".join(
        f'              <div key="{i}" style={{{{background:"#{COLORS["CARD2"]}",border:"1px solid #ffffff0d",'
        f'borderRadius:"12px",padding:"1rem 1.1rem",marginBottom:"8px"}}}}>'
        f'<p style={{{{fontWeight:700,fontSize:"13px",color:"white",marginBottom:"5px"}}}}>{q}</p>'
        f'<p style={{{{fontSize:"13px",color:"#{COLORS["SLATE4"]}",lineHeight:"1.55",margin:0}}}}>{a}</p></div>'
        for i, (q, a) in enumerate(zip(copy["faq_preguntas"], copy["faq_respuestas"]))
    )

    tsx = f'''import {{ Helmet }} from 'react-helmet-async';

// ── Colores Goodman Tech ───────────────────────────────────────────────────
const DARK   = '#{COLORS["DARK"]}';
const CARD   = '#{COLORS["CARD"]}';
const CARD2  = '#{COLORS["CARD2"]}';
const BLUE   = '#{COLORS["BLUE"]}';
const YELLOW = '#{COLORS["YELLOW"]}';
const GREEN  = '#{COLORS["GREEN"]}';
const SLATE3 = '#{COLORS["SLATE3"]}';
const SLATE4 = '#{COLORS["SLATE4"]}';
const SLATE5 = '#{COLORS["SLATE5"]}';

const WA_LINK = '{wa}';
const SCHEMA  = `{schema_escaped}`;

const {comp} = () => {{
  return (
    <div style={{{{ fontFamily: '"Inter", sans-serif', backgroundColor: DARK, color: 'white', minHeight: '100vh' }}}}>
      <Helmet>
        <title>{copy["meta_title"]} | Goodman Tech</title>
        <meta name="description" content="{copy["meta_desc"]}" />
        <link rel="canonical" href="{can}" />

        {{/* Open Graph */}}
        <meta property="og:title" content="{copy["meta_title"]} | Goodman Tech" />
        <meta property="og:description" content="{copy["meta_desc"]}" />
        <meta property="og:url" content="{can}" />
        <meta property="og:type" content="website" />
        <meta property="og:locale" content="es_MX" />
        <meta property="og:site_name" content="Goodman Tech" />
        <meta property="og:image" content="{BRAND["dominio"]}/og/{slug}.jpg" />
        <meta property="og:image:alt" content="{copy["og_image_alt"]}" />

        {{/* Twitter Cards */}}
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:title" content="{copy["meta_title"]}" />
        <meta name="twitter:description" content="{copy["meta_desc"]}" />
        <meta name="twitter:image" content="{BRAND["dominio"]}/og/{slug}.jpg" />

        {{/* Geo */}}
        <meta name="geo.region" content="MX-NL" />
        <meta name="geo.placename" content="Monterrey, Nuevo León" />
        <meta name="geo.position" content="25.6866;-100.3161" />
        <meta name="ICBM" content="25.6866, -100.3161" />

        {{/* Fuentes */}}
        <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800;900&family=Inter:wght@400;500;600&display=swap" rel="stylesheet" />
        <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" rel="stylesheet" />

        {{/* Schema JSON-LD */}}
        <script type="application/ld+json">{{SCHEMA}}</script>
      </Helmet>

      {{/* ═══ HERO ═══ */}}
      <section style={{{{ padding: '5rem 1.5rem 4rem', background: DARK, position: 'relative', overflow: 'hidden' }}}}>
        {{/* Glows decorativos */}}
        <div style={{{{ position:'absolute', top:'-60px', right:'-40px', width:'380px', height:'380px',
          borderRadius:'50%', background:`radial-gradient(circle, #2463eb 0%, transparent 70%)`,
          opacity: 0.07, pointerEvents:'none' }}}} />
        <div style={{{{ position:'absolute', bottom:'-40px', left:'-20px', width:'280px', height:'280px',
          borderRadius:'50%', background:`radial-gradient(circle, #FACC15 0%, transparent 70%)`,
          opacity: 0.07, pointerEvents:'none' }}}} />

        <div style={{{{ maxWidth:'860px', margin:'0 auto', position:'relative' }}}}>
          {{/* Badge */}}
          <div style={{{{ display:'inline-flex', alignItems:'center', gap:'6px',
            background:'#2463eb22', border:'1px solid #2463eb44',
            color:'#60a5fa', fontSize:'11px', fontWeight:600, letterSpacing:'0.08em',
            textTransform:'uppercase', padding:'5px 14px', borderRadius:'100px',
            marginBottom:'1.2rem' }}}}>
            <span className="material-symbols-outlined" style={{{{ fontSize:'14px', fontVariationSettings:'"FILL" 1' }}}}>smart_toy</span>
            Goodman Tech · IA para Empresas · {today}
          </div>

          {{/* H1 */}}
          <h1 style={{{{ fontFamily:'"Plus Jakarta Sans", sans-serif', fontWeight:900,
            fontSize:'clamp(26px, 5vw, 44px)', lineHeight:1.15, marginBottom:'1rem',
            color:'white' }}}}>
            {copy["h1"]}
          </h1>

          {{/* Subtítulo */}}
          <p style={{{{ fontSize:'16px', color: SLATE4, lineHeight:1.65,
            maxWidth:'560px', marginBottom:'1.5rem' }}}}>
            {copy["subtitulo"]}
          </p>

          {{/* Stat hero */}}
          <div style={{{{ background: CARD2, border:`1px solid #2463eb33`,
            borderRadius:'12px', padding:'0.75rem 1.1rem',
            display:'inline-flex', alignItems:'center', gap:'8px',
            marginBottom:'1.8rem' }}}}>
            <span className="material-symbols-outlined" style={{{{ fontSize:'16px', color: YELLOW, fontVariationSettings:'"FILL" 1' }}}}>bar_chart</span>
            <span style={{{{ fontSize:'13px', color: SLATE3 }}}}>{copy["hero_stat"]}</span>
          </div>

          {{/* CTAs */}}
          <div style={{{{ display:'flex', gap:'10px', flexWrap:'wrap' }}}}>
            <a href={{WA_LINK}} target="_blank" rel="noopener noreferrer"
              style={{{{ display:'inline-flex', alignItems:'center', gap:'6px',
                background: YELLOW, color:'#0F172A',
                fontFamily:'"Plus Jakarta Sans", sans-serif', fontWeight:700,
                fontSize:'14px', padding:'11px 22px', borderRadius:'8px',
                textDecoration:'none' }}}}>
              <span className="material-symbols-outlined" style={{{{ fontSize:'18px', fontVariationSettings:'"FILL" 1' }}}}>calendar_month</span>
              Agendar Diagnóstico Gratuito
            </a>
            <a href="#que-es"
              style={{{{ display:'inline-flex', alignItems:'center', gap:'6px',
                background:'transparent', color:'white', fontSize:'14px',
                fontWeight:600, padding:'11px 22px', borderRadius:'8px',
                border:'1px solid #ffffff22', textDecoration:'none' }}}}>
              <span className="material-symbols-outlined" style={{{{ fontSize:'16px' }}}}>arrow_downward</span>
              Ver el análisis
            </a>
          </div>
        </div>
      </section>

      {{/* ═══ PROBLEMA ═══ */}}
      <section id="que-es" style={{{{ padding:'2.5rem 1.5rem', background:'#0a1628' }}}}>
        <div style={{{{ maxWidth:'860px', margin:'0 auto' }}}}>
          <p style={{{{ fontSize:'10px', fontWeight:700, letterSpacing:'0.12em',
            textTransform:'uppercase', color:'#f87171', marginBottom:'0.8rem' }}}}>
            EL PROBLEMA
          </p>
          <h2 style={{{{ fontFamily:'"Plus Jakarta Sans", sans-serif', fontWeight:900,
            fontSize:'clamp(18px,3vw,26px)', color:'white', marginBottom:'1rem' }}}}>
            {copy["problema_h2"]}
          </h2>
          {{/* Answer-First paragraph — citable por IA */}}
          <p className="answer-first-paragraph"
            style={{{{ fontSize:'15px', color: SLATE3, lineHeight:1.7,
              maxWidth:'680px', marginBottom:'1.2rem',
              borderLeft:`3px solid #2463eb`, paddingLeft:'1rem' }}}}>
            {copy["problema_answer"]}
          </p>
          <p style={{{{ fontSize:'13px', color: SLATE5 }}}}>
            Fuente: {stat2[1]}
          </p>

          {{/* KPIs */}}
          <div style={{{{ display:'grid', gridTemplateColumns:'repeat(auto-fit,minmax(160px,1fr))',
            gap:'10px', marginTop:'1.5rem' }}}}>
            <div style={{{{ background: CARD, border:'1px solid #ffffff0d', borderRadius:'12px', padding:'1rem', textAlign:'center' }}}}>
              <p style={{{{ fontFamily:'"Plus Jakarta Sans",sans-serif', fontWeight:900, fontSize:'26px', color: YELLOW, margin:0 }}}}>60%</p>
              <p style={{{{ fontSize:'11px', color: SLATE5, marginTop:'4px' }}}}>ahorro en procesos repetitivos</p>
            </div>
            <div style={{{{ background: CARD, border:'1px solid #ffffff0d', borderRadius:'12px', padding:'1rem', textAlign:'center' }}}}>
              <p style={{{{ fontFamily:'"Plus Jakarta Sans",sans-serif', fontWeight:900, fontSize:'26px', color: GREEN, margin:0 }}}}>90 días</p>
              <p style={{{{ fontSize:'11px', color: SLATE5, marginTop:'4px' }}}}>al primer resultado medible</p>
            </div>
            <div style={{{{ background: CARD, border:'1px solid #ffffff0d', borderRadius:'12px', padding:'1rem', textAlign:'center' }}}}>
              <p style={{{{ fontFamily:'"Plus Jakarta Sans",sans-serif', fontWeight:900, fontSize:'26px', color:'#60a5fa', margin:0 }}}}>280%</p>
              <p style={{{{ fontSize:'11px', color: SLATE5, marginTop:'4px' }}}}>ROI promedio primer año</p>
            </div>
          </div>
        </div>
      </section>

      {{/* ═══ SOLUCIÓN ═══ */}}
      <section style={{{{ padding:'2.5rem 1.5rem', background: DARK }}}}>
        <div style={{{{ maxWidth:'860px', margin:'0 auto' }}}}>
          <p style={{{{ fontSize:'10px', fontWeight:700, letterSpacing:'0.12em',
            textTransform:'uppercase', color:'#60a5fa', marginBottom:'0.8rem' }}}}>
            LA SOLUCIÓN
          </p>
          <h2 style={{{{ fontFamily:'"Plus Jakarta Sans", sans-serif', fontWeight:900,
            fontSize:'clamp(18px,3vw,26px)', color:'white', marginBottom:'0.5rem' }}}}>
            {copy["solucion_h2"]}
          </h2>
          <p style={{{{ fontSize:'14px', color: SLATE4, marginBottom:'1.5rem' }}}}>
            {BRAND["propuesta"]}. Sin cambiar tu ERP, sin tirar lo que ya funciona.
          </p>

          <div style={{{{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:'1.5rem' }}}}>
            <div>
              <p style={{{{ fontSize:'12px', fontWeight:600, color: YELLOW,
                marginBottom:'0.75rem', textTransform:'uppercase', letterSpacing:'0.06em' }}}}>
                Lo que obtienes
              </p>
              {beneficios_jsx}
            </div>
            <div>
              <p style={{{{ fontSize:'12px', fontWeight:600, color:'#60a5fa',
                marginBottom:'0.75rem', textTransform:'uppercase', letterSpacing:'0.06em' }}}}>
                Nuestro proceso
              </p>
              {pasos_jsx}
            </div>
          </div>
        </div>
      </section>

      {{/* ═══ FAQ ═══ */}}
      <section style={{{{ padding:'2.5rem 1.5rem', background:'#0a1628' }}}}>
        <div style={{{{ maxWidth:'860px', margin:'0 auto' }}}}>
          <p style={{{{ fontSize:'10px', fontWeight:700, letterSpacing:'0.12em',
            textTransform:'uppercase', color:'#60a5fa', marginBottom:'0.8rem' }}}}>
            PREGUNTAS FRECUENTES
          </p>
          <h2 style={{{{ fontFamily:'"Plus Jakarta Sans", sans-serif', fontWeight:900,
            fontSize:'clamp(18px,3vw,24px)', color:'white', marginBottom:'1.2rem' }}}}>
            Lo que preguntan los directores
          </h2>
          {faq_jsx}
        </div>
      </section>

      {{/* ═══ GEO — SECCIÓN CITABLE POR IA (ChatGPT, Perplexity, Claude) ═══ */}}
      <section style={{{{ padding:'2.5rem 1.5rem', background: DARK }}}}>
        <div style={{{{ maxWidth:'860px', margin:'0 auto' }}}}>
          <p style={{{{ fontSize:'10px', fontWeight:700, letterSpacing:'0.12em',
            textTransform:'uppercase', color:'#a78bfa', marginBottom:'0.6rem' }}}}>
            GLOSARIO PARA IA
          </p>
          <h2 style={{{{ fontFamily:'"Plus Jakarta Sans", sans-serif', fontWeight:900,
            fontSize:'clamp(16px,2.5vw,22px)', color:'white', marginBottom:'1.2rem' }}}}>
            Conceptos clave sobre {keyword}
          </h2>
          {geo_def_jsx}
          <div style={{{{ marginTop:'1.2rem', display:'flex', flexWrap:'wrap', gap:'8px' }}}}>
            <p style={{{{ fontSize:'11px', color: SLATE5, width:'100%',
              textTransform:'uppercase', letterSpacing:'0.08em', marginBottom:'4px' }}}}>
              Explora más:
            </p>
            {geo_links_jsx}
          </div>
        </div>
      </section>

      {{/* ═══ CTA FINAL ═══ */}}
      <section style={{{{ padding:'3rem 1.5rem',
        background:'linear-gradient(135deg,#0f2547 0%,#1a1a2e 50%,#0f172a 100%)',
        textAlign:'center' }}}}>
        <div style={{{{ maxWidth:'600px', margin:'0 auto' }}}}>
          <div style={{{{ display:'inline-flex', alignItems:'center', gap:'6px',
            background:'#2463eb22', border:'1px solid #2463eb44', color:'#60a5fa',
            fontSize:'10px', fontWeight:700, letterSpacing:'0.1em', textTransform:'uppercase',
            padding:'4px 14px', borderRadius:'100px', marginBottom:'1rem' }}}}>
            SIN COSTO · SIN COMPROMISO · 45 MINUTOS
          </div>
          <h2 style={{{{ fontFamily:'"Plus Jakarta Sans", sans-serif', fontWeight:900,
            fontSize:'clamp(20px,4vw,30px)', color:'white', marginBottom:'0.6rem' }}}}>
            {copy["cta_h2"]}
          </h2>
          <p style={{{{ fontSize:'14px', color: SLATE4, lineHeight:1.65, marginBottom:'1.5rem' }}}}>
            En 45 minutos identificamos los 3 procesos con mayor desperdicio
            en tu empresa y te mostramos cómo la IA los resuelve con tus números reales.
          </p>

          <a href={{WA_LINK}} target="_blank" rel="noopener noreferrer"
            style={{{{ display:'inline-flex', alignItems:'center', gap:'8px',
              background: YELLOW, color:'#0F172A',
              fontFamily:'"Plus Jakarta Sans", sans-serif', fontWeight:700,
              fontSize:'15px', padding:'13px 28px', borderRadius:'8px',
              textDecoration:'none', marginBottom:'1.2rem' }}}}>
            <span className="material-symbols-outlined" style={{{{ fontSize:'20px', fontVariationSettings:'"FILL" 1' }}}}>calendar_month</span>
            Agendar Diagnóstico Gratuito →
          </a>

          <div style={{{{ display:'flex', justifyContent:'center', gap:'1.5rem',
            flexWrap:'wrap', marginTop:'1rem' }}}}>
            <span style={{{{ fontSize:'12px', color: SLATE5, display:'flex', alignItems:'center', gap:'5px' }}}}>
              <span className="material-symbols-outlined" style={{{{ fontSize:'14px', color: BLUE, fontVariationSettings:'"FILL" 1' }}}}>person</span>
              {BRAND["contacto"]}
            </span>
            <span style={{{{ fontSize:'12px', color: SLATE5, display:'flex', alignItems:'center', gap:'5px' }}}}>
              <span className="material-symbols-outlined" style={{{{ fontSize:'14px', color: BLUE, fontVariationSettings:'"FILL" 1' }}}}>phone</span>
              {BRAND["telefono"]}
            </span>
            <span style={{{{ fontSize:'12px', color: SLATE5, display:'flex', alignItems:'center', gap:'5px' }}}}>
              <span className="material-symbols-outlined" style={{{{ fontSize:'14px', color: BLUE, fontVariationSettings:'"FILL" 1' }}}}>language</span>
              goodmantech.com.mx
            </span>
          </div>
        </div>
      </section>

    </div>
  );
}};

export default {comp};
'''
    return tsx


# ─────────────────────────────────────────────────────────────────────────────
# PASO 4 — GENERAR REGISTROS PARA App.tsx y Header.tsx (100% Python)
# ─────────────────────────────────────────────────────────────────────────────

def generar_registros(keyword: str, comp: str, copy: dict) -> dict:
    slug = slugify(keyword)
    path = url_path(keyword)

    app_import = f"import {comp} from './pages/{comp}';"
    app_route  = f'<Route path="{path}" element={{<{comp} />}} />'

    header_desktop = f'''<DropdownMenuItem asChild>
  <Link to="{path}" className="w-full cursor-pointer">
    <div className="flex flex-col items-start">
      <span className="font-medium">{keyword.title()}</span>
      <span className="text-sm text-muted-foreground">IA aplicada a tu empresa</span>
    </div>
  </Link>
</DropdownMenuItem>'''

    header_mobile = f'<Link to="{path}" className="block text-sm text-muted-foreground hover:text-primary transition-colors" onClick={{() => setIsMobileMenuOpen(false)}}>{keyword.title()}</Link>'

    sitemap_entry = f'''  <url>
    <loc>{BRAND["dominio"]}{path}/</loc>
    <priority>0.85</priority>
    <changefreq>monthly</changefreq>
    <lastmod>{date.today().isoformat()}</lastmod>
  </url>'''

    llms_entry = f"- [{keyword.title()}]({BRAND['dominio']}{path}/): {copy['meta_desc'][:80]}"

    return {
        "app_import":      app_import,
        "app_route":       app_route,
        "header_desktop":  header_desktop,
        "header_mobile":   header_mobile,
        "sitemap_entry":   sitemap_entry,
        "llms_entry":      llms_entry,
    }


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("Uso: python generar_landing.py \"Como aplicar la IA en mi empresa\"")
        sys.exit(1)

    keyword = " ".join(sys.argv[1:])
    comp    = component_name(keyword)
    slug    = slugify(keyword)

    print(f"\n🚀 Goodman Tech — Generador de Landing Pages")
    print(f"   Keyword  : {keyword}")
    print(f"   Componente: {comp}")
    print(f"   URL      : {url_path(keyword)}")
    print(f"   Canónica : {canonical(keyword)}\n")

    # ── 1. Copy con Claude (mínimo tokens) ───────────────────────────────────
    print("⏳ Generando copy con Claude API (Haiku — mínimo tokens)...")
    try:
        copy = generar_copy_con_claude(keyword)
        print("   ✅ Copy generado\n")
    except Exception as e:
        print(f"   ❌ Error en API: {e}")
        print("   Usando copy de respaldo...")
        copy = {
            "meta_title":      f"{keyword.title()} en Monterrey — Goodman Tech",
            "meta_desc":       f"Implementa {keyword} en tu empresa con resultados en 90 días. Sin cambiar tu ERP. Diagnóstico gratuito con Goodman Tech Monterrey.",
            "h1":              f"{keyword.title()} en Monterrey | Resultados en 90 Días",
            "subtitulo":       f"Implementación de IA para directores y dueños de empresa en México que quieren resultados medibles sin reemplazar sus sistemas actuales.",
            "hero_stat":       "El 68% de las PyMEs en México pierde más de 340 horas al mes en tareas que la IA puede automatizar (INEGI, 2025)",
            "problema_h2":     f"¿Tu empresa aún no aplica {keyword.lower()} y pierde competitividad?",
            "problema_answer": f"El 75% de las empresas medianas en México no tienen procesos automatizados con IA, perdiendo entre 30 y 50% de su capacidad productiva en tareas repetitivas (McKinsey, 2025). Mientras la competencia avanza, cada mes de espera amplía la brecha.",
            "solucion_h2":     f"Cómo implementamos {keyword.lower()} en tu empresa sin interrumpir operaciones",
            "solucion_items":  ["Automatiza reportes que hoy toman 4 horas — en 8 minutos", "Genera leads B2B calificados sin vendedor prospectando", "Reduce costos operativos hasta 60% en procesos repetitivos", "Obtén datos en tiempo real sin esperar el reporte de la semana", "Escala sin contratar — la IA trabaja 24/7 sin rotación"],
            "proceso_pasos":   ["Paso 1: Diagnóstico — Mapeamos tus procesos con mayor desperdicio", "Paso 2: Diseño — Definimos la solución con tus datos reales", "Paso 3: Piloto — Implementamos el proceso de mayor impacto", "Paso 4: Escala — Expandimos a toda la organización"],
            "autoridad_h2":    "Por qué más de 50 empresas en Monterrey confían en Goodman Tech",
            "cta_h2":          "Es el momento de que la IA trabaje para tu empresa",
            "faq_preguntas":   FAQ_BASE[:5],
            "faq_respuestas":  [
                "Los primeros resultados son visibles entre 30 y 90 días. Comenzamos con el proceso de mayor impacto para demostrar ROI antes de escalar.",
                "No. La IA trabaja sobre los datos que ya tienes en tu ERP. SAP sigue ejecutando transacciones — la IA añade inteligencia encima sin riesgo operativo.",
                "No necesitan saber programar. Si usan WhatsApp, pueden operar las soluciones. Capacitamos a tu equipo en 3 sesiones prácticas.",
                "El diagnóstico es gratuito. Los programas van desde $45,000 MXN para PyMEs hasta proyectos enterprise a convenir según alcance.",
                "Medimos con tus propios KPIs antes de iniciar. Al cierre del piloto entregamos reporte antes/después documentado para dirección.",
            ],
            "og_image_alt":    f"Implementación de {keyword} en empresas de Monterrey — Goodman Tech",
        }

    # ── 2. Schema (Python puro) ───────────────────────────────────────────────
    print("⚙️  Generando Schema JSON-LD...")
    schema_str = generar_schema(keyword, copy)
    print("   ✅ Schema generado\n")

    # ── 3. TSX completo (Python puro) ────────────────────────────────────────
    print("⚙️  Generando archivo .tsx...")
    tsx_content = generar_tsx(keyword, copy, schema_str)
    print("   ✅ TSX generado\n")

    # ── 4. Registros para otros archivos ─────────────────────────────────────
    registros = generar_registros(keyword, comp, copy)

    # ── 5. Guardar archivos ───────────────────────────────────────────────────
    out_dir = f"C:/Users/Dell/CascadeProjects/Godman_Webpage/Godman_Webpage/src/pages"
    os.makedirs(out_dir, exist_ok=True)

    tsx_path = f"{out_dir}/{comp}.tsx"

    # Validar que Claude no haya generado sintaxis de template invalida
    if "{%" in tsx_content or "%}" in tsx_content:
        print(f"⚠️  Claude genero sintaxis invalida. Abortando escritura de {comp}.tsx")
        print(f"   Vuelve a intentar generando esta keyword manualmente.")
        return False

    with open(tsx_path, "w", encoding="utf-8") as f:
        f.write(tsx_content)

    reg_path = f"{out_dir}/REGISTROS.md"
    with open(reg_path, "w", encoding="utf-8") as f:
        f.write(f"# Registros para: {keyword}\n\n")
        f.write(f"## 1. App.tsx — Importación\n```tsx\n{registros['app_import']}\n```\n\n")
        f.write(f"## 2. App.tsx — Ruta\n```tsx\n{registros['app_route']}\n```\n\n")
        f.write(f"## 3. Header.tsx — Menú Desktop\n```tsx\n{registros['header_desktop']}\n```\n\n")
        f.write(f"## 4. Header.tsx — Menú Mobile\n```tsx\n{registros['header_mobile']}\n```\n\n")
        f.write(f"## 5. sitemap.xml\n```xml\n{registros['sitemap_entry']}\n```\n\n")
        f.write(f"## 6. llms.txt\n```\n{registros['llms_entry']}\n```\n\n")
        f.write(f"## Copy generado\n")
        f.write(f"- **Meta title:** {copy['meta_title']}\n")
        f.write(f"- **H1:** {copy['h1']}\n")
        f.write(f"- **URL:** {canonical(keyword)}\n")

    # ── 6. Auto-registrar en App.tsx (NUEVO - Evita olvidos) ────────────────
    app_tsx_path = r"C:\Users\Dell\CascadeProjects\Godman_Webpage\Godman_Webpage\src\App.tsx"
    
    if os.path.exists(app_tsx_path):
        try:
            with open(app_tsx_path, 'r', encoding='utf-8') as f:
                app_content = f.read()
            
            # Verificar si ya está registrado
            if comp not in app_content:
                # Agregar import después de EmpresasEmbajadoresIa
                import_marker = 'import EmpresasEmbajadoresIa from "./pages/EmpresasEmbajadoresIa";'
                if import_marker in app_content:
                    app_content = app_content.replace(
                        import_marker,
                        import_marker + '\n' + registros['app_import']
                    )
                
                # Agregar route antes de LeadsInstantly section
                route_marker = '            {/* ── LeadsInstantly ────────────────────────────────────────── */}'
                if route_marker in app_content:
                    app_content = app_content.replace(
                        route_marker,
                        '            ' + registros['app_route'] + '\n\n' + route_marker
                    )
                
                # Guardar App.tsx actualizado
                with open(app_tsx_path, 'w', encoding='utf-8') as f:
                    f.write(app_content)
                
                print(f"\n✅ RUTA AUTO-REGISTRADA EN App.tsx")
                print(f"   → Import agregado")
                print(f"   → Route agregada: /empresas/{slug(keyword)}")
            else:
                print(f"\n⚠️  Ruta ya existía en App.tsx (omitido)")
        except Exception as e:
            print(f"\n⚠️  No se pudo auto-registrar en App.tsx: {e}")
            print(f"   → Usa REGISTROS.md para registrar manualmente")
    else:
        print(f"\n⚠️  App.tsx no encontrado en ruta esperada")
        print(f"   → Usa REGISTROS.md para registrar manualmente")

    # ── 7. Reporte final ─────────────────────────────────────────────────────
    print("=" * 60)
    print(f"✅ LANDING GENERADA EXITOSAMENTE")
    print("=" * 60)
    print(f"\n📁 Archivos creados en: {out_dir}/")
    print(f"   → {comp}.tsx         (pegar en src/pages/)")
    print(f"   → REGISTROS.md       (backup de registros)")
    print(f"\n📋 Pasos para activar:")
    print(f"   1. Copia {comp}.tsx → src/pages/")
    print(f"   2. ✅ Ruta YA REGISTRADA en App.tsx automáticamente")
    print(f"   3. git add . && git commit -m 'Feat: {keyword}' && git push")
    print(f"\n🌐 URL final: {canonical(keyword)}")
    print(f"\n💡 Tokens usados: ~1,000 (solo copy creativo via Haiku)")
    print(f"   Sin tokens: Schema, OG, meta tags, TSX completo, registros")
    print(f"\n🎯 NUEVO: Auto-registro en App.tsx activado (evita 404s)\n")


if __name__ == "__main__":
    main()
