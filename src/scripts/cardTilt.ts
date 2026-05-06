type TiltOptions = {
  maxX?: number;
  maxY?: number;
  glareRange?: number;
};

export function initCardTilt(selector: string, opts: TiltOptions = {}) {
  if (typeof window === "undefined") return;
  const isTouch = matchMedia("(hover: none)").matches;
  const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (isTouch || reduced) return;

  const maxX = opts.maxX ?? 8;
  const maxY = opts.maxY ?? 6;

  const cards = document.querySelectorAll<HTMLElement>(selector);
  cards.forEach((card) => {
    if ((card as any).__tiltInit) return;
    (card as any).__tiltInit = true;

    let raf = 0;
    let tx = 0, ty = 0, gx = 50, gy = 50;
    let cx = 0, cy = 0, cgx = 50, cgy = 50;

    const lerp = (a: number, b: number, t: number) => a + (b - a) * t;

    function tick() {
      cx = lerp(cx, tx, 0.18);
      cy = lerp(cy, ty, 0.18);
      cgx = lerp(cgx, gx, 0.22);
      cgy = lerp(cgy, gy, 0.22);
      card.style.transform = `rotateY(${cx}deg) rotateX(${cy}deg)`;
      card.style.setProperty("--gx", `${cgx}%`);
      card.style.setProperty("--gy", `${cgy}%`);
      if (
        Math.abs(tx - cx) > 0.05 ||
        Math.abs(ty - cy) > 0.05 ||
        Math.abs(gx - cgx) > 0.1 ||
        Math.abs(gy - cgy) > 0.1
      ) {
        raf = requestAnimationFrame(tick);
      } else {
        raf = 0;
      }
    }

    card.addEventListener("pointermove", (e: PointerEvent) => {
      const rect = card.getBoundingClientRect();
      const px = (e.clientX - rect.left) / rect.width;
      const py = (e.clientY - rect.top) / rect.height;
      tx = (px - 0.5) * maxX;
      ty = -(py - 0.5) * maxY;
      gx = px * 100;
      gy = py * 100;
      if (!raf) raf = requestAnimationFrame(tick);
    });

    card.addEventListener("pointerleave", () => {
      tx = 0; ty = 0; gx = 50; gy = 50;
      if (!raf) raf = requestAnimationFrame(tick);
    });
  });
}
