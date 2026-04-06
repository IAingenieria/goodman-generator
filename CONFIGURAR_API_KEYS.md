# 🔐 Configuración de API Keys - Goodman Generator

## ⚠️ IMPORTANTE: Seguridad de API Keys

**NUNCA hardcodear API keys en el código fuente.**

Este documento explica cómo configurar las API keys necesarias para el sistema.

---

## 📋 API Keys Necesarias

### 1. SerpAPI (Búsqueda de Keywords)
- **Servicio:** https://serpapi.com
- **Uso:** Detección de keywords, autocompletado Google, People Also Ask
- **Costo:** ~100 búsquedas gratis/mes, luego $50/mes

**Configurar:**
```powershell
$env:SERPAPI_KEY = "836d18db349501e7b72d89b56dac404d1984ce80561caf4c04596b220220a390"
```

### 2. Anthropic Claude (Generación de Contenido)
- **Servicio:** https://console.anthropic.com
- **Uso:** Generación de landing pages, análisis de keywords
- **Costo:** ~$3 por 1M tokens input, ~$15 por 1M tokens output

**Configurar:**
```powershell
$env:ANTHROPIC_API_KEY = "sk-ant-api03-..."
```

### 3. OpenAI (Generación de Blogs)
- **Servicio:** https://platform.openai.com
- **Uso:** Generación de artículos de blog con GPT-4
- **Costo:** ~$0.10 por blog (2000-3000 palabras)

**Configurar:**
```powershell
$env:OPENAI_API_KEY = "sk-proj-..."
```

### 4. Telegram Bot (Opcional)
- **Servicio:** https://t.me/BotFather
- **Uso:** Control del sistema desde Telegram
- **Costo:** Gratis

**Configurar:**
```powershell
$env:TELEGRAM_TOKEN = "obtener-de-@BotFather"
```

---

## 🚀 Configuración Rápida

### PowerShell (Windows)

```powershell
# Navegar al directorio del proyecto
cd C:\Users\Dell\Documents\goodman_generator

# Configurar encoding UTF-8
$env:PYTHONIOENCODING = "utf-8"

# Configurar API keys
$env:SERPAPI_KEY = "836d18db349501e7b72d89b56dac404d1984ce80561caf4c04596b220220a390"
$env:ANTHROPIC_API_KEY = "tu-key-aqui"
$env:OPENAI_API_KEY = "tu-key-aqui"
$env:TELEGRAM_TOKEN = "tu-token-aqui"

# Verificar configuración
python -c "import os; print('SerpAPI:', 'OK' if os.environ.get('SERPAPI_KEY') else 'FALTA')"
python -c "import os; print('Anthropic:', 'OK' if os.environ.get('ANTHROPIC_API_KEY') else 'FALTA')"
python -c "import os; print('OpenAI:', 'OK' if os.environ.get('OPENAI_API_KEY') else 'FALTA')"
```

### Bash (Linux/Mac)

```bash
export PYTHONIOENCODING="utf-8"
export SERPAPI_KEY="836d18db349501e7b72d89b56dac404d1984ce80561caf4c04596b220220a390"
export ANTHROPIC_API_KEY="tu-key-aqui"
export OPENAI_API_KEY="tu-key-aqui"
export TELEGRAM_TOKEN="tu-token-aqui"
```

---

## 🔒 Mejores Prácticas de Seguridad

### ✅ HACER:
- Usar variables de entorno para todas las API keys
- Rotar keys regularmente (cada 3-6 meses)
- Usar `.env` files locales (NO subirlos a Git)
- Agregar `*.env` a `.gitignore`
- Verificar código antes de cada commit

### ❌ NO HACER:
- Hardcodear keys en el código fuente
- Compartir keys en mensajes/emails
- Subir keys a repositorios públicos
- Usar la misma key en múltiples proyectos
- Dejar keys en historial de Git

---

## 🛡️ Verificación Pre-Commit

**Antes de cada `git push`, ejecutar:**

```powershell
# Buscar API keys hardcodeadas
Select-String -Path "*.py" -Pattern "sk-proj-|sk-ant-|SERPAPI_KEY.*=.*\`"[a-f0-9]{40}|ANTHROPIC.*=.*\`"sk-"

# Si encuentra algo, NO hacer push
```

---

## 🔄 Rotación de Keys (Si se exponen)

### SerpAPI
1. Ir a https://serpapi.com/manage-api-key
2. Click en "Regenerate API Key"
3. Copiar nueva key
4. Actualizar variable de entorno
5. Eliminar key antigua del código (si existe)

### Anthropic
1. Ir a https://console.anthropic.com/settings/keys
2. Click en "Create Key"
3. Copiar nueva key
4. Revocar key antigua
5. Actualizar variable de entorno

### OpenAI
1. Ir a https://platform.openai.com/api-keys
2. Click en "Create new secret key"
3. Copiar nueva key
4. Revocar key antigua
5. Actualizar variable de entorno

---

## 📝 Historial de Rotaciones

| Fecha | Servicio | Razón | Estado |
|-------|----------|-------|--------|
| 2026-04-05 | SerpAPI | Expuesta en Git | ✅ Rotada |

---

## 🆘 Soporte

Si tienes problemas con las API keys:

1. Verificar que las variables de entorno estén configuradas
2. Reiniciar terminal/PowerShell
3. Verificar que las keys sean válidas en los servicios
4. Revisar logs de error para más detalles

**Contacto:** info@goodmantech.com.mx
