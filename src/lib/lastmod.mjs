// Fecha real de la última edición de cada página, sacada de git.
//
// Fuentes de una página: su archivo en src/pages + los src/data/*.ts que
// importa (ahí vive el contenido, ver CLAUDE.md §3). Cambios de layout o
// estilos no cuentan como "contenido nuevo".
//
// Si no hay historial confiable, devuelve undefined: es mejor omitir la fecha
// que inventarla. Eso pasa sin git, o en un clon parcial (Vercel clona con
// poca profundidad) cuando el último cambio de la página quedó fuera del
// historial descargado. Con VERCEL_DEEP_CLONE=true en el proyecto de Vercel
// todas las páginas reciben fecha.
//
// La usan el sitemap (astro.config.mjs → lastmod) y Base.astro (dateModified).

import { execFileSync } from "node:child_process";
import { existsSync, readFileSync } from "node:fs";
import path from "node:path";

const ROOT = process.cwd();
const cache = new Map();
/** @type {Set<string> | null | undefined} */
let shallowBoundary;

/** @param {string[]} args */
function git(args) {
  return execFileSync("git", args, {
    cwd: ROOT,
    encoding: "utf8",
    stdio: ["ignore", "pipe", "ignore"],
  }).trim();
}

/** Commits frontera de un clon parcial (vacío si el clon es completo; null sin git). */
function boundary() {
  if (shallowBoundary !== undefined) return shallowBoundary;
  try {
    const file = path.resolve(ROOT, git(["rev-parse", "--git-path", "shallow"]));
    shallowBoundary = existsSync(file)
      ? new Set(readFileSync(file, "utf8").split(/\s+/).filter(Boolean))
      : new Set();
  } catch {
    shallowBoundary = null;
  }
  return shallowBoundary;
}

/** @param {string} route ej. "/productos/llaveros-con-logo/" */
function pageFile(route) {
  const clean = route.replace(/^\/+|\/+$/g, "");
  const candidates = clean
    ? [`src/pages/${clean}.astro`, `src/pages/${clean}/index.astro`]
    : ["src/pages/index.astro"];
  const parent = clean.split("/").slice(0, -1).join("/");
  if (parent) candidates.push(`src/pages/${parent}/[slug].astro`);
  return candidates.find((f) => existsSync(path.join(ROOT, f)));
}

/** @param {string} file */
function dataImports(file) {
  const src = readFileSync(path.join(ROOT, file), "utf8");
  const dir = path.dirname(file);
  const out = [];
  for (const m of src.matchAll(/from\s+["']((?:\.{1,2}\/)+data\/[^"']+)["']/g)) {
    let rel = path.normalize(path.join(dir, m[1]));
    if (!path.extname(rel)) rel += ".ts";
    if (existsSync(path.join(ROOT, rel))) out.push(rel);
  }
  return out;
}

/**
 * Fecha ISO 8601 de la última edición de la página, o undefined si no se sabe.
 * @param {string} pathname ruta o URL de la página
 * @returns {string | undefined}
 */
export function lastModified(pathname) {
  const route = new URL(pathname, "https://lumocancun.com").pathname;
  if (cache.has(route)) return cache.get(route);

  let result;
  const shallow = boundary();
  const page = shallow && pageFile(route);
  if (shallow && page) {
    try {
      const out = git(["log", "-1", "--format=%H %cI", "--", page, ...dataImports(page)]);
      const [sha, date] = out.split(" ");
      if (sha && date && !shallow.has(sha)) result = date;
    } catch {
      result = undefined;
    }
  }
  cache.set(route, result);
  return result;
}
