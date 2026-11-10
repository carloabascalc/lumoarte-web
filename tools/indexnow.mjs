// Avisa a Bing (y a los buscadores que comparten IndexNow) que hay páginas
// nuevas o cambiadas en lumocancun.com. ChatGPT search y Copilot leen de Bing,
// así que esto acelera que dejen de citar la versión vieja del sitio.
// Google no usa IndexNow: para Google sigue siendo Search Console.
//
// Correr DESPUÉS de que el deploy esté en vivo (la llave debe ser pública):
//   npm run indexnow                      → todas las URLs del sitemap en vivo
//   npm run indexnow -- /productos/ /sectores/souvenirs-mayoreo/
//
// La llave vive en public/<KEY>.txt. Si se cambia, cambiar las dos.

const HOST = "lumocancun.com";
const KEY = "f09c4011f2a875233915209ff59c9dfb";
const SITE = `https://${HOST}`;

async function sitemapUrls() {
  const index = await (await fetch(`${SITE}/sitemap-index.xml`)).text();
  const maps = [...index.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1]);
  const urls = [];
  for (const map of maps) {
    const xml = await (await fetch(map)).text();
    urls.push(...[...xml.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1]));
  }
  return urls;
}

const args = process.argv.slice(2);
const urlList = args.length
  ? args.map((a) => new URL(a, SITE).href)
  : await sitemapUrls();

const keyCheck = await fetch(`${SITE}/${KEY}.txt`);
if (!keyCheck.ok || (await keyCheck.text()).trim() !== KEY) {
  console.error(`La llave no está publicada en ${SITE}/${KEY}.txt — ¿ya se desplegó?`);
  process.exit(1);
}

const res = await fetch("https://api.indexnow.org/indexnow", {
  method: "POST",
  headers: { "Content-Type": "application/json; charset=utf-8" },
  body: JSON.stringify({ host: HOST, key: KEY, keyLocation: `${SITE}/${KEY}.txt`, urlList }),
});

console.log(`IndexNow: HTTP ${res.status} · ${urlList.length} URLs`);
if (res.status !== 200 && res.status !== 202) {
  console.error(await res.text());
  process.exit(1);
}
