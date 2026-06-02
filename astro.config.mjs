// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  site: 'https://lumocancun.com',
  integrations: [
    sitemap({
      i18n: undefined,
      changefreq: 'monthly',
      lastmod: new Date(),
      // EMD pages are served at their own canonical domains via Vercel rewrites.
      // Exclude them from the lumocancun.com sitemap so Google doesn't index duplicates.
      filter: (page) =>
        !page.includes('/cortelasercancun') &&
        !page.includes('/impresion3dcancun'),
      serialize(item) {
        if (item.url === 'https://lumocancun.com/') {
          item.priority = 1.0;
        } else if (item.url.includes('/servicios/')) {
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
