# Guía para Adriano — Cómo construir y editar la web de Lumo con Claude Code

Hola Adriano. Esta guía es para ti, no para Claude (de ti Claude ya sabe
porque lee el `CLAUDE.md` del repo automáticamente). Aquí te explico **cómo
hablarle a Claude** para que haga cambios en la web como quieras.

---

## 1. Instalación (una sola vez)

Necesitas tres cosas en tu Mac:

1. **Git y GitHub CLI**

   ```sh
   brew install git gh
   gh auth login
   ```

   Elige `GitHub.com` → `HTTPS` → `Login with a web browser`. Se abre el
   navegador, le das login con tu cuenta `lumocancun` y listo.

2. **Node.js 22+**

   ```sh
   brew install node
   node -v    # debe decir v22.algo o superior
   ```

3. **Claude Code**

   Descarga desde https://claude.com/claude-code y sigue el instalador.
   Al abrirlo por primera vez te pedirá iniciar sesión con tu cuenta de Claude.

Después, **clona el repo una sola vez**:

```sh
cd ~/Documents      # o donde quieras tenerlo
git clone https://github.com/carloabascalc/lumoarte-web.git
cd lumoarte-web
npm install         # instala dependencias (tarda 1-2 min)
```

---

## 2. Trabajar un día normal

Siempre que vayas a empezar a hacer cambios:

```sh
cd ~/Documents/lumoarte-web
git checkout main
git pull            # trae lo último que Carlo o tú hayáis mergeado
claude              # abre Claude Code dentro del repo
```

Dentro de Claude Code ya puedes pedirle cambios en lenguaje normal. Ejemplos:

> "Cambia el teléfono de contacto a 998 123 4567"

> "En la página de corte láser, añade una sección arriba de 'Precios' que
> diga que hacemos entregas a hoteles de la zona hotelera"

> "El precio de impresión 3D por gramo ahora es 8 pesos, no 7"

> "Añade un nuevo caso de éxito: hicimos 500 llaveros para el hotel Riu"

Claude va a:
1. **Pensar** qué archivos tocar (los ve y te dice cuáles).
2. **Hacerte los cambios** (te enseña exactamente qué está modificando).
3. **Crear una rama** (ej. `claude/precio-3d-8pesos`) y pushearla a GitHub.
4. Decirte el **link al deploy preview** para que lo veas en vivo antes
   de mergear.

---

## 3. Cómo revisar lo que Claude hizo

Claude te enseñará los cambios con un diff tipo:

```
- const PRECIO_POR_GRAMO = 7
+ const PRECIO_POR_GRAMO = 8
```

Lo rojo (`-`) es lo que quita, lo verde (`+`) lo que pone. Si te parece bien,
le dices **"sí, mergealo"** o **"ok, pushea"**. Si no, le dices qué cambiar.

Después del push, Vercel despliega automáticamente. Claude te pasará un link
tipo `https://lumoarte-abc123.vercel.app` — ábrelo y revisa visualmente.

Si todo bien, le dices a Claude: **"mergea la rama a main"**. Eso publica
el cambio en `lumocancun.com` en ~1 minuto.

Si algo está mal: **"deshaz esto y prueba otra cosa"**. Claude revierte y
vuelve a intentar.

---

## 4. Las partes editables más comunes

Si alguna vez quieres ser más específico, estos son los archivos que más
se tocan. Pero **no hace falta que los memorices** — dile a Claude en lenguaje
natural lo que quieres y él encuentra dónde cambiarlo.

| Qué quieres cambiar | Dónde vive |
|---|---|
| Teléfono, dirección, email, redes | `src/data/services.ts` (objeto `SITE`) |
| Precios de corte láser, 3D, plotter | `src/data/pricing.ts` |
| Productos del catálogo `/productos/` | `src/data/products.ts` |
| Sectores (hotel, corp, eventos) | `src/data/segments.ts` |
| Casos de éxito | `src/data/cases.ts` |
| Textos de la home | `src/pages/index.astro` |
| Texto "Sobre nosotros" | `src/pages/sobre-nosotros.astro` |
| Nav / menú | `src/components/Nav.astro` |
| Footer | `src/components/Footer.astro` |
| Fotos de galería | `src/assets/gallery/` |

---

## 5. Cómo pedirle cambios efectivos a Claude

Reglas sencillas para que Claude acierte a la primera:

### Sé específico con la página

Mal: *"cambia el título"*
Bien: *"en la home, cambia el título grande que dice 'Producción en serie
en Cancún' por 'Fabricamos para hoteles y eventos en Cancún'"*

### Da contexto del porqué cuando ayude

*"El precio de resina subió a 12 por gramo porque el proveedor subió
precios. Actualízalo en pricing y también en los PDFs de descarga si los
tocamos desde el código."*

Claude al saber el porqué hace cambios más consistentes.

### Para cambios visuales, dile qué quieres **conseguir**, no cómo

Mal: *"ponle `padding: 40px` al hero"*
Bien: *"el hero se ve muy apretado en móvil, dale más aire arriba y abajo"*

Claude decide la solución técnica mejor que tú (y que yo).

### Si quieres probar algo "a ver qué tal"

*"haz una rama de prueba y mete X — si no me gusta la borro"*

Claude crea rama `claude/prueba-X`, pushea, te pasa preview URL, y si no
te gusta, le dices **"descarta la rama"** y queda como si nada.

---

## 5bis. Lo que tu Claude hace solo (sin que se lo pidas)

**No tienes que pedir SEO, GEO, UI/UX ni diseño.** Tu Claude los aplica
de oficio en todo lo que haga. Está escrito como regla no negociable en
el `CLAUDE.md` que lee al abrir el repo.

### Qué significa en la práctica

Tú le pides algo normal como:

> "Cambia el precio de impresión 3D a 9 pesos el gramo"

Y por debajo tu Claude, sin preguntarte, además de cambiar el precio:

- Verifica que el precio nuevo quede en **HTML plano**, no solo en una
  imagen (así ChatGPT y Perplexity lo pueden leer y citar — GEO).
- Comprueba que el `<title>` y la `description` de la página sigan
  siendo coherentes (SEO).
- Revisa que en móvil el número se siga leyendo bien (UI).
- Mantiene la tipografía, color y espaciado del sistema (Diseño).

Si de paso ve un problema obvio en el área que está tocando (un `alt`
vacío, un heading mal usado, un contraste bajo), lo arregla **en el
mismo commit** y te lo menciona en una línea.

Si ve un problema **fuera** del área que estás cambiando (ej. editando
el Nav ve que una página aparte tiene título duplicado), te lo
**menciona al final** y tú decides si lo arregla o no.

### Qué sigue siendo tu decisión

Tu Claude aplica las disciplinas de oficio, pero **no inventa
estrategia** sin que lo pidas. Para cosas de dirección — "quiero
posicionar mejor en Google para la palabra X", "quiero rediseñar la
home entera", "la paleta necesita refresco" — ahí sí tienes que
arrancar tú la conversación.

Lo mismo con decisiones de negocio: Claude no decide bajar precios,
cambiar el teléfono, eliminar un servicio ni añadir una promoción.
Eso siempre viene de ti.

---

## 6. Las reglas que Claude ya sabe (no te preocupes)

Claude lee `CLAUDE.md` del repo cada vez que se abre, así que ya sabe:

- Marca siempre "Lumo" o "Lumo Cancún", nunca "Lumo Arte".
- No usar fotos de la "desatadora de nudos".
- No prometer "mismo día" ni "piezas únicas" — somos B2B por volumen.
- No mencionar "Riviera Maya", solo Cancún.
- Teléfono único 998 188 8048.
- No tocar `astro.config.mjs`, `vercel.json`, ni los IDs de JSON-LD sin preguntarte.

Si Claude propone algo que choca con tus reglas, **páralo**. Lee el
`CLAUDE.md` del repo y si crees que falta una regla, dile a Claude que la
añada:

> "Añade al CLAUDE.md que no usemos nunca la palabra 'barato', queremos
> posicionarnos como premium"

---

## 7. Cuándo pedirle a Carlo (no a tu Claude)

Tu Claude puede hacer el 95% del trabajo. Pero estas cosas pasan por Carlo
porque no estás en el team de Vercel:

- **Añadir o configurar un dominio nuevo** (ej. si compras otra URL).
- **Cambiar variables secretas** del proyecto (tokens, API keys).
- **Rollback de un deploy** desde la UI de Vercel (si publicas algo
  roto y quieres volver atrás rápido — aunque Claude también puede
  hacerlo con git revert).
- **Ver analytics** de visitas.

Para todo lo demás (código, textos, imágenes, precios, estructura, SEO,
diseño), tu Claude es independiente.

---

## 8. Si algo sale mal

### "Publiqué algo roto en producción"

Dile a Claude:

> "Lo último que mergeé rompió la web. Hazme un git revert del último
> commit en main y pushea"

Vercel despliega el revert en ~1 min.

### "Mi Claude no entiende lo que quiero"

Prueba con un ejemplo concreto. En vez de *"queda feo"*, abre
`lumocancun.com` en el navegador, haz una captura, pégasela a Claude y
dile *"lo que está marcado con rojo lo quiero así en vez de así"*.

### "No sé si Claude hizo lo que le pedí"

Pregúntale:

> "Resume en 3 líneas qué cambios acabas de hacer y en qué archivos"

### "Hay un conflicto con la rama de Carlo"

> "Haz pull de main, mergea main sobre mi rama actual, resuelve conflictos
> y vuelve a pushear"

---

## 9. Comandos útiles dentro de Claude Code

Puedes teclearlos directamente como mensaje:

| Comando | Qué hace |
|---|---|
| `/code-review` | Claude revisa los cambios actuales buscando bugs/problemas |
| `/security-review` | Revisión de seguridad (útil si tocas formularios) |
| `/simplify` | Limpia duplicación/complejidad después de un cambio |
| `/clear` | Borra la conversación actual (empezar fresco) |
| `/help` | Lista todos los comandos |

---

## 10. Tu primer cambio de prueba (recomendado)

Para probar que todo funciona, haz un cambio pequeño reversible:

1. Abre Claude Code en el repo.
2. Dile: *"Cambia temporalmente el teléfono del footer por 998 999 9999
   para hacer una prueba, haz la rama `claude/prueba-adriano`, pushea y
   pásame el link del preview"*.
3. Claude lo hace. Abre el link del preview, ve que el footer dice el
   nuevo número.
4. Dile: *"Perfecto, revierte el cambio y borra la rama"*.

Con eso compruebas que: clonado ✅, Claude funciona ✅, despliegues van
✅, y puedes revertir ✅.

---

## 11. Preguntas para resolver con Carlo

Si surge cualquiera de estas, mándale mensaje a Carlo antes de tocar:

- "Quiero comprar un dominio nuevo, ¿cómo lo conectamos?"
- "El formulario de contacto debería enviarme un email, ¿cómo lo
  configuramos?"
- "Quiero ver las visitas del sitio" (analytics de Vercel).
- "Rompí algo y no sé cómo volver atrás".

---

**Última cosa:** no tengas miedo de experimentar. Todo lo que hagas en una
rama no afecta a producción hasta que mergees. Y hasta un merge a main
tiene vuelta atrás en 1 minuto con un revert. La web no se rompe por
probar cosas.

Adelante.
