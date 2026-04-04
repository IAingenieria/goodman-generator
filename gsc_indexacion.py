"""
gsc_indexacion.py
Goodman Tech — Analizador de Indexación GSC
=============================================
Analiza el estado de indexación de goodmantech.com.mx
Puede usar CSVs exportados manualmente de GSC O la API oficial.

Uso:
  python gsc_indexacion.py              # lee CSVs locales si existen
  python gsc_indexacion.py --api        # usa Google Search Console API
  python gsc_indexacion.py --watch      # monitoreo continuo cada 24h
"""

import csv, json, os, time, argparse
from datetime import datetime, timedelta
from pathlib import Path

GENERATOR_PATH = Path(r"C:\Users\Dell\Documents\goodman_generator")
SITE_URL       = "https://www.goodmantech.com.mx"

# ── Leer CSVs exportados de GSC ──────────────────────────────────────────────

def leer_grafico_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def leer_problemas_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with open(path, newline="", encoding="utf-8") as f:
        filas = list(csv.DictReader(f))
    return [r for r in filas if int(r.get("Páginas", 0) or 0) > 0]

# ── Análisis principal ───────────────────────────────────────────────────────

def analizar(grafico: list[dict], problemas_crit: list[dict], problemas_no_crit: list[dict]) -> dict:
    resultado = {
        "timestamp": datetime.now().isoformat(),
        "sitio": SITE_URL,
        "indexadas": 0,
        "sin_indexar": 0,
        "total_conocidas": 0,
        "pct_indexacion": 0.0,
        "impresiones_7d": 0,
        "impresiones_30d": 0,
        "impresiones_total": 0,
        "tendencia_indexacion": "estable",
        "pico_maximo_indexadas": 0,
        "problemas_criticos": [],
        "problemas_no_criticos": [],
        "recomendaciones": [],
        "alertas": [],
        "historial": [],
    }

    if grafico:
        # Últimos valores
        ultima = grafico[-1]
        resultado["indexadas"]    = int(ultima.get("Indexadas", 0) or 0)
        resultado["sin_indexar"]  = int(ultima.get("Sin indexar", 0) or 0)
        resultado["total_conocidas"] = resultado["indexadas"] + resultado["sin_indexar"]

        if resultado["total_conocidas"] > 0:
            resultado["pct_indexacion"] = round(
                resultado["indexadas"] / resultado["total_conocidas"] * 100, 1
            )

        # Impresiones
        resultado["impresiones_7d"]    = sum(int(r.get("Impresiones", 0) or 0) for r in grafico[-7:])
        resultado["impresiones_30d"]   = sum(int(r.get("Impresiones", 0) or 0) for r in grafico[-30:])
        resultado["impresiones_total"] = sum(int(r.get("Impresiones", 0) or 0) for r in grafico)

        # Pico máximo de indexación
        resultado["pico_maximo_indexadas"] = max(
            int(r.get("Indexadas", 0) or 0) for r in grafico if r.get("Indexadas")
        )

        # Tendencia (comparar primera vs última mitad)
        mitad = len(grafico) // 2
        prom_primera = sum(int(r.get("Indexadas", 0) or 0) for r in grafico[:mitad]) / max(mitad, 1)
        prom_segunda = sum(int(r.get("Indexadas", 0) or 0) for r in grafico[mitad:]) / max(len(grafico) - mitad, 1)

        if prom_segunda > prom_primera * 1.1:
            resultado["tendencia_indexacion"] = "📈 creciendo"
        elif prom_segunda < prom_primera * 0.9:
            resultado["tendencia_indexacion"] = "📉 bajando"
        else:
            resultado["tendencia_indexacion"] = "➡️  estable"

        # Historial simplificado (semanal)
        resultado["historial"] = [
            {
                "fecha": r["Fecha"],
                "indexadas": int(r.get("Indexadas", 0) or 0),
                "sin_indexar": int(r.get("Sin indexar", 0) or 0),
                "impresiones": int(r.get("Impresiones", 0) or 0),
            }
            for r in grafico[-14:]  # últimas 2 semanas
        ]

    # Problemas críticos
    for p in problemas_crit:
        paginas = int(p.get("Páginas", 0) or 0)
        motivo  = p.get("Motivo", "")
        resultado["problemas_criticos"].append({
            "motivo": motivo,
            "fuente": p.get("Fuente", ""),
            "paginas": paginas,
            "validacion": p.get("Validación", ""),
        })

    resultado["problemas_no_criticos"] = [
        {"motivo": p.get("Motivo",""), "paginas": int(p.get("Páginas",0) or 0)}
        for p in problemas_no_crit
    ]

    # ── Recomendaciones automáticas ────────────────────────────────────────
    recs = []
    alertas = []

    for p in resultado["problemas_criticos"]:
        m = p["motivo"].lower()
        n = p["paginas"]
        if "noindex" in m:
            recs.append({
                "prioridad": "ALTA",
                "accion": f"Eliminar etiqueta noindex de {n} páginas",
                "detalle": "Estas páginas no aparecerán en Google. Revisa el código fuente de cada una.",
                "url_ayuda": "https://support.google.com/webmasters/answer/93710"
            })
        if "redirección" in m:
            recs.append({
                "prioridad": "MEDIA",
                "accion": f"Revisar {n} páginas con redirección",
                "detalle": "Verifica que sean redirecciones 301 permanentes y no cadenas de redirecciones.",
                "url_ayuda": "https://support.google.com/webmasters/answer/2721217"
            })
        if "sin indexar" in m and "descubierta" in m:
            recs.append({
                "prioridad": "ALTA",
                "accion": f"Solicitar indexación de {n} páginas descubiertas",
                "detalle": "Páginas conocidas por Google pero aún no rastreadas. Envíalas manualmente en GSC.",
                "url_ayuda": "https://support.google.com/webmasters/answer/9012289"
            })
        if "sin indexar" in m and "rastreada" in m:
            recs.append({
                "prioridad": "ALTA",
                "accion": f"Mejorar contenido de {n} páginas rastreadas pero no indexadas",
                "detalle": "Google las vio pero no las consideró suficientemente útiles. Agrega más contenido y obtén backlinks.",
                "url_ayuda": "https://developers.google.com/search/docs/crawling-indexing/fix-search-coverage-issues"
            })
        if "canónica" in m:
            recs.append({
                "prioridad": "MEDIA",
                "accion": "Agregar etiqueta canonical en páginas duplicadas",
                "detalle": 'Agrega <link rel="canonical" href="URL_PRINCIPAL"> en el <head> de cada página.',
                "url_ayuda": "https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls"
            })

    # Alerta de regresión
    if resultado["sin_indexar"] > resultado["indexadas"]:
        alertas.append("🚨 CRÍTICO: Más páginas sin indexar que indexadas. Acción inmediata requerida.")

    if resultado["pico_maximo_indexadas"] > resultado["indexadas"]:
        perdidas = resultado["pico_maximo_indexadas"] - resultado["indexadas"]
        alertas.append(f"⚠️ Perdiste {perdidas} páginas indexadas desde el pico histórico.")

    if resultado["impresiones_7d"] < 30:
        alertas.append("📉 Impresiones muy bajas esta semana. Considera agregar más contenido y keywords.")

    resultado["recomendaciones"] = recs
    resultado["alertas"] = alertas

    return resultado


def imprimir_reporte(r: dict):
    sep = "═" * 62
    print(f"\n{sep}")
    print(f"  📊 REPORTE DE INDEXACIÓN — {r['sitio']}")
    print(f"  {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print(sep)

    print(f"\n  Estado actual")
    print(f"  ├─ Páginas indexadas:     {r['indexadas']:>3}  ({r['pct_indexacion']}%)")
    print(f"  ├─ Páginas sin indexar:   {r['sin_indexar']:>3}")
    print(f"  ├─ Total conocidas:       {r['total_conocidas']:>3}")
    print(f"  └─ Tendencia:             {r['tendencia_indexacion']}")

    print(f"\n  Impresiones en Google")
    print(f"  ├─ Últimos 7 días:        {r['impresiones_7d']:>5}")
    print(f"  ├─ Últimos 30 días:       {r['impresiones_30d']:>5}")
    print(f"  └─ Total histórico:       {r['impresiones_total']:>5}")

    if r["alertas"]:
        print(f"\n  Alertas")
        for a in r["alertas"]:
            print(f"  {a}")

    if r["problemas_criticos"]:
        print(f"\n  Problemas críticos de indexación")
        for p in r["problemas_criticos"]:
            print(f"  ├─ {p['motivo']}: {p['paginas']} páginas")

    if r["recomendaciones"]:
        print(f"\n  Acciones recomendadas")
        recs_ord = sorted(r["recomendaciones"], key=lambda x: x["prioridad"])
        for rec in recs_ord:
            print(f"  [{rec['prioridad']}] {rec['accion']}")
            print(f"         {rec['detalle'][:80]}")

    print(f"\n{sep}\n")


def guardar_reporte(resultado: dict):
    path = GENERATOR_PATH / "reporte_indexacion.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)
    print(f"  💾 Reporte guardado: {path}")


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--watch", action="store_true", help="Monitoreo continuo cada 24h")
    parser.add_argument("--api",   action="store_true", help="Usar GSC API en lugar de CSVs")
    args = parser.parse_args()

    # Buscar CSVs en la carpeta del generador
    grafico_path = GENERATOR_PATH / "Gráfico.csv"
    crit_path    = GENERATOR_PATH / "Problemas_críticos.csv"
    nocrit_path  = GENERATOR_PATH / "Problemas_no_críticos.csv"

    print(f"\n🔍 Goodman Tech — Analizador de Indexación GSC")
    print(f"   Buscando CSVs en: {GENERATOR_PATH}")

    grafico       = leer_grafico_csv(grafico_path)
    prob_crit     = leer_problemas_csv(crit_path)
    prob_no_crit  = leer_problemas_csv(nocrit_path)

    print(f"   Registros de gráfico: {len(grafico)}")
    print(f"   Problemas críticos:   {len(prob_crit)}")

    resultado = analizar(grafico, prob_crit, prob_no_crit)
    imprimir_reporte(resultado)
    guardar_reporte(resultado)

    if args.watch:
        print("  🔄 Modo monitoreo activo. Próxima revisión en 24h. Ctrl+C para salir.\n")
        while True:
            time.sleep(86400)
            resultado = analizar(grafico, prob_crit, prob_no_crit)
            imprimir_reporte(resultado)
            guardar_reporte(resultado)


if __name__ == "__main__":
    main()
