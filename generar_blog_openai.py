#!/usr/bin/env python3
"""
GOODMAN TECH — Generador de Blogs con OpenAI
==============================================
Uso:  python generar_blog_openai.py "Cómo implementar IA en tu empresa"

Genera blogs largos (2000-3000 palabras) con OpenAI GPT-4
Incluye vinculación automática con landing pages existentes
"""

import sys
import re
import json
import os
from datetime import date
from openai import OpenAI

# ── CONFIGURACIÓN ─────────────────────────────────────────────────────────────
# API Key desde variable de entorno (más seguro)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    print("❌ Error: Variable de entorno OPENAI_API_KEY no configurada")
    print("   Configúrala con: $env:OPENAI_API_KEY = 'tu-api-key'")
    sys.exit(1)

client = OpenAI(api_key=OPENAI_API_KEY)

BRAND = {
    "nombre": "Goodman Tech",
    "ciudad": "Monterrey, Nuevo León",
    "dominio": "https://www.goodmantech.com.mx",
    "whatsapp": "528126350902",
    "email": "info@goodmantech.com.mx",
}

# Mapeo de keywords a landing pages para vinculación automática
VINCULACION_LANDINGS = {
    "claude": "/empresas/claude-para-empresas-mexico",
    "automatización": "/empresas/automatizacion-de-procesos-con-inteligencia-artificial",
    "manufactura": "/empresas/como-se-utiliza-la-ia-en-la-manufactura",
    "embajadores": "/empresas/embajadores-ia",
    "dirección": "/empresas/direccion",
    "operaciones": "/empresas/operaciones",
    "ventas": "/empresas/ventas",
    "finanzas": "/empresas/finanzas",
    "rrhh": "/empresas/rrhh",
    "ti": "/empresas/ti",
}

CATEGORIAS = {
    "ia-empresas": "IA para Empresas",
    "automatizacion": "Automatización",
    "casos-exito": "Casos de Éxito",
    "tutoriales": "Tutoriales",
    "tendencias": "Tendencias IA"
}

# ── FUNCIONES AUXILIARES ──────────────────────────────────────────────────────

def slugify(text):
    """Convierte texto a slug URL-friendly"""
    text = text.lower()
    text = re.sub(r'[áàäâ]', 'a', text)
    text = re.sub(r'[éèëê]', 'e', text)
    text = re.sub(r'[íìïî]', 'i', text)
    text = re.sub(r'[óòöô]', 'o', text)
    text = re.sub(r'[úùüû]', 'u', text)
    text = re.sub(r'[ñ]', 'n', text)
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s-]+', '-', text)
    return text.strip('-')

def generar_contenido_openai(titulo, categoria):
    """Genera contenido del blog usando OpenAI GPT-4"""
    
    prompt = f"""Eres un experto en inteligencia artificial y transformación digital para empresas en México.

Escribe un artículo de blog completo y detallado sobre: "{titulo}"

CONTEXTO DE LA EMPRESA:
- Nombre: Goodman Tech
- Ubicación: Monterrey, Nuevo León
- Especialidad: Implementación de IA en empresas con resultados en 90 días
- Propuesta: Formamos embajadores internos de IA, no vendemos software

REQUISITOS DEL ARTÍCULO:
1. Longitud: 2000-3000 palabras
2. Tono: Profesional pero accesible, directo, sin fluff
3. Estructura:
   - Introducción enganchadora (problema real)
   - 5-7 secciones principales con subtítulos H2
   - Cada sección con 3-4 párrafos
   - Ejemplos concretos de empresas mexicanas (PyMEs y manufactura)
   - Datos y estadísticas cuando sea posible
   - Conclusión con call-to-action suave

4. Incluir:
   - Casos de uso específicos para Monterrey/México
   - Mención de tecnologías: Claude AI, Anthropic, OpenAI
   - Enfoque en ROI medible y resultados en 90 días
   - Mencionar "embajadores de IA" como metodología

5. Estilo:
   - Usa "tú" para dirigirte al lector
   - Evita jerga técnica excesiva
   - Incluye listas numeradas y bullets
   - Usa negritas para conceptos clave
   - Incluye preguntas retóricas

6. NO incluir:
   - Conclusiones genéricas tipo "en conclusión..."
   - Promesas exageradas
   - Lenguaje de venta agresivo
   - Información desactualizada

FORMATO DE SALIDA (Markdown):
# {titulo}

## Introducción
[Párrafo problema]
[Párrafo contexto]
[Párrafo promesa del artículo]

## [Subtítulo H2]
[Contenido...]

## [Subtítulo H2]
[Contenido...]

[... más secciones ...]

## Conclusión
[Resumen de valor]
[CTA suave: "¿Listo para implementar IA en tu empresa? Agenda un diagnóstico gratuito de 45 minutos."]

---

Genera el artículo completo ahora:"""

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "Eres un experto en IA empresarial y redacción de contenido técnico para empresas mexicanas."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=4000
        )
        
        contenido = response.choices[0].message.content
        return contenido
    
    except Exception as e:
        print(f"❌ Error al generar contenido con OpenAI: {e}")
        return None

def extraer_secciones(contenido_md):
    """Extrae secciones H2 para tabla de contenidos"""
    secciones = re.findall(r'^## (.+)$', contenido_md, re.MULTILINE)
    return secciones

def generar_metadata(titulo, contenido, categoria):
    """Genera metadata SEO del blog"""
    
    # Extraer primer párrafo como descripción
    parrafos = re.findall(r'^[A-Z].+?\.', contenido, re.MULTILINE)
    descripcion = parrafos[0] if parrafos else f"Artículo sobre {titulo} - Goodman Tech Monterrey"
    
    # Limitar descripción a 155 caracteres
    if len(descripcion) > 155:
        descripcion = descripcion[:152] + "..."
    
    return {
        "title": f"{titulo} — Goodman Tech Blog",
        "description": descripcion,
        "keywords": f"{titulo}, IA empresas, Monterrey, {categoria}",
        "author": "Goodman Tech",
        "date": date.today().strftime("%Y-%m-%d"),
        "category": categoria
    }

def convertir_md_a_jsx(contenido_md):
    """Convierte Markdown a JSX de React"""
    
    # Convertir H2 a componentes
    contenido_md = re.sub(
        r'^## (.+)$',
        r'<h2 className="text-3xl font-bold mb-6 mt-12" style={{ color: DARK, fontFamily: \'"Plus Jakarta Sans", sans-serif\' }}>\1</h2>',
        contenido_md,
        flags=re.MULTILINE
    )
    
    # Convertir H3
    contenido_md = re.sub(
        r'^### (.+)$',
        r'<h3 className="text-2xl font-bold mb-4 mt-8" style={{ color: BLUE }}>\1</h3>',
        contenido_md,
        flags=re.MULTILINE
    )
    
    # Convertir negritas
    contenido_md = re.sub(r'\*\*(.+?)\*\*', r'<strong className="text-slate-900">\1</strong>', contenido_md)
    
    # Convertir listas
    contenido_md = re.sub(r'^\- (.+)$', r'<li className="mb-2">\1</li>', contenido_md, flags=re.MULTILINE)
    contenido_md = re.sub(r'^\d+\. (.+)$', r'<li className="mb-2">\1</li>', contenido_md, flags=re.MULTILINE)
    
    # Envolver listas en <ul>
    contenido_md = re.sub(r'(<li.+?</li>\n)+', r'<ul className="list-disc pl-6 mb-6 space-y-2">\n\g<0></ul>\n', contenido_md)
    
    # Convertir párrafos
    lineas = contenido_md.split('\n')
    jsx_lines = []
    for linea in lineas:
        if linea.strip() and not linea.startswith('<'):
            jsx_lines.append(f'<p className="text-lg text-slate-700 mb-4 leading-relaxed">{linea}</p>')
        else:
            jsx_lines.append(linea)
    
    return '\n'.join(jsx_lines)

def generar_tsx_blog(titulo, contenido_md, metadata, categoria):
    """Genera archivo .tsx completo del blog"""
    
    slug = slugify(titulo)
    comp_name = f"Blog{slug.replace('-', ' ').title().replace(' ', '')}"
    
    # Extraer secciones para tabla de contenidos
    secciones = extraer_secciones(contenido_md)
    
    # Convertir contenido a JSX
    contenido_jsx = convertir_md_a_jsx(contenido_md)
    
    # Generar componente React
    tsx = f"""import {{ Helmet }} from 'react-helmet-async';
import {{ Link }} from 'react-router-dom';

const DARK   = '#0F172A';
const BLUE   = '#2463eb';
const YELLOW = '#FACC15';
const GREEN  = '#4ade80';

const {comp_name} = () => {{
  const secciones = {json.dumps(secciones, ensure_ascii=False, indent=4)};

  return (
    <div className="min-h-screen" style={{ fontFamily: '"Inter", sans-serif' }}>
      <Helmet>
        <title>{metadata['title']}</title>
        <meta name="description" content="{metadata['description']}" />
        <meta name="keywords" content="{metadata['keywords']}" />
        <meta name="author" content="{metadata['author']}" />
        <meta property="og:title" content="{metadata['title']}" />
        <meta property="og:description" content="{metadata['description']}" />
        <meta property="og:type" content="article" />
        <meta property="article:published_time" content="{metadata['date']}" />
        <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800;900&family=Inter:wght@400;500;600&display=swap" rel="stylesheet" />
      </Helmet>

      {{/* Breadcrumbs */}}
      <nav className="bg-slate-50 py-4">
        <div className="max-w-4xl mx-auto px-6">
          <div className="flex items-center gap-2 text-sm text-slate-600">
            <Link to="/" className="hover:text-blue-600">Inicio</Link>
            <span>/</span>
            <Link to="/blog" className="hover:text-blue-600">Blog</Link>
            <span>/</span>
            <Link to="/blog/{categoria}" className="hover:text-blue-600">{CATEGORIAS.get(categoria, categoria)}</Link>
            <span>/</span>
            <span className="text-slate-900">{titulo}</span>
          </div>
        </div>
      </nav>

      {{/* Hero del Blog */}}
      <section className="py-16" style={{ backgroundColor: DARK }}>
        <div className="max-w-4xl mx-auto px-6">
          <div className="inline-block px-4 py-1.5 rounded-full text-sm font-semibold mb-6" style={{ backgroundColor: `${{BLUE}}20`, color: YELLOW }}>
            {CATEGORIAS.get(categoria, categoria)}
          </div>
          <h1 className="text-5xl font-black text-white mb-6 leading-tight" style={{ fontFamily: '"Plus Jakarta Sans", sans-serif' }}>
            {titulo}
          </h1>
          <div className="flex items-center gap-6 text-slate-300 text-sm">
            <span>📅 {metadata['date']}</span>
            <span>✍️ {metadata['author']}</span>
            <span>⏱️ 12 min lectura</span>
          </div>
        </div>
      </section>

      {{/* Contenido Principal */}}
      <div className="max-w-7xl mx-auto px-6 py-16">
        <div className="grid grid-cols-12 gap-12">
          
          {{/* Sidebar Izquierdo - Tabla de Contenidos */}}
          <aside className="col-span-3 hidden lg:block">
            <div className="sticky top-24">
              <h3 className="text-sm font-bold text-slate-900 mb-4 uppercase tracking-wide">En este artículo</h3>
              <ul className="space-y-2">
                {{secciones.map((seccion, idx) => (
                  <li key={{idx}}>
                    <a 
                      href={{`#seccion-${{idx}}`}}
                      className="text-sm text-slate-600 hover:text-blue-600 transition-colors block py-1"
                    >
                      {{seccion}}
                    </a>
                  </li>
                ))}}
              </ul>
            </div>
          </aside>

          {{/* Contenido del Artículo */}}
          <article className="col-span-12 lg:col-span-6">
            <div className="prose prose-lg max-w-none">
              {contenido_jsx}
            </div>

            {{/* CTA Final */}}
            <div className="mt-16 p-8 rounded-2xl" style={{ backgroundColor: `${{BLUE}}10`, border: `2px solid ${{BLUE}}` }}>
              <h3 className="text-2xl font-bold mb-4" style={{ color: DARK }}>¿Listo para implementar IA en tu empresa?</h3>
              <p className="text-slate-700 mb-6">
                Agenda un diagnóstico gratuito de 45 minutos. Identificamos los 3 procesos con mayor desperdicio y te mostramos cómo resolverlos con IA.
              </p>
              <a 
                href="https://wa.me/528126350902?text=Hola%2C%20quiero%20agendar%20un%20diagn%C3%B3stico%20gratuito"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-block px-8 py-4 rounded-full font-bold transition-all hover:scale-105"
                style={{ backgroundColor: YELLOW, color: DARK }}
              >
                Agendar diagnóstico gratuito →
              </a>
            </div>

            {{/* Tags */}}
            <div className="mt-12 flex flex-wrap gap-2">
              {{metadata['keywords'].split(', ').map(tag => (
                <span 
                  key={{tag}}
                  className="px-3 py-1 rounded-full text-sm"
                  style={{ backgroundColor: '#f1f5f9', color: '#475569' }}
                >
                  {{tag}}
                </span>
              ))}}
            </div>
          </article>

          {{/* Sidebar Derecho - Blogs Relacionados */}}
          <aside className="col-span-12 lg:col-span-3">
            <div className="sticky top-24">
              <h3 className="text-sm font-bold text-slate-900 mb-4 uppercase tracking-wide">Artículos relacionados</h3>
              <div className="space-y-4">
                {{/* Placeholder - agregar blogs relacionados */}}
                <div className="p-4 rounded-xl border border-slate-200 hover:border-blue-300 transition-colors">
                  <h4 className="font-bold text-sm mb-2">
                    <Link to="/blog" className="hover:text-blue-600">Más artículos →</Link>
                  </h4>
                </div>
              </div>
            </div>
          </aside>

        </div>
      </div>
    </div>
  );
}};

export default {comp_name};
"""
    
    return tsx, comp_name, slug

# ── FUNCIÓN PRINCIPAL ─────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("Uso: python generar_blog_openai.py \"Título del blog\" [categoria]")
        print("\nCategorías disponibles:")
        for key, val in CATEGORIAS.items():
            print(f"  - {key}: {val}")
        sys.exit(1)
    
    titulo = sys.argv[1]
    categoria = sys.argv[2] if len(sys.argv) > 2 else "ia-empresas"
    
    if categoria not in CATEGORIAS:
        print(f"⚠️  Categoría '{categoria}' no válida. Usando 'ia-empresas'")
        categoria = "ia-empresas"
    
    print("=" * 60)
    print(f"🤖 GENERADOR DE BLOGS CON OPENAI GPT-4")
    print("=" * 60)
    print(f"\n📝 Título: {titulo}")
    print(f"📁 Categoría: {CATEGORIAS[categoria]}")
    print(f"\n⏳ Generando contenido con OpenAI (esto puede tomar 30-60 seg)...\n")
    
    # Generar contenido con OpenAI
    contenido_md = generar_contenido_openai(titulo, CATEGORIAS[categoria])
    
    if not contenido_md:
        print("❌ Error al generar contenido. Abortando.")
        sys.exit(1)
    
    print(f"✅ Contenido generado: {len(contenido_md)} caracteres")
    print(f"   (~{len(contenido_md.split())} palabras)\n")
    
    # Generar metadata
    metadata = generar_metadata(titulo, contenido_md, categoria)
    
    # Generar archivo TSX
    tsx_content, comp_name, slug = generar_tsx_blog(titulo, contenido_md, metadata, categoria)
    
    # Guardar archivos
    out_dir = f"C:/Users/Dell/Documents/goodman_generator/output_blogs/{slug}"
    os.makedirs(out_dir, exist_ok=True)
    
    # Guardar TSX
    tsx_path = f"{out_dir}/{comp_name}.tsx"
    with open(tsx_path, "w", encoding="utf-8") as f:
        f.write(tsx_content)
    
    # Guardar Markdown original
    md_path = f"{out_dir}/contenido.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(contenido_md)
    
    # Guardar metadata
    meta_path = f"{out_dir}/metadata.json"
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    # Reporte final
    print("=" * 60)
    print(f"✅ BLOG GENERADO EXITOSAMENTE")
    print("=" * 60)
    print(f"\n📁 Archivos creados en: {out_dir}/")
    print(f"   → {comp_name}.tsx (componente React)")
    print(f"   → contenido.md (Markdown original)")
    print(f"   → metadata.json (SEO metadata)")
    print(f"\n📋 Pasos para activar:")
    print(f"   1. Copia {comp_name}.tsx → src/pages/blog/")
    print(f"   2. Registra en App.tsx:")
    print(f"      import {comp_name} from './pages/blog/{comp_name}';")
    print(f"      <Route path=\"/blog/{categoria}/{slug}\" element={{<{comp_name} />}} />")
    print(f"   3. git add . && git commit && git push")
    print(f"\n🌐 URL final: {BRAND['dominio']}/blog/{categoria}/{slug}")
    print(f"\n💡 Tokens usados: ~3,000-4,000 (OpenAI GPT-4)")
    print(f"   Contenido: 100% generado por IA\n")

if __name__ == "__main__":
    main()
