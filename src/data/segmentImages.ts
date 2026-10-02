import type { ImageMetadata } from "astro";
import { altByFile } from "./galleryImages";
import { CATALOG } from "./catalog";

// Sector pages reuse real shop photos from the gallery and the catalog.
const gallery = import.meta.glob<{ default: ImageMetadata }>(
  "../assets/gallery/gal-*.jpg",
  { eager: true },
);
const catalogo = import.meta.glob<{ default: ImageMetadata }>(
  "../assets/catalogo/*.jpg",
  { eager: true },
);
const sectores = import.meta.glob<{ default: ImageMetadata }>(
  "../assets/sectores/*.jpg",
  { eager: true },
);

// Photos shot for the sector pages (src/assets/sectores), from the LUMO album.
const sectorAlts: Record<string, string> = {
  "hotel-cuadros.jpg": "Lote de cuadros enmarcados producidos para hotelería, apilados en el taller",
  "hotel-senaletica.jpg": "Letreros de madera grabados Organic, Inorganic y Trash para separación de residuos",
  "hotel-la-central.jpg": "Tres letreros de acrílico negro y dorado de La Central Vinos & Licores",
  "corp-trofeos.jpg": "Lote de trofeos dorados impresos en 3D para un evento corporativo",
  "corp-placas.jpg": "Placa de aluminio grabada con láser para el evento BeStar Generation",
  "corp-termo.jpg": "Termo blanco grabado con láser con el logo de Emerald B2",
  "souv-llaveros-cancun.jpg": "Llaveros Cancún tricolor impresos en 3D en serie sobre la cama de impresión",
  "souv-peces.jpg": "Decenas de llaveros de pez multicolor impresos en 3D por lote",
  "souv-tiburones.jpg": "Lote de tiburones articulados impresos en 3D",
  "evento-recuerdos.jpg": "Decenas de recuerdos de madera grabados con texto para un evento",
  "evento-cajas.jpg": "Torre de cajas de madera cortadas a láser, producción para evento",
  "evento-cajas-corazon.jpg": "Lote de cajas de regalo con corazón apiladas en el taller",
};

/** Resolves a filename from src/assets/{sectores,gallery,catalogo}. */
export function segmentImage(file: string): ImageMetadata {
  const mod =
    sectores[`../assets/sectores/${file}`] ??
    gallery[`../assets/gallery/${file}`] ??
    catalogo[`../assets/catalogo/${file}`];
  if (!mod) throw new Error(`Falta imagen de sector: ${file}`);
  return mod.default;
}

/** Descriptive alt for a sector, gallery or catalog photo. */
export function segmentAlt(file: string): string {
  if (sectorAlts[file]) return sectorAlts[file];
  if (altByFile[file]) return altByFile[file];
  const id = file.replace(/\.jpg$/, "");
  return CATALOG.find((p) => p.id === id)?.name ?? "";
}
