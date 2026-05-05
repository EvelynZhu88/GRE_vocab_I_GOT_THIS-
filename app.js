/* GRE Vocab — single-page app
 * Storage:
 *   localStorage['gre.progress'] -> { [key]: { ef, interval, reps, due, lapses, last } }
 *     key = `${listNum}::${word.toLowerCase()}`
 *   localStorage['gre.settings'] -> { currentList, sessionSize, mixRatio, direction }
 *
 * SRS: SM-2 (Anki-flavored 4-button: Again/Hard/Good/Easy mapping to q=0/3/4/5)
 */

const DAY = 86400000;
const STORE_KEY = 'gre.progress';
const SETTINGS_KEY = 'gre.settings';
const DEFAULT_SETTINGS = {
  currentList: 1,
  sessionSize: 20,
  mixRatio: 0.3,        // fraction of session pulled from earlier lists' due pile
  direction: 'en2zh',   // 'en2zh' shows English, asks for Chinese (default for native CN speaker)
};

let VOCAB = null;
let PASSAGES = null;
let SETTINGS = loadSettings();
let PROGRESS = loadProgress();
let CURRENT_QUIZ = null;
let CURRENT_PASSAGE = null;

const $ = (sel, root = document) => root.querySelector(sel);
const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));

// --- bootstrap ---
async function init() {
  try {
    [VOCAB, PASSAGES] = await Promise.all([
      fetch('vocab.json').then(r => r.json()),
      fetch('passages.json').then(r => r.json()).catch(() => ({})),
    ]);
  } catch (e) {
    $('#view').innerHTML = `<div class="quiz-empty"><h2>Couldn't load vocab</h2><p>${e}</p></div>`;
    return;
  }
  buildListPicker();
  bindTabs();
  render();
}

function loadProgress() {
  try { return JSON.parse(localStorage.getItem(STORE_KEY)) || {}; }
  catch { return {}; }
}
function saveProgress() { localStorage.setItem(STORE_KEY, JSON.stringify(PROGRESS)); }

function loadSettings() {
  try {
    const s = JSON.parse(localStorage.getItem(SETTINGS_KEY)) || {};
    return Object.assign({}, DEFAULT_SETTINGS, s);
  } catch { return { ...DEFAULT_SETTINGS }; }
}
function saveSettings() { localStorage.setItem(SETTINGS_KEY, JSON.stringify(SETTINGS)); }

function key(listNum, word) {
  return `${listNum}::${word.toLowerCase()}`;
}
function getCard(listNum, word) {
  const k = key(listNum, word);
  if (!PROGRESS[k]) {
    PROGRESS[k] = { ef: 2.5, interval: 0, reps: 0, due: 0, lapses: 0, last: 0 };
  }
  return PROGRESS[k];
}
function isFresh(card) { return card.reps === 0; }
function isMature(card) { return card.interval >= 21; }
function isLearning(card) { return card.reps > 0 && card.interval < 21; }

// --- SM-2 update ---
function rateCard(listNum, word, q) {
  const card = getCard(listNum, word);
  if (q < 3) {
    card.reps = 0;
    card.interval = 1;
    card.lapses += 1;
  } else {
    if (card.reps === 0) card.interval = 1;
    else if (card.reps === 1) card.interval = 6;
    else card.interval = Math.round(card.interval * card.ef);
    card.reps += 1;
  }
  card.ef = Math.max(1.3, card.ef + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02)));
  card.last = Date.now();
  card.due = Date.now() + card.interval * DAY;
  saveProgress();
}

// --- list picker / tabs ---
function buildListPicker() {
  const sel = $('#listPicker');
  const lists = Object.keys(VOCAB).sort((a, b) => +a - +b);
  for (const n of lists) {
    const opt = document.createElement('option');
    opt.value = n;
    opt.textContent = `${n}  (${VOCAB[n].length})`;
    sel.appendChild(opt);
  }
  sel.value = String(SETTINGS.currentList);
  sel.addEventListener('change', () => {
    SETTINGS.currentList = +sel.value;
    saveSettings();
    render();
  });
}

function bindTabs() {
  $$('.tab').forEach(t => {
    t.addEventListener('click', () => {
      $$('.tab').forEach(x => x.classList.remove('active'));
      t.classList.add('active');
      render();
    });
  });
}

function activeMode() {
  return $('.tab.active')?.dataset.mode || 'browse';
}

// --- top-level render ---
function render() {
  const mode = activeMode();
  if (mode === 'browse') return renderBrowse();
  if (mode === 'quiz') return renderQuizStart();
  if (mode === 'read') return renderReadList();
  if (mode === 'stats') return renderStats();
}

// --- BROWSE ---
function renderBrowse() {
  const num = SETTINGS.currentList;
  const words = VOCAB[String(num)] || [];
  const summary = computeListSummary(num);
  const html = [];
  html.push(`<div class="browse-summary">
    <span><b>${words.length}</b> words</span>
    <span><b>${summary.fresh}</b> new</span>
    <span><b>${summary.learning}</b> learning</span>
    <span><b>${summary.mature}</b> mature</span>
    <span><b>${summary.due}</b> due now</span>
  </div>`);
  for (const w of words) {
    const card = getCard(num, w.word);
    const tag = tagFor(card);
    html.push(`<div class="word-card">
      <div class="head"><span class="word">${esc(w.word)}</span><span class="ipa">${esc(w.ipa)}</span></div>
      <div class="zh">${esc(w.def_zh)}</div>
      <div class="en">${esc(w.def_en)}</div>
      ${w.synonym ? `<div class="syn">≈ ${esc(w.synonym)}</div>` : ''}
      ${w.ex_en ? `<div class="ex">${esc(w.ex_en)}<div class="ex-zh">${esc(w.ex_zh)}</div></div>` : ''}
      <div class="stats">${tag}</div>
    </div>`);
  }
  $('#view').innerHTML = html.join('');
}

function tagFor(card) {
  const now = Date.now();
  if (isFresh(card)) return `<span class="tag fresh">new</span>`;
  if (isMature(card)) return `<span class="tag mature">mature · ${card.interval}d</span>`;
  if (isLearning(card)) return `<span class="tag learning">learning · ${card.interval}d</span>`;
  return `<span class="tag">${card.interval}d</span>`;
}

function computeListSummary(num) {
  const words = VOCAB[String(num)] || [];
  let fresh = 0, learning = 0, mature = 0, due = 0;
  const now = Date.now();
  for (const w of words) {
    const c = getCard(num, w.word);
    if (isFresh(c)) fresh++;
    else if (isMature(c)) mature++;
    else learning++;
    if (c.due <= now) due++;
  }
  return { fresh, learning, mature, due };
}

// --- QUIZ ---
function renderQuizStart() {
  const num = SETTINGS.currentList;
  const session = buildSession(num, SETTINGS.sessionSize);
  if (session.length === 0) {
    $('#view').innerHTML = `<div class="quiz-empty">
      <h2>All caught up!</h2>
      <p>No cards due in list ${num} right now. Try Browse or Read mode, or come back later.</p>
      <button class="btn-primary" id="forceNew">Study new words anyway</button>
    </div>`;
    $('#forceNew').addEventListener('click', () => startQuiz(buildSession(num, SETTINGS.sessionSize, true)));
    return;
  }
  startQuiz(session);
}

function buildSession(currentNum, size, forceNew = false) {
  const now = Date.now();
  const currentList = (VOCAB[String(currentNum)] || []).map(w => ({ list: currentNum, w }));
  const earlierLists = [];
  for (let i = 1; i < currentNum; i++) {
    for (const w of VOCAB[String(i)] || []) earlierLists.push({ list: i, w });
  }

  const isDue = ({ list, w }) => {
    const c = getCard(list, w.word);
    return c.due <= now;
  };
  const dueScore = ({ list, w }) => {
    const c = getCard(list, w.word);
    if (isFresh(c)) return 1;       // fresh = high priority
    return Math.max(0, (now - c.due) / DAY); // overdue days
  };

  let dueCurrent = currentList.filter(isDue);
  let dueOld = earlierLists.filter(isDue);
  if (forceNew && dueCurrent.length === 0) {
    dueCurrent = currentList.slice();
  }

  // Sort by overdue priority, fresh first
  dueCurrent.sort((a, b) => dueScore(b) - dueScore(a));
  dueOld.sort((a, b) => dueScore(b) - dueScore(a));

  const oldQuota = Math.min(Math.floor(size * SETTINGS.mixRatio), dueOld.length);
  const curQuota = Math.min(size - oldQuota, dueCurrent.length);
  const finalOldQuota = Math.min(size - curQuota, dueOld.length);

  const session = [...dueCurrent.slice(0, curQuota), ...dueOld.slice(0, finalOldQuota)];
  shuffle(session);
  return session;
}

function startQuiz(session) {
  CURRENT_QUIZ = {
    session,
    idx: 0,
    correct: 0,
    wrong: 0,
    answered: false,
  };
  renderQuizCard();
}

function renderQuizCard() {
  const q = CURRENT_QUIZ;
  if (!q || q.idx >= q.session.length) return finishQuiz();
  const { list, w } = q.session[q.idx];
  const card = getCard(list, w.word);
  const dir = SETTINGS.direction;

  // Build distractors
  const pool = pickDistractors(list, w, 3);
  const options = shuffle([w, ...pool]);

  const promptHtml = dir === 'en2zh'
    ? `<div class="prompt-label">What does it mean?</div>
       <div class="prompt">${esc(w.word)}</div>
       <div class="ipa">${esc(w.ipa || '')}</div>`
    : `<div class="prompt-label">Which English word?</div>
       <div class="prompt">${esc(w.def_zh)}</div>`;

  const optionHtml = options.map((o, i) => {
    const text = dir === 'en2zh' ? o.def_zh : o.word;
    return `<button data-i="${i}" data-correct="${o.word === w.word ? '1' : '0'}">${esc(text)}</button>`;
  }).join('');

  const listLabel = list === SETTINGS.currentList
    ? `list ${list}`
    : `<span style="color:var(--warn)">↺ list ${list}</span>`;

  const html = `
    <div class="quiz-stage">
      <div class="quiz-progress">
        <span class="pill">${q.idx + 1} / ${q.session.length}</span>
        <span class="pill">${listLabel}</span>
        <span class="pill">✓ ${q.correct} · ✗ ${q.wrong}</span>
      </div>
      <div class="quiz-card ${dir === 'zh2en' ? 'zh-prompt' : ''}">${promptHtml}</div>
      <div class="quiz-options">${optionHtml}</div>
      <div class="quiz-reveal" id="reveal" style="display:none"></div>
      <div class="quiz-grade" id="grade" style="display:none">
        <button data-grade="0">Again</button>
        <button data-grade="3">Hard</button>
        <button data-grade="4">Good</button>
        <button data-grade="5">Easy</button>
      </div>
    </div>`;
  $('#view').innerHTML = html;

  $$('.quiz-options button').forEach(btn => {
    btn.addEventListener('click', () => onQuizAnswer(btn, w, list));
  });
}

function pickDistractors(list, target, n) {
  // Prefer same list, fall back to nearby lists
  const pool = (VOCAB[String(list)] || []).filter(w => w.word !== target.word && w.def_zh);
  shuffle(pool);
  const chosen = pool.slice(0, n);
  if (chosen.length < n) {
    const all = Object.values(VOCAB).flat().filter(w => w.word !== target.word && w.def_zh);
    shuffle(all);
    for (const w of all) {
      if (chosen.length >= n) break;
      if (!chosen.includes(w)) chosen.push(w);
    }
  }
  return chosen;
}

function onQuizAnswer(btn, w, list) {
  const q = CURRENT_QUIZ;
  if (q.answered) return;
  q.answered = true;
  const correct = btn.dataset.correct === '1';
  q.lastCorrect = correct;
  if (correct) q.correct++; else q.wrong++;

  $$('.quiz-options button').forEach(b => {
    b.classList.add('disabled');
    if (b.dataset.correct === '1') b.classList.add('correct');
    else if (b === btn) b.classList.add('wrong');
  });

  // Reveal
  const reveal = $('#reveal');
  reveal.style.display = 'block';
  reveal.innerHTML = `
    <div><b>${esc(w.word)}</b> ${esc(w.ipa || '')}</div>
    <div>${esc(w.def_en)}</div>
    <div>${esc(w.def_zh)}</div>
    ${w.synonym ? `<div class="syn">≈ ${esc(w.synonym)}</div>` : ''}
    ${w.ex_en ? `<div class="ex">${esc(w.ex_en)}<div>${esc(w.ex_zh)}</div></div>` : ''}
  `;
  const grade = $('#grade');
  grade.style.display = 'grid';
  $$('#grade button').forEach(g => {
    g.addEventListener('click', () => {
      const quality = +g.dataset.grade;
      // If they got it wrong, force quality <= 2 even if they tap "Good"
      const final = !correct ? Math.min(quality, 2) : quality;
      rateCard(list, w.word, final);
      q.idx++;
      q.answered = false;
      renderQuizCard();
    });
  });
}

function finishQuiz() {
  const q = CURRENT_QUIZ;
  CURRENT_QUIZ = null;
  const total = q.correct + q.wrong;
  const pct = total ? Math.round((q.correct / total) * 100) : 0;
  $('#view').innerHTML = `
    <div class="quiz-empty">
      <h2>Session complete</h2>
      <p>${q.correct} correct out of ${total} (${pct}%)</p>
      <p style="margin-top:12px">
        <button class="btn-primary" id="again">Another session</button>
        <button class="btn-secondary" id="back">Browse list</button>
      </p>
    </div>`;
  $('#again').addEventListener('click', () => renderQuizStart());
  $('#back').addEventListener('click', () => {
    $$('.tab').forEach(x => x.classList.remove('active'));
    $('.tab[data-mode="browse"]').classList.add('active');
    render();
  });
}

// --- READ ---
function renderReadList() {
  const num = SETTINGS.currentList;
  const list = (PASSAGES && PASSAGES[String(num)]) || [];
  if (list.length === 0) {
    $('#view').innerHTML = `<div class="quiz-empty">
      <h2>No passages yet</h2>
      <p>Reading passages for list ${num} haven't been written yet.</p>
    </div>`;
    return;
  }
  CURRENT_PASSAGE = null;
  const html = ['<div class="passage-list">'];
  list.forEach((p, i) => {
    const targets = (p.targets || []).length;
    html.push(`<div class="passage-item" data-i="${i}">
      <h3>${i + 1}. ${esc(p.title)}</h3>
      <div class="meta">${targets} target words · ~${approxWordCount(p.text)} words</div>
    </div>`);
  });
  html.push('</div>');
  $('#view').innerHTML = html.join('');
  $$('.passage-item').forEach(el => {
    el.addEventListener('click', () => openPassage(+el.dataset.i));
  });
}

function approxWordCount(t) {
  return (t || '').split(/\s+/).filter(Boolean).length;
}

function openPassage(i) {
  const num = SETTINGS.currentList;
  const passage = (PASSAGES[String(num)] || [])[i];
  if (!passage) return;
  CURRENT_PASSAGE = passage;

  // Build target lookup, include earlier-list review words appearing in text
  const wordIndex = buildGlobalWordIndex();
  const targetSet = new Set((passage.targets || []).map(t => t.toLowerCase()));

  const rendered = highlightPassage(passage.text, wordIndex, targetSet, num);

  $('#view').innerHTML = `
    <div class="passage-reader">
      <h2>${esc(passage.title)}</h2>
      <div class="passage-text">${rendered}</div>
      <div class="passage-back">
        <button class="btn-secondary" id="backList">← All passages</button>
      </div>
    </div>
    <div id="popover" class="popover">
      <button class="pop-close">×</button>
      <div class="pop-word"></div>
      <div class="pop-zh"></div>
      <div class="pop-en"></div>
    </div>
  `;
  $('#backList').addEventListener('click', renderReadList);
  bindPassageInteractions();
}

function buildGlobalWordIndex() {
  // Map lowercase word -> { list, entry }
  const idx = new Map();
  for (const [list, words] of Object.entries(VOCAB)) {
    for (const w of words) {
      const k = w.word.toLowerCase();
      if (!idx.has(k)) idx.set(k, { list: +list, w });
    }
  }
  return idx;
}

function highlightPassage(text, wordIndex, targetSet, currentList) {
  // Tokenize on word boundaries; preserve original spacing/punct.
  // Use a regex that captures words including hyphens and apostrophes.
  const re = /([A-Za-z][A-Za-z'\-]*)/g;
  return text.replace(re, (match) => {
    const lower = match.toLowerCase();
    // Check exact match or simple stem match (strip trailing s/ed/ing/ly/'s/es)
    const candidates = [lower, ...stemVariants(lower)];
    let hit = null;
    for (const c of candidates) {
      if (wordIndex.has(c)) { hit = wordIndex.get(c); break; }
    }
    if (!hit) return match;
    const isTarget = targetSet.has(hit.w.word.toLowerCase());
    const isReview = !isTarget && hit.list !== currentList;
    if (!isTarget && !isReview) return match;
    const cls = isReview ? 'target review' : 'target';
    const key = hit.w.word;
    return `<mark class="${cls}" data-key="${esc(key)}">${match}</mark>`;
  });
}

function stemVariants(word) {
  const v = [];
  // Strip common suffixes
  const suf = [/'s$/, /s$/, /es$/, /ed$/, /d$/, /ing$/, /ly$/, /ies$/, /ied$/];
  for (const s of suf) {
    if (s.test(word)) v.push(word.replace(s, ''));
  }
  // Try doubling consonant removal: "running" -> "runn" -> "run"
  if (/[a-z]ing$/.test(word)) v.push(word.replace(/ing$/, ''));
  // -ies -> -y
  if (/ies$/.test(word)) v.push(word.replace(/ies$/, 'y'));
  // -ied -> -y
  if (/ied$/.test(word)) v.push(word.replace(/ied$/, 'y'));
  return v;
}

function bindPassageInteractions() {
  const idx = buildGlobalWordIndex();
  const pop = $('#popover');
  $$('mark.target').forEach(m => {
    m.addEventListener('click', (e) => {
      e.stopPropagation();
      const k = m.dataset.key.toLowerCase();
      const info = idx.get(k);
      if (!info) return;
      pop.querySelector('.pop-word').textContent = `${info.w.word}  ${info.w.ipa || ''}`;
      pop.querySelector('.pop-zh').textContent = info.w.def_zh || '';
      pop.querySelector('.pop-en').textContent = info.w.def_en || '';
      const r = m.getBoundingClientRect();
      const top = Math.min(window.innerHeight - 160, r.bottom + 8);
      const left = Math.max(8, Math.min(window.innerWidth - 290, r.left));
      pop.style.top = top + 'px';
      pop.style.left = left + 'px';
      pop.classList.add('show');
    });
  });
  pop.querySelector('.pop-close').addEventListener('click', () => pop.classList.remove('show'));
  document.addEventListener('click', (e) => {
    if (!pop.contains(e.target) && !e.target.matches('mark.target')) pop.classList.remove('show');
  });
}

// --- STATS ---
function renderStats() {
  const lists = Object.keys(VOCAB).sort((a, b) => +a - +b);
  let fresh = 0, learning = 0, mature = 0, due = 0, total = 0;
  const now = Date.now();
  const perList = lists.map(n => {
    const s = computeListSummary(+n);
    fresh += s.fresh; learning += s.learning; mature += s.mature; due += s.due;
    total += VOCAB[n].length;
    return { n, ...s };
  });
  const html = [];
  html.push(`<div class="stats-grid">
    <div class="stat-card"><div class="label">Mature</div><div class="value">${mature}</div></div>
    <div class="stat-card"><div class="label">Learning</div><div class="value">${learning}</div></div>
    <div class="stat-card"><div class="label">New</div><div class="value">${fresh}</div></div>
    <div class="stat-card"><div class="label">Due now</div><div class="value">${due}</div></div>
  </div>`);
  html.push(`<div class="stats-list">`);
  for (const r of perList) {
    html.push(`<div class="row"><span>List ${r.n}</span><span class="num">m ${r.mature} · l ${r.learning} · n ${r.fresh}  ·  due ${r.due}</span></div>`);
  }
  html.push('</div>');
  html.push(`<div style="margin-top:18px">
    <button class="btn-secondary" id="resetBtn">Reset all progress</button>
  </div>`);
  $('#view').innerHTML = html.join('');
  $('#resetBtn').addEventListener('click', () => {
    if (confirm('This will erase all your study progress. Continue?')) {
      PROGRESS = {};
      saveProgress();
      toast('Progress reset.');
      render();
    }
  });
}

// --- helpers ---
function shuffle(arr) {
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}
function esc(s) {
  return String(s ?? '').replace(/[&<>"']/g, c =>
    ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}
let toastT;
function toast(msg) {
  const t = $('#toast');
  t.textContent = msg;
  t.classList.add('show');
  clearTimeout(toastT);
  toastT = setTimeout(() => t.classList.remove('show'), 1800);
}

init();
