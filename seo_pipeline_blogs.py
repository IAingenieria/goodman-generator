#!/usr/bin/env python3
"""
GOODMAN TECH — SEO Pipeline para Blogs
========================================
Audita blogs en src/pages/blog/*.tsx y calcula Citability Score

Uso:
  python seo_pipeline_blogs.py                    # Scan + score todos los blogs
  python seo_pipeline_blogs.py --advise           # + Claude mejora blogs < 70pts
  python seo_pipeline_blogs.py --blog BlogNombre.tsx --advise  # 1 blog específico
"""

import os, sys, re, json, argparse
from pathlib import Path
from datetime import datetime

# ── Configuración ─────────────────────────────────────────────────────────────
PROYECTO_PATH = Path(r"C:\Users\Dell\CascadeProjects\Godman_Webpage\Godman_Webpage")
BLOGS_PATH = PROYECTO_PATH / "src" / "pages" / "blog"
OUTPUT_PATH = Path(__file__).parent / "seo_reports"
OUTPUT_PATH.mkdir(exist_ok=True)

ANTHROPIC_KEY = os.environ.get("ANTHROPIC_API_KEY")

# ── Funciones de análisis ────────────────────────────────────────────────────

def extraer_metadata_blog(tsx_content: str, filename: str) -> dict:
    """Extrae metadata del blog TSX"""
    metadata = {
        "archivo": filename,
        "titulo": "",
        "description": "",
        "tags": [],
        "secciones": [],
        "tiene_helmet": False,
        "tiene_geo": False,
        "tiene_faq": False,
        "definiciones_rag": [],
        "citability_score": 0
    }
    
    # Título (de Helmet)
    title_match = re.search(r'<title>(.+?)</title>', tsx_content)
    if title_match:
        metadata["titulo"] = title_match.group(1)
        metadata["tiene_helmet"] = True
    
    # Description
    desc_match = re.search(r'<meta name="description" content="(.+?)"', tsx_content)
    if desc_match:
        metadata["description"] = desc_match.group(1)
    
    # Tags
    tags_match = re.search(r'const tags = \[(.*?)\]', tsx_content, re.DOTALL)
    if tags_match:
        tags_str = tags_match.group(1)
        metadata["tags"] = re.findall(r'"([^"]+)"', tags_str)
    
    # Secciones (h2)
    secciones = re.findall(r'<h2[^>]*>(.+?)</h2>', tsx_content)
    metadata["secciones"] = secciones
    
    # Definiciones RAG (id="def-{slug}")
    definiciones = re.findall(r'id="def-([^"]+)"', tsx_content)
    metadata["definiciones_rag"] = definiciones
    metadata["tiene_geo"] = len(definiciones) > 0
    
    # FAQ (schema o sección)
    metadata["tiene_faq"] = bool(re.search(r'FAQPage|<h2[^>]*>FAQ|Preguntas Frecuentes', tsx_content, re.I))
    
    return metadata

def calcular_citability_score(metadata: dict) -> int:
    """
    Calcula Citability Score 0-100 para blogs
    Similar al de landings pero adaptado para contenido informativo
    """
    score = 0
    
    # 1. Helmet y meta tags básicos (20 pts)
    if metadata["tiene_helmet"]:
        score += 10
    if metadata["description"] and len(metadata["description"]) > 100:
        score += 10
    
    # 2. Tags SEO (10 pts)
    if len(metadata["tags"]) >= 5:
        score += 10
    elif len(metadata["tags"]) >= 3:
        score += 5
    
    # 3. Estructura de contenido (20 pts)
    num_secciones = len(metadata["secciones"])
    if num_secciones >= 5:
        score += 20
    elif num_secciones >= 3:
        score += 15
    elif num_secciones >= 1:
        score += 10
    
    # 4. Sección GEO - Definiciones RAG-citables (30 pts) ⭐ CRÍTICO
    num_definiciones = len(metadata["definiciones_rag"])
    if num_definiciones >= 3:
        score += 30
    elif num_definiciones >= 2:
        score += 20
    elif num_definiciones >= 1:
        score += 10
    
    # 5. FAQ Schema (20 pts)
    if metadata["tiene_faq"]:
        score += 20
    
    metadata["citability_score"] = min(score, 100)
    return score

def escanear_blogs() -> list[dict]:
    """Escanea todos los blogs y calcula scores"""
    if not BLOGS_PATH.exists():
        print(f"❌ No se encontró directorio de blogs: {BLOGS_PATH}")
        return []
    
    blogs = []
    archivos = list(BLOGS_PATH.glob("Blog*.tsx"))
    
    print(f"\n🔍 Escaneando {len(archivos)} blogs...\n")
    
    for archivo in archivos:
        try:
            contenido = archivo.read_text(encoding="utf-8")
            metadata = extraer_metadata_blog(contenido, archivo.name)
            score = calcular_citability_score(metadata)
            blogs.append(metadata)
            
            # Emoji según score
            if score >= 70:
                emoji = "✅"
            elif score >= 50:
                emoji = "⚠️"
            else:
                emoji = "❌"
            
            print(f"{emoji} {score:3d}/100  {archivo.name[:50]}")
            
        except Exception as e:
            print(f"❌ Error procesando {archivo.name}: {e}")
    
    return blogs

def generar_reporte(blogs: list[dict]) -> dict:
    """Genera reporte JSON con estadísticas"""
    total = len(blogs)
    if total == 0:
        return {}
    
    scores = [b["citability_score"] for b in blogs]
    promedio = sum(scores) / total
    
    # Clasificar por score
    excelentes = [b for b in blogs if b["citability_score"] >= 70]
    buenos = [b for b in blogs if 50 <= b["citability_score"] < 70]
    malos = [b for b in blogs if b["citability_score"] < 50]
    
    # Problemas comunes
    sin_geo = [b for b in blogs if not b["tiene_geo"]]
    sin_faq = [b for b in blogs if not b["tiene_faq"]]
    
    reporte = {
        "fecha": datetime.now().isoformat(),
        "total_blogs": total,
        "promedio_score": round(promedio, 1),
        "distribucion": {
            "excelentes_70+": len(excelentes),
            "buenos_50-69": len(buenos),
            "malos_0-49": len(malos)
        },
        "problemas": {
            "sin_seccion_geo": len(sin_geo),
            "sin_faq": len(sin_faq)
        },
        "blogs": blogs
    }
    
    return reporte

def guardar_reporte(reporte: dict):
    """Guarda reporte JSON"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archivo = OUTPUT_PATH / f"blog_audit_{timestamp}.json"
    
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(reporte, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Reporte guardado: {archivo}")
    return archivo

def mostrar_resumen(reporte: dict):
    """Muestra resumen en consola"""
    print("\n" + "="*60)
    print("📊 RESUMEN DE AUDITORÍA SEO - BLOGS")
    print("="*60)
    print(f"Total blogs:        {reporte['total_blogs']}")
    print(f"Score promedio:     {reporte['promedio_score']}/100")
    print(f"\nDistribución:")
    print(f"  ✅ Excelentes (70+):  {reporte['distribucion']['excelentes_70+']}")
    print(f"  ⚠️  Buenos (50-69):    {reporte['distribucion']['buenos_50-69']}")
    print(f"  ❌ Malos (0-49):      {reporte['distribucion']['malos_0-49']}")
    print(f"\nProblemas detectados:")
    print(f"  Sin sección GEO:    {reporte['problemas']['sin_seccion_geo']}")
    print(f"  Sin FAQ:            {reporte['problemas']['sin_faq']}")
    print("="*60)
    
    # Recomendaciones
    if reporte['problemas']['sin_seccion_geo'] > 0:
        print("\n⚠️  CRÍTICO: Blogs sin sección GEO (definiciones RAG-citables)")
        print("   → Regenerar con generar_blog_openai_v2.py actualizado")
    
    if reporte['promedio_score'] < 70:
        print(f"\n⚠️  Score promedio bajo ({reporte['promedio_score']}/100)")
        print("   → Ejecutar: python seo_pipeline_blogs.py --advise")

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Auditoría SEO para blogs")
    parser.add_argument("--advise", action="store_true", help="Usar Claude para mejorar blogs < 70pts")
    parser.add_argument("--blog", type=str, help="Auditar un blog específico")
    args = parser.parse_args()
    
    print("\n🤖 GOODMAN TECH — SEO Pipeline para Blogs")
    print("="*60)
    
    # Escanear blogs
    blogs = escanear_blogs()
    
    if not blogs:
        print("❌ No se encontraron blogs para auditar")
        return
    
    # Generar reporte
    reporte = generar_reporte(blogs)
    
    # Mostrar resumen
    mostrar_resumen(reporte)
    
    # Guardar reporte
    guardar_reporte(reporte)
    
    # Advise con Claude (futuro)
    if args.advise:
        print("\n⚠️  Función --advise aún no implementada")
        print("   Por ahora: regenerar blogs con generar_blog_openai_v2.py actualizado")

if __name__ == "__main__":
    main()
