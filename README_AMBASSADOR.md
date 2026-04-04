# 🤖 Goodman Tech — SEO Ambassador Module

Sistema completo de detección de keywords y monitoreo de indexación.

---

## Archivos incluidos

| Archivo | Función |
|---------|---------|
| `detectar_keywords_ambassador.py` | Motor principal — combina GSC + Suggest + Trends |
| `gsc_indexacion.py` | Analiza páginas indexadas, problemas y recomienda acciones |
| `generar_lote.py` | Genera landings en lote desde keywords.txt |

---

## Instalación (una sola vez)

```bash
cd C:\Users\Dell\Documents\goodman_generator

pip install requests pytrends
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

---

## Configurar Google Search Console API (para datos reales)

1. Ve a https://console.cloud.google.com
2. Crea proyecto `goodman-seo`
3. Habilita **Search Console API**
4. Credenciales → Crear → OAuth 2.0 → Aplicación de escritorio
5. Descarga el JSON → renómbralo `gsc_credentials.json`
6. Ponlo en `C:\Users\Dell\Documents\goodman_generator\`
7. Primera vez corre: `python detectar_keywords_ambassador.py` → autoriza en el navegador

---

## Flujo diario recomendado

```bash
# 1. Analizar estado de indexación (usa tus CSVs exportados de GSC)
python gsc_indexacion.py

# 2. Detectar keywords nuevas (combina GSC API + Suggest + Trends)
python detectar_keywords_ambassador.py

# 3. Generar landings para las mejores keywords
python generar_lote.py --limite 5

# 4. Generar artículos de blog
python generar_lote.py --blog --limite 3

# Todo en uno:
python generar_lote.py --auto-detectar --limite 5
```

---

## Usar con CSVs exportados de GSC (sin API)

Exporta de Google Search Console y coloca en la carpeta del generador:
- `Gráfico.csv`
- `Problemas_críticos.csv`  
- `Problemas_no_críticos.csv`

Luego:
```bash
python gsc_indexacion.py
```

---

## Estado actual de goodmantech.com.mx (al 30/Mar/2026)

| Métrica | Valor |
|---------|-------|
| Páginas indexadas | 8 |
| Páginas sin indexar | 14 |
| % de indexación | 36.4% |
| Impresiones últimos 7d | ~60 |
| Tendencia | 📉 bajando |

### Problemas detectados (acción inmediata)

| Problema | Páginas | Prioridad |
|----------|---------|-----------|
| Excluida por noindex | 4 | 🔴 ALTA |
| Descubiertas sin indexar | 5 | 🔴 ALTA |
| Rastreadas sin indexar | 3 | 🔴 ALTA |
| Páginas con redirección | 2 | 🟡 MEDIA |

### Acciones prioritarias

1. **Eliminar noindex** de las 4 páginas que lo tienen — revisar `<meta name="robots" content="noindex">`
2. **Solicitar indexación manual** en GSC para las 5 páginas descubiertas
3. **Mejorar contenido** de las 3 páginas rastreadas pero rechazadas por Google
4. **Agregar canonical** en páginas duplicadas

---

## Outputs generados

| Archivo | Contenido |
|---------|-----------|
| `keywords.txt` | Keywords para landing pages (ordenadas por score) |
| `keywords_blog.txt` | Keywords para artículos de blog |
| `reporte_seo.json` | Reporte completo con todos los datos |
| `reporte_indexacion.json` | Estado de indexación con recomendaciones |
| `keywords_ambassador.csv` | Exportación CSV (con flag --csv) |
