# sato-yuichi-homepage

佐藤雄一の個人サイト。プロフィールとMediaToolboxアプリの紹介ページ。

## ローカルで確認する

`serve.ps1` をダブルクリックするか、PowerShellでこのフォルダに移動して実行:

```
powershell -ExecutionPolicy Bypass -File serve.ps1
```

ブラウザで `http://localhost:8734/` を開く。

## GitHub Pagesへの公開手順（無料）

1. https://github.com でアカウントを作成（すでにあればスキップ）
2. 右上の「+」→「New repository」で新規リポジトリを作成
   - Repository name: `sato-yuichi-homepage`（何でもよい）
   - Public を選択
   - 「Create repository」をクリック
3. このフォルダの中身をアップロード
   - 作成されたリポジトリ画面の「uploading an existing file」リンクから
     `index.html` / `style.css` / `assets` フォルダをドラッグ&ドロップしてコミット
4. リポジトリの「Settings」→左メニュー「Pages」を開く
   - Source を「Deploy from a branch」、Branch を「main」/ 「/(root)」にして Save
5. 数分待つと、ページ上部に公開URL（`https://ユーザー名.github.io/sato-yuichi-homepage/`）が表示される

以後、内容を更新したいときはファイルを差し替えてアップロードし直せば自動的にサイトが更新される。

## sitemap.xml の更新

記事やページを追加・更新したら、リポジトリのルートで次を実行して `sitemap.xml` を作り直す(Python 3 が必要、追加ライブラリは不要)。

```
python scripts/generate_sitemap.py
```

- 公開中の全HTML(`docs/` `scripts/` を除く)から作り直す。`<meta name="robots" content="noindex">` のページは載せない。
- URL は各ページの canonical、hreflang は各ページの `<link rel="alternate" hreflang>` をそのまま使う。
- lastmod は「前回 sitemap.xml を更新したコミット以降に変更したページ」だけ、そのページの最終コミット日(未コミットなら今日)に更新する。それ以外は前の値を引き継ぐ。
- 既存URLの並び順・changefreq・priority は引き継ぎ、新しいURLは末尾に追加する(新規URLの changefreq・priority はスクリプト内の `RULES` で決まる)。
- `python scripts/generate_sitemap.py --check` で、更新が必要かどうかだけを確認できる(必要なら終了コード1)。

`robots.txt` には `Sitemap: https://yuichi-sato.com/sitemap.xml` を記載済み。

## docs/ と scripts/ について

`docs/`(作業メモ・提案書)と `scripts/`(補助スクリプト)は `_config.yml` の `exclude` でサイトの公開対象から外している。ただしこのリポジトリ自体は公開リポジトリなので、GitHub上では誰でも読める。認証情報や非公開にしたい数字は書かないこと。
