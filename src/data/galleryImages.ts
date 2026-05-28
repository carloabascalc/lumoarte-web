import type { ServiceId } from "./services";

/**
 * Single source of truth for gallery photo metadata (filename → alt + service).
 * Consumed by Gallery.astro (filterable grid) and Hero.astro (marquee) so the
 * descriptive alt text lives in one place. Order here is the gallery order.
 */
export interface GalleryItem {
  file: string;
  alt: string;
  service: ServiceId;
}

export const galleryItems: GalleryItem[] = [
  { file: "gal-01.jpg", alt: "Lámparas corazón en MDF apiladas, corte láser de precisión", service: "corte-laser" },
  { file: "gal-02.jpg", alt: "Biombo de copos de nieve en madera y acrílico sobre terraza con vista al mar", service: "corte-laser" },
  { file: "gal-03.jpg", alt: "Caja de regalo en madera con corazón de acrílico y medallón de marca lumo", service: "corte-laser" },
  { file: "gal-04.jpg", alt: "Lámpara trébol de cuatro corazones en MDF cortada a láser", service: "corte-laser" },
  { file: "gal-05.jpg", alt: "Caja de cirio Luz del Mundo con grabado en metal dorado y madera", service: "corte-laser" },
  { file: "gal-06.jpg", alt: "Letrero La Central Vinos & Licores en acrílico negro y dorado", service: "corte-laser" },
  { file: "gal-07.jpg", alt: "Cajones de madera apilados con ensamble dovetail cortado a láser", service: "corte-laser" },
  { file: "gal-08.jpg", alt: "Caja corazón de madera con rosas rojas y chocolates Ferrero", service: "corte-laser" },
  { file: "gal-09.jpg", alt: "Panel decorativo de copo de nieve sobre sarape mexicano de colores", service: "corte-laser" },
  { file: "gal-10.jpg", alt: "Paletas de madera grabadas con nombres para evento corporativo L'Oréal", service: "corte-laser" },
  { file: "gal-11.jpg", alt: "Llavero de Cancún grabado con patrón maya y perforaciones decorativas", service: "corte-laser" },
  { file: "gal-12.jpg", alt: "Cesta pequeña de madera oscura con ensamble de dedos cortado a láser", service: "corte-laser" },
  { file: "gal-13.jpg", alt: "Caja larga de madera con tapa de dos tonos, diseño minimalista", service: "corte-laser" },
  { file: "gal-14.jpg", alt: "Marco corazón de madera con corazones de acrílico sobre escultura de bronce", service: "corte-laser" },
];

/** filename → alt lookup, for components that resolve images via import.meta.glob. */
export const altByFile: Record<string, string> = Object.fromEntries(
  galleryItems.map((it) => [it.file, it.alt]),
);
