# 🎨 GUÍA DE DISEÑO — EMBAJADORES DE IA
## Estilo "Nano Banana" para Presentaciones

---

## 📐 TIPOGRAFÍAS

### Fuente Principal — Títulos y Headlines
**Plus Jakarta Sans**
- Weights: 400 (Regular), 600 (SemiBold), 700 (Bold), 800 (ExtraBold), 900 (Black)
- Uso: Títulos principales (H1, H2, H3), CTAs, números destacados
- Google Fonts: `https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800;900&display=swap`

**Ejemplos de uso:**
- H1 Hero: `font-size: 60px` | `font-weight: 900` (Black) | `line-height: tight`
- H2 Secciones: `font-size: 48px` | `font-weight: 700` (Bold)
- H3 Tarjetas: `font-size: 24px` | `font-weight: 700` (Bold)
- Botones: `font-size: 18-20px` | `font-weight: 700` (Bold)

### Fuente Secundaria — Cuerpo de Texto
**Inter**
- Weights: 400 (Regular), 500 (Medium), 600 (SemiBold)
- Uso: Párrafos, descripciones, texto secundario
- Google Fonts: `https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap`

**Ejemplos de uso:**
- Párrafos: `font-size: 18-20px` | `font-weight: 400` | `line-height: relaxed`
- Subtítulos: `font-size: 16px` | `font-weight: 500`
- Texto pequeño: `font-size: 14px` | `font-weight: 400`

### Iconografía
**Material Symbols Outlined**
- Estilo: Outlined (contorno)
- Variable Settings: `'FILL' 1` para iconos rellenos
- Google Fonts: `https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200`

---

## 🎨 PALETA DE COLORES

### Colores Principales (Brand)

#### 🔵 AZUL PRIMARIO
- **HEX:** `#2463eb`
- **RGB:** `36, 99, 235`
- **Uso:** Elementos principales, bordes destacados, iconos primarios, gradientes
- **Variantes:**
  - 20% opacidad: `#2463eb33` (fondos sutiles)
  - 30% opacidad: `#2463eb4D` (bordes)
  - 40% opacidad: `#2463eb66` (hover states)

#### 🟡 AMARILLO ACENTO
- **HEX:** `#FACC15`
- **RGB:** `250, 204, 21`
- **Uso:** CTAs principales, badges destacados, acentos importantes
- **Variantes:**
  - 15% opacidad: `#FACC1526` (fondos de iconos)
  - 40% opacidad: `#FACC1566` (sombras de botones)

#### 🟢 VERDE ÉXITO
- **HEX:** `#4ade80`
- **RGB:** `74, 222, 128`
- **Uso:** Indicadores de éxito, métricas positivas, checks

### Colores de Fondo

#### ⬛ DARK (Fondo Oscuro Principal)
- **HEX:** `#0F172A`
- **RGB:** `15, 23, 42`
- **Uso:** Secciones hero, secciones alternas, fondos de tarjetas oscuras
- **Nombre Tailwind:** `slate-900`

#### 🔲 CARD (Tarjetas Oscuras)
- **HEX:** `#1e293b`
- **RGB:** `30, 41, 59`
- **Uso:** Tarjetas sobre fondo oscuro, elementos elevados
- **Nombre Tailwind:** `slate-800`

#### ⬜ LIGHT (Fondo Claro)
- **HEX:** `#f8fafc`
- **RGB:** `248, 250, 252`
- **Uso:** Secciones alternas claras, fondo general
- **Nombre Tailwind:** `slate-50`

#### ⚪ WHITE (Blanco Puro)
- **HEX:** `#ffffff`
- **RGB:** `255, 255, 255`
- **Uso:** Tarjetas sobre fondo claro, texto sobre oscuro

### Colores de Texto

#### Sobre Fondo Oscuro:
- **Texto Principal:** `#ffffff` (white)
- **Texto Secundario:** `#cbd5e1` (slate-300)
- **Texto Terciario:** `#94a3b8` (slate-400)

#### Sobre Fondo Claro:
- **Texto Principal:** `#0f172a` (DARK / slate-900)
- **Texto Secundario:** `#475569` (slate-600)
- **Texto Terciario:** `#64748b` (slate-500)

### Colores Adicionales (Iconos y Acentos)

- **Púrpura:** `#8b5cf6` (violet-500)
- **Rosa:** `#ec4899` (pink-500)
- **Cyan:** `#06b6d4` (cyan-500)
- **Naranja:** `#f59e0b` (amber-500)
- **Verde Oscuro:** `#10b981` (emerald-500)
- **Azul Claro:** `#3b82f6` (blue-500)
- **Gris Oscuro:** `#64748b` (slate-500)

---

## 🎭 GRADIENTES

### Gradiente de Texto Principal
**Clase CSS:** `.cnp-text-gradient`
```css
background: linear-gradient(135deg, #2463eb 0%, #FACC15 100%);
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
```
**Uso:** Palabras clave destacadas en títulos (ej: "desde adentro", "IA con embajadores internos")

### Gradiente de Fondo (Dot Grid)
**Clase CSS:** `.cnp-dot-grid-dark`
- Patrón de puntos sobre fondo oscuro
- Opacidad: 40%
- Uso: Textura sutil en secciones hero

---

## 📦 COMPONENTES Y ESTILOS

### 🔘 Botones

#### CTA Principal (Amarillo)
```css
background-color: #FACC15
color: #0f172a
padding: 20px 48px
border-radius: 9999px (full)
font-family: Plus Jakarta Sans
font-weight: 700
font-size: 20px
box-shadow: 0 8px 32px rgba(250, 204, 21, 0.25)
transition: scale 0.2s
hover: scale(1.05)
```

#### CTA Secundario (Azul Outline)
```css
background-color: transparent
color: #2463eb
border: 2px solid #2463eb
padding: 16px 32px
border-radius: 9999px
font-family: Plus Jakarta Sans
font-weight: 700
font-size: 18px
hover: background-color: rgba(36, 99, 235, 0.1)
```

### 🏷️ Badges

#### Badge de Categoría
```css
background-color: rgba(36, 99, 235, 0.13)
color: #FACC15
border: 1px solid rgba(36, 99, 235, 0.25)
padding: 6px 16px
border-radius: 9999px
font-family: Plus Jakarta Sans
font-weight: 600
font-size: 14px
```

#### Badge de Destacado
```css
background-color: #FACC15
color: #0f172a
padding: 4px 16px
border-radius: 9999px
font-weight: 700
font-size: 12px
position: absolute
top: -12px
```

### 🃏 Tarjetas

#### Tarjeta sobre Fondo Claro
```css
background-color: #ffffff
border: 1px solid #e2e8f0
border-radius: 16px
padding: 24px
transition: transform 0.2s, box-shadow 0.2s
hover: transform: translateY(-4px)
hover: box-shadow: 0 20px 40px rgba(0,0,0,0.1)
```

#### Tarjeta sobre Fondo Oscuro
```css
background-color: #1e293b
border: 1px solid rgba(36, 99, 235, 0.2)
border-radius: 16px
padding: 24px
transition: transform 0.2s
hover: transform: translateY(-4px)
```

#### Tarjeta con Borde de Color (Izquierdo)
```css
background-color: #1e293b
border-left: 6px solid #2463eb
border-radius: 16px
padding: 24px
```

### 🎯 Iconos

#### Contenedor de Icono (Circular)
```css
width: 56px
height: 56px
border-radius: 16px
display: flex
align-items: center
justify-content: center
background-color: rgba([COLOR], 0.15)
```

#### Icono Material Symbol
```css
font-size: 24px
color: [COLOR_PRINCIPAL]
font-variation-settings: 'FILL' 1
```

---

## 📊 ESPACIADO Y LAYOUT

### Márgenes de Sección
- **Padding Vertical:** `py-32` (128px top/bottom)
- **Contenedor Máximo:** `max-w-7xl` (1280px)
- **Padding Horizontal:** `px-6` (24px)

### Espaciado entre Elementos
- **Título a Subtítulo:** `mb-6` (24px)
- **Subtítulo a Contenido:** `mb-12` (48px)
- **Entre Tarjetas:** `gap-6` (24px)
- **Dentro de Tarjetas:** `space-y-3` (12px)

### Grid Layouts
- **2 Columnas:** `grid-cols-1 md:grid-cols-2`
- **3 Columnas:** `grid-cols-1 md:grid-cols-2 lg:grid-cols-3`
- **Gap:** `gap-6` (24px)

---

## 🎬 ANIMACIONES Y TRANSICIONES

### Hover en Tarjetas
```css
transition: all 0.2s ease
hover: transform: translateY(-4px)
hover: box-shadow: 0 20px 40px rgba(0,0,0,0.1)
```

### Hover en Botones
```css
transition: all 0.2s ease
hover: transform: scale(1.05)
active: transform: scale(0.95)
```

### Animaciones de Widgets (Dashboard)
```css
.cnp-widget-float-y {
  animation: float-y 3s ease-in-out infinite;
}

.cnp-widget-float-x {
  animation: float-x 4s ease-in-out infinite;
}

.cnp-widget-float-diag {
  animation: float-diagonal 5s ease-in-out infinite;
}
```

---

## 📱 RESPONSIVE BREAKPOINTS

- **Mobile:** `< 768px`
- **Tablet:** `768px - 1024px` (md)
- **Desktop:** `> 1024px` (lg)

### Ajustes Responsive
- **Títulos H1:** `text-5xl` (mobile) → `md:text-6xl` (desktop)
- **Títulos H2:** `text-4xl` (mobile) → `md:text-5xl` (desktop)
- **Grid:** `grid-cols-1` (mobile) → `md:grid-cols-2` → `lg:grid-cols-3`

---

## 🎨 EFECTOS ESPECIALES

### Diagonal Skew (Hero Section)
```css
.cnp-diagonal-skew {
  clip-path: polygon(0 0, 100% 0, 100% 95%, 0 100%);
}
```

### Diagonal Top (Sección siguiente)
```css
.cnp-diagonal-top {
  clip-path: polygon(0 5%, 100% 0, 100% 100%, 0 100%);
  margin-top: -80px;
}
```

---

## 📋 ESTRUCTURA DE SECCIONES

### 1. HERO (Fondo Oscuro)
- Background: `#0F172A`
- Dot Grid Pattern con 40% opacidad
- Diagonal skew en la parte inferior
- Título en Plus Jakarta Sans 900
- Gradiente en palabra clave
- Badge amarillo con borde azul
- CTA amarillo + CTA outline azul

### 2. PROBLEMA (Fondo Claro)
- Background: `#f8fafc`
- Diagonal top para conectar con hero
- Tarjetas blancas con iconos de colores
- Grid 2 columnas

### 3. SOLUCIÓN (Fondo Oscuro)
- Background: `#0F172A`
- Tarjetas oscuras con bordes de color
- Grid 3 columnas
- Iconos con fondos de color al 15%

### 4. METODOLOGÍA (Fondo Claro)
- Background: `#f8fafc`
- Tarjetas blancas con borde izquierdo de color
- Grid 2 columnas
- Números grandes en color

### 5. CASOS DE ÉXITO (Fondo Oscuro)
- Background: `#0F172A`
- Tarjetas oscuras con métricas
- Grid 3 columnas

### 6. VENTAJAS (Fondo Claro)
- Background: `#f8fafc`
- Grid 3 columnas
- 12 tarjetas con iconos de colores variados
- CTA amarillo centrado al final

### 7. CTA FINAL (Fondo Oscuro)
- Background: `#0F172A`
- Centrado
- Grid 3 columnas para entregables
- CTA amarillo grande
- Contacto en texto gris

---

## 💡 TIPS PARA PRESENTACIÓN "NANO BANANA"

### Estilo Visual
1. **Contraste Alto:** Alterna secciones oscuras (#0F172A) y claras (#f8fafc)
2. **Acentos Vibrantes:** Usa amarillo (#FACC15) para CTAs y elementos importantes
3. **Iconografía Consistente:** Material Symbols con relleno activado
4. **Espacios Generosos:** No temas el espacio en blanco (py-32)
5. **Bordes Sutiles:** Usa bordes de color al 20-30% de opacidad

### Jerarquía Tipográfica
1. **H1:** Plus Jakarta Sans 900, 60px, gradiente en palabra clave
2. **H2:** Plus Jakarta Sans 700, 48px, color sólido
3. **H3:** Plus Jakarta Sans 700, 24px
4. **Body:** Inter 400, 18-20px, line-height relaxed
5. **Small:** Inter 400, 14px, color secundario

### Paleta de Iconos por Categoría
- **Proceso/Operaciones:** Azul (#2463eb)
- **Éxito/Resultados:** Verde (#4ade80)
- **Destacado/Premium:** Amarillo (#FACC15)
- **Tecnología:** Púrpura (#8b5cf6)
- **Datos/Analytics:** Cyan (#06b6d4)
- **Seguridad:** Naranja (#f59e0b)

### Animaciones Sutiles
- Hover en tarjetas: `translateY(-4px)` + sombra
- Hover en botones: `scale(1.05)`
- Active en botones: `scale(0.95)`
- Widgets dashboard: animaciones float suaves

---

## 📦 RECURSOS PARA DESCARGAR

### Fuentes
- Plus Jakarta Sans: https://fonts.google.com/specimen/Plus+Jakarta+Sans
- Inter: https://fonts.google.com/specimen/Inter

### Iconos
- Material Symbols: https://fonts.google.com/icons

### Herramientas de Color
- Generador de variantes: https://www.tailwindshades.com/
- Convertidor HEX a RGB: https://www.rgbtohex.net/

---

## 🎯 CHECKLIST DE DISEÑO

- [ ] Tipografía: Plus Jakarta Sans para títulos, Inter para cuerpo
- [ ] Paleta: Azul #2463eb, Amarillo #FACC15, Verde #4ade80
- [ ] Fondos: Alterna #0F172A (oscuro) y #f8fafc (claro)
- [ ] Iconos: Material Symbols con FILL activado
- [ ] Espaciado: py-32 entre secciones, gap-6 en grids
- [ ] Bordes: 1px solid con 20-30% opacidad del color principal
- [ ] Sombras: 0 8px 32px con 25% opacidad en CTAs
- [ ] Animaciones: Hover translateY(-4px) en tarjetas
- [ ] Gradientes: Azul a Amarillo en palabras clave
- [ ] Responsive: Mobile-first, breakpoints en md (768px) y lg (1024px)

---

**Creado para:** Presentación Embajadores de IA  
**Estilo:** Nano Banana (Moderno, Vibrante, Alto Contraste)  
**Última actualización:** Abril 2026
