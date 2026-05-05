"""Parse the GRE PDF into structured vocab.json.

Each PDF page is a 5-column table with alternating row fills. The narrow
filled rectangles in the leftmost (word) column mark every other row, so
their y0/y1 values, combined with the header bottom and page bottom, give
us the y-cuts that bound every row.

Columns (by x):
  word     :  17 -  93
  IPA      :  93 - 169
  def      : 169 - 312  (English meaning + Chinese gloss)
  synonym  : 312 - 377
  example  : 377 - 572  (English sentence + Chinese gloss)
"""
import fitz
import glob
import json
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

PDF_PATH = glob.glob('*.pdf')[0]
OUT_PATH = 'vocab.json'

COL_BOUNDS = [(17, 93, 'word'),
              (93, 169, 'ipa'),
              (169, 312, 'definition'),
              (312, 377, 'synonym'),
              (377, 700, 'example')]

JUNK_PATTERNS = [
    r'微信公众号', r'张巍老师',
    r'镇考', r'乱序版', r'^3000$', r'^词乱序版$',
    r'^list\s*\d+\s*$',
    r'^单词$', r'^音标$', r'^释义$', r'^等价词$', r'^例句$',
    r'don.t be',
    r'^第\s*\d+\s*页', r'^共\s*\d+\s*页', r'第.*页.*共.*页',
    r'^一$',  # stray horizontal-stroke artifacts in some PDF renderings
]
JUNK_RE = re.compile('|'.join(JUNK_PATTERNS), re.IGNORECASE)


def clean_headword(text):
    """Reduce a word/synonym cell to its longest letter-run.

    The word and synonym columns sometimes pick up arrow-like glyphs or
    section markers from category headers in the PDF. We keep the longest
    contiguous run of [A-Za-z'-] which is always the actual headword.
    """
    if not text:
        return ''
    # Split on anything that isn't a letter, hyphen, or apostrophe
    candidates = re.split(r"[^A-Za-z'\-]+", text)
    candidates = [c.strip("-'") for c in candidates if c.strip("-'")]
    if not candidates:
        return ''
    # Heuristic: pick the longest candidate that contains at least one vowel
    candidates.sort(key=len, reverse=True)
    for c in candidates:
        if re.search(r'[aeiouyAEIOUY]', c):
            return c
    return candidates[0]


def is_word_junk(text):
    """Filter out spans that should never appear inside the word column."""
    s = text.strip()
    if not s:
        return True
    # Pure-digit sense markers like "1", "2"
    if re.fullmatch(r'\d{1,2}', s):
        return True
    # Single CJK glyphs / dingbats that drift into the word column
    if re.fullmatch(r'[　-〿一-鿿 -⁯○●·•※川一二三四五六七八九十]+', s):
        return True
    return is_junk(s)


def col_of(x):
    for x0, x1, name in COL_BOUNDS:
        if x0 <= x < x1:
            return name
    return None


def is_junk(text):
    s = text.strip()
    if not s:
        return True
    if JUNK_RE.search(s):
        return True
    return False


def get_row_cuts(page):
    """Return sorted y-cut points that bound every data row on this page.

    Uses the narrow filled rects in the word column (x ≈ 17, width ≈ 76)
    to find every other row's top/bottom edges.
    """
    page_h = page.rect.height
    cuts = set()
    for d in page.get_drawings():
        r = d.get('rect')
        if not r or not d.get('fill'):
            continue
        if 15 < r.x0 < 25 and 30 < r.width < 100 and r.height > 18:
            cuts.add(round(r.y0, 1))
            cuts.add(round(r.y1, 1))
    cuts.add(round(page_h, 1))
    return sorted(cuts)


CJK_RE = re.compile(r'[一-鿿，。、；：！？「」（）《》〈〉【】“”‘’……—]')


def is_cjk_char(c):
    return bool(c) and bool(CJK_RE.match(c))


def smart_join_lines(line_strings):
    """Join visual lines, omitting spaces between two CJK chars."""
    out = ''
    for piece in line_strings:
        piece = piece.replace('\xa0', ' ').strip()
        if not piece:
            continue
        if not out:
            out = piece
            continue
        last = out[-1]
        first = piece[0]
        if is_cjk_char(last) and is_cjk_char(first):
            out += piece
        elif is_cjk_char(last) or is_cjk_char(first):
            # English-Chinese boundary: keep a single space for readability
            out += ' ' + piece
        else:
            out += ' ' + piece
    return out


def merge_spans_by_line(spans, line_tol=4.0, no_space=False):
    """Group spans by approximate y-line, then concatenate left-to-right.

    Without this, sorting purely by y interleaves Chinese (placed at higher x
    on the same visual line) before English wrapped to the next line.

    If `no_space=True`, all line pieces are concatenated with no separator
    (used for word/synonym columns where mid-word line wraps must rejoin).
    """
    if not spans:
        return ''
    spans = sorted(spans, key=lambda p: (p[0], p[1]))
    lines = []
    for y, x, t in spans:
        if lines and abs(y - lines[-1][0]) <= line_tol:
            lines[-1][1].append((x, t))
            lines[-1] = (
                (lines[-1][0] * (len(lines[-1][1]) - 1) + y) / len(lines[-1][1]),
                lines[-1][1],
            )
        else:
            lines.append((y, [(x, t)]))
    line_strings = []
    for _, items in lines:
        items.sort(key=lambda p: p[0])
        line_strings.append(''.join(t for _, t in items))
    if no_space:
        s = ''.join(line_strings).replace('\xa0', '').strip()
        s = re.sub(r'\s+', '', s)
    else:
        s = smart_join_lines(line_strings)
        s = re.sub(r' +', ' ', s).strip()
    return s


CJK_PUNCT = '，。、；：！？「」（）《》〈〉【】“”‘’……—'


def is_cjk(c):
    return ('一' <= c <= '鿿') or c in CJK_PUNCT


def split_en_zh(text):
    """Split into (english, chinese) by character class.

    Handles multi-sense entries like:
      '(1)adj. not usual 不寻常的 (2)adj. much better than average 杰出的'
    by collecting all English runs and all Chinese runs separately.
    """
    if not text:
        return '', ''
    en_parts, zh_parts, buf, mode = [], [], '', None
    for c in text:
        cur = 'zh' if is_cjk(c) else 'en'
        if mode is None:
            mode = cur
            buf = c
        elif cur == mode:
            buf += c
        else:
            (zh_parts if mode == 'zh' else en_parts).append(buf)
            mode = cur
            buf = c
    if buf:
        (zh_parts if mode == 'zh' else en_parts).append(buf)
    en = re.sub(r' +', ' ', ' '.join(p.strip() for p in en_parts).strip())
    zh_parts = [p.strip() for p in zh_parts if p.strip()]
    zh = '；'.join(zh_parts) if len(zh_parts) > 1 else (zh_parts[0] if zh_parts else '')
    return en, zh


def split_def(text):
    return split_en_zh(text)


def extract_page(page):
    """Return list of vocab dicts for this page."""
    cuts = get_row_cuts(page)
    if len(cuts) < 2:
        return []

    d = page.get_text('dict')
    spans = []
    for block in d['blocks']:
        if 'lines' not in block:
            continue
        for line in block['lines']:
            for span in line['spans']:
                x0, y0, x1, y1 = span['bbox']
                txt = span['text']
                if not txt.strip():
                    continue
                font = span.get('font', '')
                size = span.get('size', 0)
                # The PDF has user-drawn annotations in fonts that start with
                # a dot (e.g. '.SFUI-Regular...', '.PingFangUIDisplaySC-Reg').
                # Drop those — only legit content uses 11.5pt Helvetica /
                # PingFangSC. Also drop oversize watermark text.
                if font.startswith('.') or size > 14 or size < 8:
                    continue
                spans.append((y0, x0, txt))

    rows = []
    for i in range(len(cuts) - 1):
        y_top, y_bot = cuts[i], cuts[i+1]
        # Skip only the column-title header row (y_top ~ 11)
        if y_top < 30:
            continue
        if y_bot - y_top < 25:
            continue

        row_spans = [(y0, x0, t) for (y0, x0, t) in spans if y_top - 1 <= y0 < y_bot - 1]
        if not row_spans:
            continue

        buckets = {name: [] for _, _, name in COL_BOUNDS}
        for y0, x0, t in row_spans:
            col = col_of(x0)
            if col is None:
                continue
            if col == 'word':
                if is_word_junk(t):
                    continue
            else:
                if is_junk(t):
                    continue
            buckets[col].append((y0, x0, t))

        row = {}
        for k, v in buckets.items():
            row[k] = merge_spans_by_line(v, no_space=(k in ('word', 'synonym')))
        row['word'] = clean_headword(row['word'])
        row['synonym'] = clean_headword(row['synonym'])
        if not row['word']:
            continue
        rows.append(row)

    return rows


def main():
    doc = fitz.open(PDF_PATH)
    n = doc.page_count

    list_start = {}
    for i in range(n):
        text = doc[i].get_text()
        m = re.search(r'list\s*(\d+)', text, re.IGNORECASE)
        if m:
            num = int(m.group(1))
            if num not in list_start:
                list_start[num] = i

    list_nums = sorted(list_start.keys())
    print(f'Lists found: {len(list_nums)}', flush=True)

    lists = {}
    seen_words = set()  # global dedup across page boundaries
    for idx, num in enumerate(list_nums):
        start = list_start[num]
        end = list_start[list_nums[idx+1]] if idx+1 < len(list_nums) else n
        words = []
        local_seen = set()
        for p in range(start, end):
            for r in extract_page(doc[p]):
                w = r['word'].lower()
                if w in local_seen:
                    continue
                local_seen.add(w)
                en_def, zh_def = split_def(r['definition'])
                en_ex, zh_ex = split_en_zh(r['example'])
                words.append({
                    'word': r['word'],
                    'ipa': r['ipa'],
                    'def_en': en_def,
                    'def_zh': zh_def,
                    'synonym': r['synonym'],
                    'ex_en': en_ex,
                    'ex_zh': zh_ex,
                })
        lists[str(num)] = words
        print(f'  list {num}: {len(words)} words (pages {start+1}-{end})', flush=True)

    with open(OUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(lists, f, ensure_ascii=False, indent=2)
    print(f'\nWrote {OUT_PATH}')


if __name__ == '__main__':
    main()
