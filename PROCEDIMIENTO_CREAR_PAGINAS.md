# 📋 PROCEDIMIENTO CORRECTO PARA CREAR NUEVAS PÁGINAS LANDING

## ⚠️ PROBLEMA IDENTIFICADO (Abril 2026)

Se crearon 5 páginas nuevas pero **NO se registraron las rutas en App.tsx**, causando que las páginas no fueran accesibles en línea a pesar de estar en el repositorio.

---

## ✅ PROCEDIMIENTO CORRECTO (3 PASOS OBLIGATORIOS)

### PASO 1: Crear el archivo .tsx de la página
**Ubicación:** `C:\Users\Dell\CascadeProjects\Godman_Webpage\Godman_Webpage\src\pages\`

**Formato del nombre:**
- Prefijo: `Empresas`
- Keyword en PascalCase: `ClaudeParaEmpresasMexico`
- Extensión: `.tsx`
- Ejemplo completo: `EmpresasClaudeParaEmpresasMexico.tsx`

---

### PASO 2: Registrar en App.tsx (CRÍTICO - NO OMITIR)

**Archivo:** `C:\Users\Dell\CascadeProjects\Godman_Webpage\Godman_Webpage\src\App.tsx`

#### 2.1 Agregar IMPORT (líneas 1-80)
```tsx
import EmpresasClaudeParaEmpresasMexico from "./pages/EmpresasClaudeParaEmpresasMexico";
```

**Ubicación:** Después de los otros imports de `Empresas*`, antes de `const queryClient`

#### 2.2 Agregar ROUTE (líneas 150-185)
```tsx
<Route path="/empresas/claude-para-empresas-mexico" element={<EmpresasClaudeParaEmpresasMexico />} />
```

**Ubicación:** En la sección `{/* ── Empresas — Páginas SEO keyword ────────────────────────── */}`

**IMPORTANTE:**
- El `path` debe usar **kebab-case** (guiones): `/empresas/claude-para-empresas-mexico`
- El componente debe usar **PascalCase**: `<EmpresasClaudeParaEmpresasMexico />`
- Debe ir ANTES de la ruta `<Route path="*" element={<NotFound />} />`

---

### PASO 3: Git add, commit y push

```bash
# En el directorio del proyecto React
cd C:\Users\Dell\CascadeProjects\Godman_Webpage\Godman_Webpage

# Agregar todos los cambios
git add .

# Commit descriptivo
git commit -m "Feat: Agregar página [NOMBRE] - [KEYWORD]"

# Push a GitHub
git push
```

---

## 🔍 CHECKLIST DE VERIFICACIÓN

Antes de hacer el git push, verificar:

- [ ] ✅ Archivo `.tsx` creado en `src/pages/`
- [ ] ✅ Import agregado en `App.tsx` (líneas 1-80)
- [ ] ✅ Route registrada en `App.tsx` (líneas 150-185)
- [ ] ✅ Path en kebab-case coincide con nombre de archivo
- [ ] ✅ Componente en PascalCase coincide con nombre de clase
- [ ] ✅ Route está ANTES de `<Route path="*" element={<NotFound />} />`
- [ ] ✅ `git add .` ejecutado
- [ ] ✅ `git commit` con mensaje descriptivo
- [ ] ✅ `git push` completado
- [ ] ✅ Esperar 2-3 minutos para deploy automático
- [ ] ✅ Verificar URL en navegador: `https://www.goodmantech.com.mx/empresas/[slug]`

---

## 🚨 ERRORES COMUNES A EVITAR

### ❌ Error 1: Crear página pero NO registrar ruta
**Síntoma:** Página existe en GitHub pero da 404 en producción
**Solución:** Siempre hacer PASO 2 (registrar en App.tsx)

### ❌ Error 2: Path no coincide con nombre de archivo
**Ejemplo incorrecto:**
- Archivo: `EmpresasClaudeParaEmpresasMexico.tsx`
- Path: `/empresas/claude-empresas-mexico` ❌

**Ejemplo correcto:**
- Archivo: `EmpresasClaudeParaEmpresasMexico.tsx`
- Path: `/empresas/claude-para-empresas-mexico` ✅

### ❌ Error 3: Route después de NotFound
```tsx
// ❌ INCORRECTO
<Route path="*" element={<NotFound />} />
<Route path="/empresas/nueva-pagina" element={<NuevaPagina />} />

// ✅ CORRECTO
<Route path="/empresas/nueva-pagina" element={<NuevaPagina />} />
<Route path="*" element={<NotFound />} />
```

### ❌ Error 4: Olvidar el import
```tsx
// ❌ INCORRECTO - Solo route sin import
<Route path="/empresas/nueva-pagina" element={<NuevaPagina />} />
// Error: NuevaPagina is not defined

// ✅ CORRECTO - Import + Route
import NuevaPagina from "./pages/NuevaPagina";
...
<Route path="/empresas/nueva-pagina" element={<NuevaPagina />} />
```

---

## 🤖 AUTOMATIZACIÓN FUTURA

### Opción 1: Script de validación pre-push
Crear `validar_rutas.py` que verifique:
1. Todos los archivos `Empresas*.tsx` en `src/pages/`
2. Tienen su import correspondiente en `App.tsx`
3. Tienen su route correspondiente en `App.tsx`
4. El path coincide con el nombre del archivo

### Opción 2: Modificar `generar_landing.py`
Agregar función que automáticamente:
1. Crea el archivo `.tsx`
2. Agrega el import a `App.tsx`
3. Agrega la route a `App.tsx`
4. Hace git add, commit y push

**Código sugerido para agregar a `generar_landing.py`:**

```python
def registrar_ruta_en_app_tsx(nombre_componente, slug):
    """
    Registra automáticamente la ruta en App.tsx
    """
    app_tsx_path = r"C:\Users\Dell\CascadeProjects\Godman_Webpage\Godman_Webpage\src\App.tsx"
    
    # Leer archivo
    with open(app_tsx_path, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Agregar import (después de los otros imports de Empresas)
    import_line = f'import {nombre_componente} from "./pages/{nombre_componente}";\n'
    
    # Buscar última línea de imports de Empresas
    import_marker = 'import EmpresasEmbajadoresIa from "./pages/EmpresasEmbajadoresIa";'
    contenido = contenido.replace(import_marker, import_marker + '\n' + import_line)
    
    # Agregar route (antes de LeadsInstantly section)
    route_line = f'            <Route path="/empresas/{slug}" element={<{nombre_componente} />} />\n'
    route_marker = '            {/* ── LeadsInstantly ────────────────────────────────────────── */}'
    contenido = contenido.replace(route_marker, route_line + '\n' + route_marker)
    
    # Guardar archivo
    with open(app_tsx_path, 'w', encoding='utf-8') as f:
        f.write(contenido)
    
    print(f"✅ Ruta registrada en App.tsx: /empresas/{slug}")
```

---

## 📊 EJEMPLO COMPLETO

### Crear página: "Claude para empresas México"

#### 1. Crear archivo
**Archivo:** `EmpresasClaudeParaEmpresasMexico.tsx`
**Ubicación:** `src/pages/`

#### 2. Registrar en App.tsx

**Import (línea ~75):**
```tsx
import EmpresasClaudeParaEmpresasMexico from "./pages/EmpresasClaudeParaEmpresasMexico";
```

**Route (línea ~179):**
```tsx
<Route path="/empresas/claude-para-empresas-mexico" element={<EmpresasClaudeParaEmpresasMexico />} />
```

#### 3. Git workflow
```bash
git add .
git commit -m "Feat: Agregar página Claude para empresas México - keyword: claude para empresas mexico"
git push
```

#### 4. Verificar
- Esperar 2-3 minutos
- Abrir: `https://www.goodmantech.com.mx/empresas/claude-para-empresas-mexico`
- Debe cargar la página (no 404)

---

## 🎯 RESUMEN EJECUTIVO

**3 PASOS OBLIGATORIOS:**
1. ✅ Crear `.tsx` en `src/pages/`
2. ✅ Registrar import + route en `App.tsx` (CRÍTICO)
3. ✅ Git add + commit + push

**Si omites el PASO 2:** La página NO será accesible en producción.

---

**Última actualización:** Abril 5, 2026  
**Autor:** Cascade AI  
**Contexto:** Fix de 5 páginas sin rutas registradas
