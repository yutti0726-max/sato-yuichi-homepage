#!/usr/bin/env python3
"""年間の吉日カレンダー(kichijitsu-calendar/index.html)の表を、暦の計算から作り直す。

使い方(リポジトリのルートで実行。Python 3 の標準ライブラリだけで動く):
    python scripts/generate_kichijitsu_calendar.py 2027           # 2026年11月〜2027年12月で作り直す
    python scripts/generate_kichijitsu_calendar.py 2027 --check   # 書き込まずに、ページの全日を計算と照合
    python scripts/generate_kichijitsu_calendar.py 2027 --check --garmin ~/garmin-kichijitsu
                                                                  # 元の計算(吉日ウォッチの tools/verify.py)とも照合

- 年を指定すると、その年の1月〜12月と、前の年の最後の LEAD_MONTHS か月(既定2。--lead で変更)を載せる。
  毎年、次の年を指定して作り直す(例: 2027年の秋に 2028 を指定 → 2027年11月〜2028年12月)。
- 暦は ~/kichijitsu-planner/src/koyomi.py(吉日デジタル手帳の暦。吉日ウォッチと同じ計算の写し)を
  読み込んで使う。新しい計算は持たない。場所は --koyomi か環境変数 KICHI_KOYOMI で変えられる。
  koyomi.py の範囲は 2025-01-01〜2036-12-31。範囲外の日があると止まる。
- 書き換えるのは、ページの中の <!-- GEN:名前 --> 〜 <!-- /GEN:名前 --> の区間だけ。
  本文の文章の区間(<!-- TEXT:… -->)やデザインの部分には触らない。
- 「次の天赦日・一粒万倍日」は、作成日(--today、既定は今日)の時点の日付を書く。
  見る人の日付での探し直しは、ページの中のスクリプトが行う。
- 作り直したあとは python scripts/generate_sitemap.py で sitemap も作り直す。
- 年を変えたときは、本文の文章(TEXT の区間)の中の期間・年(導入の「2026年11月から2027年12月まで」、
  手帳の名前の「2027年」など)も手で直す。--check は、本文の「〜年〜月から〜年〜月まで」が表の期間と合うかを確かめる。
- --check は、表に載せた日・載せなかった日の全日について、六曜と暦注が koyomi.py と一致するか、
  日数のまとめ・天赦日の一覧・重なる日の一覧・「次の」の日付・title などの期間の表記が計算と合うかを確かめる。
  問題がなければ最後に ALL PASS と出して終了コード 0、違いがあれば 1。
"""
import argparse
import datetime as dt
import html
import html.parser
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, 'kichijitsu-calendar', 'index.html')
URL = 'https://yuichi-sato.com/kichijitsu-calendar/'
OG_IMAGE = 'https://yuichi-sato.com/assets/img/og-image.png'
DEFAULT_KOYOMI = os.environ.get('KICHI_KOYOMI', os.path.join(os.path.expanduser('~'), 'kichijitsu-planner', 'src'))

# 載せる暦注(koyomi.py の名前のまま。表示の順)。大安は六曜から取る。
TAGS = ['天赦日', '一粒万倍日', '己巳の日', '寅の日', '巳の日', '不成就日']
BAD = {'不成就日'}
TAIAN = '大安'
# 重なりを数える吉日(大安を含む)
LUCKY = ['天赦日', '一粒万倍日', '己巳の日', '寅の日', '巳の日', TAIAN]
TAG_CLASS = {'天赦日': 'kc-t-tensha', '一粒万倍日': 'kc-t-ichi', '己巳の日': 'kc-t-tsuchinotomi',
             '寅の日': 'kc-t-tora', '巳の日': 'kc-t-mi', '不成就日': 'kc-t-fujoju'}
SUMMARY_ROWS = ['天赦日', '一粒万倍日', '己巳の日', '寅の日', '巳の日', TAIAN, '不成就日']
BEST_LABEL = '天赦日と一粒万倍日が重なる日'
WEEKDAY = '月火水木金土日'
ONE = dt.timedelta(days=1)


def load_koyomi(path):
    sys.dont_write_bytecode = True  # 手帳のリポジトリに .pyc を書かない
    sys.path.insert(0, path)
    try:
        import koyomi  # noqa: E402
    except ImportError as e:
        sys.exit(f'koyomi.py を読み込めません({path}): {e}')
    return koyomi


# ---- データ ----

class Day:
    def __init__(self, d, r):
        self.date = d
        self.roku = r['roku']
        self.tags = [t for t in TAGS if t in r['tags']]
        self.lucky = [t for t in LUCKY if t in self.tags or (t == TAIAN and self.roku == TAIAN)]
        self.best = '天赦日' in self.tags and '一粒万倍日' in self.tags
        self.listed = bool(self.tags) or self.roku == TAIAN

    def has(self, name):
        return self.roku == TAIAN if name == TAIAN else name in self.tags


def month_range(year, lead):
    """(年, 月) の一覧。前の年の最後の lead か月 + その年の12か月。"""
    out = [(year - 1, m) for m in range(13 - lead, 13)] if lead else []
    return out + [(year, m) for m in range(1, 13)]


def build_days(K, year, lead):
    months = month_range(year, lead)
    first = dt.date(*months[0], 1)
    last = dt.date(year, 12, 31)
    days, d = [], first
    while d <= last:
        r = K.day(d)
        if r is None:
            sys.exit(f'{d} は koyomi.py の範囲の外です')
        days.append(Day(d, r))
        d += ONE
    return months, days


def segments(year, lead):
    """日数のまとめの列: (見出し, 年, 月の集合)。"""
    segs = []
    if lead:
        ms = list(range(13 - lead, 13))
        segs.append((f'{year - 1}年{ms[0]}〜{ms[-1]}月' if len(ms) > 1 else f'{year - 1}年{ms[0]}月', year - 1, set(ms)))
    segs.append((f'{year}年', year, set(range(1, 13))))
    return segs


def count(days, seg, name):
    _, y, ms = seg
    return sum(1 for x in days if x.date.year == y and x.date.month in ms and
               (x.best if name == BEST_LABEL else x.has(name)))


def period_text(months):
    (y0, m0), (y1, m1) = months[0], months[-1]
    return f'{y0}年{m0}月〜{y1}年{m1}月'


def md(d, wd=True):
    return f'{d.month}月{d.day}日' + (f'({WEEKDAY[d.weekday()]})' if wd else '')


def ymd(d, wd=True):
    return f'{d.year}年' + md(d, wd)


# ---- HTML ----

def esc(s):
    return html.escape(s, quote=True)


def tag_spans(x):
    out = [f'<span class="kc-tag {TAG_CLASS[t]}">{t}</span>' for t in x.tags]
    if x.best:
        out.append(f'<span class="kc-flag">{BEST_LABEL}</span>')
    return ''.join(out)


def roku_cell(x):
    return f'<span class="kc-roku-taian">{x.roku}</span>' if x.roku == TAIAN else x.roku


def row_class(x):
    if x.best:
        return 'kc-best'
    if len(x.lucky) >= 2:
        return 'kc-multi'
    return ''


def tr(x, ind):
    cls = row_class(x)
    attrs = f'data-date="{x.date.isoformat()}" data-roku="{x.roku}" data-tags="{" ".join(x.tags)}"'
    if cls:
        attrs += f' class="{cls}"'
    return (f'{ind}<tr {attrs}><td><time datetime="{x.date.isoformat()}">{md(x.date)}</time></td>'
            f'<td>{roku_cell(x)}</td><td>{tag_spans(x)}</td></tr>')


def gen_head(year, months, days, published, today):
    period = period_text(months)
    title = title_text(year)
    desc = (f'{period_from_to(months)}の一粒万倍日・天赦日・寅の日・巳の日・己巳の日・大安・不成就日を月ごとに一覧にしました。'
            '天赦日と一粒万倍日が重なる日など、吉日が重なる日もまとめています。予定を考えるときの参考に。')
    h1 = h1_text(months)
    L = [
        f'<title>{esc(title)}</title>',
        f'<meta name="description" content="{esc(desc)}">',
        f'<link rel="canonical" href="{URL}">',
        f'<link rel="alternate" hreflang="ja" href="{URL}">',
        f'<link rel="alternate" hreflang="x-default" href="{URL}">',
        '<meta property="og:type" content="article">',
        f'<meta property="og:url" content="{URL}">',
        f'<meta property="og:title" content="{esc(title)}">',
        f'<meta property="og:description" content="{esc(desc)}">',
        '<meta property="og:site_name" content="佐藤雄一 公式サイト">',
        '<meta property="og:locale" content="ja_JP">',
        f'<meta property="og:image" content="{OG_IMAGE}">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{esc(title)}">',
        f'<meta name="twitter:description" content="{esc(desc)}">',
        f'<meta name="twitter:image" content="{OG_IMAGE}">',
        '',
        '<script type="application/ld+json">',
        '{',
        '  "@context": "https://schema.org",',
        '  "@type": "Article",',
        f'  "headline": "{h1}",',
        f'  "description": "{desc}",',
        f'  "image": "{OG_IMAGE}",',
        '  "author": { "@type": "Person", "@id": "https://yuichi-sato.com/profile/#person", "name": "佐藤雄一", "url": "https://yuichi-sato.com/profile/" },',
        '  "publisher": { "@type": "Person", "name": "佐藤雄一" },',
        f'  "mainEntityOfPage": "{URL}",',
        f'  "datePublished": "{published}",',
        f'  "dateModified": "{today.isoformat()}"',
        '}',
        '</script>',
        '<script type="application/ld+json">',
        '{',
        '  "@context": "https://schema.org",',
        '  "@type": "BreadcrumbList",',
        '  "itemListElement": [',
        '    { "@type": "ListItem", "position": 1, "name": "ホーム", "item": "https://yuichi-sato.com/" },',
        '    { "@type": "ListItem", "position": 2, "name": "一粒万倍日・天赦日カレンダー" }',
        '  ]',
        '}',
        '</script>',
    ]
    return L


# title・h1 の文は、本文の文書(T-120)の title 案A と h1 の案。年だけを差し替える。
def title_text(year):
    return f'{year}年の吉日カレンダー｜一粒万倍日・天赦日・寅の日の一覧'


def h1_text(months):
    return f'{months[-1][0]}年の吉日カレンダー｜一粒万倍日・天赦日・重なる日の一覧'


def period_from_to(months):
    """本文の書き方の期間(例: 2026年11月から2027年12月まで)。"""
    (y0, m0), (y1, m1) = months[0], months[-1]
    return f'{y0}年{m0}月から{y1}年{m1}月まで'


def gen_header(months, today):
    return [
        f'      <h1>{h1_text(months)}</h1>',
        f'      <p class="article-meta">更新日：{today.year}年{today.month}月{today.day}日</p>',
    ]


def next_day(days, today, f):
    for x in days:
        if x.date >= today and f(x):
            return x
    return None


NEXT_ITEMS = [
    ('tensha', '次の天赦日', lambda x: '天赦日' in x.tags),
    ('ichi', '次の一粒万倍日', lambda x: '一粒万倍日' in x.tags),
    ('best', f'次の{BEST_LABEL}', lambda x: x.best),
]


def next_text(x, today):
    if x is None:
        return 'このページの期間の中にはありません'
    return ymd(x.date) + ('(今日)' if x.date == today else '')


def gen_next(days, today):
    L = ['      <section class="kc-next" aria-labelledby="kcNextTitle">',
         '        <h2 id="kcNextTitle">次の天赦日・一粒万倍日</h2>',
         '        <dl>']
    for key, label, f in NEXT_ITEMS:
        L.append(f'          <dt>{label}</dt><dd data-kc-next="{key}">{next_text(next_day(days, today, f), today)}</dd>')
    L += ['        </dl>',
          f'        <p class="kc-asof" id="kcAsof">このページの作成日({today.year}年{today.month}月{today.day}日)の時点の日付です(日本時間)。</p>',
          '      </section>']
    return L


def gen_toc(year, lead):
    segs = segments(year, lead)
    items = ['<a href="#best">吉日が重なる日</a>', '<a href="#tensha">天赦日の一覧</a>',
             '<a href="#summary">日数のまとめ</a>', '<a href="#legend">表の見方</a>']
    items += [f'<a href="#y{y}">{label}の表</a>' for label, y, _ in segs]
    items += ['<a href="#meanings">吉日・暦注の意味</a>', '<a href="#products">吉日ウォッチ・吉日手帳</a>']
    return [f'      <p class="kc-toc">目次：{" ／ ".join(items)}</p>']


def gen_best(months, days):
    period = period_text(months)
    best = [x for x in days if x.best]
    if best:
        return [f'      <p id="bestDays">{period}に、天赦日と一粒万倍日が重なる日は、'
                f'<strong>{"・".join(ymd(x.date) for x in best)}の{len(best)}日</strong>です。</p>']
    return [f'      <p id="bestDays">{period}には、天赦日と一粒万倍日が重なる日はありません。</p>']


def gen_highlights(year, lead, months, days):
    period = period_text(months)
    tensha = [x for x in days if '天赦日' in x.tags]
    L = ['      <h2 id="tensha">天赦日の一覧</h2>',
          f'      <p>{period}の天赦日は{len(tensha)}日です。同じ日に当たる暦注と、その日の六曜も載せています。</p>',
          '      <div class="table-wrap">',
          '        <table class="kc-table kc-list-table">',
          '          <thead><tr><th scope="col">日付</th><th scope="col">六曜</th><th scope="col">同じ日の暦注</th></tr></thead>',
          '          <tbody>']
    for x in tensha:
        cls = row_class(x)
        attrs = f'data-date="{x.date.isoformat()}"' + (f' class="{cls}"' if cls else '')
        L.append(f'            <tr {attrs}><td><time datetime="{x.date.isoformat()}">{ymd(x.date)}</time></td>'
                 f'<td>{roku_cell(x)}</td><td>{tag_spans(x)}</td></tr>')
    L += ['          </tbody>', '        </table>', '      </div>', '']
    segs = segments(year, lead)
    L += ['      <h2 id="summary">日数のまとめ</h2>',
          '      <div class="table-wrap">',
          '        <table class="kc-summary">',
          '          <thead><tr><th scope="col">吉日・暦注</th>' +
          ''.join(f'<th scope="col">{label}</th>' for label, _, _ in segs) + '</tr></thead>',
          '          <tbody>']
    for name in SUMMARY_ROWS + [BEST_LABEL]:
        L.append(f'            <tr data-kc-count="{name}"><td>{name}</td>' +
                 ''.join(f'<td>{count(days, s, name)}日</td>' for s in segs) + '</tr>')
    L += ['          </tbody>', '        </table>', '      </div>',
          '      <p class="article-meta">巳の日の日数には、己巳の日に当たる日を含めていません。</p>']
    return L


def gen_tables(year, lead, months, days):
    L = []
    by_month = {}
    for x in days:
        by_month.setdefault((x.date.year, x.date.month), []).append(x)
    for label, y, ms in segments(year, lead):
        mlist = [(yy, m) for (yy, m) in months if yy == y and m in ms]
        L += ['', f'      <h2 class="kc-year" id="y{y}">{label}の吉日(月ごとの表)</h2>',
              '      <ul class="kc-monthnav">' +
              ''.join(f'<li><a href="#m{yy}-{m:02d}">{m}月</a></li>' for yy, m in mlist) + '</ul>']
        for yy, m in mlist:
            rows = [x for x in by_month[(yy, m)] if x.listed]
            L += [f'      <h3 class="kc-month" id="m{yy}-{m:02d}">{yy}年{m}月</h3>',
                  '      <div class="table-wrap">',
                  '        <table class="kc-table kc-month-table">',
                  '          <thead><tr><th scope="col">日付</th><th scope="col">六曜</th><th scope="col">暦注</th></tr></thead>',
                  '          <tbody>']
            L += [tr(x, '            ') for x in rows]
            L += ['          </tbody>', '        </table>', '      </div>']
    return L


def replace_region(src, name, lines):
    pat = re.compile(r'(<!-- GEN:%s -->\r?\n)(.*?)(<!-- /GEN:%s -->)' % (re.escape(name), re.escape(name)), re.S)
    if len(pat.findall(src)) != 1:
        sys.exit(f'ページに <!-- GEN:{name} --> 〜 <!-- /GEN:{name} --> の区間が1つだけある必要があります')
    body = '\n'.join(lines) + '\n' if lines else ''
    return pat.sub(lambda m: m.group(1) + body + m.group(3), src)


def read_page():
    with open(PAGE, encoding='utf-8', newline='') as f:
        return f.read().replace('\r\n', '\n')


def generate(K, year, lead, today):
    months, days = build_days(K, year, lead)
    src = read_page()
    m = re.search(r'"datePublished": "(\d{4}-\d{2}-\d{2})"', src)
    published = m.group(1) if m else today.isoformat()
    src = replace_region(src, 'head', gen_head(year, months, days, published, today))
    src = replace_region(src, 'header', gen_header(months, today))
    src = replace_region(src, 'next', gen_next(days, today))
    src = replace_region(src, 'toc', gen_toc(year, lead))
    src = replace_region(src, 'best', gen_best(months, days))
    src = replace_region(src, 'highlights', gen_highlights(year, lead, months, days))
    src = replace_region(src, 'tables', gen_tables(year, lead, months, days))
    with open(PAGE, 'w', encoding='utf-8', newline='\r\n') as f:
        f.write(src)
    n = sum(1 for x in days if x.listed)
    print(f'{os.path.relpath(PAGE, ROOT)} を作り直しました: {period_text(months)}、{len(days)}日のうち {n}日を表に載せた')


# ---- 照合(--check) ----

class Rows(html.parser.HTMLParser):
    """表の行(data-date のある tr)の属性と、セルの文字を集める。"""

    def __init__(self):
        super().__init__()
        self.tables = []   # [(table の class, [row])]
        self.row = None
        self.cell = None
        self.span_cls = None
        self.count_rows = {}  # 日数のまとめ: 名前 -> [セルの文字]
        self.count_name = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'table':
            self.tables.append((a.get('class', ''), []))
        elif tag == 'tr' and 'data-date' in a:
            self.row = dict(attrs=a, cells=[], tags=[], flags=[], time=None)
            self.tables[-1][1].append(self.row)
        elif tag == 'tr' and 'data-kc-count' in a:
            self.count_name = a['data-kc-count']
            self.count_rows[self.count_name] = []
        elif tag == 'td':
            self.cell = ''
        elif tag == 'span' and self.row is not None:
            self.span_cls = a.get('class', '')
        elif tag == 'time' and self.row is not None:
            self.row['time'] = a.get('datetime')

    def handle_endtag(self, tag):
        if tag == 'td' and self.cell is not None:
            if self.row is not None:
                self.row['cells'].append(self.cell)
            elif self.count_name is not None:
                self.count_rows[self.count_name].append(self.cell)
            self.cell = None
        elif tag == 'tr':
            self.row = None
            self.count_name = None
        elif tag == 'span':
            self.span_cls = None

    def handle_data(self, data):
        if self.cell is not None:
            self.cell += data
        if self.row is not None and self.span_cls:
            if 'kc-tag' in self.span_cls:
                self.row['tags'].append(data)
            elif 'kc-flag' in self.span_cls:
                self.row['flags'].append(data)


def check(K, year, lead, today, garmin):
    months, days = build_days(K, year, lead)
    src = read_page()
    fails = []

    def ok(cond, msg):
        print(('PASS ' if cond else 'FAIL ') + msg)
        if not cond:
            fails.append(msg)

    p = Rows()
    p.feed(src)
    month_rows = [r for cls, rows in p.tables if 'kc-month-table' in cls for r in rows]
    list_rows = [r for cls, rows in p.tables if 'kc-list-table' in cls for r in rows]
    n_tables = sum(1 for cls, _ in p.tables if 'kc-month-table' in cls)
    ok(n_tables == len(months), f'月ごとの表の数 {n_tables}(期待 {len(months)}か月)')

    # 1. 全日の照合: 載せた日と載せなかった日
    by_date = {}
    dup = 0
    for r in month_rows:
        d = r['attrs']['data-date']
        dup += d in by_date
        by_date[d] = r
    ok(dup == 0, f'表に同じ日が2回出ていない(重複 {dup})')
    bad = []
    for x in days:
        iso = x.date.isoformat()
        r = by_date.get(iso)
        if not x.listed:
            if r is not None:
                bad.append(f'{iso}: 暦注がないのに表にある')
            continue
        if r is None:
            bad.append(f'{iso}: 表にない')
            continue
        a = r['attrs']
        exp_cells = [md(x.date), x.roku]
        if a.get('data-roku') != x.roku:
            bad.append(f'{iso}: data-roku {a.get("data-roku")} / 計算 {x.roku}')
        if a.get('data-tags', '').split() != x.tags:
            bad.append(f'{iso}: data-tags {a.get("data-tags")} / 計算 {x.tags}')
        if r['time'] != iso or r['cells'][:2] != exp_cells:
            bad.append(f'{iso}: 日付・六曜の表示 {r["cells"][:2]} / 計算 {exp_cells}')
        if r['tags'] != x.tags:
            bad.append(f'{iso}: 暦注の表示 {r["tags"]} / 計算 {x.tags}')
        if r['flags'] != ([BEST_LABEL] if x.best else []):
            bad.append(f'{iso}: 重なりの印 {r["flags"]}')
        cls = a.get('class', '')
        if cls != row_class(x):
            bad.append(f'{iso}: 行の目立たせ方 "{cls}" / 期待 "{row_class(x)}"')
        # 月の表の中の位置: その月の表にあること
    stray = set(by_date) - {x.date.isoformat() for x in days}
    if stray:
        bad.append(f'期間の外の日が表にある: {sorted(stray)}')
    n_listed = sum(1 for x in days if x.listed)
    ok(not bad, f'全日の照合({days[0].date}〜{days[-1].date} の {len(days)}日。表に載せる {n_listed}日・'
                f'載せない {len(days) - n_listed}日)で、六曜・暦注・日付の表示・重なりの印が koyomi.py と一致'
                + (f'。違い {len(bad)}件: {bad[:5]}' if bad else ''))
    # 月の表の順と所属
    order_ok = [r['attrs']['data-date'] for r in month_rows] == [x.date.isoformat() for x in days if x.listed]
    ok(order_ok, '月ごとの表の行が日付の順で、その月の表に入っている')

    # 2. 天赦日の一覧
    tensha = [x for x in days if '天赦日' in x.tags]
    got = [(r['attrs']['data-date'], r['cells'][1], r['tags'], r['flags']) for r in list_rows]
    exp = [(x.date.isoformat(), x.roku, x.tags, [BEST_LABEL] if x.best else []) for x in tensha]
    ok(got == exp, f'天赦日の一覧({len(exp)}日)が計算と一致')

    # 3. 日数のまとめ
    segs = segments(year, lead)
    exp_counts = {name: [f'{count(days, s, name)}日' for s in segs] for name in SUMMARY_ROWS + [BEST_LABEL]}
    got_counts = {k: v[1:] for k, v in p.count_rows.items()}
    ok(got_counts == exp_counts, '日数のまとめが計算と一致: ' +
       '、'.join(f'{k} {"/".join(v)}' for k, v in exp_counts.items()))
    # 手帳のページ(2027年の日数)とも突き合わせる(年が 2027 のときだけ)
    if year == 2027:
        techo = {'天赦日': 6, '一粒万倍日': 60, '己巳の日': 6, '寅の日': 30, '巳の日': 25, '不成就日': 48}
        ok(all(exp_counts[k][-1] == f'{v}日' for k, v in techo.items()),
           '2027年の日数が吉日デジタル手帳のページの表(天赦日6・一粒万倍日60・己巳6・寅30・巳25・不成就48)と同じ')

    # 4. 重なる日の文
    best = [x for x in days if x.best]
    m = re.search(r'<p id="bestDays">(.*?)</p>', src, re.S)
    txt = re.sub(r'<[^>]+>', '', m.group(1)) if m else ''
    ok(all(ymd(x.date) in txt for x in best) and f'{len(best)}日' in txt,
       f'「重なる日」の文に {len(best)}日すべての日付: ' + '・'.join(ymd(x.date) for x in best))

    # 5. 「次の」(作成日の時点。ページの作成日を読む)
    m = re.search(r'このページの作成日\((\d+)年(\d+)月(\d+)日\)', src)
    if m:
        made = dt.date(*map(int, m.groups()))
        for key, label, f in NEXT_ITEMS:
            mm = re.search(r'data-kc-next="%s">(.*?)</dd>' % key, src)
            ok(mm and mm.group(1) == next_text(next_day(days, made, f), made),
               f'{label}(作成日 {made} の時点): {mm.group(1) if mm else "なし"}')
    else:
        ok(False, '「次の天赦日」の作成日の表記が見つからない')

    # 6. 期間の表記・head
    period = period_text(months)
    ok(f'<h1>{h1_text(months)}</h1>' in src, f'h1: {h1_text(months)}')
    ok(f'<link rel="canonical" href="{URL}">' in src, 'canonical')
    t = re.search(r'<title>(.*?)</title>', src)
    ok(t and t.group(1) == title_text(year), f'title: {t.group(1) if t else ""}')
    ok(f'"headline": "{h1_text(months)}"' in src, '構造化データの headline が h1 と同じ')
    # 本文の文章(TEXT の区間)に書いた期間が、表の期間と合っているか(年を変えたら本文も直す)
    texts = ''.join(re.findall(r'<!-- TEXT:\w+ BEGIN.*?-->(.*?)<!-- TEXT:\w+ END -->', src, re.S))
    found = set(re.findall(r'\d{4}年\d{1,2}月から\d{4}年\d{1,2}月まで', texts))
    ok(found <= {period_from_to(months)}, f'本文の文章の期間の表記が表の期間({period_from_to(months)})と合う: {sorted(found) or "表記なし"}')

    # 7. 元の計算(吉日ウォッチの tools/verify.py)との照合
    if garmin:
        tools = os.path.join(os.path.expanduser(garmin), 'tools')
        sys.path.insert(0, tools)
        try:
            import verify as V  # noqa: E402
        except Exception as e:  # pragma: no cover
            ok(False, f'元の verify.py を読み込めない: {e!r}')
        else:
            diff = []
            for x in days:
                r = V.sim(V.G.jdn(x.date.year, x.date.month, x.date.day))
                if r != K.day(x.date):
                    diff.append(x.date.isoformat())
                    continue
                row = by_date.get(x.date.isoformat())
                exp_tags = [t for t in TAGS if t in r['tags']]
                listed = bool(exp_tags) or r['roku'] == TAIAN
                if listed != (row is not None) or (row and (row['attrs']['data-roku'] != r['roku'] or
                                                            row['attrs']['data-tags'].split() != exp_tags)):
                    diff.append(x.date.isoformat())
            ok(not diff, f'元の計算(verify.sim)とも全日一致({len(days)}日、違い {len(diff)}日)')

    print('ALL PASS' if not fails else f'FAIL {len(fails)}件')
    return 0 if not fails else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description='年間の吉日カレンダーのページを作り直す')
    ap.add_argument('year', type=int, help='載せる年(前の年の最後の数か月も載せる)')
    ap.add_argument('--lead', type=int, default=2, help='前の年の何か月を載せるか(既定 2 = 11月・12月)')
    ap.add_argument('--today', type=dt.date.fromisoformat, default=dt.date.today(),
                    help='作成日(「次の天赦日」と更新日の基準)。既定は今日')
    ap.add_argument('--koyomi', default=DEFAULT_KOYOMI, help='koyomi.py のあるフォルダ')
    ap.add_argument('--check', action='store_true', help='書き込まずに照合だけする')
    ap.add_argument('--garmin', help='--check のとき、元の計算(garmin-kichijitsu)とも照合する')
    a = ap.parse_args(argv)
    if not 0 <= a.lead <= 11:
        sys.exit('--lead は 0〜11')
    K = load_koyomi(a.koyomi)
    if a.check:
        return check(K, a.year, a.lead, a.today, a.garmin)
    generate(K, a.year, a.lead, a.today)
    return 0


if __name__ == '__main__':
    sys.exit(main())
