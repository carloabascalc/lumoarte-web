// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  site: 'https://lumocancun.com',
  trailingSlash: 'always',
  integrations: [
    sitemap({
      i18n: undefined,
      changefreq: 'monthly',
      // EMD pages are served at their own canonical domains via Vercel rewrites.
      // Exclude them from the lumocancun.com sitemap so Google doesn't index duplicates.
      filter: (page) =>
        !page.includes('/cortelasercancun') &&
        !page.includes('/impresion3dcancun') &&
        // Informational only (Lumo no imprime gran formato) — kept noindex.
        !page.includes('/recursos/sublimacion-vs-vinil'),
      serialize(item) {
        if (item.url === 'https://lumocancun.com/') {
          item.priority = 1.0;
        } else if (item.url.includes('/sectores/') || item.url.includes('/servicios/') || item.url.includes('/productos/')) {
          item.priority = 0.9;
        } else if (item.url.includes('/recursos/')) {
          item.priority = 0.7;
        } else {
          item.priority = 0.3;
        }
        return item;
      },
    }),
  ],
});
