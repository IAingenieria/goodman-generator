"""
bot_goodman.py  (versión Ambassador 2.0)
Goodman Tech — Bot de Telegram con SEO Ambassador
==================================================
Comandos disponibles:
  /start          → Bienvenida y menú principal
  /estado         → Estado de indexación de goodmantech.com.mx
  /alertas        → Ver problemas críticos de GSC
  /keywords       → Detectar keywords nuevas y aprobarlas
  /siguiente      → Siguiente keyword pendiente de aprobación
  /pendientes     → Cuántas keywords esperan aprobación
  /generadas      → Páginas creadas en esta sesión
  /agregar        → Agregar keyword manual
  /ayuda          → Lista de comandos

Botones inline en keywords:
  ✅ Aprobar    → genera landing inmediatamente
  ❌ Rechazar   → descarta
  ✏️ Editar     → corregir antes de generar
  ⏭️ Siguiente  → pasar sin decidir
  📝 Blog       → generar como artículo en vez de landing

Alertas automáticas:
  → Cada 24h revisa indexación y notifica si algo cambió
  → Alerta inmediata si páginas indexadas bajan
  → Notifica cuando una landing nueva es generada
"""

import os, json, logging, asyncio, subprocess, csv
from pathlib import Path
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes, ConversationHandler
)

# ── Configuración ─────────────────────────────────────────────────────────────
CONFIGURACION = {
    "telegram_token": os.environ.get("TELEGRAM_TOKEN", "TU_TOKEN_AQUI"),
    "chat_id":        7938754022,
    "anthropic_key":  os.environ.get("ANTHROPIC_API_KEY", ""),
    "modelo":         "claude-sonnet-4-6",
    "proyecto_path":  r"C:\Users\Dell\CascadeProjects\Godman_Webpage\Godman_Webpage",
    "generator_path": r"C:\Users\Dell\Documents\goodman_generator",
    "site_url":       "https://www.goodmantech.com.mx",
}

GENERATOR_PATH = Path(CONFIGURACION["generator_path"])
PROYECTO_PATH  = Path(CONFIGURACION["proyecto_path"])

# Estados para ConversationHandler
ESPERANDO_KEYWORD_MANUAL = 1
ESPERANDO_EDICION        = 2

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def keyword_a_slug(keyword: str) -> str:
    import re
    slug = keyword.lower().strip()
    slug = slug.replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u').replace('ñ','n')
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'\s+', '-', slug)
    return slug.strip('-')
# ── Estado en memoria ─────────────────────────────────────────────────────────
estado_bot = {
    "keywords_pendientes": [],   # lista de dicts {query, intencion, score, fuente}
    "keywords_generadas":  [],   # esta sesión
    "keyword_en_edicion":  None,
    "ultimo_estado_idx":   None, # para detectar cambios
    "ultima_revision":     None,
}


# ── Helpers ───────────────────────────────────────────────────────────────────

def slugify(text: str) -> str:
    """Convierte keyword a slug URL-friendly."""
    import unicodedata
    import re
    # Normalizar unicode
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    # Convertir a minúsculas y limpiar
    text = text.lower().strip()
    # Eliminar caracteres especiales
    text = re.sub(r"[^\w\s-]", "", text)
    # Reemplazar espacios por guiones
    text = re.sub(r"[\s_]+", "-", text)
    return text

def generar_url_landing(keyword: str) -> str:
    """Genera URL completa de la landing page."""
    slug = slugify(keyword)
    return f"{CONFIGURACION['site_url']}/empresas/{slug}"

def leer_grafico_csv() -> list[dict]:
    path = GENERATOR_PATH / "Gráfico.csv"
    if not path.exists():
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def leer_problemas_csv(nombre: str) -> list[dict]:
    path = GENERATOR_PATH / nombre
    if not path.exists():
        return []
    with open(path, newline="", encoding="utf-8") as f:
        filas = list(csv.DictReader(f))
    return [r for r in filas if int(r.get("Páginas", 0) or 0) > 0]

def obtener_estado_indexacion() -> dict:
    grafico = leer_grafico_csv()
    problemas_crit = leer_problemas_csv("Problemas_críticos.csv")

    if not grafico:
        return {"error": "No se encontraron datos de GSC. Exporta los CSVs a la carpeta del generador."}

    ultima = grafico[-1]
    indexadas   = int(ultima.get("Indexadas", 0) or 0)
    sin_indexar = int(ultima.get("Sin indexar", 0) or 0)
    total       = indexadas + sin_indexar
    pct         = round(indexadas / total * 100, 1) if total > 0 else 0

    impr_7d  = sum(int(r.get("Impresiones", 0) or 0) for r in grafico[-7:])
    impr_30d = sum(int(r.get("Impresiones", 0) or 0) for r in grafico[-30:])

    # Tendencia
    mitad = len(grafico) // 2
    p1 = sum(int(r.get("Indexadas", 0) or 0) for r in grafico[:mitad]) / max(mitad, 1)
    p2 = sum(int(r.get("Indexadas", 0) or 0) for r in grafico[mitad:]) / max(len(grafico)-mitad, 1)
    if p2 > p1 * 1.1:
        tendencia = "📈 Creciendo"
    elif p2 < p1 * 0.9:
        tendencia = "📉 Bajando"
    else:
        tendencia = "➡️ Estable"

    pico = max((int(r.get("Indexadas", 0) or 0) for r in grafico if r.get("Indexadas")), default=0)

    return {
        "indexadas":    indexadas,
        "sin_indexar":  sin_indexar,
        "total":        total,
        "pct":          pct,
        "impr_7d":      impr_7d,
        "impr_30d":     impr_30d,
        "tendencia":    tendencia,
        "pico":         pico,
        "fecha":        ultima.get("Fecha", ""),
        "problemas":    problemas_crit,
    }

def formatear_estado(e: dict) -> str:
    if "error" in e:
        return f"⚠️ {e['error']}"

    perdidas = e["pico"] - e["indexadas"]
    perdidas_txt = f"\n⚠️ *{perdidas} páginas perdidas* desde el pico histórico" if perdidas > 0 else ""

    problemas_txt = ""
    for p in e["problemas"]:
        motivo = p.get("Motivo", "")[:45]
        pags   = p.get("Páginas", 0)
        problemas_txt += f"\n  • {motivo}: *{pags} pág.*"

    return (
        f"📊 *Estado de Indexación*\n"
        f"`{CONFIGURACION['site_url']}`\n"
        f"🗓 {e['fecha']}\n\n"
        f"✅ Indexadas:     *{e['indexadas']}* ({e['pct']}%)\n"
        f"❌ Sin indexar:   *{e['sin_indexar']}*\n"
        f"📄 Total conocidas: {e['total']}\n"
        f"{e['tendencia']}{perdidas_txt}\n\n"
        f"👁 Impresiones 7d:  *{e['impr_7d']}*\n"
        f"👁 Impresiones 30d: *{e['impr_30d']}*"
        + (f"\n\n🔴 *Problemas críticos:*{problemas_txt}" if problemas_txt else "")
    )

def generar_landing_sync(keyword: str, tipo: str = "landing") -> tuple[bool, str]:
    """Llama a generar_landing.py de forma síncrona."""
    script = GENERATOR_PATH / "generar_landing.py"
    if not script.exists():
        return False, f"No se encontró generar_landing.py en {GENERATOR_PATH}"
    try:
        result = subprocess.run(
            ["python", str(script), keyword],
            cwd=str(GENERATOR_PATH),
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0:
            return True, result.stdout[-300:] if result.stdout else "Generado correctamente"
        else:
            return False, result.stderr[-300:] if result.stderr else "Error desconocido"
    except subprocess.TimeoutExpired:
        return False, "Timeout: la generación tardó más de 2 minutos"
    except Exception as e:
        return False, str(e)

def cargar_keywords_desde_archivo() -> list[dict]:
    """Lee keywords.txt y keywords_blog.txt y los combina."""
    resultado = []
    for archivo, tipo in [("keywords.txt", "landing"), ("keywords_blog.txt", "blog")]:
        path = GENERATOR_PATH / archivo
        if path.exists():
            with open(path, encoding="utf-8") as f:
                for line in f:
                    kw = line.strip()
                    if kw and not kw.startswith("#"):
                        resultado.append({"query": kw, "intencion": tipo, "score": 50, "fuente": "archivo"})
    return resultado

def teclado_keyword(idx: int, total: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Landing", callback_data=f"aprobar_landing_{idx}"),
            InlineKeyboardButton("📝 Blog",    callback_data=f"aprobar_blog_{idx}"),
        ],
        [
            InlineKeyboardButton("✏️ Editar",   callback_data=f"editar_{idx}"),
            InlineKeyboardButton("❌ Rechazar", callback_data=f"rechazar_{idx}"),
        ],
        [
            InlineKeyboardButton(f"⏭️ Siguiente ({idx+1}/{total})", callback_data=f"siguiente_{idx}"),
        ],
    ])


# ── Handlers de comandos ──────────────────────────────────────────────────────

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 Estado indexación", callback_data="ver_estado")],
        [InlineKeyboardButton("🔍 Detectar keywords",  callback_data="detectar_keywords")],
        [InlineKeyboardButton("📋 Ver pendientes",     callback_data="ver_pendientes")],
        [InlineKeyboardButton("✅ Ver generadas",      callback_data="ver_generadas")],
    ])
    await update.message.reply_text(
        "🤖 *Goodman Tech — SEO Ambassador*\n\n"
        "Controla tu estrategia SEO desde Telegram.\n"
        "Aprueba keywords, monitorea indexación y genera landings.",
        parse_mode="Markdown",
        reply_markup=kb
    )

async def cmd_estado(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message or update.callback_query.message
    await msg.reply_text("⏳ Analizando indexación...", parse_mode="Markdown")
    e = obtener_estado_indexacion()
    texto = formatear_estado(e)

    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 Actualizar", callback_data="ver_estado")],
        [InlineKeyboardButton("🔍 Detectar keywords ahora", callback_data="detectar_keywords")],
    ])
    await msg.reply_text(texto, parse_mode="Markdown", reply_markup=kb)

async def cmd_alertas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    problemas = leer_problemas_csv("Problemas_críticos.csv")
    if not problemas:
        await update.message.reply_text("✅ No se detectaron problemas críticos en los CSVs.")
        return

    texto = "🔴 *Problemas críticos de indexación*\n\n"
    acciones = {
        "noindex":      "Eliminar etiqueta `<meta name='robots' content='noindex'>` de estas páginas",
        "redirección":  "Verificar que sean redirecciones 301 permanentes",
        "sin indexar":  "Solicitar indexación manual en GSC → Inspección de URL",
        "canónica":     "Agregar `<link rel='canonical'>` en el `<head>` de cada página",
    }

    for p in problemas:
        motivo  = p.get("Motivo", "")
        paginas = p.get("Páginas", 0)
        accion  = next((v for k, v in acciones.items() if k in motivo.lower()), "Revisar en GSC")
        texto += f"⚠️ *{motivo}*\n   📄 {paginas} páginas\n   💡 _{accion}_\n\n"

    await update.message.reply_text(texto, parse_mode="Markdown")

async def cmd_keywords(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message or update.callback_query.message
    await msg.reply_text("⏳ Detectando keywords desde GSC + Suggest + Trends...\nEsto puede tardar 1-2 minutos.")

    # Intentar correr el detector
    script = GENERATOR_PATH / "detectar_keywords_ambassador.py"
    if script.exists():
        try:
            result = subprocess.run(
                ["python", str(script), "--auto"],
                cwd=str(GENERATOR_PATH),
                capture_output=True, text=True, timeout=180
            )
        except Exception as e:
            await msg.reply_text(f"⚠️ Error al detectar: {e}\nCargando desde keywords.txt...")

    # Cargar lo que haya en archivos
    keywords = cargar_keywords_desde_archivo()

    if not keywords:
        await msg.reply_text(
            "⚠️ No se encontraron keywords.\n\n"
            "Opciones:\n"
            "• Corre `python detectar_keywords_ambassador.py` en tu PC\n"
            "• Usa /agregar para añadir keywords manualmente"
        )
        return

    estado_bot["keywords_pendientes"] = keywords
    await msg.reply_text(
        f"✅ *{len(keywords)} keywords detectadas*\n\n"
        f"Landing pages: {sum(1 for k in keywords if k['intencion']=='landing')}\n"
        f"Blog: {sum(1 for k in keywords if k['intencion']=='blog')}\n\n"
        f"Usa /siguiente para empezar a aprobarlas.",
        parse_mode="Markdown"
    )

async def cmd_siguiente(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message or update.callback_query.message
    pendientes = estado_bot["keywords_pendientes"]

    if not pendientes:
        await msg.reply_text(
            "📭 No hay keywords pendientes.\n\n"
            "Usa /keywords para detectar nuevas\no /agregar para añadir una manual."
        )
        return

    idx = 0
    kw = pendientes[idx]
    tipo_emoji = "🏠" if kw["intencion"] == "landing" else "📝"

    await msg.reply_text(
        f"{tipo_emoji} *Keyword #{idx+1} de {len(pendientes)}*\n\n"
        f"`{kw['query']}`\n\n"
        f"Tipo: {kw['intencion']} | Score: {kw.get('score', '?')} | Fuente: {kw.get('fuente', '?')}",
        parse_mode="Markdown",
        reply_markup=teclado_keyword(idx, len(pendientes))
    )

async def cmd_pendientes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    n = len(estado_bot["keywords_pendientes"])
    if n == 0:
        await update.message.reply_text("📭 No hay keywords pendientes de aprobación.")
    else:
        lista = "\n".join(
            f"  {i+1}. `{k['query']}` ({k['intencion']})"
            for i, k in enumerate(estado_bot["keywords_pendientes"][:10])
        )
        await update.message.reply_text(
            f"📋 *{n} keywords pendientes*\n\n{lista}"
            + ("\n  ..." if n > 10 else ""),
            parse_mode="Markdown"
        )

async def cmd_generadas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    generadas = estado_bot["keywords_generadas"]
    if not generadas:
        await update.message.reply_text("📭 No se han generado páginas en esta sesión.")
        return
    lista = "\n".join(
        f"  ✅ `{k}`\n     🔗 {generar_url_landing(k)}"
        for k in generadas
    )
    await update.message.reply_text(
        f"✅ *{len(generadas)} páginas generadas esta sesión*\n\n{lista}",
        parse_mode="Markdown"
    )

async def cmd_agregar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✏️ Escribe la keyword que quieres agregar:\n\n"
        "_Ejemplo: IA para empresas de logística en Monterrey_",
        parse_mode="Markdown"
    )
    return ESPERANDO_KEYWORD_MANUAL

async def recibir_keyword_manual(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kw = update.message.text.strip()
    if len(kw) < 5:
        await update.message.reply_text("⚠️ La keyword es muy corta. Intenta con algo más específico.")
        return ESPERANDO_KEYWORD_MANUAL

    nueva = {"query": kw, "intencion": "landing", "score": 50, "fuente": "manual"}
    estado_bot["keywords_pendientes"].insert(0, nueva)

    await update.message.reply_text(
        f"✅ Keyword agregada:\n`{kw}`\n\nUsa /siguiente para aprobarla.",
        parse_mode="Markdown"
    )
    return ConversationHandler.END

async def cmd_ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 *Comandos disponibles*\n\n"
        "/start         → Menú principal\n"
        "/estado        → Indexación de tu sitio\n"
        "/alertas       → Problemas críticos GSC\n"
        "/keywords      → Detectar keywords nuevas\n"
        "/siguiente     → Aprobar/rechazar keywords\n"
        "/pendientes    → Lista de keywords en cola\n"
        "/generadas     → Páginas creadas hoy\n"
        "/agregar       → Añadir keyword manual\n"
        "/ayuda         → Esta ayuda\n\n"
        "💡 _Tip: Exporta los CSVs de GSC a la carpeta del generador para tener datos en tiempo real._",
        parse_mode="Markdown"
    )


# ── Callback handler (botones inline) ────────────────────────────────────────

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data  = query.data
    msg   = query.message

    # ── Menú principal ────────────────────────────────────────────────────
    if data == "ver_estado":
        await cmd_estado(update, context)
        return

    if data == "detectar_keywords":
        await cmd_keywords(update, context)
        return

    if data == "ver_pendientes":
        pendientes = estado_bot["keywords_pendientes"]
        if not pendientes:
            await msg.reply_text("📭 No hay keywords pendientes. Usa /keywords para detectar.")
            return
        await cmd_siguiente(update, context)
        return

    if data == "ver_generadas":
        await cmd_generadas(update, context)
        return

    # ── Acciones sobre keyword ────────────────────────────────────────────
    partes = data.split("_")
    accion = "_".join(partes[:-1])
    try:
        idx = int(partes[-1])
    except:
        return

    pendientes = estado_bot["keywords_pendientes"]
    if idx >= len(pendientes):
        await msg.reply_text("⚠️ Ya no hay más keywords pendientes.")
        return

    kw = pendientes[idx]

    if accion in ("aprobar_landing", "aprobar_blog"):
        tipo = "blog" if accion == "aprobar_blog" else "landing"
        await msg.reply_text(f"⚙️ Generando {tipo}:\n`{kw['query']}`\n\nEspera...", parse_mode="Markdown")

        ok, detalle = await asyncio.get_event_loop().run_in_executor(
            None, generar_landing_sync, kw["query"], tipo
        )

        if ok:
            estado_bot["keywords_generadas"].append(kw["query"])
            pendientes.pop(idx)
            url_landing = generar_url_landing(kw["query"])
            await msg.reply_text(
                f"✅ *Generado correctamente*\n\n`{kw['query']}`\n\n🔗 https://www.goodmantech.com.mx/empresas/{keyword_a_slug(kw['query'])}\n\n"
                f"🔗 *Link directo:*\n{url_landing}\n\n"
                f"📁 Revisa `src/pages/` y sigue las instrucciones de `REGISTROS.md`\n\n"
                f"⏳ Quedan {len(pendientes)} keywords pendientes.",
                parse_mode="Markdown"
            )
        else:
            await msg.reply_text(f"❌ Error al generar:\n```{detalle}```", parse_mode="Markdown")

        # Mostrar siguiente si hay
        if pendientes:
            siguiente = pendientes[0]
            tipo_e = "🏠" if siguiente["intencion"] == "landing" else "📝"
            await msg.reply_text(
                f"{tipo_e} *Siguiente keyword*\n\n`{siguiente['query']}`",
                parse_mode="Markdown",
                reply_markup=teclado_keyword(0, len(pendientes))
            )
        return

    if accion == "rechazar":
        rechazada = pendientes.pop(idx)
        await msg.reply_text(
            f"❌ Rechazada: `{rechazada['query']}`\n\nQuedan {len(pendientes)} pendientes.",
            parse_mode="Markdown"
        )
        if pendientes:
            siguiente = pendientes[0]
            await msg.reply_text(
                f"➡️ Siguiente:\n`{siguiente['query']}`",
                parse_mode="Markdown",
                reply_markup=teclado_keyword(0, len(pendientes))
            )
        return

    if accion == "editar":
        estado_bot["keyword_en_edicion"] = idx
        await msg.reply_text(
            f"✏️ Edita la keyword:\n\nActual: `{kw['query']}`\n\nEscribe la versión corregida:",
            parse_mode="Markdown"
        )
        return

    if accion == "siguiente":
        siguiente_idx = (idx + 1) % len(pendientes)
        siguiente = pendientes[siguiente_idx]
        tipo_e = "🏠" if siguiente["intencion"] == "landing" else "📝"
        await msg.reply_text(
            f"{tipo_e} *Keyword #{siguiente_idx+1} de {len(pendientes)}*\n\n"
            f"`{siguiente['query']}`\n\n"
            f"Tipo: {siguiente['intencion']} | Score: {siguiente.get('score','?')}",
            parse_mode="Markdown",
            reply_markup=teclado_keyword(siguiente_idx, len(pendientes))
        )
        return


async def recibir_edicion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Recibe el texto editado de una keyword."""
    idx = estado_bot.get("keyword_en_edicion")
    if idx is None:
        return

    nueva_kw = update.message.text.strip()
    pendientes = estado_bot["keywords_pendientes"]

    if idx < len(pendientes):
        vieja = pendientes[idx]["query"]
        pendientes[idx]["query"] = nueva_kw
        estado_bot["keyword_en_edicion"] = None

        await update.message.reply_text(
            f"✅ Keyword actualizada\n\nAntes: `{vieja}`\nAhora: `{nueva_kw}`",
            parse_mode="Markdown",
            reply_markup=teclado_keyword(idx, len(pendientes))
        )


# ── Monitor automático de indexación ─────────────────────────────────────────

async def monitor_indexacion(context: ContextTypes.DEFAULT_TYPE):
    """
    Corre cada 24h. Compara el estado actual vs el anterior
    y envía alerta si algo cambió negativamente.
    """
    e = obtener_estado_indexacion()
    if "error" in e:
        return

    anterior = estado_bot["ultimo_estado_idx"]
    estado_bot["ultimo_estado_idx"] = e
    estado_bot["ultima_revision"]   = datetime.now()

    if anterior is None:
        return  # Primera corrida, sin comparación

    alertas = []

    if e["indexadas"] < anterior["indexadas"]:
        diff = anterior["indexadas"] - e["indexadas"]
        alertas.append(f"🚨 *Perdiste {diff} página(s) indexada(s)*\n   Antes: {anterior['indexadas']} → Ahora: {e['indexadas']}")

    if e["impr_7d"] < anterior["impr_7d"] * 0.7:
        alertas.append(f"📉 *Impresiones bajaron 30%* esta semana\n   Antes: {anterior['impr_7d']} → Ahora: {e['impr_7d']}")

    if alertas:
        texto = "⚠️ *Alerta de indexación — Goodman Tech*\n\n" + "\n\n".join(alertas)
        texto += f"\n\n[Ver detalle completo → /estado]"
        await context.bot.send_message(
            chat_id=CONFIGURACION["chat_id"],
            text=texto,
            parse_mode="Markdown"
        )

async def resumen_diario(context: ContextTypes.DEFAULT_TYPE):
    """Envía resumen diario a las 9am."""
    e = obtener_estado_indexacion()
    generadas_hoy = len(estado_bot["keywords_generadas"])

    texto = (
        f"☀️ *Resumen diario — Goodman Tech*\n"
        f"{datetime.now().strftime('%d/%m/%Y')}\n\n"
        f"🌐 Indexadas: *{e.get('indexadas','?')}* ({e.get('pct','?')}%)\n"
        f"👁 Impresiones 7d: *{e.get('impr_7d','?')}*\n"
        f"📄 Landings generadas hoy: *{generadas_hoy}*\n"
        f"{e.get('tendencia','')}\n\n"
    )

    if e.get("problemas"):
        texto += f"🔴 *{len(e['problemas'])} problemas críticos pendientes*\n"
        texto += "Usa /alertas para ver detalles.\n\n"

    texto += "Usa /keywords para detectar oportunidades de hoy."

    # Reset contadores diarios
    estado_bot["keywords_generadas"] = []

    await context.bot.send_message(
        chat_id=CONFIGURACION["chat_id"],
        text=texto,
        parse_mode="Markdown"
    )


# ── Inicialización ────────────────────────────────────────────────────────────

def main():
    token = CONFIGURACION["telegram_token"]
    if token == "TU_TOKEN_AQUI":
        print("❌ Configura tu TELEGRAM_TOKEN")
        return

    print(f"\n🤖 Goodman Tech — SEO Ambassador Bot")
    print(f"   Sitio: {CONFIGURACION['site_url']}")
    print(f"   {datetime.now().strftime('%d/%m/%Y %H:%M')}")

    import asyncio
    asyncio.set_event_loop(asyncio.new_event_loop())

    app = Application.builder().token(token).build()

    conv_agregar = ConversationHandler(
        entry_points=[CommandHandler("agregar", cmd_agregar)],
        states={ESPERANDO_KEYWORD_MANUAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_keyword_manual)]},
        fallbacks=[CommandHandler("start", cmd_start)],
    )

    app.add_handler(CommandHandler("start",      cmd_start))
    app.add_handler(CommandHandler("estado",     cmd_estado))
    app.add_handler(CommandHandler("alertas",    cmd_alertas))
    app.add_handler(CommandHandler("keywords",   cmd_keywords))
    app.add_handler(CommandHandler("siguiente",  cmd_siguiente))
    app.add_handler(CommandHandler("pendientes", cmd_pendientes))
    app.add_handler(CommandHandler("generadas",  cmd_generadas))
    app.add_handler(CommandHandler("ayuda",      cmd_ayuda))
    app.add_handler(conv_agregar)
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_edicion))

    app.job_queue.run_repeating(monitor_indexacion, interval=86400, first=300)
    app.job_queue.run_daily(resumen_diario, time=__import__("datetime").time(15, 0, 0))

    # Cargar keywords automáticamente al arrancar
    keywords_iniciales = cargar_keywords_desde_archivo()
    if keywords_iniciales:
        estado_bot["keywords_pendientes"] = keywords_iniciales
        print(f"📋 {len(keywords_iniciales)} keywords cargadas desde archivos")
        print(f"   Landing: {sum(1 for k in keywords_iniciales if k['intencion']=='landing')}")
        print(f"   Blog: {sum(1 for k in keywords_iniciales if k['intencion']=='blog')}")
    else:
        print("⚠️  No se encontraron keywords en keywords.txt o keywords_blog.txt")

    print("✅ Bot iniciado. Ctrl+C para detener.\n")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()