"""Parse 真经GRE等价词汇总（2026年版）.pdf into vocab_equiv.json.

Layout: 3 columns per row.
  x≈100 : word
  x≈220 : equivalent (synonym) word(s)
  x≈420 : Chinese meaning (sometimes with numbered senses like '1.xxx 2.yyy')

Section markers: '第N天' (Day N) appears at the top of each section. The
book divides into 5 days; we use them as our 5 lists. Day 1/2 markers are
implicit (the first two sections); we infer their page ranges by spacing
the 3rd/4th/5th markers backwards.
"""
import fitz, re, json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

PDF = '真经GRE等价词汇总（2026年版 ）.pdf'
OUT = 'vocab_equiv.json'

COLS = [
    (60, 200, 'word'),
    (200, 380, 'syn'),
    (380, 700, 'zh'),
]

WORD_RE = re.compile(r"^[A-Za-z][A-Za-z'\-\s]*[A-Za-z]$|^[A-Za-z]$")


def col_of(x):
    for x0, x1, name in COLS:
        if x0 <= x < x1:
            return name
    return None


def find_day_starts(doc):
    """Return {day_n: pdf_page_index} for the explicit and implicit days."""
    day_re = re.compile(r'第([一二三四五六七八九十])天')
    cn_to_n = {'一':1,'二':2,'三':3,'四':4,'五':5,'六':6,'七':7,'八':8,'九':9,'十':10}
    found = {}
    for pgn in range(doc.page_count):
        t = doc[pgn].get_text()
        m = day_re.search(t)
        if m:
            found[cn_to_n[m.group(1)]] = pgn
    # Infer days 1 & 2 by even spacing — distance between known days
    if 3 in found and 4 in found:
        delta = found[4] - found[3]
        if 2 not in found:
            found[2] = found[3] - delta
        if 1 not in found:
            found[1] = found[2] - delta
    return found


def parse():
    doc = fitz.open(PDF)
    day_starts = find_day_starts(doc)
    day_nums = sorted(day_starts.keys())
    print('day starts:', day_starts, file=sys.stderr)

    lists = {}
    seen_global = set()

    for idx, day in enumerate(day_nums):
        start = day_starts[day]
        end = day_starts[day_nums[idx+1]] if idx+1 < len(day_nums) else doc.page_count
        entries = []
        local_seen = set()
        for pgn in range(start, end):
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
                        if sz < 9 or sz > 13:
                            continue
                        x0, y0, _, _ = span['bbox']
                        spans.append((y0, x0, txt))
            spans.sort()

            # Group into rows by y proximity
            rows = []
            for y, x, t in spans:
                if rows and abs(y - rows[-1][0]) < 5:
                    rows[-1][1].append((x, t))
                else:
                    rows.append([y, [(x, t)]])

            current = None
            for y, items in rows:
                items.sort()
                buckets = {n: [] for _, _, n in COLS}
                for x, t in items:
                    c = col_of(x)
                    if c:
                        buckets[c].append(t)

                if buckets['word']:
                    if current:
                        entries.append(current)
                    current = {
                        'word': buckets['word'][0].strip(),
                        'syn': [],
                        'zh': [],
                    }
                if current is None:
                    continue
                for k in ('syn', 'zh'):
                    for t in buckets[k]:
                        s = t.strip()
                        if s:
                            current[k].append(s)
            if current:
                entries.append(current)

        out = []
        for e in entries:
            w = e['word']
            if not WORD_RE.match(w):
                continue
            wl = w.lower()
            if wl in local_seen or wl in seen_global:
                continue
            local_seen.add(wl); seen_global.add(wl)
            syn = ' '.join(e['syn']).strip()
            syn = re.sub(r'\s+', ' ', syn)
            zh = ''.join(e['zh']).strip()
            zh = re.sub(r'\s+', '', zh)
            if not (syn or zh):
                continue
            out.append({
                'word': w,
                'ipa': '',
                'def_en': '',
                'def_zh': zh,
                'synonym': syn,
                'ex_en': '',
                'ex_zh': '',
            })
        lists[str(day)] = out
        print(f'  day {day}: {len(out)} entries (pages {start+1}-{end})', file=sys.stderr)

    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(lists, f, ensure_ascii=False, indent=2)
    total = sum(len(v) for v in lists.values())
    print(f'Wrote {total} entries across {len(lists)} lists to {OUT}', file=sys.stderr)


if __name__ == '__main__':
    parse()
