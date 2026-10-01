# 収益化14日プラン 実施レポート

実施日: 2026-09-29(Day 0)
ブランチ: `feature/monetize-14days`

対象リポジトリ(指示書の【設定】がプレースホルダーのままだったため、実在するパスを使用):

| 区分 | パス | 作業内容 |
|---|---|---|
| HP | `C:\Users\yutti\sato-yuichi-homepage`(GitHub Pages / yuichi-sato.com) | 変更・コミット・PR |
| Android | `C:\Users\yutti\Media Toolbox` / `PdfToolkit` / `SeniorPedometer` / `Readshot` / `HagLog` | 読み取りのみ |
| Garmin | `C:\Users\yutti\garmin-watchface`(Aurum) / `garmin-overwatch` / `garmin-empress` / `garmin-cairn` / `garmin-cairn-cycle` / `garmin-multitime` | 読み取りのみ |

---

## 1. 実施した変更の一覧(ファイル単位)

### タスクA: トップページのSEOメタ情報

| ファイル | 変更内容 |
|---|---|
| `index.html` | title / og:title / twitter:title を「佐藤雄一 公式サイト｜自作PC・Garminウォッチフェイス・Androidアプリ・Kindle本」に変更。description / og:description / twitter:description を4領域に触れる116文字の文に変更。og:site_name を他ページと同じ「佐藤雄一 公式サイト」に統一。アプリ欄に `/apps/` へのリンクを追加 |
| `en/index.html` | 同じ方針で英語の title / description を変更、`/en/apps/` へのリンクを追加 |
| `zh/index.html` | 同じ方針で中国語の title / description を変更、`/zh/apps/` へのリンクを追加 |
| `apps/index.html`(新規) | アプリ一覧ページ。旧トップの「Androidアプリでこれだけは入れておきたいアプリ特集 \| 佐藤雄一」の title・description を移設 |
| `en/apps/index.html`(新規) | 同上(英語。旧 en トップの title・description) |
| `zh/apps/index.html`(新規) | 同上(中国語。旧 zh トップの title・description) |

全ページ(213ページ+新規7ページ)の title / description / canonical / og:title / og:description を一括チェックした結果、**空欄・重複・canonical の誤りはありませんでした**(既存ページは修正不要)。

### タスクB: sitemap.xml と robots.txt

| ファイル | 変更内容 |
|---|---|
| `scripts/generate_sitemap.py`(新規) | 公開中の全HTMLから sitemap.xml を作り直すスクリプト(Python 3、追加ライブラリ不要) |
| `sitemap.xml` | 新規7URL(`/apps/` ×3言語、自作PC構成記事4本)を追加。今回変更した7ページの lastmod を 2026-09-29 に更新(213 → 220 URL) |
| `README.md` | sitemap の更新方法と、docs/ scripts/ の扱いを追記 |
| `_config.yml`(新規) | GitHub Pages(Jekyll)で `docs/` と `scripts/` をサイトの公開対象から除外 |
| `robots.txt` | 変更なし(`Sitemap: https://yuichi-sato.com/sitemap.xml` が既に記載済み) |

### タスクC: Garminページの導線強化

| ファイル | 変更内容 |
|---|---|
| `index.html` / `en/index.html` / `zh/index.html` | Garmin欄の末尾に「無料版とPro版の比較」(Cairn / Cairn Cycle / Multitime の3組の比較表+各ストアボタン)と「有料版の無料お試し」一覧(6本の試用条件・価格・ストアリンク)を追加 |
| `style.css` | 比較表用の `.compare-block` を追加(記事内の表と同じ値) |
| `docs/garmin_store_update_proposal.md`(新規) | 対応機種の現状、SDKのデバイス定義と比べた追加候補、無料版冒頭のPro案内文(英日)、有料版6本の説明文改善案(英語、各約300語) |

### タスクD: 自作PC構成記事

| ファイル | 変更内容 |
|---|---|
| `docs/drafts/pc-build-budget-150k-gaming.html`(下書き) | 予算15万円のゲーミングPC構成。**公開見送り**(2026-10-01時点の価格では合計約36万円で題名と合わないため) |
| `docs/drafts/pc-build-budget-200k-video-editing.html`(下書き) | 予算20万円の動画編集用PC構成。**公開見送り**(同、合計約49万円) |
| `column/pc-build-rtx5060ti-vs-egpu.html`(新規) | RTX 5060 Ti構成と外付けGPU(eGPU)の比較 |
| `column/home-office-desk-setup.html`(新規) | 在宅ワーク用デスク環境の一式 |
| `column/index.html` | 自作PC欄の先頭に公開する2本(eGPU比較・在宅ワーク環境)を登録 |
| `column/pc-parts-priority-cpu-memory-gpu.html` / `column/pc-case-airflow-build-planning.html` / `column/portable-egpu-desk-setup.html` | 本文末尾(著者欄の前)に「用途別の構成例」として公開する2本への内部リンクを追加 |

### タスクE・F・レポート

| ファイル | 変更内容 |
|---|---|
| `docs/android_monetization_audit.md`(新規) | Android 5本の AdMob / UMP / Billing / バージョン / targetSdk の調査と、課金を入れる場合の手順・工数 |
| `docs/kindle_backmatter.md`(新規) | Kindle本4冊の巻末原稿と KDPセレクトの注意点 |
| `docs/REPORT_monetize_14days.md`(新規) | このレポート |

Android・Garmin のリポジトリは一切変更していません(読み取りのみ)。

---

## 2. TODO(要確認)と TODO(画像)の全件リスト

| # | ファイル:行 | 種別 | 内容 |
|---|---|---|---|
| 1 | `column/home-office-desk-setup.html:115` | TODO(画像) | 構成全体またはデスクの写真(著者撮影)を入れる |
| 2 | `column/pc-build-rtx5060ti-vs-egpu.html:115` | TODO(画像) | 構成全体またはデスクの写真(著者撮影)を入れる |
| 3 | `docs/android_monetization_audit.md:61` | TODO(要確認) | - **注意: 作業ツリーに未コミットの変更が33件あります**(`app/build.gradle.kts`・`AndroidManife |
| 4 | `docs/android_monetization_audit.md:71` | TODO(要確認) | - **注意: 作業ツリーに未コミットの変更が18件あります**(`app/build.gradle.kts` で versionCode  |
| 5 | `docs/drafts/pc-build-budget-150k-gaming.html:115` | TODO(画像) | 構成全体またはデスクの写真(著者撮影)を入れる |
| 6 | `docs/drafts/pc-build-budget-150k-gaming.html:122` | TODO(要確認) | 価格の目安 |
| 7 | `docs/drafts/pc-build-budget-150k-gaming.html:123` | TODO(要確認) | 価格の目安 |
| 8 | `docs/drafts/pc-build-budget-150k-gaming.html:124` | TODO(要確認) | 価格の目安 |
| 9 | `docs/drafts/pc-build-budget-150k-gaming.html:125` | TODO(要確認) | 価格の目安 |
| 10 | `docs/drafts/pc-build-budget-150k-gaming.html:126` | TODO(要確認) | 価格の目安 |
| 11 | `docs/drafts/pc-build-budget-150k-gaming.html:127` | TODO(要確認) | 価格の目安 |
| 12 | `docs/drafts/pc-build-budget-150k-gaming.html:128` | TODO(要確認) | 価格の目安 |
| 13 | `docs/drafts/pc-build-budget-150k-gaming.html:129` | TODO(要確認) | 価格の目安 |
| 14 | `docs/drafts/pc-build-budget-150k-gaming.html:133` | TODO(要確認) | 合計金額 |
| 15 | `docs/drafts/pc-build-budget-200k-video-editing.html:115` | TODO(画像) | 構成全体またはデスクの写真(著者撮影)を入れる |
| 16 | `docs/drafts/pc-build-budget-200k-video-editing.html:122` | TODO(要確認) | 価格の目安 |
| 17 | `docs/drafts/pc-build-budget-200k-video-editing.html:123` | TODO(要確認) | 価格の目安 |
| 18 | `docs/drafts/pc-build-budget-200k-video-editing.html:124` | TODO(要確認) | 価格の目安 |
| 19 | `docs/drafts/pc-build-budget-200k-video-editing.html:125` | TODO(要確認) | 価格の目安 |
| 20 | `docs/drafts/pc-build-budget-200k-video-editing.html:126` | TODO(要確認) | 価格の目安 |
| 21 | `docs/drafts/pc-build-budget-200k-video-editing.html:127` | TODO(要確認) | 価格の目安 |
| 22 | `docs/drafts/pc-build-budget-200k-video-editing.html:128` | TODO(要確認) | 価格の目安 |
| 23 | `docs/drafts/pc-build-budget-200k-video-editing.html:129` | TODO(要確認) | 価格の目安 |
| 24 | `docs/drafts/pc-build-budget-200k-video-editing.html:133` | TODO(要確認) | 合計金額 |
| 25 | `docs/kindle_backmatter.md:21` | TODO(要確認) | - 巻末のリンクには、**Amazon アソシエイトのトラッキングID(`?tag=...`)を付けない**でください。Amazon アソシ |
| 26 | `docs/kindle_backmatter.md:190` | TODO(画像) | > MY 100 DIVES が紙の本(ペーパーバック)として販売されている場合、巻末のURLはクリックできないため、QRコードの併記を検討 |

合計 26 件(TODO(要確認) 21 件、TODO(画像) 5 件。`docs/drafts/` の下書き2本の分を含む)。行番号は 2026-10-01 時点。再生成: `git grep -n -e "TODO(要確認)" -e "TODO(画像)" -- ":!docs/REPORT_monetize_14days.md"`

### ファイル内のマーカー以外で、確認が必要な事項

| # | 内容 | 関連ファイル |
|---|---|---|
| 1 | (対応済み 2026-10-01)**Multitime Pro の同時タイマー数**: 「無制限」表記を実装どおり「最大20個」に統一した。HP(トップ・個別ページ ja/en/zh、llms.txt)はこのPRで修正、ストアは Multitime / Multitime Pro の英日説明文を修正済み | `garmin/multitime/index.html` ほか |
| 2 | **Multitime Pro の日本語説明文がストアに無い**(公開APIの掲載言語が英語のみ。他の8本は英日両方) | `docs/garmin_store_update_proposal.md` |
| 3 | (取り下げ)当初「Aurum / Empress の manifest にある `quatix847mm` がSDKに無い」と書いたが、manifest のコメント内のメモを誤って拾っていた。実際の対応機種は3本とも13機種で、問題なし | `docs/garmin_store_update_proposal.md` |
| 4 | **らくらく歩数計・Readshot の未コミット変更**(33件・18件)。GitHubにバックアップされていない | `docs/android_monetization_audit.md` |
| 5 | **電子書籍内のアソシエイトリンク**: 巻末原稿はタグを外したURLにしてある。Amazonアソシエイト規約の該当条文は未確認 | `docs/kindle_backmatter.md` |
| 6 | **構成記事の本文**: 型番は実在を確認済みだが、筆者自身の実機検証にもとづく記述ではない部分がある(特に15万円・20万円構成)。公開前に筆者の経験・判断を加筆することを推奨 | `column/pc-build-*.html` |

---

## 3. 人間が行う作業のチェックリスト

Day 0 = 2026-09-29(火)

- [ ] **Day 0(9/29)**: Readshot・ハグログのクローズドテストに15〜20名を登録し、全員のオプトインを確認。開始日を記録
- [ ] **Day 0(9/29)**: Play Console で公開済み3アプリ(MediaToolbox・PDFツールキット・らくらく歩数計)の収益化設定を確認
- [ ] **Day 0(9/29)**: らくらく歩数計・Readshot の未コミット変更をコミット・push(上の表の#4)
- [ ] **Day 1(9/30)**: PR を確認してマージ。Search Console で sitemap.xml を送信し、トップページのインデックス登録をリクエスト
  - 構成記事4本は「価格確認中」の表示のまま公開されます。価格を埋めてから公開したい場合は、マージ前にTODOを埋めるか、記事4本を別PRに分けてください
  - マージ後、`https://yuichi-sato.com/docs/REPORT_monetize_14days.md` が 404 になること(docs/ が公開されていないこと)を確認
- [ ] **Day 1〜2(9/30〜10/1)**: `docs/garmin_store_update_proposal.md` の説明文を Connect IQ ストアに反映(「詳細を編集」から。英日両方。Multitime の「無制限」表記の判断を先に)
- [ ] **Day 2(10/1)**: KDP の本棚で4冊の KDPセレクト登録状況を確認し、未登録なら登録(Amazon 以外での電子書籍配信がないことを確認してから)。巻末原稿(`docs/kindle_backmatter.md`)を差し替える場合は同時に再出版
- [ ] **Day 3〜14(10/2〜10/13)**: 構成記事の価格・画像の TODO を埋めて公開。公開ごとに `python scripts/generate_sitemap.py` を実行し、Search Console でインデックス登録をリクエスト
- [ ] **Day 14(10/13)**: テスターが12名以上残っていることを確認し、本番公開へのアクセスを申請

---

## 4. 実行中に判断した事項とその理由

1. **対象パスの特定**: 指示書の【設定】が `C:\path\to\...` のままだったため、ホームディレクトリにある実在のリポジトリ(上表)を対象にした。HPは `CNAME` が `yuichi-sato.com` の `sato-yuichi-homepage`。
2. **「アプリ一覧ページ」の新設**: HPにはアプリ一覧ページが存在しなかった(アプリはトップの `#works` 欄と個別ページのみ)。旧トップの title・description の移し先として `/apps/`(ja/en/zh)を新設した。旧 title は既存の個別ページと重複しないため、比較して残す判断は不要だった。
3. **既存ページのメタ情報は変更せず**: 全ページを機械的にチェックし、空欄・重複・canonical の誤りが無かったため、トップ以外は触っていない。
4. **sitemap の lastmod**: 既存の sitemap.xml は、9/26 の全ページ一括修正後も多くのページの lastmod を 9/14 のまま据え置いていた。これを尊重し、スクリプトは「前回 sitemap.xml を更新したコミット以降に変更したページだけ lastmod を更新」する方式にした。並び順・priority も既存を引き継ぎ、差分を最小にした。
5. **`_config.yml` の追加**: このリポジトリは公開リポジトリで、GitHub Pages(Jekyll、legacy ビルド)は `docs/*.md` をそのままサイトに公開してしまう。作業用の提案書・調査結果が yuichi-sato.com 上で読めないよう、`docs/` と `scripts/` を除外した。GitHub上では読めるため、収益額などの非公開の数字は docs に書いていない。
6. **比較表の置き場所**: HPに Garmin 専用の一覧ページは無く、トップの `#garmin` 欄が「Garminページ」にあたるため、ここに追加した。Cairn / Cairn Cycle / Multitime の個別ページには既に比較表があったので変更していない。英語版に加え、同じ構造の中国語版にも反映した。
7. **「トライアルあり」の表記**: トップのカードには既に「24時間無料お試し」「5アクティビティ無料お試し」のバッジとストアボタンがあったため、カードは変更せず、6本の試用条件をまとめた一覧表を追加した。Multitime Pro は「期間限定の試用」ではなく「タイマー3個まで無期限で無料」なので、表ではそのとおりに書いた(「トライアルあり」とは書いていない)。
8. **Pro版の機能差はソースから確認**: 比較表の内容は、HP・ストアの既存文言ではなく各リポジトリのソース(`metricList()`、`Config.mc`、`FREE_USES = 5` など)で確認した。その結果、Multitime Pro の上限が「無制限」ではなく20個であることが分かった(上の#1)。
9. **追加候補機種の範囲**: SDKのデバイス定義で機械的に条件(アプリ種別・API レベル)を満たす機種のうち、Connect IQ 5.0 以上の現行世代だけを載せた。文字盤は既存と同じ解像度の AMOLED 円形機に限定した(既存の画像リソースを流用できるため)。販売台数・人気は確認していないため、優先度は「既存対応機の後継かどうか」で付けた。
10. **構成記事の型番**: メーカー・販売店のページで実在を確認できた型番だけを使った(RTX 5060 Ti 16GB は ASUS DUAL-RTX5060TI-O16G など)。価格は一切書かず、表示は「価格確認中」、HTMLコメントに `TODO(要確認)` を残した(公開ページに「TODO」という文字列を出さないため)。
11. **構成記事のリンク**: 新しい製品は Amazon の検索結果リンク(`tag=yuttitti-22`)にした。楽天は既存ページのリンク(個別のアフィリエイトURL)を新規に作れないため、在宅ワーク記事で既存の楽天リンクを流用した2製品以外には付けていない。在宅ワーク記事は「おすすめ機材」ページの既存リンクをそのまま使った。
12. **広告表記**: 指示どおり末尾にアフィリエイト表記を置いたうえで、ステルスマーケティング規制を考慮し、冒頭にも短い【広告】表記を入れた(既存の「おすすめ機材」ページと同じ `disclosure-box`)。
13. **構成記事は日本語版のみ**: 既存コラムは英中版もあるが、今回は下書き扱いのため日本語版だけを作った。言語切替の EN / 中 は各言語のコラム一覧に飛ぶようにした。
14. **絵文字**: 既存ページのボタンには絵文字(📲・⌚)があるが、指示に従い今回追加した部分では使っていない。
15. **Kindle巻末のリンク**: 電子書籍内でのアソシエイトリンク使用は Amazon の規約で認められていないと理解しているため、HPの短縮URLから `?tag=` を外したものを使った(規約本文は未確認のため上の#5)。
16. **Androidの調査**: 広告ユニットIDの値は出力・記載せず、「本番ID / テストID / なし」の区分だけにした。`local.properties`・keystore・`google-services.json` は読んでいない。
17. **画像**: 画像は作成していない。必要な箇所は `TODO(画像)` として残した。

---

## 5. 追記(2026-10-01)

- **構成記事の価格**: 「RTX 5060 Ti構成とeGPUの比較」「在宅ワーク用デスク環境の一式」に、2026年10月1日時点の価格(価格.comの最安値。掲載のない商品はリンク先ショップの表示価格)を記入した。
- **予算付き2本は公開見送り**: 価格を調べた結果、「予算15万円のゲーミングPC」は合計約36万円、「予算20万円の動画編集用PC」は約49万円になった(メモリ DDR5 32GB が最安でも約6万円、RTX 5060 Ti 16GB が最安でも約13万円)。題名と内容が合わないため、ユーザー判断(案C)で公開を見送り、`docs/drafts/` に下書きとして退避した。
- **リンク切れ**: おすすめ機材ページ(`gear/index.html` ほか)の Titan Army P245MS+ の楽天リンクは、商品ページがエラーになっている(販売終了とみられる)。在宅ワーク記事では販売終了と明記し、同シリーズの P245MS PRO の価格とリンクを載せた。おすすめ機材ページ側の扱いは要判断 TODO(要確認)。
- **HPの Multitime 表記**: 「無制限」を実装どおり「最大20個」に修正済み(ストア側も修正済み)。
- **Aurum・Empress・Overwatch**: 2026-10-01 にストアで47機種対応版を公開。HPの対応機種の記載も更新済み。
