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
 *   #/review                 Cumulative spaced-repetition review
 *   #/stats                  Stats overview
 *
 * Storage:
 *   gre.progress -> { [listN::word]: { ef, interval, reps, due, lapses, last } }
 *   gre.units    -> { [listN]: { tested, lastScore, lastTested } }
 *   gre.settings -> { unitTestSize, reviewSize, mixRatio }
 */

const DAY = 86400000;
const STORE_KEY = 'gre.progress';
const UNITS_KEY = 'gre.units';
const SETTINGS_KEY = 'gre.settings';
const DEFAULTS = {
  unitTestSize: 20,
  reviewSize: 20,
  mixRatio: 0.35,
};

let VOCAB = null;
let PASSAGES = null;
let SETTINGS = loadJson(SETTINGS_KEY, DEFAULTS);
let PROGRESS = loadJson(STORE_KEY, {});
let UNITS = loadJson(UNITS_KEY, {});

const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));

// --- bootstrap ---
async function init() {
  try {
    [VOCAB, PASSAGES] = await Promise.all([
      fetch('vocab.json?v=5').then(r => r.json()),
      fetch('passages.json?v=5').then(r => r.json()).catch(() => ({})),
    ]);
  } catch (e) {
    $('#view').innerHTML = `<div class="empty-state"><h2>Couldn't load data</h2><p>${escHtml(String(e))}</p></div>`;
    return;
  }
  window.addEventListener('hashchange', router);
  $('#backBtn').addEventListener('click', () => history.back());
  if (!location.hash) location.hash = '#/';
  router();
}

// --- storage helpers ---
function loadJson(k, fallback) {
  try { return Object.assign({}, fallback, JSON.parse(localStorage.getItem(k)) || {}); }
  catch { return { ...fallback }; }
}
function save(k, v) { localStorage.setItem(k, JSON.stringify(v)); }
function saveProgress() { save(STORE_KEY, PROGRESS); }
function saveUnits() { save(UNITS_KEY, UNITS); }

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

function router() {
  const segs = parseRoute();
  const back = $('#backBtn');
  back.hidden = segs.length === 0;
  // Highlight bottom nav
  $$('.nav-link').forEach(a => a.classList.remove('active'));
  if (segs.length === 0) $('.nav-link[data-route="lists"]').classList.add('active');
  else if (segs[0] === 'review') $('.nav-link[data-route="review"]').classList.add('active');
  else if (segs[0] === 'stats') $('.nav-link[data-route="stats"]').classList.add('active');
  else if (segs[0] === 'list') $('.nav-link[data-route="lists"]').classList.add('active');

  // Dispatch
  if (segs.length === 0) return renderLists();
  if (segs[0] === 'review') return renderReview();
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

function setHeader(title, rightHtml = '') {
  $('#headerTitle').textContent = title;
  $('#topbarRight').innerHTML = rightHtml;
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
  let dueCount = 0, poolCount = 0, starredDue = 0;
  for (const n of active) {
    for (const w of VOCAB[String(n)]) {
      const c = getCard(n, w.word);
      if (isFresh(c)) continue;
      poolCount++;
      if (isReviewDue(c)) {
        dueCount++;
        if (c.starred) starredDue++;
      }
    }
  }
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
  const rangeLabel = active.length === 1
    ? `list ${active[0]}`
    : (active.length <= 4
        ? `lists ${active.join(', ')}`
        : `lists ${active[0]}–${active[active.length - 1]} (${active.length} units)`);
  const ctaText = dueCount > 0 ? `Start review (${dueCount} due)` : 'Start review';
  const ctaDisabled = dueCount === 0 ? 'disabled' : '';
  const starredBlurb = starredDue > 0 ? ` · ${starredDue} starred` : '';
  return `
    <div class="section-heading">Mixed Review · ${rangeLabel}</div>
    <a class="review-banner" href="#/review">
      <div class="review-banner-body">
        <div class="rb-title">${dueCount > 0 ? `${dueCount} word${dueCount === 1 ? '' : 's'} due${starredBlurb}` : 'All caught up'}</div>
        <div class="rb-desc">${poolCount} word${poolCount === 1 ? '' : 's'} in your review pool across ${active.length} unit${active.length === 1 ? '' : 's'}. Starred words ★ surface here daily until you un-star them.</div>
      </div>
      <div class="review-banner-cta">
        <span class="btn-primary ${ctaDisabled}" style="pointer-events:none">${ctaText}</span>
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
  html.push(`<div class="words-controls">
    <span class="words-hint">Tap a card to reveal · ★ to star</span>
    <button class="btn-secondary" id="revealAll" type="button">Reveal all</button>
  </div>`);
  for (let i = 0; i < words.length; i++) {
    const w = words[i];
    const c = getCard(n, w.word);
    html.push(`<div class="word-card hidden-meaning" data-i="${i}" data-word="${escAttr(w.word)}">
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

  let allShown = false;
  $('#revealAll').addEventListener('click', (e) => {
    e.stopPropagation();
    allShown = !allShown;
    $$('.word-card').forEach(c => c.classList.toggle('hidden-meaning', !allShown));
    e.currentTarget.textContent = allShown ? 'Hide all' : 'Reveal all';
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
  // 50/50 between en->zh and zh->en
  const dir = Math.random() < 0.5 ? 'en2zh' : 'zh2en';
  const distractors = pickDistractors(n, w, 3, dir);
  const opts = shuffle([w, ...distractors]);
  return { w, dir, opts };
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

  const promptHtml = q.dir === 'en2zh'
    ? `<div class="prompt-label">What does this mean?</div>
       <div class="prompt">${escHtml(w.word)}</div>
       <div class="ipa">${escHtml(w.ipa || '')}</div>`
    : `<div class="prompt-label">Which English word?</div>
       <div class="prompt">${escHtml(w.def_zh)}</div>`;

  const optsHtml = q.opts.map((o, i) => {
    const text = q.dir === 'en2zh' ? o.def_zh : o.word;
    const isCorrect = o.word === w.word;
    return `<button data-i="${i}" data-correct="${isCorrect ? '1' : '0'}">${escHtml(text)}</button>`;
  }).join('');

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
  reveal.innerHTML = `
    <div class="reveal-head">
      <div class="word">${escHtml(q.w.word)} <span style="color:var(--muted);font-weight:normal">${escHtml(q.w.ipa || '')}</span></div>
      <button class="star-btn ${card.starred ? 'on' : ''}" id="revealStar" type="button" aria-label="Star">${card.starred ? '★' : '☆'}</button>
    </div>
    <div>${escHtml(q.w.def_zh)}</div>
    <div style="color:var(--muted);font-size:13px;margin-top:4px">${escHtml(q.w.def_en)}</div>
    ${q.w.ex_en ? `<div class="ex">${escHtml(q.w.ex_en)}<br>${escHtml(q.w.ex_zh)}</div>` : ''}
  `;
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
  if (session.length === 0) {
    $('#view').innerHTML = `<div class="empty-state">
      <h2>All caught up</h2>
      <p>No words from your active lists are due right now.</p>
      <p>Active: lists ${active.join(', ')}.</p>
      <a class="btn-secondary" href="#/">Back to lists</a>
    </div>`;
    return;
  }
  startReview(session, active);
}

function buildReviewSession(activeLists, size) {
  const now = Date.now();
  const due = [];
  for (const n of activeLists) {
    for (const w of VOCAB[String(n)]) {
      const c = getCard(n, w.word);
      if (!isReviewDue(c)) continue;
      const overdue = c.starred
        ? Math.max(1, (now - (c.last || 0)) / DAY)
        : Math.max(0, (now - c.due) / DAY);
      due.push({ n, w, overdue, starred: c.starred });
    }
  }
  // Sort: starred words first, then most overdue
  due.sort((a, b) => {
    if (a.starred !== b.starred) return a.starred ? -1 : 1;
    return b.overdue - a.overdue;
  });
  return due.slice(0, size);
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

function renderReviewQ(state) {
  if (state.idx >= state.qs.length) return finishReview(state);
  const q = state.qs[state.idx];
  const w = q.w;
  const pct = Math.round((state.idx / state.qs.length) * 100);

  const promptHtml = q.dir === 'en2zh'
    ? `<div class="prompt-label">What does this mean?</div>
       <div class="prompt">${escHtml(w.word)}</div>
       <div class="ipa">${escHtml(w.ipa || '')}</div>`
    : `<div class="prompt-label">Which English word?</div>
       <div class="prompt">${escHtml(w.def_zh)}</div>`;

  const optsHtml = q.opts.map((o, i) => {
    const text = q.dir === 'en2zh' ? o.def_zh : o.word;
    const isCorrect = o.word === w.word;
    return `<button data-i="${i}" data-correct="${isCorrect ? '1' : '0'}">${escHtml(text)}</button>`;
  }).join('');

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
  $('#reveal').innerHTML = `
    <div class="reveal-head">
      <div class="word">${escHtml(q.w.word)}</div>
      <button class="star-btn ${card.starred ? 'on' : ''}" id="revealStar" type="button" aria-label="Star">${card.starred ? '★' : '☆'}</button>
    </div>
    <div>${escHtml(q.w.def_zh)}</div>
    <div style="color:var(--muted);font-size:13px;margin-top:4px">${escHtml(q.w.def_en)}</div>
  `;
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
  setHeader('Review · Results');
  const wrong = state.answers.filter(a => !a.correct);
  const html = [];
  html.push(`<div class="results">
    <div class="score">${pct}%</div>
    <div class="breakdown">${correct} of ${total} correct · ${state.activeLists.length} lists in pool</div>
    <div class="actions">
      <a class="btn-primary" href="#/review">Another round</a>
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
