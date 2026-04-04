"""
actualizar_sitemap.py
Goodman Tech — Actualizador automático de sitemap
==================================================
Lee todas las rutas de App.tsx, genera sitemap.xml actualizado
y notifica a Google Search Console.

Uso:
  python actualizar_sitemap.py          # actualiza sitemap
  python actualizar_sitemap.py --ping   # actualiza + notifica a Google
"""

import re, requests
from pathlib import Path
from datetime import datetime

PROYECTO_PATH = Path(r"C:\Users\Dell\CascadeProjects\Godman_Webpage\Godman_Webpage")
SITE_URL      = "https://www.goodmantech.com.mx"
SITEMAP_PATH  = PROYECTO_PATH / "public" / "sitemap.xml"
APP_TSX       = PROYECTO_PATH / "src" / "App.tsx"

# Prioridades por tipo de página
PRIORIDADES = {
    "/":           ("1.0", "weekly"),
    "/contacto":   ("0.9", "monthly"),
    "/nosotros":   ("0.9", "monthly"),
    "/empresas/":  ("0.85", "monthly"),
    "/caso-":      ("0.80", "monthly"),
    "/blog/":      ("0.75", "monthly"),
}

def get_prioridad(path: str) -> tuple:
    for key, val in PRIORIDADES.items():
        if key in path:
            return val
    return ("0.7", "monthly")

def extraer_rutas_app() -> list[str]:
    """Lee App.tsx y extrae todos los path= de las rutas."""
    content = APP_TSX.read_text(encoding="utf-8")
    rutas = re.findall(r'path="([^"]+)"', content)
    # Filtrar rutas de sistema
    excluir = ["*", "/leads", "/admin", "/login", "/dashboard",
                "/diagnostico", "/formulario", "/thank-you", "/leads_instantly"]
    return [r for r in rutas if not any(e in r for e in excluir)]

def generar_sitemap(rutas: list[str]) -> str:
    hoy = datetime.now().strftime("%Y-%m-%d")
    urls = []

    for ruta in rutas:
        prioridad, freq = get_prioridad(ruta)
        url_completa = f"{SITE_URL}{ruta}"
        urls.append(f"""  <url>
    <loc>{url_completa}</loc>
    <lastmod>{hoy}</lastmod>
    <changefreq>{freq}</changefreq>
    <priority>{prioridad}</priority>
  </url>""")

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>"""

def notificar_google(sitemap_url: str):
    """Ping a Google para que reindexe el sitemap."""
    ping_url = f"https://www.google.com/ping?sitemap={sitemap_url}"
    try:
        r = requests.get(ping_url, timeout=10)
        if r.status_code == 200:
            print(f"✅ Google notificado correctamente")
        else:
            print(f"⚠️ Google respondió: {r.status_code}")
    except Exception as e:
        print(f"❌ Error notificando a Google: {e}")

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--ping", action="store_true", help="Notificar a Google después de actualizar")
    args = parser.parse_args()

    print(f"\n🗺️  Goodman Tech — Actualizador de Sitemap")
    print(f"   {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")

    # Extraer rutas
    rutas = extraer_rutas_app()
    print(f"   Rutas encontradas en App.tsx: {len(rutas)}")

    # Generar sitemap
    sitemap = generar_sitemap(rutas)
    SITEMAP_PATH.write_text(sitemap, encoding="utf-8")
    print(f"   ✅ Sitemap generado: {SITEMAP_PATH}")
    print(f"   URLs incluidas: {len(rutas)}")

    # Notificar a Google
    sitemap_url = f"{SITE_URL}/sitemap.xml"
    if args.ping:
        notificar_google(sitemap_url)

    print(f"\n   📋 Siguiente paso:")
    print(f"   Ve a GSC → Sitemaps → pega: {sitemap_url}")
    print(f"   Haz commit y push del sitemap actualizado\n")

if __name__ == "__main__":
    main()
