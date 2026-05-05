import { animate, inView, scroll, stagger } from "motion";

const prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

const spring = { type: "spring" as const, stiffness: 110, damping: 20, mass: 0.9 };
const ease = { duration: 0.7, ease: [0.22, 1, 0.36, 1] as [number, number, number, number] };

export function revealOnScroll() {
  if (prefersReduced) {
    document.querySelectorAll<HTMLElement>("[data-reveal]").forEach((el) => {
      el.style.opacity = "1";
      el.style.transform = "none";
    });
    return;
  }

  inView("[data-reveal]", (el) => {
    const target = el as HTMLElement;
    const delay = Number(target.dataset.revealDelay ?? 0);
    animate(
      target,
      { opacity: [0, 1], transform: ["translateY(28px)", "translateY(0px)"] },
      { ...ease, delay },
    );
  }, { margin: "0px 0px -12% 0px" });
}

export function staggerChildren(selector: string, childSelector: string, startDelay = 0) {
  if (prefersReduced) {
    document.querySelectorAll<HTMLElement>(`${selector} ${childSelector}`).forEach((el) => {
      el.style.opacity = "1";
      el.style.transform = "none";
    });
    return;
  }

  inView(selector, (container) => {
    const items = container.querySelectorAll<HTMLElement>(childSelector);
    animate(
      items,
      { opacity: [0, 1], transform: ["translateY(24px) scale(0.985)", "translateY(0px) scale(1)"] },
      { ...spring, delay: stagger(0.06, { startDelay }) },
    );
  }, { margin: "0px 0px -10% 0px" });
}

export function heroIntro() {
  if (prefersReduced) return;

  const eyebrow = document.querySelector<HTMLElement>(".hero-eyebrow");
  const titleLines = document.querySelectorAll<HTMLElement>(".hero-title-line");
  const sub = document.querySelector<HTMLElement>(".hero-sub");
  const cta = document.querySelector<HTMLElement>(".hero-ctas, .hero-cta");
  const scrollHint = document.querySelector<HTMLElement>(".hero-scroll");

  if (eyebrow) {
    animate(
      eyebrow,
      { opacity: [0, 1], transform: ["translateY(12px)", "translateY(0px)"] },
      { duration: 0.7, delay: 0.15, ease: [0.22, 1, 0.36, 1] },
    );
  }

  if (titleLines.length) {
    animate(
      titleLines,
      { opacity: [0, 1], transform: ["translateY(110%)", "translateY(0%)"] },
      { duration: 0.9, delay: stagger(0.09, { startDelay: 0.25 }), ease: [0.22, 1, 0.36, 1] },
    );
  }

  if (sub) {
    animate(
      sub,
      { opacity: [0, 1], transform: ["translateY(16px)", "translateY(0px)"] },
      { duration: 0.8, delay: 0.65, ease: [0.22, 1, 0.36, 1] },
    );
  }

  if (cta) {
    animate(
      cta,
      { opacity: [0, 1], transform: ["translateY(12px) scale(0.96)", "translateY(0px) scale(1)"] },
      { ...spring, delay: 0.8 },
    );
  }

  if (scrollHint) {
    animate(scrollHint, { opacity: [0, 1] }, { duration: 0.6, delay: 1.2 });
  }
}

export function heroParallax() {
  if (prefersReduced) return;
  const bg = document.querySelector<HTMLElement>(".hero-bg");
  const content = document.querySelector<HTMLElement>(".hero-content");
  const hero = document.querySelector<HTMLElement>(".hero");
  if (!bg || !hero) return;

  scroll(
    animate(bg, { transform: ["translateY(0%) scale(1)", "translateY(14%) scale(1.08)"] }),
    { target: hero, offset: ["start start", "end start"] },
  );

  if (content) {
    scroll(
      animate(content, { transform: ["translateY(0px)", "translateY(-40px)"], opacity: [1, 0.55] }),
      { target: hero, offset: ["start start", "end start"] },
    );
  }
}

export function galleryReveal() {
  if (prefersReduced) return;
  const items = document.querySelectorAll<HTMLElement>(".film-item");
  if (!items.length) return;

  inView(".filmstrip", () => {
    animate(
      items,
      { opacity: [0, 1], transform: ["translateY(24px)", "translateY(0px)"] },
      { duration: 0.6, delay: stagger(0.04), ease: [0.22, 1, 0.36, 1] },
    );
  }, { margin: "0px 0px -15% 0px" });
}

// Scroll-linked ambient drift: writes --glow-shift-x/y to the section so its
// ::before radial gradients can read them and shift glow centers as the user
// scrolls. Cheap (rAF-throttled) and pure CSS once the values land.
function ambientDrift(selector: string, intensityX = 6, intensityY = 4) {
  if (prefersReduced) return;
  const section = document.querySelector<HTMLElement>(selector);
  if (!section) return;

  let raf = 0;
  const onScroll = () => {
    if (raf) return;
    raf = requestAnimationFrame(() => {
      const rect = section.getBoundingClientRect();
      const vh = window.innerHeight;
      const progress = Math.max(-1, Math.min(1, (rect.top + rect.height / 2 - vh / 2) / vh));
      section.style.setProperty("--glow-shift-x", `${progress * intensityX}%`);
      section.style.setProperty("--glow-shift-y", `${progress * intensityY}%`);
      raf = 0;
    });
  };
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });
}

export function materialsAmbient() {
  ambientDrift(".materials", 6, 4);
}

export function contactAmbient() {
  ambientDrift(".page-end", 5, 3);
}

// ─────────────────────────────────────────────────────────────
// Page transitions — Linear-style two-panel vertical sweep.
// Hooks Astro's <ClientRouter /> events. Listeners on `document`
// persist across navigations, so we register exactly once.
// ─────────────────────────────────────────────────────────────
let pageTransitionsBound = false;

const findPanels = () => ({
  overlay: document.querySelector<HTMLElement>(".page-transition"),
  back: document.querySelector<HTMLElement>(".page-transition-back"),
  front: document.querySelector<HTMLElement>(".page-transition-front"),
});

const sweepCurve = "cubic-bezier(0.76, 0, 0.24, 1)";

const setPanel = (
  el: HTMLElement | null,
  transform: string,
  durationMs: number,
  delayMs = 0,
) => {
  if (!el) return;
  el.style.transition =
    durationMs === 0
      ? "none"
      : `transform ${durationMs}ms ${sweepCurve} ${delayMs}ms`;
  el.style.transform = transform;
};

const waitMs = (ms: number) => new Promise<void>((r) => setTimeout(r, ms));

const coverPhase = async () => {
  const { overlay, back, front } = findPanels();
  if (!overlay || !back || !front) return;
  setPanel(back, "translateY(100%)", 0);
  setPanel(front, "translateY(100%)", 0);
  overlay.classList.add("is-active");
  overlay.classList.remove("is-mark-visible");
  void overlay.offsetHeight;
  setPanel(back, "translateY(0%)", 550);
  setPanel(front, "translateY(0%)", 550, 80);
  await waitMs(640);
  overlay.classList.add("is-mark-visible");
  await waitMs(180);
};

const revealPhase = async () => {
  const { overlay, back, front } = findPanels();
  if (!overlay || !back || !front) return;
  setPanel(back, "translateY(0%)", 0);
  setPanel(front, "translateY(0%)", 0);
  overlay.classList.add("is-active");
  void overlay.offsetHeight;
  overlay.classList.remove("is-mark-visible");
  await waitMs(60);
  setPanel(front, "translateY(-100%)", 600);
  setPanel(back, "translateY(-100%)", 600, 100);
  await waitMs(720);
  setPanel(back, "translateY(100%)", 0);
  setPanel(front, "translateY(100%)", 0);
  overlay.classList.remove("is-active");
};

export function pageTransitions() {
  if (pageTransitionsBound) return;
  if (prefersReduced) return;
  const { overlay } = findPanels();
  if (!overlay) return;
  pageTransitionsBound = true;

  document.addEventListener("astro:before-preparation", (event: any) => {
    const original = event.loader;
    event.loader = async () => {
      await coverPhase();
      await original();
    };
  });

  document.addEventListener("astro:after-swap", () => {
    // Synchronously snap the overlay to the "fully covered" state so the
    // freshly-rendered new page never paints uncovered for one frame.
    const { overlay, back, front } = findPanels();
    if (overlay && back && front) {
      back.style.transition = "none";
      front.style.transition = "none";
      back.style.transform = "translateY(0%)";
      front.style.transform = "translateY(0%)";
      overlay.classList.add("is-active");
      overlay.classList.add("is-mark-visible");
    }
    requestAnimationFrame(() => {
      revealPhase();
    });
  });
}

export function initAll() {
  pageTransitions();
  heroIntro();
  heroParallax();
  revealOnScroll();
  staggerChildren(".materials-grid", ".material-card", 0.05);
  galleryReveal();
  contactAmbient();
}
