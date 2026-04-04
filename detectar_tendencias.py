#!/usr/bin/env python3
"""
GOODMAN TECH — Detector de Keywords en Tendencia
=================================================
Uso:  python detectar_tendencias.py

Monitorea keywords relacionadas con IA empresarial que están subiendo
de interés en México. Cuando detecta una keyword con potencial,
la agrega a keywords.txt automáticamente y puede lanzar el generador.

Requiere: pip install pytrends requests
"""

import time
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

try:
    from pytrends.request import TrendReq
    PYTRENDS_OK = True
except ImportError:
    PYTRENDS_OK = False
    print("⚠️  pytrends no instalado. Instalar con: pip install pytrends")

# ── CONFIGURACIÓN ─────────────────────────────────────────────────────────────

# Keywords semilla — el detector busca variaciones y tendencias de estas
KEYWORDS_SEMILLA = [
    "inteligencia artificial empresa",
    "automatizacion procesos IA",
    "chatbot empresarial",
    "implementar IA empresa",
    "transformacion digital mexico",
    "reducir costos con IA",
    "IA para pymes mexico",
    "agente IA empresas",
    "Claude IA empresas",
    "copilot empresarial",
]

# Preguntas trending que se buscan en México (actualizadas manualmente)
# Estas son keywords de alto potencial SEO detectadas manualmente
KEYWORDS_TRENDING_2026 = [
    "como aplicar la IA en mi empresa",
    "que es un agente de IA para empresas",
    "cuanto cuesta implementar inteligencia artificial",
    "IA para automatizar cotizaciones",
    "como reducir costos con inteligencia artificial",
    "automatizacion de ventas con IA mexico",
    "IA para despachos juridicos mexico",
    "inteligencia artificial manufactura monterrey",
    "chatbot para whatsapp empresas mexico",
    "como prospectar clientes con IA",
    "generador de reportes con inteligencia artificial",
    "IA para recursos humanos contratacion",
    "transformacion digital sin cambiar ERP",
    "agente cotizador automatico empresas",
    "como medir el ROI de la inteligencia artificial",
    "IA para inmobiliarias mexico",
    "automatizar seguimiento de clientes CRM IA",
    "dashboard ejecutivo con inteligencia artificial",
    "IA para empresas de manufactura mexico",
    "implementar claude AI en mi empresa",
]

UMBRAL_INTERES = 40  # Score mínimo de Google Trends (0-100) para considerar trending

# ─────────────────────────────────────────────────────────────────────────────

def cargar_keywords_procesadas() -> set:
    """Lee keywords que ya fueron generadas para no repetir."""
    procesadas = set()
    output_dir = Path("output")
    if output_dir.exists():
        for folder in output_dir.iterdir():
            if folder.is_dir():
                procesadas.add(folder.name)
    return procesadas


def slugify_simple(text: str) -> str:
    import unicodedata, re
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    return text


def analizar_con_pytrends(keywords: list) -> dict:
    """Obtiene interés de Google Trends México para cada keyword."""
    if not PYTRENDS_OK:
        return {}

    print("📊 Consultando Google Trends para México...")
    pytrends = TrendReq(hl='es-MX', tz=360)  # Zona horaria CDMX
    scores = {}

    # Procesar en grupos de 5 (límite de pytrends)
    for i in range(0, len(keywords), 5):
        grupo = keywords[i:i+5]
        try:
            pytrends.build_payload(grupo, geo='MX', timeframe='today 3-m')
            data = pytrends.interest_over_time()
            if not data.empty:
                for kw in grupo:
                    if kw in data.columns:
                        scores[kw] = int(data[kw].mean())
            time.sleep(2)  # Respetar rate limits
        except Exception as e:
            print(f"   ⚠️  Error en grupo {i}: {e}")
            continue

    return scores


def detectar_keywords_oportunidad() -> list:
    """
    Detecta keywords con potencial SEO sin usar Google Trends.
    Basado en patrones de búsqueda conocidos para IA empresarial en México.
    """
    procesadas = cargar_keywords_procesadas()
    oportunidades = []

    for kw in KEYWORDS_TRENDING_2026:
        slug = slugify_simple(kw)
        if slug not in procesadas:
            oportunidades.append({
                "keyword": kw,
                "slug":    slug,
                "fuente":  "lista_curada_2026",
                "score":   75,  # Score estimado
            })

    return oportunidades


def guardar_en_keywords_txt(nuevas: list):
    """Agrega keywords nuevas al archivo de lote."""
    archivo = Path("keywords.txt")
    existentes = set()

    if archivo.exists():
        with open(archivo, "r", encoding="utf-8") as f:
            existentes = {l.strip().lower() for l in f if l.strip()}

    nuevas_unicas = [k for k in nuevas if k["keyword"].lower() not in existentes]

    if not nuevas_unicas:
        print("   ℹ️  Todas las keywords ya están en keywords.txt")
        return 0

    with open(archivo, "a", encoding="utf-8") as f:
        f.write(f"\n# Detectadas automáticamente — {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        for k in nuevas_unicas:
            f.write(f"{k['keyword']}\n")

    print(f"   ✅ {len(nuevas_unicas)} keywords nuevas agregadas a keywords.txt")
    return len(nuevas_unicas)


def reporte_oportunidades(oportunidades: list):
    """Muestra tabla de oportunidades detectadas."""
    if not oportunidades:
        print("\n   ℹ️  No hay keywords nuevas detectadas.")
        return

    print(f"\n{'─'*60}")
    print(f"{'KEYWORD':<45} {'SCORE':>6}")
    print(f"{'─'*60}")
    for op in sorted(oportunidades, key=lambda x: x['score'], reverse=True)[:20]:
        print(f"{op['keyword']:<45} {op['score']:>6}")
    print(f"{'─'*60}")


def main():
    print("\n🔍 Goodman Tech — Detector de Keywords en Tendencia")
    print("=" * 60)
    print(f"   Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"   Mercado: México\n")

    # ── Detectar oportunidades ────────────────────────────────────────────────
    print("⏳ Analizando keywords de oportunidad...")
    oportunidades = detectar_keywords_oportunidad()
    print(f"   ✅ {len(oportunidades)} keywords sin landing page detectadas\n")

    # ── Enriquecer con Google Trends si está disponible ───────────────────────
    if PYTRENDS_OK and len(oportunidades) > 0:
        kw_list = [op["keyword"] for op in oportunidades[:20]]
        scores = analizar_con_pytrends(kw_list)
        for op in oportunidades:
            if op["keyword"] in scores:
                op["score"] = scores[op["keyword"]]
        # Filtrar por umbral
        oportunidades = [op for op in oportunidades if op["score"] >= UMBRAL_INTERES]
        print(f"   📊 {len(oportunidades)} keywords con score ≥ {UMBRAL_INTERES} en Trends\n")

    # ── Mostrar reporte ───────────────────────────────────────────────────────
    reporte_oportunidades(oportunidades)

    if not oportunidades:
        print("\n✅ No hay keywords nuevas para generar en este momento.")
        return

    # ── Preguntar qué hacer ───────────────────────────────────────────────────
    print(f"\n¿Qué quieres hacer con estas {len(oportunidades)} keywords?")
    print("  [1] Agregarlas a keywords.txt y generar todas ahora")
    print("  [2] Solo agregarlas a keywords.txt (generar después)")
    print("  [3] Generar solo las top 5")
    print("  [4] Salir sin hacer nada")

    try:
        opcion = input("\nElige (1-4): ").strip()
    except (EOFError, KeyboardInterrupt):
        opcion = "4"

    if opcion == "1":
        n = guardar_en_keywords_txt(oportunidades)
        if n > 0:
            print("\n🚀 Lanzando generador en lote...")
            subprocess.run([sys.executable, "generar_lote.py"])

    elif opcion == "2":
        guardar_en_keywords_txt(oportunidades)
        print("\n✅ Keywords guardadas. Corre 'python generar_lote.py' cuando quieras.")

    elif opcion == "3":
        top5 = oportunidades[:5]
        guardar_en_keywords_txt(top5)
        print(f"\n🚀 Generando top 5 keywords...")
        for op in top5:
            subprocess.run([sys.executable, "generar_landing.py", op["keyword"]])

    else:
        print("\n   Saliendo sin cambios.")

    print("\n" + "=" * 60)
    print("💡 Tip: Corre este script cada lunes para detectar tendencias nuevas.")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
