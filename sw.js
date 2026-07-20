/* GRE Vocab service worker
 * Cache-first for the app shell + data, so the app works fully offline once
 * it has been opened with a network connection at least once.
 *
 * Bump CACHE_VERSION when you ship new vocab.json / passages.json / app.js
 * so users get the updated data on next launch.
 */
const CACHE_VERSION = 'gre-vocab-v34';
const SHELL = [
  './',
  './index.html',
  './style.css?v=34',
  './app.js?v=34',
  './supabase-sync.js?v=34',
  './vocab.json?v=34',
  './passages.json?v=34',
  './vocab_v7.json?v=34',
  './vocab_equiv.json?v=34',
  './vocab_reading.json?v=34',
  './vocab_bb62.json?v=34',
  './manifest.webmanifest',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_VERSION).then((cache) => cache.addAll(SHELL))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE_VERSION).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;

  event.respondWith(
    caches.match(req, { ignoreSearch: false }).then((cached) => {
      if (cached) {
        // refresh in background so the next launch is current
        fetch(req).then((res) => {
          if (res && res.ok) caches.open(CACHE_VERSION).then((c) => c.put(req, res.clone()));
        }).catch(() => {});
        return cached;
      }
      return fetch(req).then((res) => {
        if (res && res.ok) {
          const copy = res.clone();
          caches.open(CACHE_VERSION).then((c) => c.put(req, copy));
        }
        return res;
      }).catch(() => {
        // last-ditch fallback: try the cached app shell for navigation requests
        if (req.mode === 'navigate') return caches.match('./index.html');
        return new Response('Offline and not cached', { status: 503, statusText: 'Offline' });
      });
    })
  );
});
