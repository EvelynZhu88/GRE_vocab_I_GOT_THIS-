"""Parse BB六选二词表（表格速记版）.pdf into vocab_bb62.json.

Each content row is a 4-column pair of equivalent English words:
  x≈44  : word A (English)
  x≈173 : Chinese meaning of A
  x≈302 : word B (English, equivalent to A)
  x≈431 : Chinese meaning of B

Both A and B are legitimate GRE prompts (the exam might show either),
so we emit two vocab entries per row — one keyed on A with B as its
synonym, one keyed on B with A as its synonym. The union-find in
buildEquivIndex on the client side then merges them into a single
equivalence class.

Content starts on page 4; pages 1-3 are cover/instructions.
"""
import fitz, re, json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

PDF = 'BB六选二词表（表格速记版）.pdf'
OUT = 'vocab_bb62.json'
CONTENT_START_PAGE = 3  # 0-indexed, so page 4

COLS = [
    (30, 165, 'wordA'),
    (165, 290, 'zhA'),
    (290, 420, 'wordB'),
    (420, 700, 'zhB'),
]

WORD_RE = re.compile(r"^[A-Za-z][A-Za-z'\-\s]*[A-Za-z\.]$|^[A-Za-z]$")


def col_of(x):
    for x0, x1, name in COLS:
        if x0 <= x < x1:
            return name
    return None


def clean_zh(s):
    s = re.sub(r'\s+', '', s)
    return s.strip()


def clean_word(s):
    return re.sub(r'\s+', ' ', s).strip()


def parse():
    doc = fitz.open(PDF)
    rows = []

    for pgn in range(CONTENT_START_PAGE, doc.page_count):
        page = doc[pgn]
        spans = []
        for block in page.get_text('dict')['blocks']:
            if 'lines' not in block:
                continue
            for line in block['lines']:
                for span in line['spans']:
                    t = span['text']
                    if not t.strip():
                        continue
                    sz = span.get('size', 0)
                    if sz < 8 or sz > 12:
                        continue
                    x0, y0, _, _ = span['bbox']
                    spans.append((y0, x0, t))
        spans.sort()

        # Group into y-lines (tolerance ~5)
        y_lines = []
        for y, x, t in spans:
            if y_lines and abs(y - y_lines[-1][0]) < 5:
                y_lines[-1][1].append((x, t))
            else:
                y_lines.append([y, [(x, t)]])

        # Two consecutive y-lines can belong to the same row when the Chinese
        # def wraps. Roll continuation lines into the previous row when they
        # have no word (nothing at wordA column).
        current = None
        for y, items in y_lines:
            items.sort()
            buckets = {n: [] for _, _, n in COLS}
            for x, t in items:
                c = col_of(x)
                if c:
                    buckets[c].append(t)
            has_wordA = bool(buckets['wordA'])
            has_wordB = bool(buckets['wordB'])
            if has_wordA or has_wordB:
                if current:
                    rows.append(current)
                current = {n: [] for _, _, n in COLS}
            if current is None:
                continue
            for k in current:
                current[k].extend(buckets[k])
        if current:
            rows.append(current)

    entries = []
    seen = set()
    for r in rows:
        wA = clean_word(''.join(r['wordA']))
        wB = clean_word(''.join(r['wordB']))
        zhA = clean_zh(''.join(r['zhA']))
        zhB = clean_zh(''.join(r['zhB']))
        for w, zh, other in ((wA, zhA, wB), (wB, zhB, wA)):
            if not w or not WORD_RE.match(w):
                continue
            wl = w.lower()
            if wl in seen:
                continue
            seen.add(wl)
            entries.append({
                'word': w,
                'ipa': '',
                'def_en': '',
                'def_zh': zh,
                'synonym': other,
                'ex_en': '',
                'ex_zh': '',
            })

    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump({"1": entries}, f, ensure_ascii=False, indent=2)
    print(f'Wrote {len(entries)} entries from {len(rows)} rows to {OUT}', file=sys.stderr)


if __name__ == '__main__':
    parse()
