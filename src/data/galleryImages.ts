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
  { file: "gal-23.jpg", alt: "Lote de cuadros enmarcados para un hotel, apilados en el taller de Lumo", service: "corte-laser" },
  { file: "gal-24.jpg", alt: "Instalación de cuadros enmarcados en el pasillo de un hotel en Cancún", service: "corte-laser" },
  { file: "gal-25.jpg", alt: "Cuadro enmarcado en madera con ilustración de peces y hojas, producido por lote", service: "corte-laser" },
  { file: "gal-26.jpg", alt: "Seis posavasos de madera grabados a láser con ilustraciones botánicas", service: "corte-laser" },
  { file: "gal-27.jpg", alt: "Señalética de reciclaje Organic, Inorganic y Trash grabada en madera, en lote", service: "corte-laser" },
  { file: "gal-28.jpg", alt: "Letreros de reciclaje grabados en serie sobre la cama de la cortadora láser", service: "corte-laser" },
  { file: "gal-29.jpg", alt: "Placas de aluminio grabadas para el evento BeStar Generation, en lote", service: "corte-laser" },
  { file: "gal-30.jpg", alt: "Tres letreros La Central Vinos & Licores en acrílico negro y dorado", service: "corte-laser" },
  { file: "gal-31.jpg", alt: "Torre de cajas de madera cortadas a láser para un pedido por volumen", service: "corte-laser" },
  { file: "gal-32.jpg", alt: "Cientos de etiquetas de cuero grabadas a láser en una sola lámina", service: "corte-laser" },
  { file: "gal-33.jpg", alt: "Par de cajas de vino de madera con frente calado de hojas de palma", service: "corte-laser" },
  { file: "gal-34.jpg", alt: "Lote de piezas religiosas de madera grabadas con oración, sobre mesa", service: "corte-laser" },
  { file: "gal-35.jpg", alt: "Anzuelos decorativos impresos en 3D con nombre grabado, recuerdo para evento", service: "impresion-3d" },
  { file: "gal-36.jpg", alt: "Termos grabados a láser con las iniciales de cada persona", service: "corte-laser" },
  { file: "gal-37.jpg", alt: "Lote de cangrejos articulados rojos impresos en 3D sobre mesa", service: "impresion-3d" },
  { file: "gal-38.jpg", alt: "Llaveros CANCÚN tricolor impresos en 3D en serie", service: "impresion-3d" },
  { file: "gal-39.jpg", alt: "Exhibidor de llaveros impresos en 3D en una tienda de souvenirs", service: "impresion-3d" },
  { file: "gal-40.jpg", alt: "Cajas con figuras impresas en 3D clasificadas por modelo, listas para entrega", service: "impresion-3d" },
  { file: "gal-41.jpg", alt: "Lote de conchas impresas en 3D con acabado tornasol", service: "impresion-3d" },
  { file: "gal-42.jpg", alt: "Lote de trofeos dorados impresos en 3D para un evento", service: "impresion-3d" },
  { file: "gal-02.jpg", alt: "Biombo de copos de nieve en madera y acrílico sobre terraza con vista al mar", service: "corte-laser" },
  { file: "gal-05.jpg", alt: "Caja de cirio Luz del Mundo con grabado en metal dorado y madera", service: "corte-laser" },
  { file: "gal-06.jpg", alt: "Letrero La Central Vinos & Licores en acrílico negro y dorado", service: "corte-laser" },
  { file: "gal-07.jpg", alt: "Cajones de madera apilados con ensamble dovetail cortado a láser", service: "corte-laser" },
  { file: "gal-10.jpg", alt: "Paletas de madera grabadas con nombres para evento corporativo L'Oréal", service: "corte-laser" },
  { file: "gal-11.jpg", alt: "Llavero de Cancún grabado con patrón maya y perforaciones decorativas", service: "corte-laser" },
  { file: "gal-12.jpg", alt: "Cesta pequeña de madera oscura con ensamble de dedos cortado a láser", service: "corte-laser" },
  { file: "gal-13.jpg", alt: "Caja larga de madera con tapa de dos tonos, diseño minimalista", service: "corte-laser" },
  { file: "gal-15.jpg", alt: "Lote de trofeos dorados impresos en 3D para un evento, sobre mesa en terraza", service: "impresion-3d" },
  { file: "gal-16.jpg", alt: "Cama de impresora 3D llena de llaveros Cancún tricolor impresos en serie", service: "impresion-3d" },
  { file: "gal-17.jpg", alt: "Lote de cangrejos articulados rojos impresos en 3D", service: "impresion-3d" },
  { file: "gal-18.jpg", alt: "Decenas de llaveros de pez impresos en 3D multicolor en la cama de impresión", service: "impresion-3d" },
  { file: "gal-19.jpg", alt: "Placas impresas en 3D en serie sobre la cama de una Bambu Lab", service: "impresion-3d" },
  { file: "gal-20.jpg", alt: "Organizador porta controles impreso en 3D en negro y terracota", service: "impresion-3d" },
  { file: "gal-21.jpg", alt: "Lote de tiburones articulados grises impresos en 3D", service: "impresion-3d" },
  { file: "gal-22.jpg", alt: "Figuras articuladas multicolor impresas en 3D por lote", service: "impresion-3d" },
];

/** filename → alt lookup, for components that resolve images via import.meta.glob. */
export const altByFile: Record<string, string> = Object.fromEntries(
  galleryItems.map((it) => [it.file, it.alt]),
);
