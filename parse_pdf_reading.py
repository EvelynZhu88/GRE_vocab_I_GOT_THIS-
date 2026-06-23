"""Parse GRE阅读机经核心词汇.pdf into vocab_reading.json (single list).

Each row is a 5-column entry:
  x≈55  : word
  x≈153 : Chinese meaning (broad, with POS markers like n./adj./v.)
  x≈363 : Chinese meaning narrowed to the GRE-passage context
  x≈494 : English equivalent (synonym used as the GRE answer)
  x≈603 : passage reference like "129-2"

We map this onto our existing word schema by joining the two Chinese defs
into def_zh and keeping the x≈494 English equivalent as synonym.
"""
import fitz, re, json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

PDF = 'GRE阅读机经核心词汇.pdf'
OUT = 'vocab_reading.json'

# x-column bounds (lower, upper, name)
COLS = [
    (30, 100, 'word'),
    (140, 350, 'zh_main'),
    (350, 490, 'zh_gre'),
    (490, 600, 'syn_en'),
    (600, 700, 'ref'),
]

POS_RE = re.compile(r'^(adj|adv|vt|vi|v|n|prep|conj|pron|int)\.?\s*$', re.I)
WORD_RE = re.compile(r"^[A-Za-z][A-Za-z'\-\s]*[A-Za-z]$|^[A-Za-z]$")


def col_of(x):
    for x0, x1, name in COLS:
        if x0 <= x < x1:
            return name
    return None


def parse():
    doc = fitz.open(PDF)
    entries = []
    seen = set()

    for pgn in range(doc.page_count):
        page = doc[pgn]
        spans = []
        for block in page.get_text('dict')['blocks']:
            if 'lines' not in block:
                continue
            for line in block['lines']:
                for span in line['spans']:
                    txt = span['text']
                    if not txt.strip():
                        continue
                    sz = span.get('size', 0)
                    if sz > 14 or sz < 8:
                        continue
                    x0, y0, _, _ = span['bbox']
                    spans.append((y0, x0, txt))
        spans.sort()

        # Group into rows by y proximity (~6px)
        rows = []
        for y, x, t in spans:
            if rows and abs(y - rows[-1][0]) < 6:
                rows[-1][1].append((x, t))
            else:
                rows.append([y, [(x, t)]])

        current = None
        for y, items in rows:
            items.sort()
            buckets = {name: [] for _, _, name in COLS}
            for x, t in items:
                c = col_of(x)
                if c:
                    buckets[c].append(t)

            has_word = bool(buckets['word'])
            if has_word:
                if current:
                    entries.append(current)
                current = {
                    'word': buckets['word'][0].strip(),
                    'zh_main': [],
                    'zh_gre': [],
                    'syn_en': [],
                }
            if current is None:
                continue
            for k in ('zh_main', 'zh_gre', 'syn_en'):
                for t in buckets[k]:
                    s = t.strip()
                    if s:
                        current[k].append(s)

        if current:
            entries.append(current)
            current = None

    out = []
    for e in entries:
        w = e['word']
        if not WORD_RE.match(w):
            continue
        wl = w.lower()
        if wl in seen:
            continue
        seen.add(wl)
        zh_main = ''.join(e['zh_main']).strip()
        zh_main = re.sub(r'\s+', ' ', zh_main)
        zh_gre  = ''.join(e['zh_gre']).strip()
        zh_gre  = re.sub(r'\s+', ' ', zh_gre)
        syn_en  = ' '.join(e['syn_en']).strip()
        syn_en  = re.sub(r'\s+', ' ', syn_en)

        # Compose def_zh: main meaning · GRE context (if different)
        if zh_gre and zh_gre != zh_main:
            zh = f'{zh_main} · GRE语境：{zh_gre}' if zh_main else zh_gre
        else:
            zh = zh_main
        if not zh:
            continue
        out.append({
            'word': w,
            'ipa': '',
            'def_en': '',
            'def_zh': zh,
            'synonym': syn_en,
            'ex_en': '',
            'ex_zh': '',
        })

    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump({"1": out}, f, ensure_ascii=False, indent=2)
    print(f'Wrote {len(out)} words to {OUT}')


if __name__ == '__main__':
    parse()
