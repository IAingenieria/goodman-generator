"""
generar_lote.py  (versión Ambassador)
Goodman Tech — Generador en lote con integración SEO
======================================================
Lee keywords.txt y keywords_blog.txt generados por
detectar_keywords_ambassador.py y ejecuta generar_landing.py
para cada una.

Uso:
  python generar_lote.py                    # procesa keywords.txt
  python generar_lote.py --blog             # procesa keywords_blog.txt
  python generar_lote.py --auto-detectar   # detecta keywords primero, luego genera
  python generar_lote.py --limite 5        # solo las primeras 5
"""

import os, time, subprocess, argparse
from pathlib import Path
from datetime import datetime

GENERATOR_PATH  = Path(r"C:\Users\Dell\Documents\goodman_generator")
PROYECTO_PATH   = Path(r"C:\Users\Dell\CascadeProjects\Godman_Webpage\Godman_Webpage")
LANDING_SCRIPT  = GENERATOR_PATH / "generar_landing.py"
KEYWORDS_FILE   = GENERATOR_PATH / "keywords.txt"
KEYWORDS_BLOG   = GENERATOR_PATH / "keywords_blog.txt"
PAUSA_SEGUNDOS  = 2.0  # entre keywords para no saturar API

def leer_keywords(path: Path) -> list[str]:
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

def generar(keyword: str, tipo: str = "landing") -> bool:
    print(f"\n  🔧 Generando {tipo}: {keyword}")
    try:
        result = subprocess.run(
            ["python", str(LANDING_SCRIPT), keyword],
            cwd=str(GENERATOR_PATH),
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0:
            print(f"  ✅ OK")
            return True
        else:
            print(f"  ❌ Error: {result.stderr[-200:]}")
            return False
    except subprocess.TimeoutExpired:
        print(f"  ⏱️  Timeout al generar: {keyword}")
        return False
    except Exception as e:
        print(f"  ❌ Excepción: {e}")
        return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--blog",           action="store_true", help="Procesar keywords_blog.txt")
    parser.add_argument("--auto-detectar",  action="store_true", help="Detectar keywords antes de generar")
    parser.add_argument("--limite",         type=int, default=0, help="Máximo de keywords a procesar")
    args = parser.parse_args()

    print(f"\n🚀 Goodman Tech — Generador en Lote (Ambassador)")
    print(f"   {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")

    # Auto-detectar si se solicita
    if args.auto_detectar:
        print("  🔍 Detectando keywords con Ambassador module...")
        subprocess.run(
            ["python", str(GENERATOR_PATH / "detectar_keywords_ambassador.py"), "--auto"],
            cwd=str(GENERATOR_PATH)
        )

    # Seleccionar archivo
    archivo = KEYWORDS_BLOG if args.blog else KEYWORDS_FILE
    tipo    = "blog" if args.blog else "landing"
    keywords = leer_keywords(archivo)

    if not keywords:
        print(f"  ⚠️  No se encontraron keywords en {archivo}")
        print(f"      Corre primero: python detectar_keywords_ambassador.py")
        return

    if args.limite:
        keywords = keywords[:args.limite]

    print(f"  📋 {len(keywords)} keywords de tipo '{tipo}' a procesar")
    print(f"  📁 Archivo: {archivo}\n")

    exitosas, fallidas = [], []

    for i, kw in enumerate(keywords, 1):
        print(f"  [{i}/{len(keywords)}] ", end="")
        ok = generar(kw, tipo)
        if ok:
            exitosas.append(kw)
        else:
            fallidas.append(kw)
        if i < len(keywords):
            time.sleep(PAUSA_SEGUNDOS)

    # Reporte final
    print(f"\n{'═'*50}")
    print(f"  RESUMEN")
    print(f"  ✅ Exitosas: {len(exitosas)}")
    print(f"  ❌ Fallidas: {len(fallidas)}")
    if fallidas:
        print(f"\n  Keywords fallidas:")
        for kw in fallidas:
            print(f"    - {kw}")
    print(f"{'═'*50}\n")

    # Guardar fallidas para reintentar
    if fallidas:
        retry_path = GENERATOR_PATH / "keywords_retry.txt"
        with open(retry_path, "w", encoding="utf-8") as f:
            f.write("\n".join(fallidas))
        print(f"  💾 Fallidas guardadas en: {retry_path}")

    # Auto-actualizar sitemap después de generar landings
    if exitosas:
        print(f"\n  🗺️  Actualizando sitemap...")
        sitemap_script = GENERATOR_PATH / "actualizar_sitemap.py"
        if sitemap_script.exists():
            try:
                subprocess.run(["python", str(sitemap_script), "--ping"],
                               cwd=str(GENERATOR_PATH), timeout=30)
                print(f"  ✅ Sitemap actualizado y Google notificado")
            except Exception as e:
                print(f"  ⚠️  Error actualizando sitemap: {e}")

if __name__ == "__main__":
    main()
