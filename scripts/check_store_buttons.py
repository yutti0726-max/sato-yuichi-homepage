# -*- coding: utf-8 -*-
"""ストアのボタンの点検(公開待ちのアプリのボタンを、公開の日に切り替えるため)。

台帳: scripts/store_buttons.json(state が pending か live)。
手順: ホームページの作業の手順書(web-seo の store-button-switch.md)

使い方(サイトのフォルダで):
  python -I scripts/check_store_buttons.py            # 外へ通信しない点検(公開の前に毎回)
  python -I scripts/check_store_buttons.py --app gigapulse
                                                      # 切り替えのときに直す行の一覧(札・注記・FAQ・llms.txt)
  python -I scripts/check_store_buttons.py --live     # 公開待ちのストアのページが開くか(1件1回。--max で上限)

外へ通信しない点検で見ること:
  1. 近日公開の札(play-badge-soon)に data-pending="<slug>:<store>" があり、台帳で pending であること
  2. ストアの URL(a の href・JSON-LD・本文・llms.txt のどこでも)が、台帳で live のものだけであること
     (公開待ちのものと台帳に無いものは止める。未公開のページへ案内しない)
  3. live のストアへ、そのアプリの紹介ページ(日英中)からリンクがあること
  4. live になったストアの札(data-pending)が残っていないこと
  5. すべての HTML の JSON-LD が読めること
問題があれば一覧を出して終了コード 1 で終わる。
"""
import argparse
import json
import pathlib
import re
import sys
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
REG = ROOT / "scripts" / "store_buttons.json"
LANGS = ("", "en/", "zh/")
SKIP_DIRS = {".git", "node_modules", "scripts"}
# 公開待ちを表す言い回し(--app で直す行を探す)
PENDING_WORDS = re.compile(
    r"近日公開|公開準備中|準備中|公開の準備|Coming soon|in preparation|being prepared|preparing for release"
    r"|即将|准备|準備|尚未上架", re.I)
# ストアの URL(href・JSON-LD・本文・llms.txt のどこにあっても拾う)
STORE_URL = re.compile(r"https?://(?:play\.google\.com|apps\.apple\.com|apps\.microsoft\.com)/[^\s\"'<>)\]]+")
STORE_NAMES = {"play": "Google Play", "appstore": "App Store", "msstore": "Microsoft Store"}


def store_key(url):
    """URL をストアと識別子の組にする(言語や国の部分の違いを無視して比べる)。"""
    if not url:
        return None
    m = re.search(r"play\.google\.com/store/apps/details\?(?:[^\"'#\s]*&)?id=([A-Za-z0-9._]+)", url)
    if m:
        return ("play", m.group(1))
    m = re.search(r"apps\.apple\.com/[^\"'#\s]*?id(\d{9,10})", url)
    if m:
        return ("appstore", m.group(1))
    m = re.search(r"apps\.microsoft\.com/(?:[a-z-]+/)?detail/([0-9A-Za-z]{12})", url)
    if m:
        return ("msstore", m.group(1).lower())
    return None


def load():
    entries = json.loads(REG.read_text(encoding="utf-8"))["entries"]
    for e in entries:
        if e["state"] not in ("pending", "live"):
            sys.exit(f"台帳の state が不正: {e}")
        if e["state"] == "live" and not e.get("url"):
            sys.exit(f"live なのに URL が無い: {e}")
    return entries


def pages():
    for p in sorted(ROOT.rglob("*.html")):
        if not SKIP_DIRS.intersection(p.relative_to(ROOT).parts):
            yield p


def rel(p):
    return p.relative_to(ROOT).as_posix()


def static_check(entries):
    errors = []
    pending = {f'{e["slug"]}:{e["store"]}' for e in entries if e["state"] == "pending"}
    live = {f'{e["slug"]}:{e["store"]}' for e in entries if e["state"] == "live"}
    pending_keys = {store_key(e["url"]): e for e in entries if e["state"] == "pending" and e.get("url")}
    live_keys = {store_key(e["url"]) for e in entries if e["state"] == "live"}

    def url_problem(k):
        """live の URL なら None。公開待ちか台帳に無い URL なら、その理由。"""
        if k is None or k in live_keys:
            return None  # ストアの開発者のページなど、アプリのページではない URL は見ない
        if k in pending_keys:
            e = pending_keys[k]
            return f"公開待ちの {e['name']}({STORE_NAMES[e['store']]})へリンクしている"
        return (f"台帳に無いストアの URL({STORE_NAMES[k[0]]} {k[1]})。"
                "台帳に足し、公開を確かめるまでリンクしない")

    texts = {p: p.read_text(encoding="utf-8") for p in pages()}
    n_badge = 0
    for p, s in texts.items():
        # 1・4: 札
        for m in re.finditer(r"<[a-z]+\b[^>]*class=\"[^\"]*play-badge-soon[^\"]*\"[^>]*>", s):
            n_badge += 1
            line = s.count("\n", 0, m.start()) + 1
            d = re.search(r'data-pending="([^"]+)"', m.group(0))
            if not d:
                errors.append(f"{rel(p)}:{line}: 札に data-pending が無い")
            elif d.group(1) in live:
                errors.append(f"{rel(p)}:{line}: {d.group(1)} は live なのに札が残っている")
            elif d.group(1) not in pending:
                errors.append(f"{rel(p)}:{line}: {d.group(1)} が台帳に無い")
        # 2: ストアの URL(href・JSON-LD・本文のどこでも)は live のものだけ
        flat = s.replace("&amp;", "&")
        for m in STORE_URL.finditer(flat):
            msg = url_problem(store_key(m.group(0)))
            if msg:
                line = flat.count("\n", 0, m.start()) + 1
                errors.append(f"{rel(p)}:{line}: {msg}")
        # 5: JSON-LD
        for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
            try:
                json.loads(m.group(1))
            except json.JSONDecodeError as ex:
                line = s.count("\n", 0, m.start()) + 1
                errors.append(f"{rel(p)}:{line}: JSON-LD が読めない({ex.msg})")
    llms = ROOT / "llms.txt"
    if llms.exists():
        for i, line in enumerate(llms.read_text(encoding="utf-8").splitlines(), 1):
            for m in STORE_URL.finditer(line):
                msg = url_problem(store_key(m.group(0)))
                if msg:
                    errors.append(f"llms.txt:{i}: {msg}")
    # 3: live のストアへのリンクが、紹介ページ(日英中)にあること
    for e in entries:
        if e["state"] != "live":
            continue
        for lang in LANGS:
            p = ROOT / f"{lang}apps/{e['slug']}/index.html"
            if not p.exists():
                errors.append(f"{rel(p)}: 紹介ページが無い")
                continue
            keys = {store_key(h.replace("&amp;", "&")) for h in re.findall(r'href="([^"]+)"', texts[p])}
            if store_key(e["url"]) not in keys:
                errors.append(f"{rel(p)}: {e['name']}({STORE_NAMES[e['store']]})へのボタンが無い")
    return errors, n_badge, len(texts)


def lines_for_app(entries, slug):
    """切り替えのときに見直す行(そのアプリに触れていて、公開待ちの言い回しがある行)。"""
    names = {e["name"] for e in entries if e["slug"] == slug}
    names |= {slug}
    extra = {"mimamori-map": {"Imadoko Share", "现在在哪儿", "いまどこシェア"},
             "mamori-note": {"Mamori Note", "守护笔记", "守護筆記"}}.get(slug, set())
    names |= extra
    own = {f"{lang}apps/{slug}/index.html" for lang in LANGS}
    files = list(pages()) + [ROOT / "llms.txt"]
    out = []
    for p in files:
        if not p.exists():
            continue
        r = rel(p)
        if "/privacy" in r:
            continue
        ls = p.read_text(encoding="utf-8").splitlines()
        # 名前・紹介ページへのリンク・札の印のある行(注記や料金の行は、その前後の行に名前がある)
        mark = [any(n in x for n in names) or f'/apps/{slug}/' in x or f'data-pending="{slug}:' in x for x in ls]
        for i, line in enumerate(ls):
            if not PENDING_WORDS.search(line):
                continue
            if r in own or any(mark[max(0, i - 3):i + 4]):
                out.append(f"{r}:{i + 1}: {line.strip()[:160]}")
    return out


def live_check(entries, limit):
    """公開待ちのストアのページが、ログインなしで開くか(200 なら公開、404 なら未公開)。"""
    n = 0
    for e in entries:
        if e["state"] != "pending":
            continue
        if not e.get("url"):
            print(f"  {e['name']}({STORE_NAMES[e['store']]}): URL 未登録(公開の知らせを受けたら台帳に入れる)")
            continue
        if n >= limit:
            print(f"  上限 {limit} 回に達したので、残りは見ていない")
            break
        url = e["url"] + ("&hl=ja" if e["store"] == "play" else "")
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (store-button-check)"})
        n += 1
        try:
            with urllib.request.urlopen(req, timeout=20) as res:
                code = res.status
        except urllib.error.HTTPError as ex:
            code = ex.code
        except urllib.error.URLError as ex:
            code = f"失敗({ex.reason})"
        verdict = {200: "公開(切り替えの対象)", 404: "未公開"}.get(code, "要確認")
        print(f"  {e['name']}({STORE_NAMES[e['store']]}): {code} {verdict}")
    print(f"外への通信: {n} 回")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--app", help="切り替えるアプリの slug(apps/<slug>/)")
    ap.add_argument("--live", action="store_true", help="公開待ちのストアのページが開くかを見る")
    ap.add_argument("--max", type=int, default=30, help="--live の通信の上限(既定 30)")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    entries = load()
    if a.live:
        live_check(entries, a.max)
        return
    if a.app:
        if a.app not in {e["slug"] for e in entries}:
            sys.exit(f"台帳に無い slug: {a.app}")
        rows = lines_for_app(entries, a.app)
        print(f"{a.app}: 見直す行 {len(rows)}")
        print("\n".join(rows))
        return
    errors, n_badge, n_pages = static_check(entries)
    print(f"HTML {n_pages} ページ、近日公開の札 {n_badge}、台帳 {len(entries)} 件"
          f"(pending {sum(e['state'] == 'pending' for e in entries)})")
    if errors:
        print(f"問題 {len(errors)} 件:")
        print("\n".join("  " + x for x in errors))
        sys.exit(1)
    print("問題なし")


if __name__ == "__main__":
    main()
