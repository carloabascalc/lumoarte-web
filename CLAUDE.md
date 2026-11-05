# Lumo Cancún — Guía del repo para Claude Code

Este archivo lo lee **automáticamente** cualquier sesión de Claude Code que
abra el repo. Sirve de onboarding tanto para Carlo como para Adriano y
asegura que Claude trabaje con el mismo contexto en las dos máquinas.

---

## 1. Qué es esto

Sitio web de **Lumo Cancún** — producción en serie en Cancún:

- Corte láser (CO₂ y fibra)
- Impresión 3D (FDM con impresoras Bambu Lab: H2C, A2L y, próximamente, H3C)
- Plotter / sublimación / recuerdos

El sitio está pensado para **B2B por volumen** (hoteles, agencias de eventos,
corporativo). Los textos no deben prometer piezas únicas ni "mismo día"
(ver reglas en §7).

### Dominios

| Dominio | Rol |
|---|---|
| `lumocancun.com` | **Canónico** del sitio principal (lo define `astro.config.mjs`). |
| `www.lumocancun.com` | Alias de `lumocancun.com`. |
| `cortelasercancun.com` | EMD para la landing de corte láser. Se sirve con rewrite en `vercel.json`. |
| `impresion3dcancun.com` | EMD para la landing de impresión 3D. Idem. |
| `lumoarte.com` | Dominio heredado — todavía está en el proyecto de Vercel pero NO se usa en el código. |

Los tres dominios activos apuntan al **mismo proyecto de Vercel** (`lumoarte`) y las
rewrites/redirects viven en `vercel.json`.

---

## 2. Stack

- **Astro 6** (SSG) con TypeScript strict.
- Hospedaje: **Vercel** (proyecto `lumoarte`, team `carloabascalc-2130s-projects`).
- Node ≥ 22.12 (ver `package.json`).
- **Sin framework UI** (ni React ni Vue) — todo `.astro` + CSS scoped.
- Animaciones: `motion` + `lenis` (smooth scroll).
- Analítica: `@vercel/analytics/astro` (inyectado en `Base.astro`).
- Sitemap: `@astrojs/sitemap` (filtra las páginas EMD).

---

## 3. Estructura del proyecto

```
src/
├── assets/            Imágenes optimizadas por Astro (gallery, logos, sectores, services)
│                      printers/*.svg: modelos animados, generados con tools/printer_art.py (no editar a mano)
├── components/        Componentes .astro (Hero, Nav, Footer, Gallery, Contact, etc.)
├── data/              SOURCE OF TRUTH — todo el contenido editable del sitio
│   ├── services.ts      Datos corporativos: SITE, ORG_ID, teléfono, dirección, JSON-LD base
│   ├── pricing.ts       Precios de láser, 3D, plotter, recuerdos
│   ├── machines.ts      Impresoras de «Equipo del taller» (H2C, A2L, H3C)
│   ├── products.ts      Catálogo /productos/
│   ├── segments.ts      Sectores (hotel, corp, souvenirs, eventos)
│   ├── cases.ts         Casos de éxito B2B
│   ├── catalog.ts       Productos destacados en home
│   └── galleryImages.ts Alt text por nombre de archivo (clave para SEO/AI)
├── layouts/
│   ├── Base.astro       Layout maestro: <head>, JSON-LD, Nav, Footer, Analytics
│   └── Article.astro    Para /recursos/
├── pages/
│   ├── index.astro             Home (lumocancun.com)
│   ├── cortelasercancun.astro  Landing que sirve cortelasercancun.com
│   ├── impresion3dcancun.astro Landing que sirve impresion3dcancun.com
│   ├── sobre-nosotros.astro
│   ├── aviso-de-privacidad.astro
│   ├── 404.astro
│   ├── servicios/              corte-laser.astro, impresion-3d.astro
│   ├── productos/              [slug].astro + index.astro (data-driven)
│   ├── sectores/               [slug].astro + index.astro (data-driven)
│   └── recursos/               Artículos E-E-A-T (fdm vs resina, etc.)
├── scripts/           TS del cliente (animations, cardTilt)
public/
├── images/            Assets estáticos que NO pasan por Astro Image
└── og/                Imágenes Open Graph
vercel.json            Rewrites, redirects, headers
astro.config.mjs       site: 'https://lumocancun.com', sitemap config
```

**Regla clave:** cambios de **contenido** (precios, teléfonos, direcciones,
productos, sectores, casos) van en `src/data/*.ts`, nunca hardcodeados en
componentes. El layout Base consume `SITE` y emite el JSON-LD a partir de ahí.

---

## 4. Comandos

```sh
npm install          # Instala dependencias
npm run dev          # Servidor local en http://localhost:4321
npm run build        # Build a ./dist/
npm run preview      # Sirve el build localmente
```

**Deploy:** cada `git push` a `main` dispara un deploy automático en Vercel. Las
ramas de feature generan preview deploys en URLs tipo `lumoarte-<hash>.vercel.app`.

---

## 5. Flujo de trabajo con Claude Code

### Ramas

- `main` — producción. No commitear directo salvo cambios triviales.
- Para cualquier cambio sustancial, Claude debe crear una rama
  `claude/<descripción-corta>` y hacer push ahí; luego el humano revisa
  y mergea a `main` desde GitHub.

### Commits

Mensajes en español o inglés, con prefijo de intención claro:

```
feat: añadir sección X
fix: corregir Y en Z
chore: actualizar dependencia W
docs: ajustar texto en /sobre-nosotros
```

Un commit = un cambio lógico. No mezclar refactor + feature + fix.

### Pull Requests

Solo cuando el humano lo pida explícitamente. No abrir PRs "por si acaso".

---

## 6. Disciplinas que Claude aplica POR DEFECTO (sin que se lo pidan)

**Regla no negociable:** en cada cambio sobre una página, componente,
texto, imagen o datos del sitio, Claude aplica las **cuatro
disciplinas** que siguen. No son servicios opcionales que el usuario
tenga que pedir explícitamente — son parte de la definición de
"terminado" en este repo.

Esto significa:

- Si el usuario pide "cambia este texto", Claude cambia el texto **y**
  verifica que el `<title>`/`description` sigan siendo coherentes
  (SEO), que el texto resultante sea legible para un LLM (GEO) y que
  siga leyéndose bien en móvil (UI/UX).
- Si el usuario pide "añade esta sección", Claude usa la jerarquía
  semántica correcta, aplica la tipografía/espaciado del sistema,
  añade `alt` a las imágenes, y si tiene datos numéricos los deja en
  HTML plano (no solo en imagen).
- Si Claude detecta de paso un problema obvio en una de las cuatro
  disciplinas en el área que está tocando, lo arregla **en el mismo
  commit** y lo menciona en una línea. No abre un commit aparte ni
  pregunta "¿quieres que también arregle X?" para fricciones menores.
- Si Claude detecta un problema fuera del área que está tocando
  (ejemplo: editando el Nav ve que una página aparte tiene título
  duplicado), lo **menciona al final del trabajo** en una línea, sin
  arreglarlo de motu propio. Eso queda a decisión del usuario.

El checklist al final de esta sección se ejecuta siempre antes de
reportar una tarea como hecha. Si alguno falla, Claude lo arregla
antes de decir "listo".

### 6.1 SEO (Google y buscadores tradicionales)

- Cada página tiene un `<title>` descriptivo y único, y una `description`
  propia. Nunca copiar entre páginas.
- `canonical` siempre con slash final (lo normaliza `Base.astro` l. 37-41).
  Mismatches de slash llevan a GSC a reportar "Alternative page with
  proper canonical tag".
- Las páginas EMD (`cortelasercancun.astro`, `impresion3dcancun.astro`)
  se excluyen del sitemap para que Google no las indexe como duplicadas
  (ver `astro.config.mjs` filter).
- Jerarquía semántica real: un solo `<h1>` por página, `<h2>` para
  secciones, `<h3>` bajo cada `<h2>`. No usar headings para tamaño.
- Imágenes con `alt` descriptivo (los alts de galería viven en
  `src/data/galleryImages.ts`, no inventar sobre la marcha).
- Internal linking entre servicios, sectores y productos — cada página
  de servicio debe enlazar a sectores relevantes y viceversa.
- Core Web Vitals: evitar bloquear el main thread, imágenes con
  `loading="lazy"` excepto el LCP, no cargar JS que no se use.

### 6.2 GEO (Generative Engine Optimization — ChatGPT, Perplexity, Claude, Gemini)

Objetivo: que cuando alguien pregunte a una IA "¿dónde hago impresión
3D en volumen en Cancún?", la respuesta cite Lumo.

- **JSON-LD rico** en `Base.astro`: `LocalBusiness` + `Person`
  (fundador) + `Service` por cada servicio + `ImageObject` con
  creator y copyright. Los `@id` (`ORG_ID`, `FOUNDER_ID`, `CATALOG_ID`)
  son estables — **no cambiar** sin razón fuerte, los crawlers ya los
  tienen indexados.
- **Datos en texto HTML, no solo en imágenes**: los crawlers de IA
  leen HTML plano. Precios, materiales, tiempos y capacidades deben
  estar en el `<body>` como texto, no solo embebidos en PDFs o
  rasterizados.
- **Lenguaje directo, estructura de pregunta-respuesta**: componentes
  como `FAQ.astro` y texto expositivo ayudan al scraping LLM. Preferir
  listas y tablas sobre párrafos densos cuando el dato es concreto
  (precio, material, dimensión).
- **E-E-A-T**: los artículos en `/recursos/` llevan autor visible
  (Adriano Abascal, arquitecto), fecha de actualización, citas
  externas. Esto sube la confianza del modelo en el contenido.
- **Consistencia de entidad**: NAP (Name, Address, Phone) idéntico
  sitewide, a través de `SITE` en `src/data/services.ts`. Cualquier
  variación confunde al grafo de conocimiento.

### 6.3 UI / UX

- **Mobile-first**: ~70% del tráfico es móvil. Diseñar primero para
  375px de ancho y escalar a desktop.
- **Jerarquía visual clara**: una sola acción primaria por vista
  (WhatsApp o cotización). Las secundarias (teléfono, descarga de PDF)
  en estilo subordinado.
- **Flujos cortos**: nunca más de 2 clicks del landing al contacto.
  El `WhatsAppButton.astro` persiste en todas las páginas.
- **Feedback inmediato**: botones con hover/active states, formularios
  con validación inline, animaciones de transición entre páginas
  (`PageTransition.astro` + `ClientRouter`).
- **Accesibilidad**: contrastes AA mínimo, `aria-label` en iconos
  interactivos, focus visible, orden de tabulación lógico.
- **Carga percibida**: hero con imagen crítica, resto diferido.
  Evitar CLS (saltos de layout) reservando espacio para imágenes.

### 6.4 Diseño web

- **Sistema tipográfico**: una familia principal, 3-4 escalas máximo.
  Jerarquía por peso + tamaño, no por color.
- **Espaciado consistente**: usar múltiplos de un grid (8 o 16px).
  No improvisar márgenes.
- **Paleta restringida**: acento `laser` y acento `3d` (ver
  `pageAccent` en `Base.astro`). No introducir colores nuevos sin
  propósito claro.
- **Fotografía real**: la galería (`src/assets/gallery/`) es el
  portfolio de piezas que ha hecho Lumo. Nunca sustituir por stock.
- **Animación con propósito**: `motion` y `lenis` están para reforzar
  jerarquía (reveal al scroll, parallax sutil), no para decorar.
  Animaciones largas o complejas se eliminan en móvil (`prefers-reduced-motion`).
- **Consistencia entre páginas**: Nav, Footer, Hero pattern, CTAs,
  todos repetibles. Si una página necesita un componente nuevo,
  considerar si debería ser global.

### Checklist tácito antes de reportar una tarea terminada

Cuando Claude termine un cambio visible, verificar:

1. ¿La página sigue respondiendo las preguntas "qué, para quién, cómo
   contactar, cuánto"?
2. ¿JSON-LD sigue validando (sin errores de schema.org)?
3. ¿El `<title>` y `description` son únicos y descriptivos?
4. ¿Funciona bien en 375px de ancho sin scroll horizontal?
5. ¿Las imágenes nuevas tienen `alt` y pasan por Astro Image?
6. ¿No hay texto o CTA que viole las reglas de marca (§7)?

---

## 7. Reglas de marca (Adriano)

Estas reglas son del cliente (Adriano). **Respetarlas siempre**, aunque
"suene mejor" lo otro:

1. **Nunca escribir "Lumo Arte"**. Solo "Lumo" o "Lumo Cancún".
2. **No usar fotos de la "desatadora de nudos"** en ningún sitio.
3. **No prometer "mismo día" ni "piezas únicas"** — el foco es volumen B2B.
4. **No mencionar "Riviera Maya"** — operamos en Cancún.
5. Teléfono único: **998 188 8048**. No listar otros números.
6. Fundador: **Adriano Abascal**, arquitecto, afiliado a Abascal Arquitectos.
7. **No mencionar impresión en resina ni "formato XL"** como equipo o servicio: solo las impresoras Bambu Lab (H2C, A2L y H3C próximamente).

---

## 8. Buenas prácticas de código

- **TypeScript strict** — no `any` ni `@ts-ignore` salvo justificación.
- Componentes `.astro` — un componente = una responsabilidad.
- Imágenes:
  - Si va a pasar por Astro Image (optimización, srcset): `src/assets/...`
  - Si es estática sin optimizar (favicon, OG): `public/...`
- CSS scoped dentro del propio `.astro`; si necesitas tokens globales
  están en `Base.astro`.
- Nada de `console.log` ni comentarios "TODO" en commits a `main`.
- Comentarios: solo si explican el **por qué**, no el **qué**.

---

## 9. Despliegue y dominios (Vercel)

- Proyecto: `lumoarte` (id `prj_8H9ciPcV3rHQjx7enhAEkuEiS8C4`).
- Team: `carloabascalc-2130s-projects`.
- Los DNS de los tres dominios activos deben apuntar al IP de Vercel
  (`216.198.79.1`). La configuración de cada dominio en el proyecto se ve en
  **Vercel → lumoarte → Settings → Domains**.
- Si un dominio nuevo muestra "This Connection Is Not Private" en Safari,
  es que **no está añadido como dominio del proyecto**: Vercel no
  provisiona cert SSL para dominios que no gestiona. Solución: añadirlo
  en el dashboard y esperar 1-2 min a que Let's Encrypt emita el cert.

---

## 10. Herramientas que usamos en Claude Code

Skills útiles para este repo:

- `/code-review` — revisión de los cambios actuales. Empezar en nivel `medium`.
- `/security-review` — revisión de seguridad antes de merge si tocamos formularios o headers.
- `/init` — regenerar o actualizar este `CLAUDE.md`.
- `/simplify` — después de un cambio, limpiar duplicación/complejidad.

MCPs conectadas que ayudan:

- **GitHub** — para leer/crear PRs, issues, archivos remotos.
- **Vercel** — para inspeccionar deploys, logs, errores de runtime,
  dominios, variables de entorno.

---

## 11. Cosas que **no** debe hacer Claude sin preguntar

- Cambiar `astro.config.mjs` (afecta sitemap y SEO).
- Tocar `vercel.json` headers/redirects (afecta producción directa).
- Alterar los `@id` de JSON-LD (`ORG_ID`, `FOUNDER_ID`, `CATALOG_ID`).
- Hacer `git push --force` sobre `main`.
- Borrar fotos de `src/assets/gallery/` (son el portfolio real).
- Añadir dependencias pesadas (React, Tailwind, etc.) sin justificar.

---

## 12. Contactos y división de accesos

- **Carlo Abascal** (`carloabascalc`) — admin del repo, owner del team de Vercel.
- **Adriano Abascal** (`lumocancun`) — colaborador Write en el repo.

### Qué puede hacer Adriano solo

Adriano **no está** en el team de Vercel (plan Hobby no lo permite sin pagar
Pro). Vercel está conectado al repo, así que cada push suyo a `main` o a una
rama dispara deploy automáticamente aunque él no tenga acceso al dashboard.

Puede hacer sin pedir nada:
- Editar cualquier archivo del repo (componentes, data, páginas, estilos).
- Crear ramas `claude/<cambio>`, pushear, y ver el resultado en la URL de
  preview que GitHub muestra en la rama.
- Mergear a `main` → despliega a producción (`lumocancun.com`).
- Leer logs de runtime/build vía el MCP de Vercel de su Claude (acceso de
  lectura limitado, suele bastar para diagnosticar errores).

### Qué tiene que pedirle a Carlo

- Añadir, quitar o configurar **dominios**.
- Cambiar **variables de entorno** del proyecto.
- Hacer **rollback** de un deploy desde la UI de Vercel.
- Ver **analytics** y métricas del dashboard.
- Añadir **integrations** (Sentry, Slack, etc.).

### Trabajo paralelo

Cuando los dos vayáis a tocar código a la vez: **pull antes de empezar**,
trabajar en rama propia (`claude/<tu-cambio>`), push a la rama, y mergear
por PR para evitar conflictos.
