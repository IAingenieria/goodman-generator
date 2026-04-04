import { Helmet } from 'react-helmet-async';

// ── Colores Goodman Tech ───────────────────────────────────────────────────
const DARK   = '#0F172A';
const CARD   = '#1e293b';
const CARD2  = '#162032';
const BLUE   = '#2463eb';
const YELLOW = '#FACC15';
const GREEN  = '#4ade80';
const SLATE3 = '#cbd5e1';
const SLATE4 = '#94a3b8';
const SLATE5 = '#64748b';

const WA_LINK = 'https://wa.me/528126350902?text=Hola%2C%20quiero%20información%20sobre%20Como%20aplicar%20la%20IA%20en%20mi%20empresa%20para%20mi%20empresa';
const SCHEMA  = `{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "WebPage",
      "@id": "https://www.goodmantech.com.mx/empresas/como-aplicar-la-ia-en-mi-empresa",
      "url": "https://www.goodmantech.com.mx/empresas/como-aplicar-la-ia-en-mi-empresa",
      "name": "Cómo Aplicar la IA en mi Empresa | Goodman Tech",
      "description": "Aprende cómo aplicar la IA en tu empresa y obtén resultados medibles en 90 días. Goodman Tech implementa soluciones de IA en Monterrey. ¡Agenda tu diagnóstico gratis!",
      "dateModified": "2026-04-03",
      "inLanguage": "es-MX",
      "breadcrumb": {
        "@type": "BreadcrumbList",
        "itemListElement": [
          {
            "@type": "ListItem",
            "position": 1,
            "name": "Inicio",
            "item": "https://www.goodmantech.com.mx"
          },
          {
            "@type": "ListItem",
            "position": 2,
            "name": "Empresas",
            "item": "https://www.goodmantech.com.mx/empresas"
          },
          {
            "@type": "ListItem",
            "position": 3,
            "name": "Como aplicar la IA en mi empresa",
            "item": "https://www.goodmantech.com.mx/empresas/como-aplicar-la-ia-en-mi-empresa"
          }
        ]
      }
    },
    {
      "@type": "ProfessionalService",
      "name": "Goodman Tech",
      "url": "https://www.goodmantech.com.mx",
      "telephone": "+52 81 2635 0902",
      "email": "info@goodmantech.com.mx",
      "address": {
        "@type": "PostalAddress",
        "addressLocality": "Monterrey",
        "addressRegion": "Nuevo León",
        "addressCountry": "MX"
      },
      "geo": {
        "@type": "GeoCoordinates",
        "latitude": "25.6866",
        "longitude": "-100.3161"
      },
      "areaServed": "México",
      "sameAs": [
        "https://wa.me/528126350902"
      ]
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "¿Cómo aplicar la IA en mi empresa si no tengo equipo técnico?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "No necesitas equipo técnico propio. Goodman Tech se encarga de toda la implementación, capacitación y soporte. Nuestro modelo está diseñado para que tu equipo adopte las herramientas de IA sin fricciones, con acompañamiento en cada etapa del proceso."
          }
        },
        {
          "@type": "Question",
          "name": "¿Cuánto cuesta implementar inteligencia artificial en una empresa en México?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "El costo varía según el alcance del proyecto, pero contamos con planes desde empresas medianas hasta corporativos. Ofrecemos un diagnóstico gratuito para definir el presupuesto exacto y el retorno estimado antes de cualquier inversión."
          }
        },
        {
          "@type": "Question",
          "name": "¿En cuánto tiempo veré resultados reales al aplicar IA en mi negocio?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Nuestros clientes empiezan a ver mejoras operativas entre las semanas 4 y 8. Al día 90 entregamos un reporte formal de KPIs con el impacto medible en productividad, costos o ingresos según los objetivos definidos al inicio."
          }
        },
        {
          "@type": "Question",
          "name": "¿La IA puede integrarse a los sistemas que ya usa mi empresa como ERP o CRM?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Sí. Integramos soluciones de IA con los principales ERP, CRM y plataformas de gestión como SAP, Salesforce, HubSpot, Odoo y sistemas propios mediante APIs. La integración no interrumpe tu operación actual."
          }
        },
        {
          "@type": "Question",
          "name": "¿Qué tipo de empresas pueden beneficiarse de aplicar inteligencia artificial?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Cualquier empresa con procesos repetitivos, datos sin explotar o cuellos de botella operativos puede aplicar IA con éxito. Trabajamos con empresas de manufactura, retail, logística, servicios financieros y salud en México."
          }
        }
      ]
    }
  ]
}`;

const EmpresasComoAplicarLaIaEnMiEmpresa = () => {
  return (
    <div style={{ fontFamily: '"Inter", sans-serif', backgroundColor: DARK, color: 'white', minHeight: '100vh' }}>
      <Helmet>
        <title>Cómo Aplicar la IA en mi Empresa | Goodman Tech | Goodman Tech</title>
        <meta name="description" content="Aprende cómo aplicar la IA en tu empresa y obtén resultados medibles en 90 días. Goodman Tech implementa soluciones de IA en Monterrey. ¡Agenda tu diagnóstico gratis!" />
        <link rel="canonical" href="https://www.goodmantech.com.mx/empresas/como-aplicar-la-ia-en-mi-empresa" />

        {/* Open Graph */}
        <meta property="og:title" content="Cómo Aplicar la IA en mi Empresa | Goodman Tech | Goodman Tech" />
        <meta property="og:description" content="Aprende cómo aplicar la IA en tu empresa y obtén resultados medibles en 90 días. Goodman Tech implementa soluciones de IA en Monterrey. ¡Agenda tu diagnóstico gratis!" />
        <meta property="og:url" content="https://www.goodmantech.com.mx/empresas/como-aplicar-la-ia-en-mi-empresa" />
        <meta property="og:type" content="website" />
        <meta property="og:locale" content="es_MX" />
        <meta property="og:site_name" content="Goodman Tech" />
        <meta property="og:image" content="https://www.goodmantech.com.mx/og/como-aplicar-la-ia-en-mi-empresa.jpg" />
        <meta property="og:image:alt" content="Director de empresa en Monterrey México aprendiendo cómo aplicar la IA en su empresa con Goodman Tech" />

        {/* Twitter Cards */}
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:title" content="Cómo Aplicar la IA en mi Empresa | Goodman Tech" />
        <meta name="twitter:description" content="Aprende cómo aplicar la IA en tu empresa y obtén resultados medibles en 90 días. Goodman Tech implementa soluciones de IA en Monterrey. ¡Agenda tu diagnóstico gratis!" />
        <meta name="twitter:image" content="https://www.goodmantech.com.mx/og/como-aplicar-la-ia-en-mi-empresa.jpg" />

        {/* Geo */}
        <meta name="geo.region" content="MX-NL" />
        <meta name="geo.placename" content="Monterrey, Nuevo León" />
        <meta name="geo.position" content="25.6866;-100.3161" />
        <meta name="ICBM" content="25.6866, -100.3161" />

        {/* Fuentes */}
        <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800;900&family=Inter:wght@400;500;600&display=swap" rel="stylesheet" />
        <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" rel="stylesheet" />

        {/* Schema JSON-LD */}
        <script type="application/ld+json">{SCHEMA}</script>
      </Helmet>

      {/* ═══ HERO ═══ */}
      <section style={{ padding: '5rem 1.5rem 4rem', background: DARK, position: 'relative', overflow: 'hidden' }}>
        {/* Glows decorativos */}
        <div style={{ position:'absolute', top:'-60px', right:'-40px', width:'380px', height:'380px',
          borderRadius:'50%', background:`radial-gradient(circle, #2463eb 0%, transparent 70%)`,
          opacity: 0.07, pointerEvents:'none' }} />
        <div style={{ position:'absolute', bottom:'-40px', left:'-20px', width:'280px', height:'280px',
          borderRadius:'50%', background:`radial-gradient(circle, #FACC15 0%, transparent 70%)`,
          opacity: 0.07, pointerEvents:'none' }} />

        <div style={{ maxWidth:'860px', margin:'0 auto', position:'relative' }}>
          {/* Badge */}
          <div style={{ display:'inline-flex', alignItems:'center', gap:'6px',
            background:'#2463eb22', border:'1px solid #2463eb44',
            color:'#60a5fa', fontSize:'11px', fontWeight:600, letterSpacing:'0.08em',
            textTransform:'uppercase', padding:'5px 14px', borderRadius:'100px',
            marginBottom:'1.2rem' }}>
            <span className="material-symbols-outlined" style={{ fontSize:'14px', fontVariationSettings:'"FILL" 1' }}>smart_toy</span>
            Goodman Tech · IA para Empresas · 03/04/2026
          </div>

          {/* H1 */}
          <h1 style={{ fontFamily:'"Plus Jakarta Sans", sans-serif', fontWeight:900,
            fontSize:'clamp(26px, 5vw, 44px)', lineHeight:1.15, marginBottom:'1rem',
            color:'white' }}>
            Cómo Aplicar la IA en tu Empresa y Crecer en 90 Días
          </h1>

          {/* Subtítulo */}
          <p style={{ fontSize:'16px', color: SLATE4, lineHeight:1.65,
            maxWidth:'560px', marginBottom:'1.5rem' }}>
            Soluciones de inteligencia artificial diseñadas para directores y dueños de empresa en México que quieren automatizar, escalar y medir resultados reales.
          </p>

          {/* Stat hero */}
          <div style={{ background: CARD2, border:`1px solid #2463eb33`,
            borderRadius:'12px', padding:'0.75rem 1.1rem',
            display:'inline-flex', alignItems:'center', gap:'8px',
            marginBottom:'1.8rem' }}>
            <span className="material-symbols-outlined" style={{ fontSize:'16px', color: YELLOW, fontVariationSettings:'"FILL" 1' }}>bar_chart</span>
            <span style={{ fontSize:'13px', color: SLATE3 }}>Las empresas que aplican IA reportan hasta 40% más eficiencia operativa en el primer año — McKinsey 2024.</span>
          </div>

          {/* CTAs */}
          <div style={{ display:'flex', gap:'10px', flexWrap:'wrap' }}>
            <a href={WA_LINK} target="_blank" rel="noopener noreferrer"
              style={{ display:'inline-flex', alignItems:'center', gap:'6px',
                background: YELLOW, color:'#0F172A',
                fontFamily:'"Plus Jakarta Sans", sans-serif', fontWeight:700,
                fontSize:'14px', padding:'11px 22px', borderRadius:'8px',
                textDecoration:'none' }}>
              <span className="material-symbols-outlined" style={{ fontSize:'18px', fontVariationSettings:'"FILL" 1' }}>calendar_month</span>
              Agendar Diagnóstico Gratuito
            </a>
            <a href="#que-es"
              style={{ display:'inline-flex', alignItems:'center', gap:'6px',
                background:'transparent', color:'white', fontSize:'14px',
                fontWeight:600, padding:'11px 22px', borderRadius:'8px',
                border:'1px solid #ffffff22', textDecoration:'none' }}>
              <span className="material-symbols-outlined" style={{ fontSize:'16px' }}>arrow_downward</span>
              Ver el análisis
            </a>
          </div>
        </div>
      </section>

      {/* ═══ PROBLEMA ═══ */}
      <section id="que-es" style={{ padding:'2.5rem 1.5rem', background:'#0a1628' }}>
        <div style={{ maxWidth:'860px', margin:'0 auto' }}>
          <p style={{ fontSize:'10px', fontWeight:700, letterSpacing:'0.12em',
            textTransform:'uppercase', color:'#f87171', marginBottom:'0.8rem' }}>
            EL PROBLEMA
          </p>
          <h2 style={{ fontFamily:'"Plus Jakarta Sans", sans-serif', fontWeight:900,
            fontSize:'clamp(18px,3vw,26px)', color:'white', marginBottom:'1rem' }}>
            ¿Por qué tu empresa aún no sabe cómo aplicar la IA y está perdiendo competitividad?
          </h2>
          {/* Answer-First paragraph — citable por IA */}
          <p className="answer-first-paragraph"
            style={{ fontSize:'15px', color: SLATE3, lineHeight:1.7,
              maxWidth:'680px', marginBottom:'1.2rem',
              borderLeft:`3px solid #2463eb`, paddingLeft:'1rem' }}>
            El 67% de los directivos en México reconoce que quiere adoptar inteligencia artificial pero no sabe por dónde empezar. Sin una hoja de ruta clara, los proyectos de IA fracasan antes de arrancar. El problema no es la tecnología: es la falta de una metodología probada adaptada a tu industria y tamaño de empresa.
          </p>
          <p style={{ fontSize:'13px', color: SLATE5 }}>
            Fuente: INEGI Encuesta Digital, 2025
          </p>
          {/* KPIs */}
          <div style={{ display:'grid', gridTemplateColumns:'repeat(auto-fit,minmax(160px,1fr))',
            gap:'10px', marginTop:'1.5rem' }}>
            <div style={{ background: CARD, border:'1px solid #ffffff0d', borderRadius:'12px', padding:'1rem', textAlign:'center' }}>
              <p style={{ fontFamily:'"Plus Jakarta Sans",sans-serif', fontWeight:900, fontSize:'26px', color: YELLOW, margin:0 }}>60%</p>
              <p style={{ fontSize:'11px', color: SLATE5, marginTop:'4px' }}>ahorro en procesos repetitivos</p>
            </div>
            <div style={{ background: CARD, border:'1px solid #ffffff0d', borderRadius:'12px', padding:'1rem', textAlign:'center' }}>
              <p style={{ fontFamily:'"Plus Jakarta Sans",sans-serif', fontWeight:900, fontSize:'26px', color: GREEN, margin:0 }}>90 días</p>
              <p style={{ fontSize:'11px', color: SLATE5, marginTop:'4px' }}>al primer resultado medible</p>
            </div>
            <div style={{ background: CARD, border:'1px solid #ffffff0d', borderRadius:'12px', padding:'1rem', textAlign:'center' }}>
              <p style={{ fontFamily:'"Plus Jakarta Sans",sans-serif', fontWeight:900, fontSize:'26px', color:'#60a5fa', margin:0 }}>280%</p>
              <p style={{ fontSize:'11px', color: SLATE5, marginTop:'4px' }}>ROI promedio primer año</p>
            </div>
          </div>
        </div>
      </section>

      {/* ═══ SOLUCIÓN ═══ */}
      <section style={{ padding:'2.5rem 1.5rem', background: DARK }}>
        <div style={{ maxWidth:'860px', margin:'0 auto' }}>
          <p style={{ fontSize:'10px', fontWeight:700, letterSpacing:'0.12em',
            textTransform:'uppercase', color:'#60a5fa', marginBottom:'0.8rem' }}>
            LA SOLUCIÓN
          </p>
          <h2 style={{ fontFamily:'"Plus Jakarta Sans", sans-serif', fontWeight:900,
            fontSize:'clamp(18px,3vw,26px)', color:'white', marginBottom:'0.5rem' }}>
            Cómo Goodman Tech implementa IA en tu empresa y convierte ineficiencias en resultados medibles
          </h2>
          <p style={{ fontSize:'14px', color: SLATE4, marginBottom:'1.5rem' }}>
            Implementamos IA en tu empresa con resultados medibles en 90 días. Sin cambiar tu ERP, sin tirar lo que ya funciona.
          </p>

          <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:'1.5rem' }}>
            <div>
              <p style={{ fontSize:'12px', fontWeight:600, color: YELLOW,
                marginBottom:'0.75rem', textTransform:'uppercase', letterSpacing:'0.06em' }}>
                Lo que obtienes
              </p>
                              <div key="0" style={{display:"flex",gap:"10px",alignItems:"flex-start",marginBottom:"10px"}}><span style={{color:"#4ade80",marginTop:"2px",flexShrink:0}}>✓</span><span style={{fontSize:"14px",color:"#cbd5e1",lineHeight:"1.5"}}>Automatiza procesos repetitivos y libera hasta 30% del tiempo de tu equipo desde el primer mes</span></div>
                <div key="1" style={{display:"flex",gap:"10px",alignItems:"flex-start",marginBottom:"10px"}}><span style={{color:"#4ade80",marginTop:"2px",flexShrink:0}}>✓</span><span style={{fontSize:"14px",color:"#cbd5e1",lineHeight:"1.5"}}>Reduce costos operativos con modelos de IA entrenados específicamente para tu industria</span></div>
                <div key="2" style={{display:"flex",gap:"10px",alignItems:"flex-start",marginBottom:"10px"}}><span style={{color:"#4ade80",marginTop:"2px",flexShrink:0}}>✓</span><span style={{fontSize:"14px",color:"#cbd5e1",lineHeight:"1.5"}}>Toma decisiones basadas en datos con dashboards inteligentes en tiempo real</span></div>
                <div key="3" style={{display:"flex",gap:"10px",alignItems:"flex-start",marginBottom:"10px"}}><span style={{color:"#4ade80",marginTop:"2px",flexShrink:0}}>✓</span><span style={{fontSize:"14px",color:"#cbd5e1",lineHeight:"1.5"}}>Escala tu operación sin aumentar plantilla gracias a agentes de IA integrados a tus sistemas actuales</span></div>
                <div key="4" style={{display:"flex",gap:"10px",alignItems:"flex-start",marginBottom:"10px"}}><span style={{color:"#4ade80",marginTop:"2px",flexShrink:0}}>✓</span><span style={{fontSize:"14px",color:"#cbd5e1",lineHeight:"1.5"}}>Mide el ROI de cada solución implementada con métricas claras desde el día uno</span></div>
            </div>
            <div>
              <p style={{ fontSize:'12px', fontWeight:600, color:'#60a5fa',
                marginBottom:'0.75rem', textTransform:'uppercase', letterSpacing:'0.06em' }}>
                Nuestro proceso
              </p>
                              <div key="0" style={{background:"#162032",border:"1px solid #2463eb33",borderRadius:"12px",padding:"1rem",marginBottom:"8px"}}><span style={{color:"#FACC15",fontWeight:700,fontSize:"13px"}}>Paso 1: Diagnóstico — Analizamos tus procesos actuales e identificamos los puntos de mayor impacto para aplicar IA en tu empresa.</span></div>
                <div key="1" style={{background:"#162032",border:"1px solid #2463eb33",borderRadius:"12px",padding:"1rem",marginBottom:"8px"}}><span style={{color:"#FACC15",fontWeight:700,fontSize:"13px"}}>Paso 2: Diseño — Creamos una hoja de ruta personalizada con soluciones de IA priorizadas por retorno de inversión y velocidad de implementación.</span></div>
                <div key="2" style={{background:"#162032",border:"1px solid #2463eb33",borderRadius:"12px",padding:"1rem",marginBottom:"8px"}}><span style={{color:"#FACC15",fontWeight:700,fontSize:"13px"}}>Paso 3: Implementación — Desplegamos las herramientas de inteligencia artificial integradas a tus sistemas en un sprint de 30 a 60 días.</span></div>
                <div key="3" style={{background:"#162032",border:"1px solid #2463eb33",borderRadius:"12px",padding:"1rem",marginBottom:"8px"}}><span style={{color:"#FACC15",fontWeight:700,fontSize:"13px"}}>Paso 4: Medición — Entregamos reporte de resultados a los 90 días con KPIs, ahorro generado y plan de escalabilidad.</span></div>
            </div>
          </div>
        </div>
      </section>

      {/* ═══ FAQ ═══ */}
      <section style={{ padding:'2.5rem 1.5rem', background:'#0a1628' }}>
        <div style={{ maxWidth:'860px', margin:'0 auto' }}>
          <p style={{ fontSize:'10px', fontWeight:700, letterSpacing:'0.12em',
            textTransform:'uppercase', color:'#60a5fa', marginBottom:'0.8rem' }}>
            PREGUNTAS FRECUENTES
          </p>
          <h2 style={{ fontFamily:'"Plus Jakarta Sans", sans-serif', fontWeight:900,
            fontSize:'clamp(18px,3vw,24px)', color:'white', marginBottom:'1.2rem' }}>
            Lo que preguntan los directores
          </h2>
                        <div key="0" style={{background:"#162032",border:"1px solid #ffffff0d",borderRadius:"12px",padding:"1rem 1.1rem",marginBottom:"8px"}}><p style={{fontWeight:700,fontSize:"13px",color:"white",marginBottom:"5px"}}>¿Cómo aplicar la IA en mi empresa si no tengo equipo técnico?</p><p style={{fontSize:"13px",color:"#94a3b8",lineHeight:"1.55",margin:0}}>No necesitas equipo técnico propio. Goodman Tech se encarga de toda la implementación, capacitación y soporte. Nuestro modelo está diseñado para que tu equipo adopte las herramientas de IA sin fricciones, con acompañamiento en cada etapa del proceso.</p></div>
              <div key="1" style={{background:"#162032",border:"1px solid #ffffff0d",borderRadius:"12px",padding:"1rem 1.1rem",marginBottom:"8px"}}><p style={{fontWeight:700,fontSize:"13px",color:"white",marginBottom:"5px"}}>¿Cuánto cuesta implementar inteligencia artificial en una empresa en México?</p><p style={{fontSize:"13px",color:"#94a3b8",lineHeight:"1.55",margin:0}}>El costo varía según el alcance del proyecto, pero contamos con planes desde empresas medianas hasta corporativos. Ofrecemos un diagnóstico gratuito para definir el presupuesto exacto y el retorno estimado antes de cualquier inversión.</p></div>
              <div key="2" style={{background:"#162032",border:"1px solid #ffffff0d",borderRadius:"12px",padding:"1rem 1.1rem",marginBottom:"8px"}}><p style={{fontWeight:700,fontSize:"13px",color:"white",marginBottom:"5px"}}>¿En cuánto tiempo veré resultados reales al aplicar IA en mi negocio?</p><p style={{fontSize:"13px",color:"#94a3b8",lineHeight:"1.55",margin:0}}>Nuestros clientes empiezan a ver mejoras operativas entre las semanas 4 y 8. Al día 90 entregamos un reporte formal de KPIs con el impacto medible en productividad, costos o ingresos según los objetivos definidos al inicio.</p></div>
              <div key="3" style={{background:"#162032",border:"1px solid #ffffff0d",borderRadius:"12px",padding:"1rem 1.1rem",marginBottom:"8px"}}><p style={{fontWeight:700,fontSize:"13px",color:"white",marginBottom:"5px"}}>¿La IA puede integrarse a los sistemas que ya usa mi empresa como ERP o CRM?</p><p style={{fontSize:"13px",color:"#94a3b8",lineHeight:"1.55",margin:0}}>Sí. Integramos soluciones de IA con los principales ERP, CRM y plataformas de gestión como SAP, Salesforce, HubSpot, Odoo y sistemas propios mediante APIs. La integración no interrumpe tu operación actual.</p></div>
              <div key="4" style={{background:"#162032",border:"1px solid #ffffff0d",borderRadius:"12px",padding:"1rem 1.1rem",marginBottom:"8px"}}><p style={{fontWeight:700,fontSize:"13px",color:"white",marginBottom:"5px"}}>¿Qué tipo de empresas pueden beneficiarse de aplicar inteligencia artificial?</p><p style={{fontSize:"13px",color:"#94a3b8",lineHeight:"1.55",margin:0}}>Cualquier empresa con procesos repetitivos, datos sin explotar o cuellos de botella operativos puede aplicar IA con éxito. Trabajamos con empresas de manufactura, retail, logística, servicios financieros y salud en México.</p></div>
        </div>
      </section>

      {/* ═══ CTA FINAL ═══ */}
      <section style={{ padding:'3rem 1.5rem',
        background:'linear-gradient(135deg,#0f2547 0%,#1a1a2e 50%,#0f172a 100%)',
        textAlign:'center' }}>
        <div style={{ maxWidth:'600px', margin:'0 auto' }}>
          <div style={{ display:'inline-flex', alignItems:'center', gap:'6px',
            background:'#2463eb22', border:'1px solid #2463eb44', color:'#60a5fa',
            fontSize:'10px', fontWeight:700, letterSpacing:'0.1em', textTransform:'uppercase',
            padding:'4px 14px', borderRadius:'100px', marginBottom:'1rem' }}>
            SIN COSTO · SIN COMPROMISO · 45 MINUTOS
          </div>
          <h2 style={{ fontFamily:'"Plus Jakarta Sans", sans-serif', fontWeight:900,
            fontSize:'clamp(20px,4vw,30px)', color:'white', marginBottom:'0.6rem' }}>
            Agenda hoy tu diagnóstico gratuito y descubre cómo aplicar la IA en tu empresa este trimestre
          </h2>
          <p style={{ fontSize:'14px', color: SLATE4, lineHeight:1.65, marginBottom:'1.5rem' }}>
            En 45 minutos identificamos los 3 procesos con mayor desperdicio
            en tu empresa y te mostramos cómo la IA los resuelve con tus números reales.
          </p>

          <a href={WA_LINK} target="_blank" rel="noopener noreferrer"
            style={{ display:'inline-flex', alignItems:'center', gap:'8px',
              background: YELLOW, color:'#0F172A',
              fontFamily:'"Plus Jakarta Sans", sans-serif', fontWeight:700,
              fontSize:'15px', padding:'13px 28px', borderRadius:'8px',
              textDecoration:'none', marginBottom:'1.2rem' }}>
            <span className="material-symbols-outlined" style={{ fontSize:'20px', fontVariationSettings:'"FILL" 1' }}>calendar_month</span>
            Agendar Diagnóstico Gratuito →
          </a>

          <div style={{ display:'flex', justifyContent:'center', gap:'1.5rem',
            flexWrap:'wrap', marginTop:'1rem' }}>
            <span style={{ fontSize:'12px', color: SLATE5, display:'flex', alignItems:'center', gap:'5px' }}>
              <span className="material-symbols-outlined" style={{ fontSize:'14px', color: BLUE, fontVariationSettings:'"FILL" 1' }}>person</span>
              Zenon Vilchis
            </span>
            <span style={{ fontSize:'12px', color: SLATE5, display:'flex', alignItems:'center', gap:'5px' }}>
              <span className="material-symbols-outlined" style={{ fontSize:'14px', color: BLUE, fontVariationSettings:'"FILL" 1' }}>phone</span>
              +52 81 2635 0902
            </span>
            <span style={{ fontSize:'12px', color: SLATE5, display:'flex', alignItems:'center', gap:'5px' }}>
              <span className="material-symbols-outlined" style={{ fontSize:'14px', color: BLUE, fontVariationSettings:'"FILL" 1' }}>language</span>
              goodmantech.com.mx
            </span>
          </div>
        </div>
      </section>

    </div>
  );
};

export default EmpresasComoAplicarLaIaEnMiEmpresa;
