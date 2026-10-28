# クローズドテスト中のアプリの「近日公開」表示(公開したら元に戻す)

Google Play でクローズドテスト中の3アプリは、Play のページが一般の人には表示されない(404)。
そのため、Play へ飛ばしていたボタンを、押せない「近日公開」の表示に置き換えた(2026-10-28、ブランチ fix/closed-test-buttons)。
公開(製品版のリリース)したら、このメモの一覧に沿って元の HTML に戻す。

| アプリ | パッケージ名 |
|---|---|
| ハグログ | `com.snaptools.haglog` |
| いまどこシェア(みまもりマップ) | `com.yuichisato.locationshare` |
| GigaPulse | `com.satoyuichi.gigapulse` |

## 置き換えた形

- ボタン: `<a class="play-badge" href="https://play.google.com/store/apps/details?id=<パッケージ名>" target="_blank" rel="noopener">…</a>` を、`<span class="play-badge play-badge-soon" aria-disabled="true">…</span>` にした。
  - 表記: 日本語「近日公開(Google Play で公開準備中)」、英語 "Coming soon on Google Play"、中国語「即将在 Google Play 上架」。狭い画面で「Google Play」の途中で折り返さないよう、HTML では `Google&nbsp;Play` と書いた。
  - 見た目は `style.css` の `.play-badge.play-badge-soon`(色を薄く、影と動きを消し、カーソルを通常に)。
- 構造化データ: トップページ(日英中)の Person の `sameAs` から、ハグログの Play の URL を外した(404 の URL を検索エンジンに伝えないため)。
- 注記: 「リンク先」を指す言い回しを、「Google Play のページ」に直した(リンクがなくなったため)。
- `llms.txt` の3アプリの Play の URL は変えていない(W-10。別途判断)。

## 公開したときの戻し方

1. 下の「ボタン」の表の行を、元の HTML に戻す(`play-badge-soon` で検索すると見つかる)。公開したアプリの分だけ戻す。
2. 「構造化データ」の表の行を、元の位置(readshot の行の次)に戻す。
3. 「注記」は、公開したら注記そのもの(`※ 現在公開準備中…` の行や、料金の段落・FAQ の「公開の準備中」の文)を消すか、公開中の言い回しに直す。
4. 3アプリとも戻したら、`style.css` の `.play-badge.play-badge-soon` の規則は消してよい。
5. `python scripts/generate_sitemap.py` で sitemap を作り直す。

行番号は、元の行が 539247f の時点、変更後の行がこの変更の直後の時点。

## ボタン

| ファイル | 元の行 | 変更後の行 | アプリ | 元の HTML |
|---|---|---|---|---|
| `apps/gigapulse/index.html` | 153 | 153 | GigaPulse | `<a class="play-badge" href="https://play.google.com/store/apps/details?id=com.satoyuichi.gigapulse" target="_blank" rel="noopener">📲 無料でダウンロード</a>` |
| `apps/gigapulse/index.html` | 224 | 224 | GigaPulse | `<a class="play-badge" href="https://play.google.com/store/apps/details?id=com.satoyuichi.gigapulse" target="_blank" rel="noopener">📲 無料でダウンロード</a>` |
| `apps/haglog/index.html` | 163 | 163 | ハグログ | `<a class="play-badge" href="https://play.google.com/store/apps/details?id=com.snaptools.haglog" target="_blank" rel="noopener">📲 無料でダウンロード</a>` |
| `apps/haglog/index.html` | 244 | 244 | ハグログ | `<a class="play-badge" href="https://play.google.com/store/apps/details?id=com.snaptools.haglog" target="_blank" rel="noopener">📲 無料でダウンロード</a>` |
| `apps/index.html` | 284 | 284 | ハグログ | `<a class="play-badge" href="https://play.google.com/store/apps/details?id=com.snaptools.haglog" target="_blank" rel="noopener">Google Playで見る</a>` |
| `apps/index.html` | 299 | 299 | GigaPulse | `<a class="play-badge" href="https://play.google.com/store/apps/details?id=com.satoyuichi.gigapulse" target="_blank" rel="noopener">Google Playで見る</a>` |
| `apps/index.html` | 314 | 314 | いまどこシェア(みまもりマップ) | `<a class="play-badge" href="https://play.google.com/store/apps/details?id=com.yuichisato.locationshare" target="_blank" rel="noopener">Google Playで見る</a>` |
| `apps/mimamori-map/index.html` | 158 | 158 | いまどこシェア(みまもりマップ) | `<a class="play-badge" href="https://play.google.com/store/apps/details?id=com.yuichisato.locationshare" target="_blank" rel="noopener">📲 無料でダウンロード</a>` |
| `apps/mimamori-map/index.html` | 238 | 238 | いまどこシェア(みまもりマップ) | `<a class="play-badge" href="https://play.google.com/store/apps/details?id=com.yuichisato.locationshare" target="_blank" rel="noopener">📲 無料でダウンロード</a>` |
| `en/apps/gigapulse/index.html` | 153 | 153 | GigaPulse | `<a class="play-badge" href="https://play.google.com/store/apps/details?id=com.satoyuichi.gigapulse" target="_blank" rel="noopener">📲 Free Download</a>` |
| `en/apps/gigapulse/index.html` | 224 | 224 | GigaPulse | `<a class="play-badge" href="https://play.google.com/store/apps/details?id=com.satoyuichi.gigapulse" target="_blank" rel="noopener">📲 Free Download</a>` |
| `en/apps/haglog/index.html` | 163 | 163 | ハグログ | `<a class="play-badge" href="https://play.google.com/store/apps/details?id=com.snaptools.haglog" target="_blank" rel="noopener">📲 Free Download</a>` |
| `en/apps/haglog/index.html` | 244 | 244 | ハグログ | `<a class="play-badge" href="https://play.google.com/store/apps/details?id=com.snaptools.haglog" target="_blank" rel="noopener">📲 Free Download</a>` |
| `en/apps/index.html` | 284 | 284 | ハグログ | `<a class="play-badge" href="https://play.google.com/store/apps/details?id=com.snaptools.haglog" target="_blank" rel="noopener">View on Google Play</a>` |
| `en/apps/index.html` | 299 | 299 | GigaPulse | `<a class="play-badge" href="https://play.google.com/store/apps/details?id=com.satoyuichi.gigapulse" target="_blank" rel="noopener">View on Google Play</a>` |
| `en/apps/index.html` | 314 | 314 | いまどこシェア(みまもりマップ) | `<a class="play-badge" href="https://play.google.com/store/apps/details?id=com.yuichisato.locationshare" target="_blank" rel="noopener">View on Google Play</a>` |
| `en/apps/mimamori-map/index.html` | 158 | 158 | いまどこシェア(みまもりマップ) | `<a class="play-badge" href="https://play.google.com/store/apps/details?id=com.yuichisato.locationshare" target="_blank" rel="noopener">📲 Free Download</a>` |
| `en/apps/mimamori-map/index.html` | 237 | 237 | いまどこシェア(みまもりマップ) | `<a class="play-badge" href="https://play.google.com/store/apps/details?id=com.yuichisato.locationshare" target="_blank" rel="noopener">📲 Free Download</a>` |
| `en/index.html` | 693 | 692 | ハグログ | 下の「複数行のボタン」を参照 |
| `en/index.html` | 730 | 729 | GigaPulse | 下の「複数行のボタン」を参照 |
| `en/index.html` | 762 | 761 | いまどこシェア(みまもりマップ) | 下の「複数行のボタン」を参照 |
| `index.html` | 687 | 686 | ハグログ | 下の「複数行のボタン」を参照 |
| `index.html` | 724 | 723 | GigaPulse | 下の「複数行のボタン」を参照 |
| `index.html` | 756 | 755 | いまどこシェア(みまもりマップ) | 下の「複数行のボタン」を参照 |
| `zh/apps/gigapulse/index.html` | 153 | 153 | GigaPulse | `<a class="play-badge" href="https://play.google.com/store/apps/details?id=com.satoyuichi.gigapulse" target="_blank" rel="noopener">📲 免费下载</a>` |
| `zh/apps/gigapulse/index.html` | 224 | 224 | GigaPulse | `<a class="play-badge" href="https://play.google.com/store/apps/details?id=com.satoyuichi.gigapulse" target="_blank" rel="noopener">📲 免费下载</a>` |
| `zh/apps/haglog/index.html` | 163 | 163 | ハグログ | `<a class="play-badge" href="https://play.google.com/store/apps/details?id=com.snaptools.haglog" target="_blank" rel="noopener">📲 免费下载</a>` |
| `zh/apps/haglog/index.html` | 244 | 244 | ハグログ | `<a class="play-badge" href="https://play.google.com/store/apps/details?id=com.snaptools.haglog" target="_blank" rel="noopener">📲 免费下载</a>` |
| `zh/apps/index.html` | 284 | 284 | ハグログ | `<a class="play-badge" href="https://play.google.com/store/apps/details?id=com.snaptools.haglog" target="_blank" rel="noopener">在Google Play查看</a>` |
| `zh/apps/index.html` | 299 | 299 | GigaPulse | `<a class="play-badge" href="https://play.google.com/store/apps/details?id=com.satoyuichi.gigapulse" target="_blank" rel="noopener">在Google Play查看</a>` |
| `zh/apps/index.html` | 314 | 314 | いまどこシェア(みまもりマップ) | `<a class="play-badge" href="https://play.google.com/store/apps/details?id=com.yuichisato.locationshare" target="_blank" rel="noopener">在Google Play查看</a>` |
| `zh/apps/mimamori-map/index.html` | 158 | 158 | いまどこシェア(みまもりマップ) | `<a class="play-badge" href="https://play.google.com/store/apps/details?id=com.yuichisato.locationshare" target="_blank" rel="noopener">📲 免费下载</a>` |
| `zh/apps/mimamori-map/index.html` | 237 | 237 | いまどこシェア(みまもりマップ) | `<a class="play-badge" href="https://play.google.com/store/apps/details?id=com.yuichisato.locationshare" target="_blank" rel="noopener">📲 免费下载</a>` |
| `zh/index.html` | 687 | 686 | ハグログ | 下の「複数行のボタン」を参照 |
| `zh/index.html` | 724 | 723 | GigaPulse | 下の「複数行のボタン」を参照 |
| `zh/index.html` | 756 | 755 | いまどこシェア(みまもりマップ) | 下の「複数行のボタン」を参照 |

### 複数行のボタン(トップページ)

トップページ(`index.html`・`en/index.html`・`zh/index.html`)のボタンは3行で書いてあった。元の HTML は次のとおり(行頭の空白も元のまま)。

`en/index.html` の元の 693 行目から(ハグログ):

```html
          <a class="play-badge" href="https://play.google.com/store/apps/details?id=com.snaptools.haglog" target="_blank" rel="noopener">
            📲 Free Download
          </a>
```

`en/index.html` の元の 730 行目から(GigaPulse):

```html
          <a class="play-badge" href="https://play.google.com/store/apps/details?id=com.satoyuichi.gigapulse" target="_blank" rel="noopener">
            📲 Free Download
          </a>
```

`en/index.html` の元の 762 行目から(いまどこシェア(みまもりマップ)):

```html
          <a class="play-badge" href="https://play.google.com/store/apps/details?id=com.yuichisato.locationshare" target="_blank" rel="noopener">
            📲 Free Download
          </a>
```

`index.html` の元の 687 行目から(ハグログ):

```html
          <a class="play-badge" href="https://play.google.com/store/apps/details?id=com.snaptools.haglog" target="_blank" rel="noopener">
            📲 無料でダウンロード
          </a>
```

`index.html` の元の 724 行目から(GigaPulse):

```html
          <a class="play-badge" href="https://play.google.com/store/apps/details?id=com.satoyuichi.gigapulse" target="_blank" rel="noopener">
            📲 無料でダウンロード
          </a>
```

`index.html` の元の 756 行目から(いまどこシェア(みまもりマップ)):

```html
          <a class="play-badge" href="https://play.google.com/store/apps/details?id=com.yuichisato.locationshare" target="_blank" rel="noopener">
            📲 無料でダウンロード
          </a>
```

`zh/index.html` の元の 687 行目から(ハグログ):

```html
          <a class="play-badge" href="https://play.google.com/store/apps/details?id=com.snaptools.haglog" target="_blank" rel="noopener">
            📲 免费下载
          </a>
```

`zh/index.html` の元の 724 行目から(GigaPulse):

```html
          <a class="play-badge" href="https://play.google.com/store/apps/details?id=com.satoyuichi.gigapulse" target="_blank" rel="noopener">
            📲 免费下载
          </a>
```

`zh/index.html` の元の 756 行目から(いまどこシェア(みまもりマップ)):

```html
          <a class="play-badge" href="https://play.google.com/store/apps/details?id=com.yuichisato.locationshare" target="_blank" rel="noopener">
            📲 免费下载
          </a>
```

## 構造化データ

| ファイル | 元の行 | 元の行の内容 |
|---|---|---|
| `en/index.html` | 44 | `"https://play.google.com/store/apps/details?id=com.snaptools.haglog",` |
| `index.html` | 45 | `"https://play.google.com/store/apps/details?id=com.snaptools.haglog",` |
| `zh/index.html` | 44 | `"https://play.google.com/store/apps/details?id=com.snaptools.haglog",` |

## 注記

| ファイル | 元の行 | 変更後の行 | 元の文 | 変更後の文 |
|---|---|---|---|---|
| `apps/gigapulse/index.html` | 154 | 154 | ※ 現在公開準備中のため、公開までリンク先が表示されない場合があります。 | ※ 現在公開準備中のため、公開までGoogle Playのページが表示されない場合があります。 |
| `apps/gigapulse/index.html` | 225 | 225 | ※ 現在公開準備中のため、公開までリンク先が表示されない場合があります。 | ※ 現在公開準備中のため、公開までGoogle Playのページが表示されない場合があります。 |
| `apps/haglog/index.html` | 164 | 164 | ※ 現在公開準備中のため、公開までリンク先が表示されない場合があります。 | ※ 現在公開準備中のため、公開までGoogle Playのページが表示されない場合があります。 |
| `apps/haglog/index.html` | 245 | 245 | ※ 現在公開準備中のため、公開までリンク先が表示されない場合があります。 | ※ 現在公開準備中のため、公開までGoogle Playのページが表示されない場合があります。 |
| `apps/index.html` | 83 | 83 | 公開までGoogle Playのリンク先が表示されない場合があります。 | 公開までGoogle Playのページが表示されない場合があります。 |
| `apps/index.html` | 202 | 202 | 公開までGoogle Playのリンク先が表示されない場合があります。 | 公開までGoogle Playのページが表示されない場合があります。 |
| `apps/index.html` | 207 | 207 | 公開までGoogle Playのリンク先が表示されない場合があります。 | 公開までGoogle Playのページが表示されない場合があります。 |
| `apps/index.html` | 212 | 212 | 公開までGoogle Playのリンク先が表示されない場合があります。 | 公開までGoogle Playのページが表示されない場合があります。 |
| `apps/index.html` | 285 | 285 | ※ 現在公開準備中のため、公開までリンク先が表示されない場合があります。 | ※ 現在公開準備中のため、公開までGoogle Playのページが表示されない場合があります。 |
| `apps/index.html` | 300 | 300 | ※ 現在公開準備中のため、公開までリンク先が表示されない場合があります。 | ※ 現在公開準備中のため、公開までGoogle Playのページが表示されない場合があります。 |
| `apps/index.html` | 315 | 315 | ※ 現在公開準備中のため、公開までリンク先が表示されない場合があります。 | ※ 現在公開準備中のため、公開までGoogle Playのページが表示されない場合があります。 |
| `apps/index.html` | 341 | 341 | 公開までGoogle Playのリンク先が表示されない場合があります。 | 公開までGoogle Playのページが表示されない場合があります。 |
| `apps/mimamori-map/index.html` | 159 | 159 | ※ 現在公開準備中のため、公開までリンク先が表示されない場合があります。 | ※ 現在公開準備中のため、公開までGoogle Playのページが表示されない場合があります。 |
| `apps/mimamori-map/index.html` | 239 | 239 | ※ 現在公開準備中のため、公開までリンク先が表示されない場合があります。 | ※ 現在公開準備中のため、公開までGoogle Playのページが表示されない場合があります。 |
| `en/apps/gigapulse/index.html` | 154 | 154 | * Still preparing for release — this link may not work until it goes live. | * Still preparing for release — the Google Play page may not be available until it goes live. |
| `en/apps/gigapulse/index.html` | 225 | 225 | * Still preparing for release — this link may not work until it goes live. | * Still preparing for release — the Google Play page may not be available until it goes live. |
| `en/apps/haglog/index.html` | 164 | 164 | * Still preparing for release — this link may not work until it goes live. | * Still preparing for release — the Google Play page may not be available until it goes live. |
| `en/apps/haglog/index.html` | 245 | 245 | * Still preparing for release — this link may not work until it goes live. | * Still preparing for release — the Google Play page may not be available until it goes live. |
| `en/apps/index.html` | 83 | 83 | so their Google Play links may not open until they go live. | so their Google Play pages may not be available until they go live. |
| `en/apps/index.html` | 202 | 202 | Still being prepared for release, so the Google Play link may not open until it goes live. | Still being prepared for release, so the Google Play page may not be available until it goes live. |
| `en/apps/index.html` | 207 | 207 | Still being prepared for release, so the Google Play link may not open until it goes live. | Still being prepared for release, so the Google Play page may not be available until it goes live. |
| `en/apps/index.html` | 212 | 212 | Still being prepared for release, so the Google Play link may not open until it goes live. | Still being prepared for release, so the Google Play page may not be available until it goes live. |
| `en/apps/index.html` | 285 | 285 | Note: this app is still being prepared for release, so the store link may not open until it goes live. | Note: this app is still being prepared for release, so the Google Play page may not be available until it goes live. |
| `en/apps/index.html` | 300 | 300 | Note: this app is still being prepared for release, so the store link may not open until it goes live. | Note: this app is still being prepared for release, so the Google Play page may not be available until it goes live. |
| `en/apps/index.html` | 315 | 315 | Note: this app is still being prepared for release, so the store link may not open until it goes live. | Note: this app is still being prepared for release, so the Google Play page may not be available until it goes live. |
| `en/apps/index.html` | 341 | 341 | so their Google Play links may not open until they go live. | so their Google Play pages may not be available until they go live. |
| `en/apps/mimamori-map/index.html` | 159 | 159 | * Still preparing for release — this link may not work until it goes live. | * Still preparing for release — the Google Play page may not be available until it goes live. |
| `en/apps/mimamori-map/index.html` | 238 | 238 | * Still preparing for release — this link may not work until it goes live. | * Still preparing for release — the Google Play page may not be available until it goes live. |
| `en/index.html` | 696 | 695 | * Still preparing for release — this link may not work until it goes live. | * Still preparing for release — the Google Play page may not be available until it goes live. |
| `en/index.html` | 733 | 732 | * Still preparing for release — this link may not work until it goes live. | * Still preparing for release — the Google Play page may not be available until it goes live. |
| `en/index.html` | 765 | 764 | * Still preparing for release — this link may not work until it goes live. | * Still preparing for release — the Google Play page may not be available until it goes live. |
| `index.html` | 690 | 689 | ※ 現在公開準備中のため、公開までリンク先が表示されない場合があります。 | ※ 現在公開準備中のため、公開までGoogle Playのページが表示されない場合があります。 |
| `index.html` | 727 | 726 | ※ 現在公開準備中のため、公開までリンク先が表示されない場合があります。 | ※ 現在公開準備中のため、公開までGoogle Playのページが表示されない場合があります。 |
| `index.html` | 759 | 758 | ※ 現在公開準備中のため、公開までリンク先が表示されない場合があります。 | ※ 現在公開準備中のため、公開までGoogle Playのページが表示されない場合があります。 |
| `zh/apps/gigapulse/index.html` | 154 | 154 | ※ 目前处于上线准备阶段，正式上线前链接可能暂时无法显示。 | ※ 目前处于上线准备阶段，正式上线前Google Play页面可能暂时无法显示。 |
| `zh/apps/gigapulse/index.html` | 225 | 225 | ※ 目前处于上线准备阶段，正式上线前链接可能暂时无法显示。 | ※ 目前处于上线准备阶段，正式上线前Google Play页面可能暂时无法显示。 |
| `zh/apps/haglog/index.html` | 164 | 164 | ※ 目前处于上线准备阶段，正式上线前链接可能暂时无法显示。 | ※ 目前处于上线准备阶段，正式上线前Google Play页面可能暂时无法显示。 |
| `zh/apps/haglog/index.html` | 245 | 245 | ※ 目前处于上线准备阶段，正式上线前链接可能暂时无法显示。 | ※ 目前处于上线准备阶段，正式上线前Google Play页面可能暂时无法显示。 |
| `zh/apps/index.html` | 83 | 83 | 上架前Google Play链接可能无法打开。 | 上架前Google Play页面可能无法打开。 |
| `zh/apps/index.html` | 202 | 202 | 上架前Google Play链接可能无法打开。 | 上架前Google Play页面可能无法打开。 |
| `zh/apps/index.html` | 207 | 207 | 上架前Google Play链接可能无法打开。 | 上架前Google Play页面可能无法打开。 |
| `zh/apps/index.html` | 212 | 212 | 上架前Google Play链接可能无法打开。 | 上架前Google Play页面可能无法打开。 |
| `zh/apps/index.html` | 285 | 285 | ※ 目前正在准备上架，上架前链接可能无法打开。 | ※ 目前正在准备上架，上架前Google Play页面可能无法打开。 |
| `zh/apps/index.html` | 300 | 300 | ※ 目前正在准备上架，上架前链接可能无法打开。 | ※ 目前正在准备上架，上架前Google Play页面可能无法打开。 |
| `zh/apps/index.html` | 315 | 315 | ※ 目前正在准备上架，上架前链接可能无法打开。 | ※ 目前正在准备上架，上架前Google Play页面可能无法打开。 |
| `zh/apps/index.html` | 341 | 341 | 上架前Google Play链接可能无法打开。 | 上架前Google Play页面可能无法打开。 |
| `zh/apps/mimamori-map/index.html` | 159 | 159 | ※ 目前处于上线准备阶段，正式上线前链接可能暂时无法显示。 | ※ 目前处于上线准备阶段，正式上线前Google Play页面可能暂时无法显示。 |
| `zh/apps/mimamori-map/index.html` | 238 | 238 | ※ 目前处于上线准备阶段，正式上线前链接可能暂时无法显示。 | ※ 目前处于上线准备阶段，正式上线前Google Play页面可能暂时无法显示。 |
| `zh/index.html` | 690 | 689 | ※ 目前处于上线准备阶段，正式上线前链接可能暂时无法显示。 | ※ 目前处于上线准备阶段，正式上线前Google Play页面可能暂时无法显示。 |
| `zh/index.html` | 727 | 726 | ※ 目前处于上线准备阶段，正式上线前链接可能暂时无法显示。 | ※ 目前处于上线准备阶段，正式上线前Google Play页面可能暂时无法显示。 |
| `zh/index.html` | 759 | 758 | ※ 目前处于上线准备阶段，正式上线前链接可能暂时无法显示。 | ※ 目前处于上线准备阶段，正式上线前Google Play页面可能暂时无法显示。 |
