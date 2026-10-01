#!/usr/bin/env python3
"""sitemap.xml を公開中の全HTMLページから作り直す。

使い方(リポジトリのルートで実行):
    python scripts/generate_sitemap.py            # sitemap.xml を上書き
    python scripts/generate_sitemap.py --check    # 差分があれば終了コード1(書き込みはしない)
    python scripts/generate_sitemap.py --all-git-dates  # 全ページの lastmod を git の最終コミット日で付け直す

ルール:
- 対象はリポジトリ内の *.html(docs/ scripts/ .git/ などは除外)。
  <meta name="robots" content="noindex"> を含むページは載せない。
- URL は canonical があればそれを使い、なければファイルパスから作る(index.html は / で終わるURL)。
- hreflang の相互リンク(xhtml:link)は、各ページの <link rel="alternate" hreflang> をそのまま写す。
- lastmod は、sitemap.xml を最後に更新したコミット以降に変更されたページだけ更新する
  (そのファイルを最後に変更したコミットの日付。未コミットの変更がある・新規ファイルなら今日の日付)。
  それ以外のページは既存の sitemap.xml の lastmod を引き継ぐ(全ページに触れる一括修正で
  lastmod がまとめて更新されてしまうのを防ぐため)。全ページを git の日付で付け直すときは
  --all-git-dates を付ける。
- 並び順と changefreq / priority は、既存の sitemap.xml に同じURLがあればそれを引き継ぐ。
  新しいURLだけ下の RULES で決める。
"""
import datetime
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://yuichi-sato.com/'
SITEMAP = os.path.join(ROOT, 'sitemap.xml')
EXCLUDE_DIRS = {'.git', 'docs', 'scripts', 'node_modules', '.github', '.claude'}

# (パスの正規表現, changefreq, 日本語ページのpriority, 他言語ページのpriority)
RULES = [
    (r'^$', 'weekly', '1.0', '0.9'),
    (r'^column/$', 'weekly', '0.8', '0.8'),
    (r'^apps/$', 'weekly', '0.8', '0.7'),
    (r'^(apps|books|garmin)/[^/]+/$', 'monthly', '0.9', '0.9'),
    (r'^column/.+\.html$', 'monthly', '0.7', '0.7'),
    (r'^(gear|profile)/$', 'monthly', '0.8', '0.7'),
    (r'^privacy/$', 'yearly', '0.3', '0.3'),
    (r'.*', 'monthly', '0.5', '0.5'),
]


def git(*args):
    return subprocess.run(['git', '-C', ROOT] + list(args), capture_output=True, text=True, encoding='utf-8').stdout


def html_files():
    for dp, dns, fns in os.walk(ROOT):
        dns[:] = sorted(d for d in dns if d not in EXCLUDE_DIRS and not d.startswith('.'))
        for fn in sorted(fns):
            if fn.endswith('.html'):
                yield os.path.relpath(os.path.join(dp, fn), ROOT).replace(os.sep, '/')


def lastmod(rel, dirty):
    if rel in dirty:
        return datetime.date.today().isoformat()
    d = git('log', '-1', '--format=%cs', '--', rel).strip()
    return d or datetime.date.today().isoformat()


def changed_since_last_sitemap():
    """sitemap.xml を最後に更新したコミット以降に変更されたファイル(未コミット分を含む)。"""
    status = git('status', '--porcelain', '--untracked-files=all')
    dirty = {line[3:].strip().strip('"').split(' -> ')[-1] for line in status.splitlines()}
    base = git('log', '-1', '--format=%H', '--', 'sitemap.xml').strip()
    changed = set(git('diff', '--name-only', base, 'HEAD').split()) if base else None
    return dirty, changed


def existing_meta():
    meta = {}
    if not os.path.exists(SITEMAP):
        return meta
    s = open(SITEMAP, encoding='utf-8').read()
    for u in re.findall(r'<url>(.*?)</url>', s, re.S):
        loc = re.search(r'<loc>(.*?)</loc>', u).group(1)
        cf = re.search(r'<changefreq>(.*?)</changefreq>', u)
        pr = re.search(r'<priority>(.*?)</priority>', u)
        lm = re.search(r'<lastmod>(.*?)</lastmod>', u)
        meta[loc] = (cf.group(1) if cf else None, pr.group(1) if pr else None, lm.group(1) if lm else None)
    return meta


def rule_for(loc):
    path = loc[len(BASE):]
    lang_path = re.sub(r'^(en|zh)/', '', path)
    is_ja = lang_path == path
    for pat, cf, pr_ja, pr_other in RULES:
        if re.match(pat, lang_path):
            return cf, (pr_ja if is_ja else pr_other)


def build():
    dirty, changed = changed_since_last_sitemap()
    all_git = '--all-git-dates' in sys.argv or changed is None
    old = existing_meta()
    entries = []
    for rel in html_files():
        s = open(os.path.join(ROOT, rel), encoding='utf-8').read()
        if re.search(r'<meta\s+name="robots"\s+content="[^"]*noindex', s, re.I):
            continue
        m = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', s)
        loc = m.group(1) if m else BASE + re.sub(r'index\.html$', '', rel)
        if not loc.startswith(BASE):
            continue
        alts = re.findall(r'<link\s+rel="alternate"\s+hreflang="([^"]+)"\s+href="([^"]+)"', s)
        cf, pr, old_lm = old.get(loc, (None, None, None))
        if not cf or not pr:
            cf, pr = rule_for(loc)
        if all_git or not old_lm or rel in dirty or rel in changed:
            lm = lastmod(rel, dirty)
        else:
            lm = old_lm
        entries.append((loc, lm, cf, pr, alts))
    # 既存の sitemap.xml の並び順を保ち、新しいURLは末尾にURL順で追加する(差分を小さくするため)
    order = {loc: i for i, loc in enumerate(old)}
    entries.sort(key=lambda e: (order.get(e[0], len(order)), e[0]))
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
           '        xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for loc, lm, cf, pr, alts in entries:
        out += ['  <url>', '    <loc>%s</loc>' % loc, '    <lastmod>%s</lastmod>' % lm,
                '    <changefreq>%s</changefreq>' % cf, '    <priority>%s</priority>' % pr]
        for lang, href in alts:
            out.append('    <xhtml:link rel="alternate" hreflang="%s" href="%s"/>' % (lang, href))
        out.append('  </url>')
    out.append('</urlset>')
    return '\n'.join(out) + '\n', len(entries)


def main():
    xml, n = build()
    current = open(SITEMAP, encoding='utf-8').read() if os.path.exists(SITEMAP) else ''
    if '--check' in sys.argv:
        if xml != current:
            print('sitemap.xml is out of date (%d URLs). Run: python scripts/generate_sitemap.py' % n)
            sys.exit(1)
        print('sitemap.xml is up to date (%d URLs)' % n)
        return
    with open(SITEMAP, 'w', encoding='utf-8', newline='\n') as f:
        f.write(xml)
    print('wrote sitemap.xml (%d URLs)' % n)


if __name__ == '__main__':
    main()
