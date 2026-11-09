import type { ImageMetadata } from 'astro';

const files = import.meta.glob<{ default: ImageMetadata }>('../assets/tienda/*.png', { eager: true });

/** Imagen de una figura de la tienda por nombre de archivo (src/assets/tienda/). */
export const shopImage = (file: string): ImageMetadata => {
  const hit = files[`../assets/tienda/${file}`];
  if (!hit) throw new Error(`Falta la imagen de tienda: ${file}`);
  return hit.default;
};
