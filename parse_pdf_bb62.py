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

Content starts on page 4 (content page 1); pages 1-3 are cover /
instructions. The 36 content pages are grouped into 9 lists of 4
consecutive pages each, so each list becomes a manageable ~170-word
unit test.
"""
import fitz, re, json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

PDF = 'BB六选二词表（表格速记版）.pdf'
OUT = 'vocab_bb62.json'
CONTENT_START_PAGE = 3       # 0-indexed, so PDF page 4 = content page 1
PAGES_PER_LIST = 4           # 4 content pages per list → 9 lists total

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


def clean_zh(s):  return re.sub(r'\s+', '', s).strip()
def clean_word(s): return re.sub(r'\s+', ' ', s).strip()


def rows_on_page(doc, pgn):
    """Return the ordered list of row dicts extracted from a single PDF page."""
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

    # A row is opened by a y-line that has a word in the wordA or wordB
    # column; subsequent y-lines with no word are Chinese-def wraps and get
    # rolled into the previous row.
    rows = []
    current = None
    for y, items in y_lines:
        items.sort()
        buckets = {n: [] for _, _, n in COLS}
        for x, t in items:
            c = col_of(x)
            if c:
                buckets[c].append(t)
        if buckets['wordA'] or buckets['wordB']:
            if current:
                rows.append(current)
            current = {n: [] for _, _, n in COLS}
        if current is None:
            continue
        for k in current:
            current[k].extend(buckets[k])
    if current:
        rows.append(current)
    return rows


def parse():
    doc = fitz.open(PDF)
    total_pages = doc.page_count
    # PDF pages that carry content (skip the 3 cover pages)
    content_pdf_pages = list(range(CONTENT_START_PAGE, total_pages))

    lists = {}
    seen_global = set()
    for list_idx, start in enumerate(range(0, len(content_pdf_pages), PAGES_PER_LIST)):
        list_num = list_idx + 1
        chunk = content_pdf_pages[start:start + PAGES_PER_LIST]
        entries = []
        local_seen = set()
        rows_in_list = 0
        for pgn in chunk:
            for r in rows_on_page(doc, pgn):
                rows_in_list += 1
                wA = clean_word(''.join(r['wordA']))
                wB = clean_word(''.join(r['wordB']))
                zhA = clean_zh(''.join(r['zhA']))
                zhB = clean_zh(''.join(r['zhB']))
                for w, zh, other in ((wA, zhA, wB), (wB, zhB, wA)):
                    if not w or not WORD_RE.match(w):
                        continue
                    wl = w.lower()
                    # Dedup within the list; but let the same word appear in
                    # a later list too, because a subsequent pair might use
                    # it against a new equivalent.
                    if wl in local_seen:
                        continue
                    local_seen.add(wl)
                    seen_global.add(wl)
                    entries.append({
                        'word': w, 'ipa': '', 'def_en': '', 'def_zh': zh,
                        'synonym': other, 'ex_en': '', 'ex_zh': '',
                    })
        lists[str(list_num)] = entries
        pdf_range = f'PDF pp. {chunk[0]+1}-{chunk[-1]+1}'
        content_range = f'content pp. {chunk[0]-CONTENT_START_PAGE+1}-{chunk[-1]-CONTENT_START_PAGE+1}'
        print(f'  list {list_num}: {len(entries)} entries ({rows_in_list} rows, {content_range}, {pdf_range})', file=sys.stderr)

    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(lists, f, ensure_ascii=False, indent=2)
    total = sum(len(v) for v in lists.values())
    print(f'Wrote {total} entries across {len(lists)} lists to {OUT}', file=sys.stderr)


if __name__ == '__main__':
    parse()
