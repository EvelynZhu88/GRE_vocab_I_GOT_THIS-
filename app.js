/* GRE Vocab — single-page app with hash routing
 *
 * Routes:
 *   #/                       Lists overview (home)
 *   #/list/N                 List N detail (Words / Test / Passages)
 *   #/list/N/words           Browse all words in list N
 *   #/list/N/test            Unit test for list N
 *   #/list/N/passages        Passage list for list N
 *   #/list/N/passages/I      Read passage I
 *   #/list/N/passages/I/quiz Comprehension quiz for passage I
 *   #/review                 Cumulative spaced-repetition review (excludes starred)
 *   #/starred-test           200-question test drawn only from starred words
 *   #/stats                  Stats overview (also: sign-in for cross-device sync)
 *
 * Storage:
 *   gre.progress         -> { [listN::word]: { ef, interval, reps, due, lapses, last, starred } }
 *   gre.units            -> { [listN]: { tested, lastScore, lastTested } }
 *   gre.settings         -> { unitTestSize, reviewSize, mixRatio }
 *   gre.localUpdatedAt   -> epoch ms of last local mutation (for Supabase sync)
 *
 * Optional sync: window.SupaSync (supabase-sync.js) — when configured, all
 * three blobs are mirrored to a per-user row in the Supabase user_state
 * table, with debounced last-write-wins.
 */

const DAY = 86400000;
const SETTINGS_KEY = 'gre.settings';
const ACTIVE_BOOK_KEY = 'gre.activeBook';
const DEFAULTS = {
  unitTestSize: 20,    // not used (unit test = full list)
  reviewSize: 100,     // mixed-review session size
  mixRatio: 0.35,
};

// Registry of every vocab book the app knows about. Each book has its own
// vocab.json + (optional) passages.json and its own SRS progress / unit
// state, persisted under per-book localStorage keys.
const BOOKS = [
  { id: 'v1',      label: 'GRE 镇考 3000词',           vocab: 'vocab.json',         passages: 'passages.json' },
  { id: 'v7',      label: 'GRE 镇考机经词 7.0',        vocab: 'vocab_v7.json',      passages: 'passages_v7.json' },
  { id: 'equiv',   label: '真经 GRE 等价词',            vocab: 'vocab_equiv.json',   passages: 'passages_equiv.json', testMode: 'equiv' },
  { id: 'bb62',    label: 'BB 六选二词表',              vocab: 'vocab_bb62.json',    passages: 'passages_bb62.json',  testMode: 'equiv' },
  { id: 'reading', label: 'GRE 阅读机经核心词汇',       vocab: 'vocab_reading.json', passages: 'passages_reading.json' },
];
const DEFAULT_BOOK_ID = 'v1';
const ASSET_VERSION = '26';
function progressKey(bookId) { return 'gre.progress.' + bookId; }
function unitsKey(bookId)    { return 'gre.units.'    + bookId; }
function bookById(id) { return BOOKS.find(b => b.id === id) || BOOKS[0]; }

// Cache of fetched book payloads: { bookId: { vocab, passages } }
const BOOK_CACHE = {};

// For books with testMode === 'equiv', a precomputed index built from the
// synonym graph: { byWord: {wordLower: [equivWordLower, ...]}, allWords: [...] }
let EQUIV_INDEX = null;

let ACTIVE_BOOK_ID = localStorage.getItem(ACTIVE_BOOK_KEY) || DEFAULT_BOOK_ID;
let VOCAB = null;
let PASSAGES = null;
let SETTINGS = loadJson(SETTINGS_KEY, DEFAULTS);
let PROGRESS = {};
let UNITS    = {};

// "Reveal all" preference for Words / Starred lists — persists across
// in-app tab switches but resets on page reload (intentional default).
let REVEAL_ALL = false;

const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));

// --- bootstrap ---
async function init() {
  migrateLegacyStorage();
  try {
    await loadBook(ACTIVE_BOOK_ID);
  } catch (e) {
    $('#view').innerHTML = `<div class="empty-state"><h2>Couldn't load data</h2><p>${escHtml(String(e))}</p></div>`;
    return;
  }
  window.addEventListener('hashchange', router);
  $('#backBtn').addEventListener('click', () => history.back());
  renderBookPicker();
  if (!location.hash) location.hash = '#/';
  router();

  // Ask the browser to mark our localStorage as persistent so iOS Safari /
  // Chrome don't evict it under storage pressure or after long inactivity.
  // Silent if granted; silent if denied (the app still works either way).
  if (navigator.storage && navigator.storage.persist) {
    navigator.storage.persist().catch(() => {});
  }

  // Supabase sync (no-op when not configured or not signed in)
  bootstrapSync();
  if (window.SupaSync && SupaSync.isConfigured()) {
    SupaSync.onAuthChange(() => {
      // After magic-link return or sign-in / sign-out, re-sync. Only
      // re-render if we're not in the middle of a quiz session — the
      // freshly-pulled data will appear on the user's next navigation.
      bootstrapSync().then(() => { if (!isStatefulRoute()) router(); });
    });
  }
}

// Merge per-card by `last` timestamp so a newer empty side cannot wipe
// the older fuller side. Bug fix for the original blob-level
// last-write-wins, which let a freshly-signed-in device with no local
// data push an empty state that then overwrote an active device.
function mergeByLast(localObj, serverObj, tsField) {
  const out = {};
  const l = localObj || {};
  const s = serverObj || {};
  const keys = new Set([...Object.keys(l), ...Object.keys(s)]);
  for (const k of keys) {
    const a = l[k], b = s[k];
    if (!a) { out[k] = b; continue; }
    if (!b) { out[k] = a; continue; }
    const aTs = +(a[tsField] || 0);
    const bTs = +(b[tsField] || 0);
    out[k] = aTs >= bTs ? a : b;
  }
  return out;
}

function stableStringify(o) {
  const keys = Object.keys(o || {}).sort();
  return JSON.stringify(o, keys);
}

// Treat a server blob that has flat `{listN::word: card}` keys (the pre
// multi-book schema) as if it were the v1 book's state. This lets users
// who pushed in the old format still recover via merge.
function normalizeServerBookBlob(blob) {
  if (!blob || typeof blob !== 'object') return {};
  const looksFlat = Object.keys(blob).some(k => /::/.test(k));
  if (looksFlat) return { v1: blob };
  return blob;
}

// Pull server state and merge with local per-book, per-card. Each side may
// have books or entries the other lacks; for shared keys we keep the more
// recently touched record. Then push the merged result if it differs.
async function bootstrapSync() {
  if (!window.SupaSync || !SupaSync.isConfigured()) return;
  const user = await SupaSync.currentUser();
  if (!user) return;
  const server = await SupaSync.pullState();
  if (!server) {
    SupaSync.pushNow(buildSyncSnapshot());
    return;
  }
  const sP = normalizeServerBookBlob(server.progress || {});
  const sU = normalizeServerBookBlob(server.units    || {});
  const sS = server.settings || {};

  const local = buildSyncSnapshot();
  const lP = local.progress, lU = local.units;

  const bookIds = new Set([...Object.keys(lP), ...Object.keys(sP), ...Object.keys(lU), ...Object.keys(sU)]);
  const mergedProgress = {}, mergedUnits = {};
  for (const id of bookIds) {
    mergedProgress[id] = mergeByLast(lP[id] || {}, sP[id] || {}, 'last');
    mergedUnits[id]    = mergeByLast(lU[id] || {}, sU[id] || {}, 'lastTested');
  }
  const mergedSettings = Object.keys(sS).length
    ? Object.assign({}, DEFAULTS, sS, Object.keys(SETTINGS).length ? SETTINGS : {})
    : (Object.keys(SETTINGS).length ? SETTINGS : DEFAULTS);

  // Write merged per-book results back to localStorage and pull the active
  // book's state into the live variables.
  let localChanged = false;
  for (const id of Object.keys(mergedProgress)) {
    const prev = stableStringify(loadJson(progressKey(id), {}));
    const next = stableStringify(mergedProgress[id]);
    if (prev !== next) {
      localStorage.setItem(progressKey(id), JSON.stringify(mergedProgress[id]));
      localChanged = true;
    }
  }
  for (const id of Object.keys(mergedUnits)) {
    const prev = stableStringify(loadJson(unitsKey(id), {}));
    const next = stableStringify(mergedUnits[id]);
    if (prev !== next) {
      localStorage.setItem(unitsKey(id), JSON.stringify(mergedUnits[id]));
      localChanged = true;
    }
  }
  if (stableStringify(SETTINGS) !== stableStringify(mergedSettings)) {
    SETTINGS = Object.assign({}, DEFAULTS, mergedSettings);
    localStorage.setItem(SETTINGS_KEY, JSON.stringify(SETTINGS));
    localChanged = true;
  }
  if (localChanged) {
    localStorage.setItem('gre.localUpdatedAt', String(Date.now()));
    // Reload the active book's in-memory state from its (potentially updated) key
    PROGRESS = loadJson(progressKey(ACTIVE_BOOK_ID), {});
    UNITS    = loadJson(unitsKey(ACTIVE_BOOK_ID),    {});
    // Don't re-render while the user is mid-quiz — that would reset
    // their session to question 1. localStorage already has the merged
    // data; the next navigation will pick it up.
    if (!isStatefulRoute()) router();
  }

  // Push merged result if the server's view differs from what we computed
  const serverNorm = { progress: sP, units: sU, settings: sS };
  if (stableStringify({ progress: mergedProgress, units: mergedUnits, settings: mergedSettings })
      !== stableStringify(serverNorm)) {
    SupaSync.pushNow({ progress: mergedProgress, units: mergedUnits, settings: mergedSettings });
  }
}

// --- storage helpers ---
function loadJson(k, fallback) {
  try { return Object.assign({}, fallback, JSON.parse(localStorage.getItem(k)) || {}); }
  catch { return { ...fallback }; }
}
function save(k, v) {
  localStorage.setItem(k, JSON.stringify(v));
  localStorage.setItem('gre.localUpdatedAt', String(Date.now()));
  if (window.SupaSync && SupaSync.isConfigured()) {
    SupaSync.schedulePush(buildSyncSnapshot());
  }
}
function saveProgress() { save(progressKey(ACTIVE_BOOK_ID), PROGRESS); }
function saveUnits()    { save(unitsKey(ACTIVE_BOOK_ID),    UNITS); }
function saveSettings() { save(SETTINGS_KEY, SETTINGS); }

// Build the multi-book snapshot we send to Supabase: progress and units
// are nested by book id so adding a book never erases another book's state.
function buildSyncSnapshot() {
  const progress = {}, units = {};
  for (const b of BOOKS) {
    const p = loadJson(progressKey(b.id), {});
    const u = loadJson(unitsKey(b.id),    {});
    if (Object.keys(p).length) progress[b.id] = p;
    if (Object.keys(u).length) units[b.id]    = u;
  }
  // Ensure the in-memory active book's state is the latest snapshot
  progress[ACTIVE_BOOK_ID] = PROGRESS;
  units[ACTIVE_BOOK_ID]    = UNITS;
  return { progress, units, settings: SETTINGS };
}

// Copy pre-multi-book localStorage keys (gre.progress, gre.units) into the
// per-book keys for v1 so existing users keep their recovered data. We do
// NOT delete the old keys — they sit there as a last-resort backup.
function migrateLegacyStorage() {
  const oldP = localStorage.getItem('gre.progress');
  const oldU = localStorage.getItem('gre.units');
  if (oldP && !localStorage.getItem(progressKey('v1'))) {
    localStorage.setItem(progressKey('v1'), oldP);
  }
  if (oldU && !localStorage.getItem(unitsKey('v1'))) {
    localStorage.setItem(unitsKey('v1'), oldU);
  }
  // Reset anyone still on a previous default reviewSize (80 or 200)
  // to the current default of 100. Custom non-default values are left alone.
  if (SETTINGS.reviewSize === 80 || SETTINGS.reviewSize === 200) {
    SETTINGS.reviewSize = 100;
    localStorage.setItem(SETTINGS_KEY, JSON.stringify(SETTINGS));
  }
}

async function loadBook(bookId) {
  const book = bookById(bookId);
  if (!BOOK_CACHE[bookId]) {
    const v = `?v=${ASSET_VERSION}`;
    const [vocab, passages] = await Promise.all([
      fetch(book.vocab + v).then(r => r.json()),
      fetch(book.passages + v).then(r => r.json()).catch(() => ({})),
    ]);
    BOOK_CACHE[bookId] = { vocab, passages };
  }
  ACTIVE_BOOK_ID = bookId;
  localStorage.setItem(ACTIVE_BOOK_KEY, bookId);
  VOCAB    = BOOK_CACHE[bookId].vocab;
  PASSAGES = BOOK_CACHE[bookId].passages;
  PROGRESS = loadJson(progressKey(bookId), {});
  UNITS    = loadJson(unitsKey(bookId),    {});
  EQUIV_INDEX = book.testMode === 'equiv' ? buildEquivIndex(VOCAB) : null;
}

// Union-find: every row (word, syn1, syn2, ...) is one equivalence edge set.
// Returns { byWord: {w: [equivs]}, allWords: [w...] } where words are lowercased.
function buildEquivIndex(vocab) {
  const parent = Object.create(null);
  const find = (x) => { let r = x; while (parent[r] !== r) r = parent[r]; while (parent[x] !== r) { const n = parent[x]; parent[x] = r; x = n; } return r; };
  const link = (a, b) => { const ra = find(a), rb = find(b); if (ra !== rb) parent[ra] = rb; };
  const splitSyns = (s) => (s || '').split(/[,，;；/]| or | and /i).map(t => t.trim().toLowerCase()).filter(t => /^[a-z][a-z'\- ]*$/.test(t));
  const allSet = new Set();
  const rows = [];
  for (const list of Object.values(vocab || {})) {
    for (const e of list) {
      const w = (e.word || '').toLowerCase().trim();
      if (!/^[a-z]/.test(w)) continue;
      const syns = splitSyns(e.synonym);
      allSet.add(w);
      syns.forEach(s => allSet.add(s));
      rows.push([w, syns]);
    }
  }
  for (const w of allSet) parent[w] = w;
  for (const [w, syns] of rows) for (const s of syns) link(w, s);
  const byClass = {};
  for (const w of allSet) {
    const r = find(w);
    (byClass[r] = byClass[r] || []).push(w);
  }
  const byWord = {};
  for (const cls of Object.values(byClass)) {
    if (cls.length < 2) continue;
    for (const w of cls) byWord[w] = cls.filter(x => x !== w);
  }
  return { byWord, allWords: [...allSet] };
}

async function switchBook(bookId) {
  if (bookId === ACTIVE_BOOK_ID) return;
  try {
    await loadBook(bookId);
  } catch (e) {
    toast('Failed to load book');
    console.warn('switchBook', e);
    return;
  }
  REVEAL_ALL = false;
  renderBookPicker();
  // Route back to the lists overview because the current route may not
  // make sense in the new book (e.g. List 16 doesn't exist in a 5-list book).
  location.hash = '#/';
  router();
}

function renderBookPicker() {
  const slot = $('#topbarRight');
  if (!slot) return;
  const opts = BOOKS.map(b =>
    `<option value="${b.id}"${b.id === ACTIVE_BOOK_ID ? ' selected' : ''}>${escHtml(b.label)}</option>`
  ).join('');
  slot.innerHTML = `<select class="book-picker" id="bookPicker" aria-label="Choose vocab book">${opts}</select>`;
  $('#bookPicker').addEventListener('change', (e) => switchBook(e.target.value));
}

function key(n, w) { return `${n}::${w.toLowerCase()}`; }
function getCard(n, w) {
  const k = key(n, w);
  if (!PROGRESS[k]) PROGRESS[k] = { ef: 2.5, interval: 0, reps: 0, due: 0, lapses: 0, last: 0, starred: false };
  if (PROGRESS[k].starred === undefined) PROGRESS[k].starred = false;
  return PROGRESS[k];
}
function toggleStar(n, word) {
  const c = getCard(n, word);
  c.starred = !c.starred;
  saveProgress();
  return c.starred;
}
function isFresh(c) { return c.reps === 0 && c.last === 0; }
function isMature(c) { return c.interval >= 21; }
function isLearning(c) { return !isFresh(c) && !isMature(c); }
function isDue(c) { return c.due <= Date.now(); }
// Starred words act as if they're due whenever it's been ~1 day since last
// review, regardless of the SM-2 interval — so words you always forget keep
// cycling back into the review pool until you un-star them.
function isReviewDue(c) {
  if (isFresh(c)) return false;
  if (c.starred) return c.last === 0 || (Date.now() - c.last) >= DAY;
  return c.due <= Date.now();
}

// --- SM-2 ---
function rateCard(n, w, q) {
  const c = getCard(n, w);
  if (q < 3) {
    c.reps = 0;
    c.interval = 1;
    c.lapses += 1;
  } else {
    if (c.reps === 0) c.interval = 1;
    else if (c.reps === 1) c.interval = 6;
    else c.interval = Math.round(c.interval * c.ef);
    c.reps += 1;
  }
  c.ef = Math.max(1.3, c.ef + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02)));
  c.last = Date.now();
  c.due = Date.now() + c.interval * DAY;
  saveProgress();
}

// --- summary helpers ---
function listSummary(n) {
  const words = VOCAB[String(n)] || [];
  let fresh = 0, learning = 0, mature = 0, due = 0;
  for (const w of words) {
    const c = getCard(n, w.word);
    if (isFresh(c)) fresh++;
    else if (isMature(c)) mature++;
    else learning++;
    if (!isFresh(c) && isDue(c)) due++;
  }
  return { total: words.length, fresh, learning, mature, due };
}

function activeListNumbers() {
  // A list is "active" if its unit has been tested OR has any non-fresh card
  const active = new Set();
  for (const n of Object.keys(VOCAB)) {
    if (UNITS[n]?.tested) { active.add(+n); continue; }
    for (const w of VOCAB[n]) {
      const c = getCard(+n, w.word);
      if (!isFresh(c)) { active.add(+n); break; }
    }
  }
  return [...active].sort((a, b) => a - b);
}

// --- routing ---
function parseRoute() {
  const h = location.hash.replace(/^#/, '') || '/';
  const segs = h.split('/').filter(Boolean);
  return segs;
}

// A "stateful" route holds an in-memory session (current question index,
// the user's selections so far, etc.) that gets destroyed by a re-render.
// Background events like sync pulls or auth token refreshes MUST NOT call
// router() while we're on one of these screens — otherwise a unit test
// or mixed review snaps back to question 1 mid-session.
function isStatefulRoute() {
  const segs = parseRoute();
  if (segs[0] === 'review' || segs[0] === 'starred-test' || segs[0] === 'random-test') return true;
  if (segs[0] === 'list' && segs[2] === 'test') return true;
  if (segs[0] === 'list' && segs[2] === 'passages' && segs[4] === 'quiz') return true;
  return false;
}

function router() {
  const segs = parseRoute();
  const back = $('#backBtn');
  back.hidden = segs.length === 0;
  // Highlight bottom nav
  $$('.nav-link').forEach(a => a.classList.remove('active'));
  if (segs.length === 0) $('.nav-link[data-route="lists"]').classList.add('active');
  else if (segs[0] === 'review') $('.nav-link[data-route="review"]').classList.add('active');
  else if (segs[0] === 'starred' || segs[0] === 'starred-test') $('.nav-link[data-route="starred"]').classList.add('active');
  else if (segs[0] === 'missed') $('.nav-link[data-route="missed"]').classList.add('active');
  else if (segs[0] === 'stats') $('.nav-link[data-route="stats"]').classList.add('active');
  else if (segs[0] === 'list' || segs[0] === 'random-test') $('.nav-link[data-route="lists"]').classList.add('active');

  // Dispatch
  if (segs.length === 0) return renderLists();
  if (segs[0] === 'review') return renderReview();
  if (segs[0] === 'starred') return renderStarred();
  if (segs[0] === 'starred-test') return renderStarredTest();
  if (segs[0] === 'random-test') return renderRandomTest();
  if (segs[0] === 'missed') return renderMissed();
  if (segs[0] === 'stats') return renderStats();
  if (segs[0] === 'list') {
    const n = +segs[1];
    if (!VOCAB[String(n)]) return notFound();
    if (segs.length === 2) return renderListDetail(n);
    if (segs[2] === 'words') return renderWords(n);
    if (segs[2] === 'test') return renderUnitTest(n);
    if (segs[2] === 'passages') {
      if (segs.length === 3) return renderPassageList(n);
      const i = +segs[3];
      if (segs.length === 4) return renderPassage(n, i);
      if (segs[4] === 'quiz') return renderPassageQuiz(n, i);
    }
  }
  return notFound();
}

function notFound() {
  setHeader('Not found');
  $('#view').innerHTML = `<div class="empty-state"><h2>Page not found</h2><p><a class="btn-secondary" href="#/">Go home</a></p></div>`;
}

function setHeader(title) {
  $('#headerTitle').textContent = title;
  // #topbarRight is owned by renderBookPicker; do not clobber it here.
}

// =====================================================
// VIEW: Lists overview
// =====================================================
function renderLists() {
  setHeader('GRE Vocab');
  const lists = Object.keys(VOCAB).sort((a, b) => +a - +b);
  let totalMature = 0, totalLearning = 0, totalFresh = 0, totalWords = 0;
  const html = [];
  for (const n of lists) {
    const s = listSummary(+n);
    totalMature += s.mature; totalLearning += s.learning; totalFresh += s.fresh; totalWords += s.total;
  }

  // Random Test banner — top of home page. Draws up to 200 random words
  // from the whole active book, no unit-test gating required.
  html.push(renderRandomTestBanner());

  html.push(`<div class="lists-summary">
    <div class="summary-card"><div class="v">${totalMature}</div><div class="l">Mature</div></div>
    <div class="summary-card"><div class="v">${totalLearning}</div><div class="l">Learning</div></div>
    <div class="summary-card"><div class="v">${totalWords - totalMature - totalLearning}</div><div class="l">New</div></div>
  </div>`);

  html.push('<div class="section-heading">Lists</div>');
  html.push('<div class="lists-grid">');
  for (const n of lists) {
    const s = listSummary(+n);
    const tested = !!UNITS[n]?.tested;
    const known = s.mature + s.learning;
    const pct = s.total ? Math.round((known / s.total) * 100) : 0;
    const badge = tested
      ? `<span class="badge tested">tested ${Math.round((UNITS[n].lastScore || 0) * 100)}%</span>`
      : (known > 0 ? `<span class="badge">started</span>` : `<span class="badge">new</span>`);
    html.push(`<a class="list-card ${tested ? 'tested' : ''}" href="#/list/${n}">
      <div class="num"><span class="n">List ${n}</span>${badge}</div>
      <div class="total">${s.total} words</div>
      <div class="progress"><div style="width:${pct}%"></div></div>
      <div class="progress-meta"><span>${known}/${s.total} learned</span><span>${pct}%</span></div>
    </a>`);
  }
  html.push('</div>');

  // Mixed Review banner — appears below lists, expands automatically
  html.push(renderReviewBanner());

  $('#view').innerHTML = html.join('');
}

function renderReviewBanner() {
  const active = activeListNumbers();
  if (active.length === 0) {
    return `
      <div class="section-heading">Mixed Review</div>
      <div class="review-banner empty">
        <div class="review-banner-body">
          <div class="rb-title">No lists active yet</div>
          <div class="rb-desc">Take a Unit Test on any list to start cumulative review. The pool grows automatically as you complete more units.</div>
        </div>
      </div>`;
  }
  // Mixed review now excludes starred words — those are tested separately
  // through the Starred Test banner at the top of the page.
  let poolCount = 0, starredCount = 0;
  for (const n of active) {
    for (const w of VOCAB[String(n)]) {
      const c = getCard(n, w.word);
      if (c.starred) { starredCount++; continue; }
      poolCount++;
    }
  }
  const rangeLabel = active.length === 1
    ? `list ${active[0]}`
    : (active.length <= 4
        ? `lists ${active.join(', ')}`
        : `lists ${active[0]}–${active[active.length - 1]} (${active.length} units)`);
  const sessionSize = Math.min(SETTINGS.reviewSize, poolCount);
  const starredBlurb = starredCount > 0
    ? ` · ${starredCount} starred ★ tested separately above.`
    : '';
  return `
    <div class="section-heading">Mixed Review · ${rangeLabel}</div>
    <a class="review-banner" href="#/review">
      <div class="review-banner-body">
        <div class="rb-title">${sessionSize}-question random review</div>
        <div class="rb-desc">${poolCount} non-starred word${poolCount === 1 ? '' : 's'} in pool across ${active.length} unit${active.length === 1 ? '' : 's'}.${starredBlurb} New random sample every time you start.</div>
      </div>
      <div class="review-banner-cta">
        <span class="btn-primary" style="pointer-events:none">Start review</span>
      </div>
    </a>`;
}

function renderRandomTestBanner() {
  const book = bookById(ACTIVE_BOOK_ID);
  let poolCount = 0;
  for (const words of Object.values(VOCAB)) poolCount += words.length;
  if (poolCount === 0) return '';
  const sessionSize = Math.min(200, poolCount);
  return `
    <div class="section-heading">Random Test</div>
    <a class="review-banner random-test" href="#/random-test">
      <div class="review-banner-body">
        <div class="rb-title">${sessionSize}-question random test · ${escHtml(book.label)}</div>
        <div class="rb-desc">${poolCount} word${poolCount === 1 ? '' : 's'} in the whole book. New random sample every time — no unit-test gating required.</div>
      </div>
      <div class="review-banner-cta">
        <span class="btn-primary" style="pointer-events:none">Start test</span>
      </div>
    </a>`;
}

function renderStarredTestBanner() {
  let starredCount = 0;
  for (const [n, words] of Object.entries(VOCAB)) {
    for (const w of words) {
      if (getCard(+n, w.word).starred) starredCount++;
    }
  }
  if (starredCount === 0) return '';
  const sessionSize = Math.min(200, starredCount);
  return `
    <div class="section-heading">Starred Test ★</div>
    <a class="review-banner starred-test" href="#/starred-test">
      <div class="review-banner-body">
        <div class="rb-title">★ ${sessionSize}-question test from your starred words</div>
        <div class="rb-desc">${starredCount} starred word${starredCount === 1 ? '' : 's'} in your pool. Up to 200 are drawn at random each session.</div>
      </div>
      <div class="review-banner-cta">
        <span class="btn-primary" style="pointer-events:none">Start test</span>
      </div>
    </a>`;
}

// =====================================================
// VIEW: List detail
// =====================================================
function renderListDetail(n) {
  setHeader(`List ${n}`);
  const s = listSummary(n);
  const known = s.mature + s.learning;
  const pct = s.total ? Math.round((known / s.total) * 100) : 0;
  const tested = !!UNITS[n]?.tested;
  const passages = (PASSAGES[String(n)] || []);
  const passagesAvailable = passages.length > 0;

  const html = `
    <div class="list-detail-header">
      <div class="title">List ${n}</div>
      <div class="subtitle">${s.total} words · ${known} learned · ${s.due} due ${tested ? `· last test ${Math.round(UNITS[n].lastScore * 100)}%` : ''}</div>
      <div class="progress"><div style="width:${pct}%"></div></div>
      <div class="progress-meta"><span>${known}/${s.total}</span><span>${pct}%</span></div>
    </div>
    <div class="action-grid">
      <a class="action-card" href="#/list/${n}/words">
        <div class="icon">≡</div>
        <div class="body">
          <div class="title">Words</div>
          <div class="desc">Browse all ${s.total} words with meanings.</div>
        </div>
      </a>
      <a class="action-card" href="#/list/${n}/test">
        <div class="icon">✎</div>
        <div class="body">
          <div class="title">Unit Test</div>
          <div class="desc">Test all ${s.total} words in this list.</div>
        </div>
      </a>
      <a class="action-card ${passagesAvailable ? '' : 'disabled'}" href="#/list/${n}/passages">
        <div class="icon">📖</div>
        <div class="body">
          <div class="title">Passages</div>
          <div class="desc">${passagesAvailable ? `${passages.length} reading passages with comprehension questions.` : 'Passages not yet available for this list.'}</div>
        </div>
      </a>
    </div>
  `;
  $('#view').innerHTML = html;
}

// =====================================================
// VIEW: Browse words
// =====================================================
function renderWords(n) {
  setHeader(`List ${n} · Words`);
  const words = VOCAB[String(n)];
  const html = [];
  const hiddenCls = REVEAL_ALL ? '' : 'hidden-meaning';
  const btnLabel  = REVEAL_ALL ? 'Hide all' : 'Reveal all';
  html.push(`<div class="words-controls">
    <span class="words-hint">Tap a card to reveal · ★ to star</span>
    <button class="btn-secondary" id="revealAll" type="button">${btnLabel}</button>
  </div>`);
  for (let i = 0; i < words.length; i++) {
    const w = words[i];
    const c = getCard(n, w.word);
    html.push(`<div class="word-card ${hiddenCls}" data-i="${i}" data-word="${escAttr(w.word)}">
      <button class="star-btn ${c.starred ? 'on' : ''}" data-word="${escAttr(w.word)}" aria-label="Toggle star" type="button">${c.starred ? '★' : '☆'}</button>
      <div class="head"><span class="word">${escHtml(w.word)}</span><span class="ipa">${escHtml(w.ipa)}</span></div>
      <div class="reveal-prompt">tap to reveal</div>
      <div class="card-body">
        <div class="zh">${escHtml(w.def_zh)}</div>
        <div class="en">${escHtml(w.def_en)}</div>
        ${w.synonym ? `<div class="syn">≈ ${escHtml(w.synonym)}</div>` : ''}
        ${w.ex_en ? `<div class="ex">${escHtml(w.ex_en)}<div class="ex-zh">${escHtml(w.ex_zh)}</div></div>` : ''}
      </div>
      <div class="row-bottom">${tagFor(c)}<span>${c.last ? new Date(c.last).toLocaleDateString() : ''}</span></div>
    </div>`);
  }
  $('#view').innerHTML = html.join('');

  $$('.word-card').forEach(card => {
    card.addEventListener('click', () => {
      card.classList.toggle('hidden-meaning');
    });
  });

  $$('.star-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const word = btn.dataset.word;
      const on = toggleStar(n, word);
      btn.textContent = on ? '★' : '☆';
      btn.classList.toggle('on', on);
    });
  });

  $('#revealAll').addEventListener('click', (e) => {
    e.stopPropagation();
    REVEAL_ALL = !REVEAL_ALL;
    $$('.word-card').forEach(c => c.classList.toggle('hidden-meaning', !REVEAL_ALL));
    e.currentTarget.textContent = REVEAL_ALL ? 'Hide all' : 'Reveal all';
  });
}

function tagFor(c) {
  if (isFresh(c)) return `<span class="tag fresh">new</span>`;
  if (isMature(c)) return `<span class="tag mature">mature · ${c.interval}d</span>`;
  if (isLearning(c)) return `<span class="tag learning">learning · ${c.interval}d</span>`;
  return `<span class="tag">${c.interval}d</span>`;
}

// =====================================================
// VIEW: Unit Test
// =====================================================
function renderUnitTest(n) {
  setHeader(`List ${n} · Unit Test`);
  const words = VOCAB[String(n)] || [];
  // Test every word in the list, in randomized order
  const session = shuffle([...words]);
  startUnitTest(n, session);
}

function startUnitTest(n, session) {
  const state = {
    n,
    qs: session.map(w => buildTestQ(n, w)),
    idx: 0,
    answers: [],   // {word, correct, picked}
  };
  renderUnitTestQ(state);
}

function buildTestQ(n, w) {
  // Equivalence-mode books test "pick the equivalent word" instead of
  // word↔Chinese. Falls back to en2zh for words that have no equivalents
  // in the index (rare; would mean an isolated entry with empty synonym).
  const book = bookById(ACTIVE_BOOK_ID);
  if (book.testMode === 'equiv' && EQUIV_INDEX) {
    const eq = buildEquivQ(w);
    if (eq) return eq;
  }
  // Always test en→zh: on the real GRE you see the English word and have
  // to recall its meaning, never the other direction.
  const dir = 'en2zh';
  const distractors = pickDistractors(n, w, 3, dir);
  const opts = shuffle([w, ...distractors]);
  return { w, dir, opts };
}

function buildRevealHtml(q, card, compact = false) {
  const w = q.w;
  const star = `<button class="star-btn ${card.starred ? 'on' : ''}" id="revealStar" type="button" aria-label="Star">${card.starred ? '★' : '☆'}</button>`;
  const head = `<div class="reveal-head">
    <div class="word">${escHtml(w.word)} ${w.ipa ? `<span style="color:var(--muted);font-weight:normal">${escHtml(w.ipa)}</span>` : ''}</div>
    ${star}
  </div>`;
  if (q.dir === 'equiv') {
    const others = (EQUIV_INDEX && EQUIV_INDEX.byWord[w.word.toLowerCase()] || []).filter(x => x !== q.correctWord);
    const otherLine = others.length
      ? `<div style="font-size:12.5px;color:var(--muted);margin-top:4px">Also equivalent: ${others.map(escHtml).join(', ')}</div>`
      : '';
    return `${head}
      <div style="margin-top:6px">≡ <b>${escHtml(q.correctWord)}</b></div>
      ${otherLine}
      ${w.def_zh ? `<div style="color:var(--muted);font-size:13px;margin-top:6px">${escHtml(w.def_zh)}</div>` : ''}`;
  }
  return `${head}
    <div>${escHtml(w.def_zh || '')}</div>
    ${w.def_en ? `<div style="color:var(--muted);font-size:13px;margin-top:4px">${escHtml(w.def_en)}</div>` : ''}
    ${!compact && w.ex_en ? `<div class="ex">${escHtml(w.ex_en)}<br>${escHtml(w.ex_zh || '')}</div>` : ''}`;
}

function renderTestPrompt(q, w) {
  if (q.dir === 'equiv') {
    return `<div class="prompt-label">Pick the equivalent word</div>
            <div class="prompt">${escHtml(w.word)}</div>
            ${w.def_zh ? `<div class="ipa">${escHtml(w.def_zh)}</div>` : ''}`;
  }
  if (q.dir === 'en2zh') {
    return `<div class="prompt-label">What does this mean?</div>
            <div class="prompt">${escHtml(w.word)}</div>
            <div class="ipa">${escHtml(w.ipa || '')}</div>`;
  }
  return `<div class="prompt-label">Which English word?</div>
          <div class="prompt">${escHtml(w.def_zh)}</div>`;
}

function renderTestOptions(q, w) {
  return q.opts.map((o, i) => {
    let text, isCorrect;
    if (q.dir === 'equiv') {
      text = o.word;
      isCorrect = !!o.equiv;
    } else if (q.dir === 'en2zh') {
      text = o.def_zh;
      isCorrect = o.word === w.word;
    } else {
      text = o.word;
      isCorrect = o.word === w.word;
    }
    return `<button data-i="${i}" data-correct="${isCorrect ? '1' : '0'}">${escHtml(text)}</button>`;
  }).join('');
}

function buildEquivQ(w) {
  if (!EQUIV_INDEX) return null;
  const wl = w.word.toLowerCase();
  const equivs = EQUIV_INDEX.byWord[wl] || [];
  if (!equivs.length) return null;
  const correct = equivs[Math.floor(Math.random() * equivs.length)];
  const equivSet = new Set([wl, ...equivs]);
  const pool = EQUIV_INDEX.allWords.filter(x => !equivSet.has(x));
  shuffle(pool);
  const distractors = pool.slice(0, 3);
  // If we somehow lack enough distractors (tiny book), bail out
  if (distractors.length < 3) return null;
  const opts = shuffle([
    { word: correct, equiv: true },
    ...distractors.map(d => ({ word: d, equiv: false })),
  ]);
  return { w, dir: 'equiv', opts, correctWord: correct };
}

function pickDistractors(n, target, k, dir) {
  // For en2zh, distractors are other words' Chinese meanings
  // For zh2en, distractors are other English words
  const candidates = (VOCAB[String(n)] || []).filter(x =>
    x.word !== target.word && (dir === 'en2zh' ? x.def_zh : x.word) && x.def_zh !== target.def_zh
  );
  shuffle(candidates);
  const chosen = candidates.slice(0, k);
  if (chosen.length < k) {
    const all = Object.values(VOCAB).flat().filter(x =>
      x.word !== target.word && (dir === 'en2zh' ? x.def_zh : x.word) && x.def_zh !== target.def_zh
    );
    shuffle(all);
    for (const x of all) {
      if (chosen.length >= k) break;
      if (!chosen.includes(x)) chosen.push(x);
    }
  }
  return chosen;
}

function renderUnitTestQ(state) {
  if (state.idx >= state.qs.length) return finishUnitTest(state);
  const q = state.qs[state.idx];
  const w = q.w;
  const total = state.qs.length;
  const pct = Math.round((state.idx / total) * 100);

  const promptHtml = renderTestPrompt(q, w);
  const optsHtml   = renderTestOptions(q, w);

  $('#view').innerHTML = `
    <div class="quiz-stage">
      <div class="quiz-progress-bar"><div style="width:${pct}%"></div></div>
      <div class="quiz-meta">
        <span class="pill">Q ${state.idx + 1} / ${total}</span>
        <span class="pill">List ${state.n}</span>
      </div>
      <div class="quiz-card ${q.dir === 'zh2en' ? 'zh-prompt' : ''}">${promptHtml}</div>
      <div class="quiz-options" id="opts">${optsHtml}</div>
      <div class="quiz-reveal" id="reveal" hidden></div>
      <div class="quiz-next" id="nextWrap" hidden>
        <button class="btn-primary" id="nextBtn">${state.idx + 1 >= total ? 'See results' : 'Next →'}</button>
      </div>
    </div>
  `;
  $$('#opts button').forEach(btn => {
    btn.addEventListener('click', () => onUnitAnswer(state, q, btn));
  });
}

function onUnitAnswer(state, q, btn) {
  const correct = btn.dataset.correct === '1';
  state.answers.push({
    w: q.w,
    correct,
    picked: btn.textContent,
    dir: q.dir,
  });
  $$('#opts button').forEach(b => {
    b.classList.add('disabled');
    if (b.dataset.correct === '1') b.classList.add('correct');
    else if (b === btn) b.classList.add('wrong');
  });

  // Update SRS for this word
  rateCard(state.n, q.w.word, correct ? 4 : 0);

  // Reveal
  const reveal = $('#reveal');
  reveal.hidden = false;
  const card = getCard(state.n, q.w.word);
  reveal.innerHTML = buildRevealHtml(q, card);
  $('#revealStar').addEventListener('click', () => {
    const on = toggleStar(state.n, q.w.word);
    const btn = $('#revealStar');
    btn.textContent = on ? '★' : '☆';
    btn.classList.toggle('on', on);
  });
  $('#nextWrap').hidden = false;
  $('#nextBtn').addEventListener('click', () => {
    state.idx += 1;
    renderUnitTestQ(state);
  });
}

function finishUnitTest(state) {
  const total = state.qs.length;
  const correct = state.answers.filter(a => a.correct).length;
  const score = correct / total;

  // Mark unit as tested
  if (!UNITS[state.n]) UNITS[state.n] = {};
  UNITS[state.n].tested = true;
  UNITS[state.n].lastScore = score;
  UNITS[state.n].lastTested = Date.now();
  saveUnits();

  setHeader(`List ${state.n} · Results`);
  const pct = Math.round(score * 100);
  const html = [];
  html.push(`<div class="results">
    <div class="score">${pct}%</div>
    <div class="breakdown">${correct} of ${total} correct</div>
    <div class="actions">
      <a class="btn-primary" href="#/list/${state.n}/test">Retake test</a>
      <a class="btn-secondary" href="#/list/${state.n}">Back to list</a>
      <a class="btn-secondary" href="#/review">Mixed review</a>
    </div>
  </div>`);

  const wrong = state.answers.filter(a => !a.correct);
  if (wrong.length) {
    html.push(`<div class="section-heading">Missed (${wrong.length})</div>`);
    html.push('<div class="results-list">');
    for (const a of wrong) {
      html.push(`<div class="results-row miss">
        <div class="head"><span class="w">${escHtml(a.w.word)}</span><span class="gloss">${escHtml(a.w.def_zh)}</span></div>
        <div class="your">your answer: ${escHtml(a.picked)}</div>
      </div>`);
    }
    html.push('</div>');
  }

  const right = state.answers.filter(a => a.correct);
  if (right.length) {
    html.push(`<div class="section-heading">Correct (${right.length})</div>`);
    html.push('<div class="results-list">');
    for (const a of right) {
      html.push(`<div class="results-row hit">
        <div class="head"><span class="w">${escHtml(a.w.word)}</span><span class="gloss">${escHtml(a.w.def_zh)}</span></div>
      </div>`);
    }
    html.push('</div>');
  }
  $('#view').innerHTML = html.join('');
}

// =====================================================
// VIEW: Cumulative Review
// =====================================================
function renderReview() {
  setHeader('Mixed Review');
  const active = activeListNumbers();
  if (active.length === 0) {
    $('#view').innerHTML = `<div class="empty-state">
      <h2>No lists active yet</h2>
      <p>Take at least one Unit Test to start cumulative review.</p>
      <a class="btn-primary" href="#/">Pick a list</a>
    </div>`;
    return;
  }
  const session = buildReviewSession(active, SETTINGS.reviewSize);
  startReview(session, active);
}

function buildReviewSession(activeLists, size) {
  // Pull a random sample of non-starred words across all active lists.
  // Starred words are excluded here because they get their own dedicated
  // Starred Test (see renderStarredTest), so mixed review concentrates on
  // the words that aren't already being tested individually.
  const pool = [];
  for (const n of activeLists) {
    for (const w of VOCAB[String(n)]) {
      const c = getCard(n, w.word);
      if (c.starred) continue;
      pool.push({ n, w });
    }
  }
  shuffle(pool);
  return pool.slice(0, Math.min(size, pool.length));
}

function startReview(session, active) {
  const state = {
    qs: session.map(({ n, w }) => ({ n, ...buildTestQ(n, w) })),
    idx: 0,
    answers: [],
    isReview: true,
    activeLists: active,
  };
  renderReviewQ(state);
}

// =====================================================
// VIEW: Starred Test (up to 200 questions, only starred words)
// =====================================================
function renderRandomTest() {
  setHeader('Random Test');
  const pool = [];
  for (const [n, words] of Object.entries(VOCAB)) {
    for (const w of words) pool.push({ n: +n, w });
  }
  if (pool.length === 0) {
    $('#view').innerHTML = `<div class="empty-state">
      <h2>This book is empty</h2>
      <a class="btn-primary" href="#/">Back to lists</a>
    </div>`;
    return;
  }
  shuffle(pool);
  const session = pool.slice(0, Math.min(200, pool.length));
  const activeLists = [...new Set(session.map(s => s.n))].sort((a, b) => a - b);
  const state = {
    qs: session.map(({ n, w }) => ({ n, ...buildTestQ(n, w) })),
    idx: 0,
    answers: [],
    isReview: true,
    isRandomTest: true,
    activeLists,
    totalPool: pool.length,
  };
  renderReviewQ(state);
}

function renderStarredTest() {
  setHeader('Starred Test ★');
  const starred = [];
  for (const [n, words] of Object.entries(VOCAB)) {
    for (const w of words) {
      const c = getCard(+n, w.word);
      if (c.starred) starred.push({ n: +n, w });
    }
  }
  if (starred.length === 0) {
    $('#view').innerHTML = `<div class="empty-state">
      <h2>No starred words yet</h2>
      <p>Star the words you keep forgetting by tapping ★ on any word card or quiz reveal. Once you have some, this test will draw up to 200 of them at random.</p>
      <a class="btn-primary" href="#/">Back to lists</a>
    </div>`;
    return;
  }
  shuffle(starred);
  const session = starred.slice(0, 200);
  const activeLists = [...new Set(session.map(s => s.n))].sort((a, b) => a - b);
  const state = {
    qs: session.map(({ n, w }) => ({ n, ...buildTestQ(n, w) })),
    idx: 0,
    answers: [],
    isReview: true,
    isStarredTest: true,
    activeLists,
    totalStarred: starred.length,
  };
  renderReviewQ(state);
}

function renderReviewQ(state) {
  if (state.idx >= state.qs.length) return finishReview(state);
  const q = state.qs[state.idx];
  const w = q.w;
  const pct = Math.round((state.idx / state.qs.length) * 100);

  const promptHtml = renderTestPrompt(q, w);
  const optsHtml   = renderTestOptions(q, w);

  $('#view').innerHTML = `
    <div class="quiz-stage">
      <div class="quiz-progress-bar"><div style="width:${pct}%"></div></div>
      <div class="quiz-meta">
        <span class="pill">Q ${state.idx + 1} / ${state.qs.length}</span>
        <span class="pill">↺ list ${q.n}</span>
      </div>
      <div class="quiz-card ${q.dir === 'zh2en' ? 'zh-prompt' : ''}">${promptHtml}</div>
      <div class="quiz-options" id="opts">${optsHtml}</div>
      <div class="quiz-reveal" id="reveal" hidden></div>
      <div class="quiz-next" id="nextWrap" hidden>
        <button class="btn-primary" id="nextBtn">${state.idx + 1 >= state.qs.length ? 'Finish' : 'Next →'}</button>
      </div>
    </div>
  `;
  $$('#opts button').forEach(btn => {
    btn.addEventListener('click', () => onReviewAnswer(state, q, btn));
  });
}

function onReviewAnswer(state, q, btn) {
  const correct = btn.dataset.correct === '1';
  state.answers.push({ n: q.n, w: q.w, correct, picked: btn.textContent });
  $$('#opts button').forEach(b => {
    b.classList.add('disabled');
    if (b.dataset.correct === '1') b.classList.add('correct');
    else if (b === btn) b.classList.add('wrong');
  });
  rateCard(q.n, q.w.word, correct ? 4 : 0);
  const card = getCard(q.n, q.w.word);
  $('#reveal').hidden = false;
  $('#reveal').innerHTML = buildRevealHtml(q, card, /*compact=*/true);
  $('#revealStar').addEventListener('click', () => {
    const on = toggleStar(q.n, q.w.word);
    const btn = $('#revealStar');
    btn.textContent = on ? '★' : '☆';
    btn.classList.toggle('on', on);
  });
  $('#nextWrap').hidden = false;
  $('#nextBtn').addEventListener('click', () => {
    state.idx += 1;
    renderReviewQ(state);
  });
}

function finishReview(state) {
  const total = state.qs.length;
  const correct = state.answers.filter(a => a.correct).length;
  const pct = total ? Math.round((correct / total) * 100) : 0;
  const isStarred = !!state.isStarredTest;
  const isRandom  = !!state.isRandomTest;
  setHeader(isStarred ? 'Starred Test · Results' : (isRandom ? 'Random Test · Results' : 'Review · Results'));
  const wrong = state.answers.filter(a => !a.correct);
  const html = [];
  const breakdown = isStarred
    ? `${correct} of ${total} correct · ${state.totalStarred} starred in pool`
    : (isRandom
        ? `${correct} of ${total} correct · drawn from ${state.totalPool} words in the book`
        : `${correct} of ${total} correct · ${state.activeLists.length} lists in pool`);
  const againHref  = isStarred ? '#/starred-test' : (isRandom ? '#/random-test' : '#/review');
  const againLabel = isStarred ? 'Another starred round' : (isRandom ? 'Another random round' : 'Another round');
  html.push(`<div class="results">
    <div class="score">${pct}%</div>
    <div class="breakdown">${breakdown}</div>
    <div class="actions">
      <a class="btn-primary" href="${againHref}">${againLabel}</a>
      <a class="btn-secondary" href="#/">Back to lists</a>
    </div>
  </div>`);
  if (wrong.length) {
    html.push(`<div class="section-heading">Missed</div><div class="results-list">`);
    for (const a of wrong) {
      html.push(`<div class="results-row miss">
        <div class="head"><span class="w">${escHtml(a.w.word)}</span><span class="gloss">${escHtml(a.w.def_zh)} <em style="color:var(--muted)">· list ${a.n}</em></span></div>
      </div>`);
    }
    html.push('</div>');
  }
  $('#view').innerHTML = html.join('');
}

// =====================================================
// VIEW: Passage list
// =====================================================
function renderPassageList(n) {
  setHeader(`List ${n} · Passages`);
  const list = PASSAGES[String(n)] || [];
  if (list.length === 0) {
    $('#view').innerHTML = `<div class="empty-state">
      <h2>No passages yet</h2>
      <p>Reading passages haven't been written for list ${n} yet.</p>
      <a class="btn-secondary" href="#/list/${n}">Back to list</a>
    </div>`;
    return;
  }
  const html = ['<div class="passage-list">'];
  list.forEach((p, i) => {
    const wc = (p.text || '').split(/\s+/).filter(Boolean).length;
    const qcount = (p.questions || []).length;
    html.push(`<a class="passage-item" href="#/list/${n}/passages/${i}">
      <h3>${i + 1}. ${escHtml(p.title)}</h3>
      <div class="meta">${(p.targets || []).length} target words · ~${wc} words · ${qcount} questions</div>
    </a>`);
  });
  html.push('</div>');
  $('#view').innerHTML = html.join('');
}

// =====================================================
// VIEW: Read passage
// =====================================================
function renderPassage(n, i) {
  const passage = (PASSAGES[String(n)] || [])[i];
  if (!passage) return notFound();
  setHeader(`List ${n} · Reading ${i + 1}`);

  const wordIndex = buildGlobalWordIndex();
  const targetSet = new Set((passage.targets || []).map(t => t.toLowerCase()));
  const rendered = highlightPassage(passage.text, wordIndex, targetSet, n);

  $('#view').innerHTML = `
    <article class="passage-reader">
      <h2>${escHtml(passage.title)}</h2>
      <div class="passage-text">${rendered}</div>
      <div class="passage-actions">
        <a class="btn-secondary" href="#/list/${n}/passages">All passages</a>
        ${(passage.questions || []).length ? `<a class="btn-primary" href="#/list/${n}/passages/${i}/quiz">Take comprehension quiz →</a>` : ''}
      </div>
    </article>
  `;
  bindPassageInteractions(wordIndex);
}

function buildGlobalWordIndex() {
  const idx = new Map();
  for (const [n, words] of Object.entries(VOCAB)) {
    for (const w of words) {
      const k = w.word.toLowerCase();
      if (!idx.has(k)) idx.set(k, { n: +n, w });
    }
  }
  return idx;
}

function highlightPassage(text, wordIndex, targetSet, currentList) {
  // Process line-by-line so we preserve newlines
  const lines = text.split('\n');
  const re = /([A-Za-z][A-Za-z'\-]*)/g;
  return lines.map(line =>
    line.replace(re, (match) => {
      const lower = match.toLowerCase();
      const candidates = [lower, ...stemVariants(lower)];
      let hit = null;
      for (const c of candidates) {
        if (wordIndex.has(c)) { hit = wordIndex.get(c); break; }
      }
      if (!hit) return match;
      const isTarget = targetSet.has(hit.w.word.toLowerCase());
      const isReview = !isTarget && hit.n !== currentList;
      if (!isTarget && !isReview) return match;
      const cls = isReview ? 'target review' : 'target';
      return `<mark class="${cls}" data-key="${escAttr(hit.w.word)}">${match}</mark>`;
    })
  ).join('\n');
}

function stemVariants(word) {
  const v = [];
  const suf = [/'s$/, /ies$/, /ied$/, /es$/, /ed$/, /ing$/, /ly$/, /s$/, /d$/];
  for (const s of suf) {
    if (s.test(word)) v.push(word.replace(s, ''));
  }
  if (/ies$/.test(word)) v.push(word.replace(/ies$/, 'y'));
  if (/ied$/.test(word)) v.push(word.replace(/ied$/, 'y'));
  if (/[a-z]ing$/.test(word)) v.push(word.replace(/ing$/, 'e'));
  return v;
}

function bindPassageInteractions(wordIndex) {
  const pop = $('#popover');
  const close = () => { pop.hidden = true; };
  $$('mark.target').forEach(m => {
    m.addEventListener('click', (e) => {
      e.stopPropagation();
      const k = m.dataset.key.toLowerCase();
      const info = wordIndex.get(k);
      if (!info) return;
      pop.querySelector('.pop-word').textContent = `${info.w.word}  ${info.w.ipa || ''}`;
      pop.querySelector('.pop-zh').textContent = info.w.def_zh || '';
      pop.querySelector('.pop-en').textContent = info.w.def_en || '';
      pop.hidden = false;
      const r = m.getBoundingClientRect();
      const popW = 280;
      const popH = pop.offsetHeight || 140;
      const top = Math.min(window.innerHeight - popH - 16, Math.max(60, r.bottom + 6));
      const left = Math.max(8, Math.min(window.innerWidth - popW - 8, r.left));
      pop.style.top = top + 'px';
      pop.style.left = left + 'px';
    });
  });
  pop.querySelector('.pop-close').onclick = close;
  document.addEventListener('click', (e) => {
    if (!pop.contains(e.target) && !e.target.closest('mark.target')) close();
  });
}

// =====================================================
// VIEW: Passage comprehension quiz
// =====================================================
function renderPassageQuiz(n, i) {
  const passage = (PASSAGES[String(n)] || [])[i];
  if (!passage || !(passage.questions || []).length) return notFound();
  setHeader(`Reading ${i + 1} · Quiz`);

  const qs = passage.questions;
  const html = [];
  html.push(`<div class="comp-quiz">`);
  qs.forEach((q, qi) => {
    html.push(`<div class="comp-q" data-i="${qi}">
      <div class="q-text">${qi + 1}. ${escHtml(q.q)}</div>
      <div class="q-options">
        ${q.opts.map((opt, oi) => `
          <label data-i="${oi}">
            <input type="radio" name="q${qi}" value="${oi}">
            <span class="letter">${String.fromCharCode(65 + oi)}</span>
            <span>${escHtml(opt)}</span>
          </label>
        `).join('')}
      </div>
      <div class="q-explain" hidden></div>
    </div>`);
  });
  html.push(`</div>`);
  html.push(`<div style="margin-top:16px;display:flex;gap:8px;flex-wrap:wrap;">
    <button class="btn-primary" id="submitQuiz">Submit answers</button>
    <a class="btn-secondary" href="#/list/${n}/passages/${i}">Back to passage</a>
  </div>`);
  $('#view').innerHTML = html.join('');

  // Selection state
  $$('.comp-q .q-options label').forEach(label => {
    label.addEventListener('click', (e) => {
      const parent = label.closest('.q-options');
      $$('label', parent).forEach(l => l.classList.remove('selected'));
      label.classList.add('selected');
      label.querySelector('input').checked = true;
    });
  });

  $('#submitQuiz').addEventListener('click', () => gradePassageQuiz(n, i, qs));
}

function gradePassageQuiz(n, i, qs) {
  let correct = 0;
  qs.forEach((q, qi) => {
    const card = $(`.comp-q[data-i="${qi}"]`);
    const labels = $$('label', card);
    const selected = labels.find(l => l.classList.contains('selected'));
    const pickedI = selected ? +selected.dataset.i : -1;
    labels.forEach(l => {
      const oi = +l.dataset.i;
      if (oi === q.ans) l.classList.add('correct');
      else if (oi === pickedI) l.classList.add('wrong');
      l.classList.remove('selected');
    });
    if (pickedI === q.ans) correct++;
    if (q.why) {
      const ex = $('.q-explain', card);
      ex.hidden = false;
      ex.innerHTML = `<b>${pickedI === q.ans ? 'Correct.' : 'Why ' + String.fromCharCode(65 + q.ans) + '.'}</b> ${escHtml(q.why)}`;
    }
  });
  const summary = document.createElement('div');
  summary.className = 'results';
  summary.style.marginTop = '16px';
  summary.innerHTML = `
    <div class="score">${Math.round((correct / qs.length) * 100)}%</div>
    <div class="breakdown">${correct} of ${qs.length} correct</div>
    <div class="actions">
      <a class="btn-secondary" href="#/list/${n}/passages/${i}">Re-read</a>
      <a class="btn-secondary" href="#/list/${n}/passages">More passages</a>
    </div>
  `;
  $('#submitQuiz').replaceWith(summary);
}

// =====================================================
// VIEW: Starred words (across all lists)
// =====================================================
function renderStarred() {
  setHeader('Starred ★');
  const starred = [];
  for (const [n, words] of Object.entries(VOCAB)) {
    for (const w of words) {
      const c = getCard(+n, w.word);
      if (c.starred) starred.push({ n: +n, w });
    }
  }
  if (starred.length === 0) {
    $('#view').innerHTML = `<div class="empty-state">
      <h2>No starred words yet</h2>
      <p>Tap ★ on any word card or quiz reveal to mark words you keep forgetting. They'll show up here, and you'll get a dedicated Starred Test once you have some.</p>
      <a class="btn-primary" href="#/">Browse lists</a>
    </div>`;
    return;
  }
  starred.sort((a, b) => a.n - b.n || a.w.word.localeCompare(b.w.word));

  const html = [];
  const hiddenCls = REVEAL_ALL ? '' : 'hidden-meaning';
  const btnLabel  = REVEAL_ALL ? 'Hide all' : 'Reveal all';
  // Starred Test banner — top of the Starred section
  html.push(renderStarredTestBanner());
  html.push(`<div class="words-controls">
    <span class="words-hint">${starred.length} starred · tap to reveal · ★ to unstar</span>
    <button class="btn-secondary" id="revealAll" type="button">${btnLabel}</button>
  </div>`);

  // Group by list
  const byList = {};
  for (const item of starred) {
    if (!byList[item.n]) byList[item.n] = [];
    byList[item.n].push(item.w);
  }
  for (const n of Object.keys(byList).sort((a, b) => +a - +b)) {
    html.push(`<div class="section-heading">List ${n} · ${byList[n].length} starred</div>`);
    for (const w of byList[n]) {
      const c = getCard(+n, w.word);
      html.push(`<div class="word-card ${hiddenCls}" data-list="${n}" data-word="${escAttr(w.word)}">
        <button class="star-btn ${c.starred ? 'on' : ''}" data-list="${n}" data-word="${escAttr(w.word)}" aria-label="Toggle star" type="button">${c.starred ? '★' : '☆'}</button>
        <div class="head"><span class="word">${escHtml(w.word)}</span><span class="ipa">${escHtml(w.ipa)}</span></div>
        <div class="reveal-prompt">tap to reveal</div>
        <div class="card-body">
          <div class="zh">${escHtml(w.def_zh)}</div>
          <div class="en">${escHtml(w.def_en)}</div>
          ${w.synonym ? `<div class="syn">≈ ${escHtml(w.synonym)}</div>` : ''}
          ${w.ex_en ? `<div class="ex">${escHtml(w.ex_en)}<div class="ex-zh">${escHtml(w.ex_zh)}</div></div>` : ''}
        </div>
        <div class="row-bottom">${tagFor(c)}<span>${c.last ? new Date(c.last).toLocaleDateString() : ''}</span></div>
      </div>`);
    }
  }
  $('#view').innerHTML = html.join('');

  $$('.word-card').forEach(card => {
    card.addEventListener('click', () => {
      card.classList.toggle('hidden-meaning');
    });
  });

  $$('.star-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const n = +btn.dataset.list;
      const word = btn.dataset.word;
      const on = toggleStar(n, word);
      if (!on) {
        // Unstarred — remove this card with a fade
        const card = btn.closest('.word-card');
        card.style.transition = 'opacity 0.2s';
        card.style.opacity = '0';
        setTimeout(() => renderStarred(), 220);
      } else {
        btn.textContent = '★';
        btn.classList.add('on');
      }
    });
  });

  $('#revealAll').addEventListener('click', (e) => {
    e.stopPropagation();
    REVEAL_ALL = !REVEAL_ALL;
    $$('.word-card').forEach(c => c.classList.toggle('hidden-meaning', !REVEAL_ALL));
    e.currentTarget.textContent = REVEAL_ALL ? 'Hide all' : 'Reveal all';
  });
}

// =====================================================
// VIEW: Missed words (ranked by lapse count, active book only)
// =====================================================
function renderMissed() {
  setHeader('Missed ✗');
  const items = [];
  for (const [n, words] of Object.entries(VOCAB)) {
    for (const w of words) {
      const c = getCard(+n, w.word);
      if ((c.lapses || 0) > 0) items.push({ n: +n, w, lapses: c.lapses });
    }
  }
  if (items.length === 0) {
    $('#view').innerHTML = `<div class="empty-state">
      <h2>No missed words yet</h2>
      <p>Words you get wrong in a unit test, mixed review, or starred test appear here — ranked from most-missed to least. Perfect for a targeted review of the ones that keep tripping you up.</p>
      <a class="btn-primary" href="#/">Back to lists</a>
    </div>`;
    return;
  }
  items.sort((a, b) => b.lapses - a.lapses || a.w.word.localeCompare(b.w.word));

  const html = [];
  const hiddenCls = REVEAL_ALL ? '' : 'hidden-meaning';
  const btnLabel  = REVEAL_ALL ? 'Hide all' : 'Reveal all';
  html.push(`<div class="words-controls">
    <span class="words-hint">${items.length} missed · ranked by ✗ count</span>
    <button class="btn-secondary" id="revealAll" type="button">${btnLabel}</button>
  </div>`);
  for (const it of items) {
    const c = getCard(it.n, it.w.word);
    html.push(`<div class="word-card ${hiddenCls}" data-list="${it.n}" data-word="${escAttr(it.w.word)}">
      <button class="star-btn ${c.starred ? 'on' : ''}" data-list="${it.n}" data-word="${escAttr(it.w.word)}" aria-label="Toggle star" type="button">${c.starred ? '★' : '☆'}</button>
      <div class="head">
        <span class="word">${escHtml(it.w.word)}</span>
        <span class="ipa">${escHtml(it.w.ipa || '')}</span>
        <span class="miss-badge">✗ ${it.lapses} · list ${it.n}</span>
      </div>
      <div class="reveal-prompt">tap to reveal</div>
      <div class="card-body">
        <div class="zh">${escHtml(it.w.def_zh)}</div>
        <div class="en">${escHtml(it.w.def_en)}</div>
        ${it.w.synonym ? `<div class="syn">≈ ${escHtml(it.w.synonym)}</div>` : ''}
        ${it.w.ex_en ? `<div class="ex">${escHtml(it.w.ex_en)}<div class="ex-zh">${escHtml(it.w.ex_zh || '')}</div></div>` : ''}
      </div>
      <div class="row-bottom">${tagFor(c)}<span>${c.last ? new Date(c.last).toLocaleDateString() : ''}</span></div>
    </div>`);
  }
  $('#view').innerHTML = html.join('');

  $$('.word-card').forEach(card => {
    card.addEventListener('click', () => card.classList.toggle('hidden-meaning'));
  });
  $$('.star-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const n = +btn.dataset.list;
      const word = btn.dataset.word;
      const on = toggleStar(n, word);
      btn.textContent = on ? '★' : '☆';
      btn.classList.toggle('on', on);
    });
  });
  $('#revealAll').addEventListener('click', (e) => {
    e.stopPropagation();
    REVEAL_ALL = !REVEAL_ALL;
    $$('.word-card').forEach(c => c.classList.toggle('hidden-meaning', !REVEAL_ALL));
    e.currentTarget.textContent = REVEAL_ALL ? 'Hide all' : 'Reveal all';
  });
}

// =====================================================
// VIEW: Stats
// =====================================================
function renderStats() {
  setHeader('Stats');
  const lists = Object.keys(VOCAB).sort((a, b) => +a - +b);
  let mature = 0, learning = 0, fresh = 0, due = 0, total = 0;
  const perList = lists.map(n => {
    const s = listSummary(+n);
    mature += s.mature; learning += s.learning; fresh += s.fresh; due += s.due;
    total += s.total;
    return { n, ...s, tested: !!UNITS[n]?.tested, score: UNITS[n]?.lastScore };
  });
  const html = [];
  html.push(`<div class="stats-grid">
    <div class="stat-card"><div class="label">Mature</div><div class="value">${mature}</div></div>
    <div class="stat-card"><div class="label">Learning</div><div class="value">${learning}</div></div>
    <div class="stat-card"><div class="label">New</div><div class="value">${fresh}</div></div>
    <div class="stat-card"><div class="label">Due now</div><div class="value">${due}</div></div>
  </div>`);
  html.push(`<div class="section-heading">Per list</div><div class="stats-list">`);
  for (const r of perList) {
    const known = r.mature + r.learning;
    const pct = r.total ? Math.round((known / r.total) * 100) : 0;
    html.push(`<div class="stats-row">
      <span class="num">List ${r.n}</span>
      <div class="bar"><div style="width:${pct}%"></div></div>
      <span class="pct">${pct}%</span>
    </div>`);
  }
  html.push('</div>');
  html.push(`<div class="section-heading">Account</div>`);
  html.push(`<div id="accountBox" class="account-box">Loading…</div>`);
  html.push(`<div style="margin-top:18px;display:flex;gap:10px;flex-wrap:wrap">
    <button class="btn-secondary" id="resetBtn">Reset all progress</button>
  </div>`);
  $('#view').innerHTML = html.join('');
  $('#resetBtn').addEventListener('click', () => {
    if (confirm('This erases all study progress and unit-test results. Continue?')) {
      PROGRESS = {}; UNITS = {};
      saveProgress(); saveUnits();
      toast('Progress reset.');
      router();
    }
  });
  renderAccountBox();
}

async function storageStatus() {
  if (!(navigator.storage && navigator.storage.persisted)) return null;
  try { return await navigator.storage.persisted(); }
  catch { return null; }
}

async function renderAccountBox() {
  const box = $('#accountBox');
  if (!box) return;
  const persisted = await storageStatus();
  const persistLine = persisted === true
    ? `<div class="account-meta">Local storage: <b>persistent</b> — the browser will not evict your progress.</div>`
    : persisted === false
      ? `<div class="account-meta">Local storage: not persistent yet. The browser may grant it after a few sessions, or on PWA install (Add to Home Screen).</div>`
      : '';
  if (!window.SupaSync || !SupaSync.isConfigured()) {
    box.innerHTML = `
      <div class="rb-title">Cross-device sync not configured</div>
      <div class="rb-desc">Paste your Supabase URL and anon key into <code>supabase-sync.js</code> to enable sign-in and automatic sync across devices. Progress will keep saving locally in the meantime.</div>
      ${persistLine}`;
    return;
  }
  const user = await SupaSync.currentUser();
  if (!user) {
    box.innerHTML = `
      <div class="rb-title">Sign in to sync across devices</div>
      <div class="rb-desc">Enter your email. We'll send you a magic link — no password.</div>
      <div class="account-form">
        <input id="signinEmail" type="email" inputmode="email" placeholder="you@example.com" autocomplete="email">
        <button class="btn-primary" id="signinBtn" type="button">Send magic link</button>
      </div>
      <div id="signinMsg" class="account-msg" hidden></div>
      ${persistLine}`;
    $('#signinBtn').addEventListener('click', async () => {
      const email = ($('#signinEmail').value || '').trim();
      const msg = $('#signinMsg');
      msg.hidden = false;
      if (!email.includes('@')) { msg.textContent = 'Please enter a valid email.'; return; }
      $('#signinBtn').disabled = true;
      msg.textContent = 'Sending…';
      try {
        await SupaSync.signInWithEmail(email);
        msg.textContent = `Magic link sent to ${email}. Open it on this device to finish signing in.`;
      } catch (e) {
        msg.textContent = 'Sign-in failed: ' + (e?.message || e);
      } finally {
        $('#signinBtn').disabled = false;
      }
    });
    return;
  }
  const syncedAt = SupaSync.lastSyncedAt();
  const syncedLabel = syncedAt
    ? new Date(syncedAt).toLocaleTimeString()
    : 'on next change';
  box.innerHTML = `
    <div class="rb-title">Signed in as ${escHtml(user.email || user.id)}</div>
    <div class="rb-desc">Cross-device sync is on. Last pushed: ${syncedLabel}.</div>
    <div class="account-form">
      <button class="btn-secondary" id="signoutBtn" type="button">Sign out (keep local data)</button>
    </div>
    ${persistLine}`;
  $('#signoutBtn').addEventListener('click', async () => {
    await SupaSync.signOut();
    toast('Signed out.');
    renderAccountBox();
  });
}

// =====================================================
// helpers
// =====================================================
function shuffle(arr) {
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}
function escHtml(s) {
  return String(s ?? '').replace(/[&<>"']/g, c =>
    ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}
function escAttr(s) { return escHtml(s); }
let toastT;
function toast(msg) {
  const t = $('#toast');
  t.textContent = msg;
  t.classList.add('show');
  clearTimeout(toastT);
  toastT = setTimeout(() => t.classList.remove('show'), 1800);
}

init();
