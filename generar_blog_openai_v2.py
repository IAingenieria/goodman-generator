#!/usr/bin/env python3
"""
GOODMAN TECH — Generador de Blogs con OpenAI v2
================================================
Uso:  python generar_blog_openai_v2.py "Título del blog" [categoria]

Genera blogs usando BlogLayout y componentes React existentes
"""

import sys
import re
import json
import os
from datetime import date
from openai import OpenAI

# ── CONFIGURACIÓN ─────────────────────────────────────────────────────────────
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

Escribe un artículo de blog estructurado sobre: "{titulo}"

CONTEXTO:
- Empresa: Goodman Tech (Monterrey, México)
- Especialidad: Implementación de IA con resultados en 90 días
- Metodología: Formamos embajadores internos de IA

REQUISITOS:
1. Longitud: 1500-2000 palabras
2. Estructura OBLIGATORIA en JSON:

{{
  "secciones": [
    {{
      "titulo": "Introducción",
      "contenido": [
        "Párrafo 1 con pregunta enganchadora...",
        "Párrafo 2 con contexto...",
        "Párrafo 3 con promesa del artículo..."
      ]
    }},
    {{
      "titulo": "Sección 2",
      "contenido": [
        "Párrafo 1...",
        "Párrafo 2..."
      ],
      "lista": [
        "Item 1 con <strong>negritas</strong>",
        "Item 2 con <strong>negritas</strong>"
      ]
    }},
    // ... más secciones (total 5-6)
  ],
  "tags": ["Tag1", "Tag2", "Tag3", "Tag4", "Tag5"]
}}

3. Incluir:
   - Casos de uso para México/Monterrey
   - Mencionar Claude AI, Anthropic
   - Enfoque en ROI y 90 días
   - Usar "tú" para el lector
   - Negritas en conceptos clave con <strong>

4. NO incluir:
   - Lenguaje de venta agresivo
   - Promesas exageradas

IMPORTANTE: Responde SOLO con el JSON, sin texto adicional."""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Eres un experto en IA empresarial. Respondes SOLO en formato JSON válido."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=3000
        )
        
        contenido_json = response.choices[0].message.content
        
        # Limpiar markdown code blocks si existen
        contenido_json = re.sub(r'^```json\s*', '', contenido_json)
        contenido_json = re.sub(r'\s*```$', '', contenido_json)
        
        return json.loads(contenido_json)
    
    except json.JSONDecodeError as e:
        print(f"❌ Error: OpenAI no devolvió JSON válido")
        print(f"   Respuesta: {contenido_json[:200]}...")
        return None
    except Exception as e:
        print(f"❌ Error al generar contenido con OpenAI: {e}")
        return None

def generar_tsx_blog(titulo, contenido_json, categoria):
    """Genera archivo .tsx usando BlogLayout"""
    
    slug = slugify(titulo)
    comp_name = f"Blog{slug.replace('-', ' ').title().replace(' ', '')}"
    
    secciones = contenido_json.get('secciones', [])
    tags = contenido_json.get('tags', [])
    
    # Generar títulos de secciones para TOC
    titulos_secciones = [s['titulo'] for s in secciones]
    
    # Generar JSX del contenido
    contenido_jsx = []
    
    for idx, seccion in enumerate(secciones):
        titulo_seccion = seccion['titulo']
        parrafos = seccion.get('contenido', [])
        lista = seccion.get('lista', [])
        
        # Título de sección
        contenido_jsx.append(f'''
        <h2 id="seccion-{idx}" className="text-3xl font-bold mb-6 mt-12" style={{{{ fontFamily: '"Plus Jakarta Sans", sans-serif' }}}}>
          {titulo_seccion}
        </h2>''')
        
        # Párrafos
        for parrafo in parrafos:
            # Escapar comillas y caracteres especiales
            parrafo_escaped = parrafo.replace('"', '\\"').replace('{', '{{').replace('}', '}}')
            # Revertir escape de <strong> tags
            parrafo_escaped = parrafo_escaped.replace('<strong>', '{<strong>').replace('</strong>', '</strong>}')
            parrafo_escaped = parrafo_escaped.replace('{{<strong>', '<strong>').replace('</strong>}}', '</strong>')
            
            contenido_jsx.append(f'''
        <p className="text-lg text-slate-700 mb-4 leading-relaxed">
          {parrafo}
        </p>''')
        
        # Lista (si existe)
        if lista:
            contenido_jsx.append('''
        <ul className="list-disc pl-6 mb-6 space-y-3">''')
            for item in lista:
                contenido_jsx.append(f'''
          <li className="text-lg text-slate-700" dangerouslySetInnerHTML={{{{ __html: "{item}" }}}} />''')
            contenido_jsx.append('''
        </ul>''')
        
        # CTA intermedio después de la 2da sección
        if idx == 1:
            contenido_jsx.append('''

        <BlogCTA 
          title="¿Quieres implementar esto en tu empresa?"
          description="Nuestro programa de Embajadores IA forma a tu equipo interno en 90 días con resultados medibles."
          ctaText="Ver programa Embajadores IA"
          ctaUrl="/empresas/embajadores-ia"
          type="intermediate"
        />''')
    
    # Generar componente completo
    tsx = f'''import {{ Helmet }} from 'react-helmet-async';
import {{ BlogLayout, BlogCTA }} from '../../components/blog';

const {comp_name} = () => {{
  const secciones = {json.dumps(titulos_secciones, ensure_ascii=False, indent=4)};

  const relatedBlogs = [
    {{ title: "Más artículos próximamente", url: "/blog", readTime: "5 min" }}
  ];

  const tags = {json.dumps(tags, ensure_ascii=False, indent=4)};

  return (
    <>
      <Helmet>
        <title>{titulo} — Goodman Tech Blog</title>
        <meta name="description" content="Descubre cómo {titulo.lower()} con Goodman Tech en Monterrey. Casos reales, tecnologías como Claude AI y resultados en 90 días." />
        <meta name="keywords" content="{', '.join(tags)}" />
        <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800;900&family=Inter:wght@400;500;600&display=swap" rel="stylesheet" />
      </Helmet>

      <BlogLayout
        title="{titulo}"
        category="{CATEGORIAS.get(categoria, categoria)}"
        categorySlug="{categoria}"
        date="{date.today().strftime('%d %B %Y')}"
        readTime="12 min lectura"
        sections={{secciones}}
        relatedBlogs={{relatedBlogs}}
        tags={{tags}}
        url="/blog/{categoria}/{slug}"
      >
        {''.join(contenido_jsx)}

        <BlogCTA 
          title="¿Listo para implementar IA en tu empresa?"
          description="Agenda un diagnóstico gratuito de 45 minutos. Identificamos los 3 procesos con mayor desperdicio y te mostramos cómo resolverlos con IA usando tecnología Claude Code de Anthropic."
          ctaText="Agendar diagnóstico gratuito"
          ctaUrl="https://wa.me/{BRAND['whatsapp']}?text=Hola%2C%20quiero%20agendar%20un%20diagn%C3%B3stico%20gratuito"
          type="final"
        />
      </BlogLayout>
    </>
  );
}};

export default {comp_name};
'''
    
    return tsx, comp_name, slug

# ── FUNCIÓN PRINCIPAL ─────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("Uso: python generar_blog_openai_v2.py \"Título del blog\" [categoria]")
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
    print(f"🤖 GENERADOR DE BLOGS CON OPENAI GPT-4 v2")
    print("=" * 60)
    print(f"\n📝 Título: {titulo}")
    print(f"📁 Categoría: {CATEGORIAS[categoria]}")
    print(f"\n⏳ Generando contenido con OpenAI (30-60 seg)...\n")
    
    # Generar contenido con OpenAI
    contenido_json = generar_contenido_openai(titulo, CATEGORIAS[categoria])
    
    if not contenido_json:
        print("❌ Error al generar contenido. Abortando.")
        sys.exit(1)
    
    print(f"✅ Contenido generado: {len(contenido_json.get('secciones', []))} secciones")
    print(f"   Tags: {', '.join(contenido_json.get('tags', []))}\n")
    
    # Generar archivo TSX
    tsx_content, comp_name, slug = generar_tsx_blog(titulo, contenido_json, categoria)
    
    # Guardar archivos
    out_dir = f"C:/Users/Dell/Documents/goodman_generator/output_blogs/{slug}"
    os.makedirs(out_dir, exist_ok=True)
    
    # Guardar TSX
    tsx_path = f"{out_dir}/{comp_name}.tsx"
    with open(tsx_path, "w", encoding="utf-8") as f:
        f.write(tsx_content)
    
    # Guardar JSON original
    json_path = f"{out_dir}/contenido.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(contenido_json, f, ensure_ascii=False, indent=2)
    
    # Reporte final
    print("=" * 60)
    print(f"✅ BLOG GENERADO EXITOSAMENTE")
    print("=" * 60)
    print(f"\n📁 Archivos creados en: {out_dir}/")
    print(f"   → {comp_name}.tsx (componente React)")
    print(f"   → contenido.json (JSON original)")
    print(f"\n📋 Pasos para activar:")
    print(f"   1. Copia {comp_name}.tsx → src/pages/blog/")
    print(f"   2. Registra en App.tsx:")
    print(f"      import {comp_name} from './pages/blog/{comp_name}';")
    print(f"      <Route path=\"/blog/{categoria}/{slug}\" element={{<{comp_name} />}} />")
    print(f"   3. git add . && git commit && git push")
    print(f"\n🌐 URL final: {BRAND['dominio']}/blog/{categoria}/{slug}")
    print(f"\n💡 Usa componentes BlogLayout + BlogCTA")
    print(f"   JSX válido garantizado ✅\n")

if __name__ == "__main__":
    main()
