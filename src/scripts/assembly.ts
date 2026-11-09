// Mecánica común de las secciones «assembly»: el progreso del scroll mueve un
// SVG que LazyArt ya descargó. Cada sección solo define sus etapas y qué mover.

export interface AssemblyConfig {
  id: string;
  /** Etapas del letrero inferior: [texto, progreso en el que termina]. */
  stages: [string, number][];
  /** Recibe el SVG cargado y devuelve la función que lo acomoda según el progreso (0-1). */
  setup: (svg: SVGSVGElement) => (p: number) => void;
}

export const clamp = (v: number, lo = 0, hi = 1) => Math.max(lo, Math.min(hi, v));
export const ease = (t: number) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);

/** Convierte un desplazamiento en milímetros a pantalla con la proyección que el generador guardó en el SVG. */
export function projector(svg: SVGSVGElement) {
  const [xx, xy, yx, yy, yz] = (svg.dataset.v as string).split(",").map(Number);
  return (el: Element, dx: number, dy: number, dz: number) => {
    (el as SVGGElement).style.transform = `translate(${xx * dx + xy * dy}px, ${yx * dx + yy * dy + yz * dz}px)`;
  };
}

export function assembly({ id, stages, setup }: AssemblyConfig) {
  let stop: (() => void) | undefined;

  document.addEventListener("astro:page-load", () => {
    stop?.();
    stop = undefined;
    const wrap = document.getElementById(id);
    if (!wrap || matchMedia("(prefers-reduced-motion: reduce)").matches) return;

    const art = wrap.querySelector<HTMLElement>("[data-lazy-art]");
    const scene = wrap.querySelector<HTMLElement>(".assembly-stage");
    const grid = wrap.querySelector<HTMLElement>(".assembly-grid-bg");
    const label = wrap.querySelector<HTMLElement>("[data-hint-label]");
    const number = wrap.querySelector<HTMLElement>("[data-hint-stage]");
    let render: ((p: number) => void) | undefined;
    let pending = false;
    let stage = -1;

    const tick = () => {
      pending = false;
      const rect = wrap.getBoundingClientRect();
      // El escenario mide lo que de verdad recorre el sticky. window.innerHeight no sirve:
      // en móvil crece si algo de la página se desborda a lo ancho y cambia con la barra del navegador.
      const total = rect.height - (scene?.offsetHeight ?? window.innerHeight);
      if (total <= 0) return;
      const p = clamp(-rect.top / total);
      if (grid) {
        grid.style.opacity = String(
          p < 0.35 ? (p / 0.35) * 0.5 : p < 0.92 ? 0.5 - ((p - 0.35) / 0.57) * 0.4 : Math.max(0, 0.1 - ((p - 0.92) / 0.08) * 0.1),
        );
      }
      const now = stages.findIndex(([, end]) => p < end);
      const current = now < 0 ? stages.length - 1 : now;
      if (current !== stage && label && number) {
        stage = current;
        label.textContent = stages[current][0];
        number.textContent = String(current + 1).padStart(2, "0");
      }
      render?.(p);
    };
    const onScroll = () => {
      if (pending) return;
      pending = true;
      requestAnimationFrame(tick);
    };
    const bind = () => {
      const svg = art?.querySelector("svg");
      if (svg) {
        render = setup(svg);
        tick();
      }
    };

    art?.addEventListener("lazy-art:loaded", bind);
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll, { passive: true });
    bind();
    tick();
    stop = () => {
      art?.removeEventListener("lazy-art:loaded", bind);
      window.removeEventListener("scroll", onScroll);
      window.removeEventListener("resize", onScroll);
    };
  });
}
