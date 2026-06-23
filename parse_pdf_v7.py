"""Parse GRE镇考机经词7.0-乱序（2026年版）.pdf into vocab_v7.json.

Each row in this PDF is bounded by a horizontal separator line (drawn as a
very thin filled rectangle spanning the full table width). Within each
band:
  Top sub-row (vocab):   word | IPA | English-def + Chinese-def | synonym
  Bottom sub-row (例句): example sentence (English only)

We split a band by the vertical midpoint to separate the two sub-rows.
DAY N markers in page text divide the book into 7 lists.
"""
import fitz, re, json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

PDF = 'GRE镇考机经词7.0-乱序（2026年版）.pdf'
OUT = 'vocab_v7.json'

COLS = [
    (10, 80,   'word'),
    (80, 180,  'ipa'),
    (180, 440, 'def'),
    (440, 700, 'syn'),
]

DAY_RE  = re.compile(r'DAY\s*(\d+)', re.I)
WORD_RE = re.compile(r"^[A-Za-z][A-Za-z'\-\s]*[A-Za-z]$|^[A-Za-z]$")
CJK_PUNCT = '，。、；：！？「」（）《》〈〉【】“”‘’……—'


def is_cjk(c):
    return ('一' <= c <= '鿿') or c in CJK_PUNCT


def split_en_zh(text):
    if not text:
        return '', ''
    en_parts, zh_parts, buf, mode = [], [], '', None
    for c in text:
        cur = 'zh' if is_cjk(c) else 'en'
        if mode is None:
            mode, buf = cur, c
        elif cur == mode:
            buf += c
        else:
            (zh_parts if mode == 'zh' else en_parts).append(buf)
            mode, buf = cur, c
    if buf:
        (zh_parts if mode == 'zh' else en_parts).append(buf)
    en = re.sub(r' +', ' ', ' '.join(p.strip() for p in en_parts).strip())
    zh = '；'.join(p.strip() for p in zh_parts if p.strip())
    return en, zh


def col_of(x):
    for x0, x1, name in COLS:
        if x0 <= x < x1:
            return name
    return None


def find_day_starts(doc):
    starts = {}
    for pgn in range(doc.page_count):
        for line in doc[pgn].get_text().splitlines()[:5]:
            m = DAY_RE.search(line)
            if m:
                n = int(m.group(1))
                if n not in starts:
                    starts[n] = pgn
                break
    return starts


def row_cuts(page):
    """Return sorted y-positions of horizontal separator lines on this page."""
    cuts = set()
    for d in page.get_drawings():
        r = d.get('rect')
        if not r:
            continue
        # Thin horizontal line spanning ~full table width
        if r.height < 2 and r.width > 400 and r.x0 < 30:
            cuts.add(round((r.y0 + r.y1) / 2, 1))
    cuts.add(page.rect.height)
    return sorted(cuts)


def page_spans(page):
    out = []
    for block in page.get_text('dict')['blocks']:
        if 'lines' not in block:
            continue
        for line in block['lines']:
            for span in line['spans']:
                t = span['text']
                if not t.strip():
                    continue
                sz = span.get('size', 0)
                if sz < 8 or sz > 13:
                    continue
                x0, y0, _, y1 = span['bbox']
                out.append((y0, x0, t, y1))
    return out


def merge_spans(items):
    """Join spans into a single string ordered by (y, x)."""
    items = sorted(items, key=lambda p: (round(p[0], 0), p[1]))
    return ''.join(t for _, _, t, _ in items)


def parse():
    doc = fitz.open(PDF)
    days = find_day_starts(doc)
    day_nums = sorted(days.keys())
    print(f'days: {days}', file=sys.stderr)

    lists = {}
    seen_global = set()

    for i, day in enumerate(day_nums):
        start = days[day]
        end = days[day_nums[i+1]] if i+1 < len(day_nums) else doc.page_count
        entries = []
        local_seen = set()

        for pgn in range(start, end):
            page = doc[pgn]
            cuts = row_cuts(page)
            if len(cuts) < 2:
                continue
            spans = page_spans(page)

            for k in range(len(cuts) - 1):
                y_top = cuts[k]
                y_bot = cuts[k+1]
                if y_bot - y_top < 20 or y_top < 30:
                    continue
                band = [(y, x, t, y1) for (y, x, t, y1) in spans if y_top <= y < y_bot]
                if not band:
                    continue
                mid = (y_top + y_bot) / 2
                vocab_spans = [(y, x, t, y1) for (y, x, t, y1) in band if y < mid + 2]
                ex_spans    = [(y, x, t, y1) for (y, x, t, y1) in band if y >= mid + 2]

                buckets = {n: [] for _, _, n in COLS}
                for y, x, t, y1 in vocab_spans:
                    c = col_of(x)
                    if c:
                        buckets[c].append((y, x, t, y1))

                word = merge_spans(buckets['word']).strip()
                if not word or word == '例句' or not WORD_RE.match(word):
                    continue
                wl = word.lower()
                if wl in local_seen or wl in seen_global:
                    continue
                local_seen.add(wl); seen_global.add(wl)
                ipa = merge_spans(buckets['ipa']).strip()
                def_full = merge_spans(buckets['def']).strip()
                def_full = re.sub(r'\s+', ' ', def_full)
                en_def, zh_def = split_en_zh(def_full)
                syn = merge_spans(buckets['syn']).strip()
                syn = re.sub(r'\s+', ' ', syn)

                ex = ''
                if ex_spans:
                    # Drop the leading '例句' marker, keep everything to its right
                    parts = [(y, x, t) for y, x, t, _ in ex_spans if x >= 50]
                    ex = re.sub(r'\s+', ' ', ''.join(t for _, _, t in sorted(parts, key=lambda p: (round(p[0]), p[1])))).strip()

                entries.append({
                    'word': word,
                    'ipa':  ipa,
                    'def_en': en_def,
                    'def_zh': zh_def,
                    'synonym': syn,
                    'ex_en':  ex,
                    'ex_zh':  '',
                })

        lists[str(day)] = entries
        print(f'  day {day}: {len(entries)} entries (pages {start+1}-{end})', file=sys.stderr)

    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(lists, f, ensure_ascii=False, indent=2)
    total = sum(len(v) for v in lists.values())
    print(f'Wrote {total} entries across {len(lists)} lists to {OUT}', file=sys.stderr)


if __name__ == '__main__':
    parse()
