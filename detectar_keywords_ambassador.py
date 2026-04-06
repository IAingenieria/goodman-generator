"""
detectar_keywords_ambassador.py  (v3 — SerpApi + Claude API)
Goodman Tech — Módulo SEO Ambassador
======================================
Fuentes de keywords (en orden de prioridad):

  NUEVAS EN v3:
  4. SerpApi → google_autocomplete   keywords reales del buscador MX
  5. SerpApi → related_searches      búsquedas relacionadas reales
  6. SerpApi → people_also_ask       preguntas reales de usuarios
  7. Claude API → investigación      gaps, clusters, ángulos, prioridades

  CONSERVADAS DE v1/v2:
  1. Google Search Console API  → queries reales de tu sitio
  2. Google Suggest público      → autocompletado (sin API key)
  3. Google Trends (pytrends)   → tendencias por región MX

Salida:
  keywords.txt            → landings comerciales → generar_lote.py
  keywords_blog.txt       → artículos informativos
  reporte_seo.json        → datos completos con scores por fuente
  analisis_claude.json    → análisis estratégico de Claude

Uso:
  python detectar_keywords_ambassador.py              # interactivo
  python detectar_keywords_ambassador.py --auto       # sin prompts
  python detectar_keywords_ambassador.py --top 10     # guarda top 10
  python detectar_keywords_ambassador.py --csv        # exporta CSV
  python detectar_keywords_ambassador.py --solo-claude  # solo Claude analiza
  python detectar_keywords_ambassador.py --solo-serpapi # solo SerpApi
"""

import os, json, time, re, csv, argparse, requests
from datetime import datetime, timedelta
from pathlib import Path

# ── Configuración ─────────────────────────────────────────────────────────────
PROYECTO_PATH   = Path(r"C:\Users\Dell\CascadeProjects\Godman_Webpage\Godman_Webpage")
GENERATOR_PATH  = Path(r"C:\Users\Dell\Documents\goodman_generator")
GSC_CREDENTIALS = GENERATOR_PATH / "gsc_credentials.json"
GSC_TOKEN       = GENERATOR_PATH / "gsc_token.json"
SITE_URL        = "https://www.goodmantech.com.mx"

SERPAPI_KEY  = os.environ.get("SERPAPI_KEY")
ANTHROPIC_KEY= os.environ.get("ANTHROPIC_API_KEY")
CLAUDE_MODEL = "claude-sonnet-4-6"

# Seeds para todas las fuentes
SEEDS_AMBASSADOR = [
    "inteligencia artificial para empresas",
    "IA en manufactura",
    "automatización con IA",
    "consultoría IA México",
    "IA para pymes México",
    "implementar IA en empresa",
    "machine learning empresas monterrey",
    "chatbot para empresas",
    "IA recursos humanos",
    "IA cadena de suministro",
    "mantenimiento predictivo IA",
    "IA control de calidad",
    "transformación digital monterrey",
    "IA ventas empresas",
    "IA logística México",
]

PALABRAS_LANDING = ["implementar","contratar","costo","precio","empresa","solución",
                    "consultoría","servicio","agencia","proveedor","cotizar","monterrey",
                    "nuevo leon","noreste","manufactura","industrial","planta"]
PALABRAS_BLOG    = ["qué es","cómo funciona","para qué","beneficios","ventajas",
                    "diferencia","guía","tutorial","ejemplos","casos de uso","tendencias"]
PALABRAS_EXCLUIR = ["gratis","free","crack","pirata","descargar","torrent","curso gratis"]


# ── Helpers ───────────────────────────────────────────────────────────────────

def log(msg: str, nivel: str = "INFO"):
    colores = {
        "INFO":   "\033[94m",
        "OK":     "\033[92m",
        "WARN":   "\033[93m",
        "ERR":    "\033[91m",
        "CLAUDE": "\033[95m",
    }
    print(f"{colores.get(nivel,'')}{datetime.now().strftime('%H:%M:%S')} [{nivel}] {msg}\033[0m")

def limpiar_query(q: str) -> str:
    return re.sub(r'\s+', ' ', q.strip().lower())

def clasificar_intencion(query: str) -> str:
    q = query.lower()
    if any(p in q for p in PALABRAS_LANDING): return "landing"
    if any(p in q for p in PALABRAS_BLOG):    return "blog"
    if q.startswith(("qué","cómo","por qué","cuál","cuándo","dónde")): return "blog"
    return "landing"

def score_keyword(query: str, impresiones: int = 0, posicion: float = 0,
                  es_nueva: bool = False, tendencia: float = 0, fuente_peso: int = 0) -> int:
    score = 0
    palabras = len(query.split())
    if 4 <= palabras <= 8:   score += 25
    elif palabras == 3:       score += 15
    elif palabras > 8:        score += 10
    if impresiones > 0:       score += min(impresiones * 2, 30)
    if 10 < posicion <= 30:   score += 20
    elif posicion <= 10:      score += 10
    if es_nueva:              score += 15
    if any(p in query.lower() for p in PALABRAS_LANDING): score += 15
    score += min(int(tendencia / 10), 10)
    score += fuente_peso
    return min(score, 100)

def serpapi_get(params: dict) -> dict:
    params["api_key"] = SERPAPI_KEY
    try:
        r = requests.get("https://serpapi.com/search", params=params, timeout=15)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        log(f"SerpApi error: {e}", "ERR")
        return {}


# ══════════════════════════════════════════════════════════════════════════════
# FUENTE 4 — SerpApi Autocomplete (keywords 100% reales de Google MX)
# ══════════════════════════════════════════════════════════════════════════════

def fuente_serpapi_autocomplete(seeds: list[str]) -> list[dict]:
    """
    Llama a google_autocomplete de SerpApi para cada seed.
    Las sugerencias son exactamente lo que Google muestra en tiempo real
    a usuarios en México — no hay inventos ni estimaciones.
    """
    resultados = []
    vistos = set()

    for seed in seeds:
        data = serpapi_get({
            "engine": "google_autocomplete",
            "q":      seed,
            "hl":     "es",
            "gl":     "mx",
        })
        for sug in data.get("suggestions", []):
            valor = sug.get("value", "")
            if not valor or sug.get("type") == "QUERY_EXPANSION":
                continue
            q = limpiar_query(valor)
            if q in vistos or len(q.split()) < 3: continue
            if any(p in q for p in PALABRAS_EXCLUIR): continue
            vistos.add(q)
            resultados.append({
                "query":       q,
                "fuente":      "SerpApi Autocomplete",
                "impresiones": 0, "posicion": 0, "clics": 0,
                "es_nueva":    True, "tendencia": 0,
                "intencion":   clasificar_intencion(q),
                "score":       score_keyword(q, fuente_peso=20),
            })
        time.sleep(0.5)

    log(f"SerpApi Autocomplete: {len(resultados)} keywords reales de Google MX", "OK")
    return resultados


# ══════════════════════════════════════════════════════════════════════════════
# FUENTE 5 & 6 — SerpApi Related Searches + People Also Ask
# ══════════════════════════════════════════════════════════════════════════════

def fuente_serpapi_related(seeds: list[str]) -> list[dict]:
    """
    Búsquedas relacionadas y preguntas reales de usuarios en Google MX.
    People Also Ask es especialmente valioso para FAQs en landing pages.
    """
    resultados = []
    vistos = set()

    for seed in seeds:
        data = serpapi_get({
            "engine": "google",
            "q":      seed,
            "hl":     "es",
            "gl":     "mx",
            "num":    10,
        })

        # Related searches
        for item in data.get("related_searches", []):
            q = limpiar_query(item.get("query", ""))
            if q and q not in vistos and len(q.split()) >= 3:
                if not any(p in q for p in PALABRAS_EXCLUIR):
                    vistos.add(q)
                    resultados.append({
                        "query":       q,
                        "fuente":      "SerpApi Related Searches",
                        "impresiones": 0, "posicion": 0, "clics": 0,
                        "es_nueva":    True, "tendencia": 0,
                        "intencion":   clasificar_intencion(q),
                        "score":       score_keyword(q, fuente_peso=25),
                    })

        # People Also Ask — preguntas reales → ideales para FAQs y blog
        for item in data.get("related_questions", []):
            q = limpiar_query(item.get("question", ""))
            if q and q not in vistos and len(q.split()) >= 3:
                vistos.add(q)
                resultados.append({
                    "query":       q,
                    "fuente":      "SerpApi People Also Ask",
                    "impresiones": 0, "posicion": 0, "clics": 0,
                    "es_nueva":    True, "tendencia": 0,
                    "intencion":   "blog",  # preguntas → blog/FAQ
                    "score":       score_keyword(q, fuente_peso=30),
                })
        time.sleep(1.0)

    log(f"SerpApi Related+PAA: {len(resultados)} búsquedas relacionadas reales", "OK")
    return resultados


# ══════════════════════════════════════════════════════════════════════════════
# FUENTE 7 — Claude API como investigador SEO estratégico
# ══════════════════════════════════════════════════════════════════════════════

def fuente_claude_investigacion(keywords_encontradas: list[dict]) -> dict:
    """
    Claude recibe el corpus completo de keywords reales encontradas
    por todas las otras fuentes y hace 4 cosas que ninguna API puede hacer:

    1. GAPS — detecta temas que nadie cubrió pero son relevantes para Goodman Tech
    2. CLUSTERS — agrupa en arquitectura temática para el sitio
    3. PRIORIZACIÓN — selecciona las 10 mejores con justificación estratégica
    4. ÁNGULO — define el enfoque de cada landing (a quién le habla, qué problema resuelve)

    Claude no inventa volúmenes ni datos — trabaja sobre datos reales de Google
    y aporta inteligencia estratégica que los algoritmos no pueden dar.
    """
    if not ANTHROPIC_KEY:
        log("ANTHROPIC_API_KEY no configurada — saltando análisis Claude.", "WARN")
        log("Configura: set ANTHROPIC_API_KEY=sk-ant-...", "WARN")
        return {}

    try:
        import anthropic
    except ImportError:
        log("anthropic no instalado. pip install anthropic", "WARN")
        return {}

    client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)

    # Mandamos las top 40 para no gastar tokens innecesariamente
    top_kw = sorted(keywords_encontradas, key=lambda x: x["score"], reverse=True)[:40]
    keywords_txt = "\n".join(
        f"- [{k['score']}pts | {k['fuente']}] {k['query']} → {k['intencion']}"
        for k in top_kw
    )

    prompt = f"""Eres un experto en SEO B2B para empresas de tecnología en México.

CONTEXTO DE LA EMPRESA:
- Nombre: Goodman Tech
- Sitio: {SITE_URL}
- Sede: Monterrey, Nuevo León
- Servicio: Implementación de Inteligencia Artificial en empresas mexicanas
- Propuesta de valor: "Implementamos IA en tu empresa con resultados medibles en 90 días"
- Sectores objetivo: manufactura (especialmente automotriz), logística, retail, RH, finanzas
- Diferenciador: equipo local en Monterrey, conoce el clúster industrial del noreste

KEYWORDS REALES DETECTADAS EN GOOGLE MX (ordenadas por score):
{keywords_txt}

Tu tarea: analizar estas keywords reales y responder con inteligencia estratégica.

Responde ÚNICAMENTE con JSON válido, sin texto adicional ni backticks:

{{
  "gaps_detectados": [
    {{
      "keyword": "keyword concreta que falta cubrir (long tail 4-7 palabras)",
      "razon": "por qué es valiosa específicamente para Goodman Tech",
      "intencion": "landing",
      "urgencia": "alta"
    }}
  ],
  "clusters": [
    {{
      "nombre": "Nombre del cluster temático",
      "descripcion": "Qué agrupa este cluster y por qué tiene sentido en la arquitectura del sitio",
      "keywords": ["keyword1 del cluster", "keyword2 del cluster"],
      "url_sugerida": "/empresas/slug-del-cluster",
      "potencial": "alto"
    }}
  ],
  "top_10_priorizadas": [
    {{
      "keyword": "keyword exacta tal como aparece arriba",
      "score_claude": 85,
      "justificacion": "Por qué esta keyword específicamente para Goodman Tech en este momento",
      "angulo_landing": "A quién le habla esta landing, qué problema resuelve, qué objeción derriba",
      "intencion": "landing",
      "tiempo_estimado_ranking": "2-4 meses"
    }}
  ],
  "recomendaciones_estrategicas": [
    "Recomendación concreta y accionable para Goodman Tech"
  ]
}}"""

    log("Claude API — analizando corpus de keywords reales...", "CLAUDE")

    try:
        response = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=2500,
            messages=[{"role": "user", "content": prompt}]
        )
        raw = response.content[0].text.strip()
        raw = re.sub(r"^```json\s*", "", raw)
        raw = re.sub(r"^```\s*",     "", raw)
        raw = re.sub(r"\s*```$",     "", raw)

        analisis = json.loads(raw)

        n_gaps     = len(analisis.get("gaps_detectados", []))
        n_clusters = len(analisis.get("clusters", []))
        n_top      = len(analisis.get("top_10_priorizadas", []))
        log(f"Claude: {n_gaps} gaps · {n_clusters} clusters · {n_top} priorizadas", "CLAUDE")
        return analisis

    except json.JSONDecodeError as e:
        log(f"Claude devolvió JSON inválido: {e}", "ERR")
        return {}
    except Exception as e:
        log(f"Claude API error: {e}", "ERR")
        return {}


def enriquecer_con_claude(keywords: list[dict], analisis: dict) -> list[dict]:
    """
    Aplica el score y ángulo de Claude a las keywords existentes,
    y agrega las keywords de gaps que Claude detectó como nuevas oportunidades.
    """
    if not analisis:
        return keywords

    score_map  = {k["keyword"].lower(): k.get("score_claude", 0)   for k in analisis.get("top_10_priorizadas", [])}
    angulo_map = {k["keyword"].lower(): k.get("angulo_landing", "") for k in analisis.get("top_10_priorizadas", [])}
    tiempo_map = {k["keyword"].lower(): k.get("tiempo_estimado_ranking", "") for k in analisis.get("top_10_priorizadas", [])}

    for k in keywords:
        kl = k["query"].lower()
        if kl in score_map:
            k["score_claude"]             = score_map[kl]
            k["angulo_landing"]           = angulo_map.get(kl, "")
            k["tiempo_estimado_ranking"]  = tiempo_map.get(kl, "")
            k["score"]                    = max(k["score"], score_map[kl])

    # Agregar gaps que Claude detectó y no estaban en ninguna fuente
    existentes = {k["query"].lower() for k in keywords}
    for gap in analisis.get("gaps_detectados", []):
        q = gap["keyword"].lower()
        if q not in existentes:
            score_gap = 80 if gap.get("urgencia") == "alta" else 65
            keywords.append({
                "query":                   gap["keyword"],
                "fuente":                  "Claude Gap Analysis",
                "impresiones":             0,
                "posicion":                0,
                "clics":                   0,
                "es_nueva":                True,
                "tendencia":               0,
                "intencion":               gap.get("intencion", "landing"),
                "score":                   score_gap,
                "score_claude":            score_gap,
                "angulo_landing":          gap.get("razon", ""),
                "tiempo_estimado_ranking": "",
            })
            existentes.add(q)

    return keywords


# ══════════════════════════════════════════════════════════════════════════════
# FUENTES CONSERVADAS — GSC, Suggest, Trends
# ══════════════════════════════════════════════════════════════════════════════

def obtener_gsc_keywords(dias: int = 28) -> list[dict]:
    try:
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build
    except ImportError:
        log("pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client", "WARN")
        return []

    SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]
    creds = None
    if GSC_TOKEN.exists():
        creds = Credentials.from_authorized_user_file(str(GSC_TOKEN), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        elif GSC_CREDENTIALS.exists():
            flow = InstalledAppFlow.from_client_secrets_file(str(GSC_CREDENTIALS), SCOPES)
            creds = flow.run_local_server(port=0)
        else:
            log(f"No se encontró gsc_credentials.json. Ver README.", "WARN")
            return []
        with open(GSC_TOKEN, "w") as f:
            f.write(creds.to_json())

    service    = build("searchconsole", "v1", credentials=creds)
    end_date   = datetime.now() - timedelta(days=3)
    start_date = end_date - timedelta(days=dias)
    prev_start = start_date - timedelta(days=dias)
    prev_end   = start_date - timedelta(days=1)

    def query_gsc(start, end):
        try:
            resp = service.searchanalytics().query(
                siteUrl=SITE_URL,
                body={
                    "startDate":  start.strftime("%Y-%m-%d"),
                    "endDate":    end.strftime("%Y-%m-%d"),
                    "dimensions": ["query"],
                    "rowLimit":   200,
                }
            ).execute()
            return {r["keys"][0]: r for r in resp.get("rows", [])}
        except Exception as e:
            log(f"GSC error: {e}", "ERR")
            return {}

    log("Consultando Google Search Console API...")
    actual   = query_gsc(start_date, end_date)
    anterior = query_gsc(prev_start, prev_end)
    resultados = []

    for query, data in actual.items():
        impr    = data.get("impressions", 0)
        impr_a  = anterior.get(query, {}).get("impressions", 0)
        pos     = data.get("position", 99)
        clics   = data.get("clicks", 0)
        es_nueva = query not in anterior
        crecio   = impr_a > 0 and impr >= impr_a * 1.5

        if len(query.split()) < 3: continue
        if impr < 3:               continue
        if pos > 40:               continue
        if any(p in query.lower() for p in PALABRAS_EXCLUIR): continue
        if not (es_nueva or crecio): continue

        resultados.append({
            "query":       query,
            "fuente":      "Google Search Console",
            "impresiones": impr,
            "posicion":    round(pos, 1),
            "clics":       clics,
            "es_nueva":    es_nueva,
            "tendencia":   0,
            "intencion":   clasificar_intencion(query),
            "score":       score_keyword(query, impr, pos, es_nueva, fuente_peso=30),
        })

    log(f"GSC: {len(resultados)} queries nuevas/en crecimiento", "OK")
    return resultados


def obtener_suggest_publico(seeds: list[str]) -> list[dict]:
    resultados = []
    vistos = set()

    def suggest(q):
        try:
            r = requests.get(
                "https://suggestqueries.google.com/complete/search",
                params={"client":"firefox","q":q,"hl":"es","gl":"mx"},
                timeout=8, headers={"User-Agent":"Mozilla/5.0"}
            )
            return r.json()[1] if r.status_code == 200 else []
        except:
            return []

    for seed in seeds:
        sug = suggest(seed)
        for letra in "abcdefghijklmnoprstuvwxyz":
            sug += suggest(f"{seed} {letra}")
            time.sleep(0.1)
        for q in sug:
            q = limpiar_query(q)
            if q in vistos or len(q.split()) < 3: continue
            if any(p in q for p in PALABRAS_EXCLUIR): continue
            vistos.add(q)
            resultados.append({
                "query":       q,
                "fuente":      "Google Suggest",
                "impresiones": 0, "posicion": 0, "clics": 0,
                "es_nueva":    True, "tendencia": 0,
                "intencion":   clasificar_intencion(q),
                "score":       score_keyword(q, fuente_peso=10),
            })
        time.sleep(0.3)

    log(f"Google Suggest público: {len(resultados)} sugerencias", "OK")
    return resultados


def obtener_trends_pytrends(seeds: list[str]) -> dict:
    try:
        from pytrends.request import TrendReq
    except ImportError:
        log("pytrends no instalado. pip install pytrends", "WARN")
        return {}

    pytrends  = TrendReq(hl="es-MX", tz=-360)
    tendencias = {}
    for i in range(0, len(seeds), 5):
        batch = seeds[i:i+5]
        try:
            pytrends.build_payload(batch, geo="MX", timeframe="today 3-m")
            df = pytrends.interest_over_time()
            if not df.empty:
                for kw in batch:
                    if kw in df.columns:
                        tendencias[kw] = float(df[kw].mean())
            time.sleep(1.5)
        except Exception as e:
            log(f"Trends error: {e}", "WARN")

    log(f"Google Trends: {len(tendencias)} keywords con tendencia MX", "OK")
    return tendencias


# ══════════════════════════════════════════════════════════════════════════════
# ORQUESTADOR
# ══════════════════════════════════════════════════════════════════════════════

def detectar_keywords(args) -> tuple[list[dict], dict]:
    todas  = []
    vistos = set()

    def agregar(lista):
        for k in lista:
            q = k["query"].lower()
            if q not in vistos:
                vistos.add(q)
                todas.append(k)
            else:
                # Actualizar si la nueva fuente tiene mejor score
                for ex in todas:
                    if ex["query"].lower() == q and k["score"] > ex["score"]:
                        ex["score"]  = k["score"]
                        ex["fuente"] = k["fuente"]
                        break

    solo_serpapi = getattr(args, "solo_serpapi", False)
    solo_claude  = getattr(args, "solo_claude",  False)

    if not solo_claude:
        log("── Fuente 1: Google Search Console ──────────────────────────")
        agregar(obtener_gsc_keywords())

        if not solo_serpapi:
            log("── Fuente 2: Google Suggest público ─────────────────────────")
            agregar(obtener_suggest_publico(SEEDS_AMBASSADOR[:6]))

            log("── Fuente 3: Google Trends (pytrends) ───────────────────────")
            tendencias_map = obtener_trends_pytrends(SEEDS_AMBASSADOR[:10])
            for k in todas:
                if k["query"] in tendencias_map:
                    k["tendencia"] = tendencias_map[k["query"]]

        log("── Fuente 4: SerpApi Autocomplete ────────────────────────────")
        agregar(fuente_serpapi_autocomplete(SEEDS_AMBASSADOR))

        log("── Fuente 5/6: SerpApi Related Searches + People Also Ask ────")
        agregar(fuente_serpapi_related(SEEDS_AMBASSADOR[:8]))

    log("── Fuente 7: Claude API — Análisis estratégico ───────────────", "CLAUDE")
    analisis_claude = fuente_claude_investigacion(todas)
    todas = enriquecer_con_claude(todas, analisis_claude)

    todas.sort(key=lambda x: x["score"], reverse=True)
    return todas, analisis_claude


# ══════════════════════════════════════════════════════════════════════════════
# GUARDAR Y MOSTRAR
# ══════════════════════════════════════════════════════════════════════════════

def guardar_resultados(keywords: list[dict], analisis_claude: dict, args):
    landings = [k for k in keywords if k["intencion"] == "landing"]
    blogs    = [k for k in keywords if k["intencion"] == "blog"]
    top_n    = args.top if args.top else len(landings)

    with open(GENERATOR_PATH / "keywords.txt", "w", encoding="utf-8") as f:
        for k in landings[:top_n]:
            f.write(k["query"] + "\n")
    log(f"✅ {min(top_n, len(landings))} keywords landing → keywords.txt", "OK")

    with open(GENERATOR_PATH / "keywords_blog.txt", "w", encoding="utf-8") as f:
        for k in blogs[:top_n]:
            f.write(k["query"] + "\n")
    log(f"✅ {min(top_n, len(blogs))} keywords blog → keywords_blog.txt", "OK")

    reporte = {
        "generado":     datetime.now().isoformat(),
        "sitio":        SITE_URL,
        "total":        len(keywords),
        "por_fuente":   {},
        "top_landings": landings[:20],
        "top_blogs":    blogs[:20],
    }
    # Conteo por fuente
    for k in keywords:
        f = k["fuente"]
        reporte["por_fuente"][f] = reporte["por_fuente"].get(f, 0) + 1

    with open(GENERATOR_PATH / "reporte_seo.json", "w", encoding="utf-8") as f:
        json.dump(reporte, f, ensure_ascii=False, indent=2)

    if analisis_claude:
        with open(GENERATOR_PATH / "analisis_claude.json", "w", encoding="utf-8") as f:
            json.dump(analisis_claude, f, ensure_ascii=False, indent=2)
        log(f"✅ Análisis Claude → analisis_claude.json", "CLAUDE")

    if getattr(args, "csv", False):
        campos = ["query","fuente","intencion","score","score_claude",
                  "impresiones","posicion","tendencia","angulo_landing","tiempo_estimado_ranking"]
        with open(GENERATOR_PATH / "keywords_ambassador.csv", "w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=campos)
            w.writeheader()
            for k in keywords[:100]:
                w.writerow({c: k.get(c, "") for c in campos})
        log("✅ CSV exportado → keywords_ambassador.csv", "OK")

    return landings, blogs


def mostrar_resumen(landings, blogs, analisis_claude):
    print("\n" + "═"*66)
    print("  🤖 RESUMEN SEO AMBASSADOR v3 — GOODMAN TECH")
    print("═"*66)

    print(f"\n  🎯 Top 5 landing pages")
    for i, k in enumerate(landings[:5], 1):
        angulo = f"\n       ↳ {k.get('angulo_landing','')[:72]}" if k.get("angulo_landing") else ""
        tiempo = f" [{k.get('tiempo_estimado_ranking','')}]" if k.get("tiempo_estimado_ranking") else ""
        print(f"     {i}. [{k['score']:3d}]{tiempo} {k['query']}")
        print(f"        Fuente: {k['fuente']}{angulo}")

    print(f"\n  📝 Top 5 blog / FAQ")
    for i, k in enumerate(blogs[:5], 1):
        print(f"     {i}. [{k['score']:3d}] {k['query']} ({k['fuente']})")

    if analisis_claude:
        gaps  = analisis_claude.get("gaps_detectados", [])
        clust = analisis_claude.get("clusters", [])
        recs  = analisis_claude.get("recomendaciones_estrategicas", [])

        if gaps:
            print(f"\n  🔍 Gaps detectados por Claude ({len(gaps)} oportunidades sin cubrir)")
            for g in gaps[:4]:
                urg = g.get("urgencia","?").upper()
                print(f"     [{urg}] {g['keyword']}")
                print(f"            {g['razon'][:75]}")

        if clust:
            print(f"\n  📦 Arquitectura de clusters ({len(clust)} grupos temáticos)")
            for c in clust[:3]:
                print(f"     • {c['nombre']} → {c.get('url_sugerida','')}")
                print(f"       {c.get('descripcion','')[:70]}")

        if recs:
            print(f"\n  💡 Estrategia recomendada por Claude")
            for r in recs[:3]:
                print(f"     • {r[:90]}")

    print("\n" + "═"*66 + "\n")


# ══════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="Goodman Tech — SEO Ambassador v3")
    parser.add_argument("--auto",         action="store_true")
    parser.add_argument("--top",          type=int, default=0)
    parser.add_argument("--csv",          action="store_true")
    parser.add_argument("--solo-claude",  action="store_true")
    parser.add_argument("--solo-serpapi", action="store_true")
    args = parser.parse_args()

    print("\n🤖 Goodman Tech — SEO Ambassador v3")
    print(f"   Sitio:    {SITE_URL}")
    print(f"   SerpApi:  {'✅' if SERPAPI_KEY else '❌ falta SERPAPI_KEY'}")
    print(f"   Claude:   {'✅' if ANTHROPIC_KEY else '❌ falta ANTHROPIC_API_KEY'}")
    print(f"   {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")

    keywords, analisis_claude = detectar_keywords(args)

    if not args.auto:
        n_l = sum(1 for k in keywords if k["intencion"] == "landing")
        n_b = sum(1 for k in keywords if k["intencion"] == "blog")
        print(f"\n  {len(keywords)} keywords encontradas · {n_l} landings · {n_b} blog")
        if input("\n  ¿Guardar? [s/n]: ").strip().lower() != "s":
            print("  Cancelado.")
            return

    landings, blogs = guardar_resultados(keywords, analisis_claude, args)
    mostrar_resumen(landings, blogs, analisis_claude)

    generar = args.auto or input("  ¿Generar landings ahora? [s/n]: ").strip().lower() == "s"
    if generar:
        import subprocess
        lote = GENERATOR_PATH / "generar_lote.py"
        if lote.exists():
            subprocess.run(["python", str(lote)], cwd=str(GENERATOR_PATH))


if __name__ == "__main__":
    main()
