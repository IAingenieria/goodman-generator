#!/usr/bin/env python3
"""
GOODMAN TECH — Generador Automático de Artículos de Blog SEO
=============================================================
Uso:  python generar_blog.py "cuánto cuesta implementar ia en una empresa"
      python generar_blog.py "cuál es la mejor ia para empresas"

Diferencias vs generar_landing.py:
  - URL: /blog/{slug}   (no /empresas/)
  - Componente: Blog{PascalCase}   (no Empresas{PascalCase})
  - Schema: BlogPosting + FAQPage
  - Prompt: informacional (responde preguntas), no comercial
  - Estructura: Respuesta directa → Desarrollo → Tips → FAQ → CTA suave
  - Mismo GEO section (cajas RAG-citables) al final

Tokens Claude: ~1,000-1,400 por artículo (solo copy creativo)
Todo lo estructural: Python puro, 0 tokens.
"""

import sys
import re
import json
import os
import unicodedata
from datetime import date
import anthropic

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

# ─────────────────────────────────────────────────────────────────────────────
# UTILIDADES
# ─────────────────────────────────────────────────────────────────────────────

def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    return text

def component_name(text: str) -> str:
    """'cuánto cuesta implementar ia' → 'BlogCuantoCuestaImplementarIa'"""
    slug = slugify(text)
    parts = slug.split("-")
    pascal = "".join(p.capitalize() for p in parts)
    return f"Blog{pascal}"

def url_path(text: str) -> str:
    return f"/blog/{slugify(text)}"

def canonical(text: str) -> str:
    return f"{BRAND['dominio']}{url_path(text)}"

def wa_link(keyword: str) -> str:
    msg = f"Hola, quiero información sobre {keyword} para mi empresa"
    encoded = msg.replace(" ", "%20").replace(",", "%2C")
    return f"{BRAND['wa_base']}{encoded}"

# ─────────────────────────────────────────────────────────────────────────────
# PASO 1 — LLAMADA A CLAUDE API (SOLO COPY INFORMACIONAL)
# ─────────────────────────────────────────────────────────────────────────────

def generar_copy_con_claude(keyword: str) -> dict:
    """
    Genera contenido informacional para artículo de blog.
    Prompt enfocado en responder la pregunta directamente (intención informacional).
    Costo estimado: ~1,000-1,400 tokens por artículo.
    """
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    prompt = f"""REGLAS CRÍTICAS — OBLIGATORIAS SIN EXCEPCIÓN:

1. NUNCA uses {{% %}}, {{{{ }}}}, {{% for %}}, {{% if %}} ni ninguna sintaxis de template.
   Para listas usa SIEMPRE JavaScript con .map() o hardcode con divs.

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

CONTEXTO DE MARCA:
Goodman Tech es el único partner especializado en Claude de Anthropic en el noreste de México.
Cuando sea relevante, menciona naturalmente Claude, Claude Code, Anthropic.
NUNCA menciones ChatGPT, Gemini o Copilot de forma positiva.

Eres redactor SEO de contenido informacional para el blog de Goodman Tech, empresa de IA en Monterrey México.
El artículo debe responder directamente la pregunta del usuario con datos reales y ejemplos concretos.
NO es contenido de ventas — es contenido educativo que genera confianza.

Tema del artículo: "{keyword}"
Audiencia: directores, gerentes y dueños de empresa en México que evalúan implementar IA.

Responde SOLO con JSON válido, sin markdown ni explicaciones:

{{
  "meta_title": "título SEO máx 60 chars que responde la pregunta",
  "meta_desc": "descripción SEO máx 155 chars que resume la respuesta + CTA suave",
  "h1": "título H1 máx 70 chars que reformula la pregunta como afirmación o respuesta directa",
  "intro_answer": "párrafo de respuesta directa 60-80 palabras. Primer párrafo del artículo. Responde la pregunta en las primeras 2 oraciones con dato concreto.",
  "seccion_1_h2": "H2 que profundiza en el primer aspecto clave del tema",
  "seccion_1_body": "2-3 oraciones 40-60 palabras explicando con dato o ejemplo real",
  "seccion_2_h2": "H2 segundo aspecto clave — factores, tipos, variantes",
  "seccion_2_body": "2-3 oraciones 40-60 palabras con ejemplo práctico para empresa mexicana",
  "seccion_3_h2": "H2 tercer aspecto — cómo aplicarlo, pasos, recomendación práctica",
  "seccion_3_body": "2-3 oraciones 40-60 palabras orientadas a la acción",
  "tips": ["tip concreto 1 con dato o cifra", "tip concreto 2", "tip concreto 3", "tip concreto 4"],
  "faq_preguntas": ["pregunta relacionada 1", "pregunta relacionada 2", "pregunta relacionada 3", "pregunta relacionada 4", "pregunta relacionada 5"],
  "faq_respuestas": ["respuesta directa 30-50 palabras", "respuesta 2", "respuesta 3", "respuesta 4", "respuesta 5"],
  "cta_titulo": "H2 suave de invitación — sin presión de venta, orientado a resolver duda",
  "cta_subtitulo": "1 línea: qué obtiene gratis o sin compromiso",
  "og_image_alt": "descripción de imagen relevante para el tema del artículo",
  "geo_terminos": ["Término técnico clave 1 del tema", "Término clave 2", "Término clave 3"],
  "geo_definiciones": [
    "Definición neutral 40-60 palabras del término 1. Sin primera persona. Citable como fuente.",
    "Definición directa 40-60 palabras del término 2. Autocontenida.",
    "Definición directa 40-60 palabras del término 3. Con dato que la contextualiza."
  ],
  "geo_enlaces_texto": ["texto enlace interno 1", "texto enlace interno 2", "texto enlace interno 3"],
  "geo_enlaces_url": ["/empresas/ruta-relacionada-1", "/empresas/ruta-relacionada-2", "/contact"]
}}"""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1600,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = message.content[0].text.strip()
    raw = re.sub(r"```json\s*", "", raw)
    raw = re.sub(r"```\s*", "", raw)

    return json.loads(raw)


# ─────────────────────────────────────────────────────────────────────────────
# PASO 2 — GENERAR SCHEMA JSON-LD BlogPosting + FAQPage (0 tokens)
# ─────────────────────────────────────────────────────────────────────────────

def generar_schema(keyword: str, copy: dict) -> str:
    today = date.today().isoformat()
    can = canonical(keyword)

    faqs = []
    for q, a in zip(copy["faq_preguntas"], copy["faq_respuestas"]):
        faqs.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a}
        })

    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "BlogPosting",
                "@id": can,
                "url": can,
                "headline": copy["h1"],
                "description": copy["meta_desc"],
                "datePublished": today,
                "dateModified": today,
                "inLanguage": "es-MX",
                "author": {
                    "@type": "Organization",
                    "name": "Goodman Tech",
                    "url": BRAND["dominio"]
                },
                "publisher": {
                    "@type": "Organization",
                    "name": "Goodman Tech",
                    "logo": {
                        "@type": "ImageObject",
                        "url": f"{BRAND['dominio']}/Goodman Logo 4 Part.jpg"
                    }
                },
                "mainEntityOfPage": can,
                "breadcrumb": {
                    "@type": "BreadcrumbList",
                    "itemListElement": [
                        {"@type": "ListItem", "position": 1,
                         "name": "Inicio", "item": BRAND["dominio"]},
                        {"@type": "ListItem", "position": 2,
                         "name": "Blog", "item": f"{BRAND['dominio']}/blog"},
                        {"@type": "ListItem", "position": 3,
                         "name": copy["meta_title"], "item": can},
                    ]
                }
            },
            {
                "@type": "FAQPage",
                "mainEntity": faqs
            }
        ]
    }

    return json.dumps(schema, ensure_ascii=False, indent=2)


# ─────────────────────────────────────────────────────────────────────────────
# PASO 3 — GENERAR ARCHIVO .TSX COMPLETO (0 tokens)
# ─────────────────────────────────────────────────────────────────────────────

def generar_tsx(keyword: str, copy: dict, schema_str: str) -> str:
    comp  = component_name(keyword)
    slug  = slugify(keyword)
    can   = canonical(keyword)
    wa    = wa_link(keyword)
    today = date.today().strftime("%d/%m/%Y")

    schema_escaped = schema_str.replace("`", "\\`").replace("${", "\\${")

    # Tips
    tips_jsx = "\n".join(
        f'              <div key="{i}" style={{{{display:"flex",gap:"12px",alignItems:"flex-start",'
        f'background:"#{COLORS["CARD2"]}",borderRadius:"10px",padding:"0.85rem 1rem",marginBottom:"8px"}}}}>'
        f'<span style={{{{color:"#{COLORS["GREEN"]}",fontWeight:700,fontSize:"18px",lineHeight:1,flexShrink:0}}}}>✓</span>'
        f'<span style={{{{fontSize:"14px",color:"#{COLORS["SLATE3"]}",lineHeight:1.55}}}}>{tip}</span></div>'
        for i, tip in enumerate(copy.get("tips", []))
    )

    # FAQ
    faq_jsx = "\n".join(
        f'              <div key="{i}" style={{{{background:"#{COLORS["CARD2"]}",border:"1px solid #ffffff0d",'
        f'borderRadius:"12px",padding:"1rem 1.1rem",marginBottom:"8px"}}}}>'
        f'<p style={{{{fontWeight:700,fontSize:"13px",color:"white",marginBottom:"5px"}}}}>{q}</p>'
        f'<p style={{{{fontSize:"13px",color:"#{COLORS["SLATE4"]}",lineHeight:"1.55",margin:0}}}}>{a}</p></div>'
        for i, (q, a) in enumerate(zip(copy["faq_preguntas"], copy["faq_respuestas"]))
    )

    # GEO section
    slug_base = slugify(keyword)
    geo_terminos  = copy.get("geo_terminos", [])
    geo_defs      = copy.get("geo_definiciones", [])
    geo_links_txt = copy.get("geo_enlaces_texto", ["Agentes de IA", "Automatización con IA", "Diagnóstico Gratuito"])
    geo_links_url = copy.get("geo_enlaces_url",   ["/agentes-ia", "/empresas/automatizacion-con-ia-para-empresas", "/contact"])

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
    ) or (
        f'          <div id="def-{slug_base}" style={{{{background:"#{COLORS["CARD2"]}",border:"1px solid #2463eb44",'
        f'borderRadius:"12px",padding:"1.2rem 1.4rem",marginBottom:"1rem",borderLeft:"4px solid #{COLORS["BLUE"]}"}}}}>'
        f'<p style={{{{fontFamily:\'"Plus Jakarta Sans",sans-serif\',fontWeight:700,fontSize:"14px",'
        f'color:"#{COLORS["YELLOW"]}",marginBottom:"0.5rem"}}}}>¿Qué es {keyword}?</p>'
        f'<p style={{{{fontSize:"14px",color:"#{COLORS["SLATE3"]}",lineHeight:1.65,margin:0}}}}>'
        f'La inteligencia artificial para empresas engloba sistemas que aprenden de datos para automatizar decisiones, '
        f'procesos y análisis que antes requerían intervención humana, con aplicaciones desde manufactura hasta ventas.</p>'
        f'<cite style={{{{fontSize:"11px",color:"#{COLORS["SLATE5"]}",marginTop:"0.5rem",display:"block"}}}}>'
        f'Fuente: Goodman Tech — goodmantech.com.mx</cite></div>'
    )

    geo_links_jsx = " ".join(
        f'<a href="{url}" style={{{{fontSize:"12px",color:"#60a5fa",textDecoration:"none",'
        f'background:"#2463eb11",border:"1px solid #2463eb33",'
        f'padding:"5px 12px",borderRadius:"100px"}}}}>{txt}</a>'
        for txt, url in zip(geo_links_txt, geo_links_url)
        if txt and url
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

      {{/* ── SEO ── */}}
      <Helmet>
        <title>{copy["meta_title"]} | Goodman Tech</title>
        <meta name="description" content="{copy["meta_desc"]}" />
        <link rel="canonical" href="{can}" />
        <meta property="og:title" content="{copy["meta_title"]}" />
        <meta property="og:description" content="{copy["meta_desc"]}" />
        <meta property="og:url" content="{can}" />
        <meta property="og:type" content="article" />
        <meta property="og:image" content="{BRAND["dominio"]}/Goodman Logo 4 Part.jpg" />
        <meta property="og:image:alt" content="{copy["og_image_alt"]}" />
        <meta property="og:locale" content="es_MX" />
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:title" content="{copy["meta_title"]}" />
        <meta name="twitter:description" content="{copy["meta_desc"]}" />
        <meta name="article:published_time" content="{date.today().isoformat()}" />
        <meta name="article:author" content="Goodman Tech" />
        <script type="application/ld+json">{{SCHEMA}}</script>
      </Helmet>

      {{/* ── HERO ── */}}
      <section style={{{{ padding: '4rem 1.5rem 3rem', maxWidth: '800px', margin: '0 auto' }}}}>
        {{/* Breadcrumb */}}
        <p style={{{{ fontSize: '12px', color: SLATE5, marginBottom: '1.5rem' }}}}>
          <a href="/" style={{{{ color: SLATE5, textDecoration: 'none' }}}}>Inicio</a>
          {{' › '}}
          <a href="/blog" style={{{{ color: SLATE5, textDecoration: 'none' }}}}>Blog</a>
          {{' › '}}
          <span style={{{{ color: SLATE4 }}}}>{keyword.title()}</span>
        </p>

        {{/* Categoría */}}
        <div style={{{{ display: 'inline-flex', alignItems: 'center', gap: '6px',
             background: '#2463eb22', border: '1px solid #2463eb55',
             borderRadius: '100px', padding: '4px 12px', marginBottom: '1.2rem' }}}}>
          <span style={{{{ fontSize: '11px', color: '#93c5fd', fontWeight: 600, letterSpacing: '0.04em' }}}}>
            BLOG · IA EMPRESARIAL
          </span>
        </div>

        <h1 style={{{{ fontFamily: '"Plus Jakarta Sans", sans-serif', fontSize: 'clamp(1.6rem, 4vw, 2.4rem)',
             fontWeight: 800, lineHeight: 1.2, marginBottom: '1.2rem', color: 'white' }}}}>
          {copy["h1"]}
        </h1>

        {{/* Meta info artículo */}}
        <div style={{{{ display: 'flex', gap: '1.5rem', flexWrap: 'wrap', marginBottom: '2rem',
             fontSize: '12px', color: SLATE5 }}}}>
          <span>📅 {today}</span>
          <span>✍️ Goodman Tech</span>
          <span>⏱️ 5 min de lectura</span>
        </div>

        {{/* Respuesta directa — answer-first paragraph */}}
        <div className="answer-first-paragraph"
             style={{{{ background: CARD, border: '1px solid #2463eb33',
                  borderLeft: '4px solid #2463eb', borderRadius: '12px',
                  padding: '1.5rem', marginBottom: '2rem' }}}}>
          <p style={{{{ fontSize: '15px', color: SLATE3, lineHeight: 1.7, margin: 0,
               fontWeight: 400 }}}}>
            {copy["intro_answer"]}
          </p>
        </div>
      </section>

      {{/* ── SECCIÓN 1 ── */}}
      <section style={{{{ padding: '1.5rem', maxWidth: '800px', margin: '0 auto' }}}}>
        <h2 style={{{{ fontFamily: '"Plus Jakarta Sans", sans-serif', fontSize: 'clamp(1.2rem, 3vw, 1.6rem)',
             fontWeight: 700, color: 'white', marginBottom: '0.75rem' }}}}>
          {copy["seccion_1_h2"]}
        </h2>
        <p style={{{{ fontSize: '14px', color: SLATE3, lineHeight: 1.7, marginBottom: '2rem' }}}}>
          {copy["seccion_1_body"]}
        </p>

        <h2 style={{{{ fontFamily: '"Plus Jakarta Sans", sans-serif', fontSize: 'clamp(1.2rem, 3vw, 1.6rem)',
             fontWeight: 700, color: 'white', marginBottom: '0.75rem' }}}}>
          {copy["seccion_2_h2"]}
        </h2>
        <p style={{{{ fontSize: '14px', color: SLATE3, lineHeight: 1.7, marginBottom: '2rem' }}}}>
          {copy["seccion_2_body"]}
        </p>

        <h2 style={{{{ fontFamily: '"Plus Jakarta Sans", sans-serif', fontSize: 'clamp(1.2rem, 3vw, 1.6rem)',
             fontWeight: 700, color: 'white', marginBottom: '0.75rem' }}}}>
          {copy["seccion_3_h2"]}
        </h2>
        <p style={{{{ fontSize: '14px', color: SLATE3, lineHeight: 1.7, marginBottom: '2rem' }}}}>
          {copy["seccion_3_body"]}
        </p>
      </section>

      {{/* ── TIPS ── */}}
      <section style={{{{ padding: '2rem 1.5rem', maxWidth: '800px', margin: '0 auto' }}}}>
        <h2 style={{{{ fontFamily: '"Plus Jakarta Sans", sans-serif', fontSize: '1.3rem',
             fontWeight: 700, color: YELLOW, marginBottom: '1rem' }}}}>
          Puntos clave a recordar
        </h2>
        <div>
{tips_jsx}
        </div>
      </section>

      {{/* ═══ GEO — SECCIÓN CITABLE POR IA (ChatGPT, Perplexity, Claude) ═══ */}}
      <section style={{{{ padding: '2.5rem 1.5rem', background: '#0c1526', maxWidth: '800px', margin: '0 auto' }}}}>
        <div style={{{{ borderBottom: '1px solid #2463eb33', paddingBottom: '0.5rem', marginBottom: '1.2rem' }}}}>
          <p style={{{{ fontSize: '11px', color: SLATE5, letterSpacing: '0.08em', textTransform: 'uppercase', margin: 0 }}}}>
            Glosario · Términos clave de este artículo
          </p>
        </div>
        <div>
{geo_def_jsx}
        </div>
        <div style={{{{ display: 'flex', gap: '8px', flexWrap: 'wrap', marginTop: '1.2rem' }}}}>
          {geo_links_jsx}
        </div>
      </section>

      {{/* ── FAQ ── */}}
      <section style={{{{ padding: '2.5rem 1.5rem', maxWidth: '800px', margin: '0 auto' }}}}>
        <h2 style={{{{ fontFamily: '"Plus Jakarta Sans", sans-serif', fontSize: '1.3rem',
             fontWeight: 700, color: 'white', marginBottom: '1rem' }}}}>
          Preguntas frecuentes
        </h2>
        <div>
{faq_jsx}
        </div>
      </section>

      {{/* ── CTA SUAVE ── */}}
      <section style={{{{ padding: '3rem 1.5rem', maxWidth: '800px', margin: '0 auto',
           textAlign: 'center' }}}}>
        <div style={{{{ background: CARD, border: '1px solid #2463eb33',
             borderRadius: '16px', padding: '2.5rem 1.5rem' }}}}>
          <h2 style={{{{ fontFamily: '"Plus Jakarta Sans", sans-serif',
               fontSize: 'clamp(1.2rem, 3vw, 1.6rem)', fontWeight: 700,
               color: 'white', marginBottom: '0.75rem' }}}}>
            {copy["cta_titulo"]}
          </h2>
          <p style={{{{ fontSize: '14px', color: SLATE4, marginBottom: '1.5rem', lineHeight: 1.6 }}}}>
            {copy["cta_subtitulo"]}
          </p>
          <div style={{{{ display: 'flex', gap: '12px', justifyContent: 'center', flexWrap: 'wrap' }}}}>
            <a href="/contact"
               style={{{{ background: BLUE, color: 'white', fontWeight: 700,
                    fontSize: '14px', padding: '12px 24px', borderRadius: '8px',
                    textDecoration: 'none', display: 'inline-block' }}}}>
              Agendar diagnóstico gratuito
            </a>
            <a href={{WA_LINK}} target="_blank" rel="noopener noreferrer"
               style={{{{ background: '#25D366', color: 'white', fontWeight: 700,
                    fontSize: '14px', padding: '12px 24px', borderRadius: '8px',
                    textDecoration: 'none', display: 'inline-block' }}}}>
              WhatsApp directo
            </a>
          </div>
          <p style={{{{ fontSize: '11px', color: SLATE5, marginTop: '1rem' }}}}>
            {BRAND["telefono"]} · {BRAND["email"]}
          </p>
        </div>
      </section>

    </div>
  );
}};

export default {comp};
'''
    return tsx


# ─────────────────────────────────────────────────────────────────────────────
# PASO 4 — GENERAR REGISTROS (0 tokens)
# ─────────────────────────────────────────────────────────────────────────────

def generar_registros(keyword: str, comp: str, copy: dict) -> dict:
    slug = slugify(keyword)
    path = url_path(keyword)

    app_import = f"import {comp} from './pages/{comp}';"
    app_route  = f'<Route path="{path}" element={{<{comp} />}} />'

    sitemap_entry = f'''  <url>
    <loc>{BRAND["dominio"]}{path}/</loc>
    <priority>0.75</priority>
    <changefreq>monthly</changefreq>
    <lastmod>{date.today().isoformat()}</lastmod>
  </url>'''

    llms_entry = f"- [Blog: {keyword.title()}]({BRAND['dominio']}{path}/): {copy['meta_desc'][:80]}"

    return {
        "app_import":    app_import,
        "app_route":     app_route,
        "sitemap_entry": sitemap_entry,
        "llms_entry":    llms_entry,
    }


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print('Uso: python generar_blog.py "cuánto cuesta implementar ia en una empresa"')
        sys.exit(1)

    keyword = " ".join(sys.argv[1:])
    comp    = component_name(keyword)
    slug    = slugify(keyword)

    print(f"\n📝 Goodman Tech — Generador de Blog Posts SEO")
    print(f"   Keyword   : {keyword}")
    print(f"   Componente: {comp}")
    print(f"   URL       : {url_path(keyword)}")
    print(f"   Canónica  : {canonical(keyword)}\n")

    # ── 1. Copy con Claude ───────────────────────────────────────────────────
    print("⏳ Generando copy informacional con Claude API (Sonnet — blog)...")
    try:
        copy = generar_copy_con_claude(keyword)
        print("   ✅ Copy generado\n")
    except Exception as e:
        print(f"   ❌ Error en API: {e}")
        sys.exit(1)

    # ── 2. Schema BlogPosting ────────────────────────────────────────────────
    print("⚙️  Generando Schema BlogPosting JSON-LD...")
    schema_str = generar_schema(keyword, copy)
    print("   ✅ Schema generado\n")

    # ── 3. TSX completo ──────────────────────────────────────────────────────
    print("⚙️  Generando archivo .tsx...")
    tsx_content = generar_tsx(keyword, copy, schema_str)
    print("   ✅ TSX generado\n")

    # ── 4. Registros ─────────────────────────────────────────────────────────
    registros = generar_registros(keyword, comp, copy)

    # ── 5. Guardar archivos ──────────────────────────────────────────────────
    out_dir = r"C:\Users\Dell\CascadeProjects\Godman_Webpage\Godman_Webpage\src\pages"
    os.makedirs(out_dir, exist_ok=True)

    tsx_path = f"{out_dir}/{comp}.tsx"

    # Validar sintaxis inválida
    if "{%" in tsx_content or "%}" in tsx_content:
        print(f"⚠️  Claude generó sintaxis inválida ({{% %}}). Abortando escritura.")
        print(f"   Vuelve a intentar con la misma keyword.")
        return False

    with open(tsx_path, "w", encoding="utf-8") as f:
        f.write(tsx_content)

    reg_path = f"{out_dir}/REGISTROS_BLOG.md"
    with open(reg_path, "w", encoding="utf-8") as f:
        f.write(f"# Registros Blog: {keyword}\n\n")
        f.write(f"## 1. App.tsx — Importación\n```tsx\n{registros['app_import']}\n```\n\n")
        f.write(f"## 2. App.tsx — Ruta\n```tsx\n{registros['app_route']}\n```\n\n")
        f.write(f"## 3. sitemap.xml\n```xml\n{registros['sitemap_entry']}\n```\n\n")
        f.write(f"## 4. llms.txt\n```\n{registros['llms_entry']}\n```\n\n")
        f.write(f"## Copy\n")
        f.write(f"- **Meta title:** {copy['meta_title']}\n")
        f.write(f"- **H1:** {copy['h1']}\n")
        f.write(f"- **URL:** {canonical(keyword)}\n")

    # ── 6. Reporte ───────────────────────────────────────────────────────────
    print("=" * 60)
    print(f"✅ BLOG GENERADO EXITOSAMENTE")
    print("=" * 60)
    print(f"\n📁 Archivo creado: {tsx_path}")
    print(f"   → {comp}.tsx")
    print(f"   → REGISTROS_BLOG.md  (App.tsx, sitemap, llms.txt)")
    print(f"\n📋 Pasos para activar:")
    print(f"   1. Abre REGISTROS_BLOG.md")
    print(f"   2. Pega el import en src/App.tsx (sección imports)")
    print(f"   3. Pega la ruta en src/App.tsx (dentro de <Routes>)")
    print(f"   4. Agrega entrada en public/sitemap.xml")
    print(f"   5. npm run build && npm run preview")
    print(f"\n🌐 URL final: {canonical(keyword)}")
    print(f"\n💡 Schema: BlogPosting + FAQPage | Sección GEO incluida\n")
    return True


if __name__ == "__main__":
    main()
