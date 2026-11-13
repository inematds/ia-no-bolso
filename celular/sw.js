// IA no bolso — service worker da página "abre e usa".
// 1) Guarda a página e o motor (wllama) para abrir sem internet (o modelo fica no cache do próprio wllama).
// 2) Fora do iPhone, liga o isolamento de origem (COOP/COEP credentialless) para o motor usar vários núcleos;
//    o GitHub Pages não deixa configurar esses cabeçalhos, então o service worker põe na resposta.
const VERSAO = 'ia-no-bolso-v2';
const CASCA = ['./', './index.html', './manifest.webmanifest', './icone.svg', './wllama/index.js', './wllama/wasm/wllama.wasm'];
const IOS = /iPhone|iPad|iPod/.test(self.navigator.userAgent);

self.addEventListener('install', e => {
  e.waitUntil(caches.open(VERSAO).then(c => c.addAll(CASCA)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k.startsWith('ia-no-bolso-') && k !== VERSAO).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});

function isolar(resp) {
  if (IOS || !resp || resp.status === 0 || resp.type === 'opaque') return resp;
  const h = new Headers(resp.headers);
  h.set('Cross-Origin-Embedder-Policy', 'credentialless');
  h.set('Cross-Origin-Opener-Policy', 'same-origin');
  return new Response(resp.body, { status: resp.status, statusText: resp.statusText, headers: h });
}

self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  if (url.origin !== location.origin || e.request.method !== 'GET') return;  // modelo e fontes: direto
  e.respondWith((async () => {
    try {
      const r = await fetch(e.request, { cache: 'no-cache' });  // com internet, sempre a versão mais nova
      if (r.ok) { const c = await caches.open(VERSAO); c.put(e.request, r.clone()); }
      return isolar(r);
    } catch (_) {
      const c = await caches.match(e.request, { ignoreSearch: true });
      return isolar(c || await caches.match('./index.html'));
    }
  })());
});
