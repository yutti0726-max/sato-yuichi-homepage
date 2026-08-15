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
