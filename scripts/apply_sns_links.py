#!/usr/bin/env python3
"""全ページのフッターと、トップの構造化データに、SNS とリンク集への導線を足す。

使い方(リポジトリのルートで実行):
    python scripts/apply_sns_links.py --dry-run    # 変更予定のファイル数と1件の例を表示(書き込みはしない)
    python scripts/apply_sns_links.py --dry-run --verbose   # 変更予定のファイルをすべて表示
    python scripts/apply_sns_links.py              # 実際に書き換える

やること(どれも、すでに入っていれば何もしない。何度実行しても二重にならない):
  (a) 全ページのフッターの X のリンクの後ろに、TikTok と Instagram のリンクを足す。
      区切り(「 ・ 」や「 &middot; 」)は、そのフッターで X のリンクの前に使われているものに合わせる。
  (b) index.html・en/index.html・zh/index.html の構造化データ(JSON-LD)の sameAs に、
      X・TikTok・Instagram の URL を足す。書き換えたあとの JSON が読めることを確かめる。
  (c) フッターに、そのページの言語のリンク集(/links/・/en/links/・/zh/links/)へのリンクを足す。

対象はリポジトリ内の *.html(docs/ scripts/ .git/ などは除外。generate_sitemap.py と同じ)。
言語は <html lang="..."> で決める(無ければパスの en/・zh/ から)。
改行コード(CRLF/LF)はファイルごとにそのまま保つ。

全ページのフッターを書き換えるので、あとで scripts/generate_sitemap.py を実行すると、
全ページの lastmod が更新される点に注意する。
"""
import argparse
import difflib
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCLUDE_DIRS = {'.git', 'docs', 'scripts', 'node_modules', '.github', '.claude'}

X_URL = 'https://x.com/yutti0726'
TIKTOK_URL = 'https://www.tiktok.com/@yuichi.sato.tech'
INSTAGRAM_URL = 'https://www.instagram.com/yuichi.sato.tech/'
SNS_URLS = [X_URL, TIKTOK_URL, INSTAGRAM_URL]

LINKS_PATH = {'ja': '/links/', 'en': '/en/links/', 'zh': '/zh/links/'}
LINKS_LABEL = {'ja': 'リンク集', 'en': 'Links', 'zh': '链接汇总'}
DEFAULT_SEP = {'ja': ' ・ ', 'en': ' &middot; ', 'zh': ' ・ '}
SAMEAS_FILES = ['index.html', 'en/index.html', 'zh/index.html']

TIKTOK_A = f'<a href="{TIKTOK_URL}" target="_blank" rel="noopener">TikTok</a>'
INSTAGRAM_A = f'<a href="{INSTAGRAM_URL}" target="_blank" rel="noopener">Instagram</a>'

FOOTER_RE = re.compile(r'<footer\b[^>]*>.*?</footer>', re.S | re.I)
X_A_RE = re.compile(r'<a\b[^>]*\bhref="https://x\.com/yutti0726/?"[^>]*>.*?</a>', re.S | re.I)
TIKTOK_A_RE = re.compile(r'<a\b[^>]*\bhref="https://(?:www\.)?tiktok\.com/@yuichi\.sato\.tech/?"[^>]*>.*?</a>', re.S | re.I)
INSTAGRAM_A_RE = re.compile(r'<a\b[^>]*\bhref="https://(?:www\.)?instagram\.com/yuichi\.sato\.tech/?"[^>]*>.*?</a>', re.S | re.I)
SEP_BEFORE_X_RE = re.compile(r'</a>(\s*(?:・|&middot;|&#183;|·|\|)\s*)<a\b[^>]*\bhref="https://x\.com/yutti0726', re.S | re.I)
LDJSON_RE = re.compile(r'(<script\b[^>]*type="application/ld\+json"[^>]*>)(.*?)(</script>)', re.S | re.I)
SAMEAS_RE = re.compile(r'("sameAs"\s*:\s*\[)(.*?)(\])', re.S)


def html_files():
    for dp, dns, fns in os.walk(ROOT):
        dns[:] = sorted(d for d in dns if d not in EXCLUDE_DIRS and not d.startswith('.'))
        for fn in sorted(fns):
            if fn.endswith('.html'):
                yield os.path.relpath(os.path.join(dp, fn), ROOT).replace(os.sep, '/')


def page_lang(rel, s):
    m = re.search(r'<html\b[^>]*\blang="([A-Za-z-]+)"', s)
    if m:
        code = m.group(1).lower().split('-')[0]
        if code in LINKS_PATH:
            return code
    first = rel.split('/', 1)[0]
    return first if first in ('en', 'zh') else 'ja'


def fix_footer(s, lang):
    """フッターに TikTok・Instagram・リンク集を足す。(新しい本文, 足したものの一覧, 警告) を返す。"""
    footers = list(FOOTER_RE.finditer(s))
    if not footers:
        return s, [], 'フッターが見つからない'
    # site-footer があればそれを、なければ最後の footer を使う
    target = next((m for m in footers if 'site-footer' in m.group(0)[:200]), footers[-1])
    footer = target.group(0)
    xm = X_A_RE.search(footer)
    if not xm:
        return s, [], 'フッターに X のリンクが見つからない'
    sm = SEP_BEFORE_X_RE.search(footer)
    sep = sm.group(1) if sm else DEFAULT_SEP[lang]
    added = []
    links_a = f'<a href="{LINKS_PATH[lang]}">{LINKS_LABEL[lang]}</a>'

    def insert_after(text, m, piece):
        return text[:m.end()] + sep + piece + text[m.end():]

    if not TIKTOK_A_RE.search(footer):
        footer = insert_after(footer, X_A_RE.search(footer), TIKTOK_A)
        added.append('TikTok')
    if not INSTAGRAM_A_RE.search(footer):
        footer = insert_after(footer, TIKTOK_A_RE.search(footer), INSTAGRAM_A)
        added.append('Instagram')
    links_re = re.compile(r'\bhref="(?:https://yuichi-sato\.com)?' + re.escape(LINKS_PATH[lang]) + r'"')
    if not links_re.search(footer):
        footer = insert_after(footer, INSTAGRAM_A_RE.search(footer), links_a)
        added.append('リンク集')
    if not added:
        return s, [], None
    return s[:target.start()] + footer + s[target.end():], added, None


def fix_sameas(s):
    """JSON-LD の sameAs に SNS の URL を足す。(新しい本文, 足したURLの一覧, 警告) を返す。"""
    nl = '\r\n' if '\r\n' in s else '\n'
    added_all = []
    out = []
    pos = 0
    found = False
    for m in LDJSON_RE.finditer(s):
        body = m.group(2)
        am = SAMEAS_RE.search(body)
        if not am:
            continue
        found = True
        items = re.findall(r'"([^"]*)"', am.group(2))
        missing = [u for u in SNS_URLS if u not in items]
        if not missing:
            continue
        inner = am.group(2)
        stripped = inner.rstrip()
        trailing = inner[len(stripped):]
        im = re.search(r'(?:^|\n)([ \t]*)"[^"\n]*"\s*$', stripped)
        indent = im.group(1) if im else '    '
        if stripped.strip():
            new_inner = stripped + ''.join(f',{nl}{indent}"{u}"' for u in missing) + trailing
        else:
            new_inner = nl + f',{nl}'.join(f'{indent}"{u}"' for u in missing) + (trailing or nl)
        new_body = body[:am.start(2)] + new_inner + body[am.end(2):]
        try:
            json.loads(body)
            original_ok = True
        except ValueError:
            original_ok = False
        if original_ok:
            try:
                json.loads(new_body)
            except ValueError as e:
                return s, [], f'sameAs を足すと JSON-LD が読めなくなる({e})。書き換えを中止'
        out.append(s[pos:m.start(2)])
        out.append(new_body)
        pos = m.end(2)
        added_all.extend(missing)
    if not found:
        return s, [], '構造化データに sameAs が見つからない'
    if not added_all:
        return s, [], None
    out.append(s[pos:])
    return ''.join(out), added_all, None


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--dry-run', action='store_true', help='書き込まずに、変更予定のファイル数と1件の例を表示する')
    ap.add_argument('--verbose', action='store_true', help='変更予定のファイルをすべて表示する')
    args = ap.parse_args()
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(errors='replace')

    total = 0
    changes = []   # (rel, 足したもの, 元, 新)
    warnings = []
    for rel in html_files():
        total += 1
        path = os.path.join(ROOT, rel)
        with open(path, encoding='utf-8', newline='') as f:
            s = f.read()
        lang = page_lang(rel, s)
        new, added, warn = fix_footer(s, lang)
        if warn:
            warnings.append((rel, warn))
        what = [f'フッター: {a}' for a in added]
        if rel in SAMEAS_FILES:
            new2, urls, warn2 = fix_sameas(new)
            if warn2:
                warnings.append((rel, warn2))
            else:
                new = new2
                what += [f'sameAs: {u}' for u in urls]
        if new != s:
            changes.append((rel, what, s, new))

    mode = '[dry-run] ' if args.dry_run else ''
    print(f'{mode}対象のHTML: {total} ファイル / 変更{"予定" if args.dry_run else ""}: {len(changes)} ファイル')
    kinds = {}
    for _, what, _, _ in changes:
        for w in what:
            kinds[w] = kinds.get(w, 0) + 1
    for k in sorted(kinds):
        print(f'  - {k}: {kinds[k]} ファイル')
    if args.verbose:
        for rel, what, _, _ in changes:
            print(f'  {rel}: {", ".join(what)}')
    for rel, warn in warnings:
        print(f'  警告 {rel}: {warn}')

    if changes:
        # 例: フッターと sameAs の両方が変わるファイルがあればそれを、なければ最初のファイル
        ex = next((c for c in changes if any(w.startswith('sameAs') for w in c[1])), changes[0])
        rel, what, s, new = ex
        print(f'\n例: {rel}({", ".join(what)})')
        diff = difflib.unified_diff(s.splitlines(), new.splitlines(), f'a/{rel}', f'b/{rel}', n=0, lineterm='')
        for line in diff:
            print(line)

    if args.dry_run:
        return 0
    for rel, _, _, new in changes:
        with open(os.path.join(ROOT, rel), 'w', encoding='utf-8', newline='') as f:
            f.write(new)
    print(f'\n{len(changes)} ファイルを書き換えた。')
    return 0


if __name__ == '__main__':
    sys.exit(main())
