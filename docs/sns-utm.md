# SNSからのリンクにUTMを付けるルール

SNSやフォーラムに yuichi-sato.com へのリンクを載せるときは、URLの末尾にUTMパラメータを付ける。
GA4(測定ID G-KVFRTBGBBQ)は追加設定なしでUTMを読み取るので、「どの投稿から来たか」を区別できる。
全ページに canonical が入っているため、UTM付きのURLが検索結果で重複ページ扱いになることはない。

## パラメータの決め方

| パラメータ | 値 | 例 |
|---|---|---|
| `utm_source` | 媒体 | `x` / `reddit` / `garmin_forum` / `instagram` / `threads` / `tiktok` / `google_play`(Google Play の掲載) |
| `utm_medium` | 種類 | `social`(SNS)/ `forum`(掲示板)/ `store`(アプリストアの掲載) |
| `utm_campaign` | 投稿の種類 | `profile`(プロフィール欄)/ `pinned`(固定ポスト)/ `kaiunbi`(開運日の定期投稿)/ `launch`(新製品の告知)/ `sns_hub_202610`(SNS 導線づくりの投稿。リンク集 `/links/` や製品ページへ送る。2026年10月開始。製品ページへ送るときは `utm_content=<製品>` を付ける)/ `developer_site`(ストアの掲載の「ウェブサイト」欄) |
| `utm_content` | 個別の投稿 | 日付 `20261005` や製品名 `kichijitsu` / `kichijitsu_techo`(2027年 吉日デジタル手帳。商品ページ `/goods/kichijitsu-techo-2027/`)。同じ製品で投稿が複数あるときは `kichijitsu_techo_20261024` のように投稿日(8桁)を後ろに付ける |

- 値は半角英小文字・数字・アンダースコアだけにする(日本語は文字化けして集計が割れるため)。
- 同じ投稿の中では同じURLを使う。

## そのまま使えるURL

| 使う場所 | URL |
|---|---|
| Xのプロフィールのウェブサイト欄 | `https://yuichi-sato.com/?utm_source=x&utm_medium=social&utm_campaign=profile` |
| Xの固定ポスト(吉日ウォッチ) | `https://yuichi-sato.com/garmin/kichijitsu/?utm_source=x&utm_medium=social&utm_campaign=pinned&utm_content=kichijitsu` |
| Xの開運日の投稿(10/5の例) | `https://yuichi-sato.com/garmin/kichijitsu/?utm_source=x&utm_medium=social&utm_campaign=kaiunbi&utm_content=20261005` |
| Garmin公式フォーラムの投稿 | `https://yuichi-sato.com/garmin/<製品>/?utm_source=garmin_forum&utm_medium=forum&utm_campaign=launch&utm_content=<製品>` |
| Reddit | `https://yuichi-sato.com/garmin/<製品>/?utm_source=reddit&utm_medium=social&utm_campaign=launch&utm_content=<製品>` |
| Xの告知の投稿(2027年 吉日デジタル手帳。1本だけのとき。複数のときは `kichijitsu_techo_20261024` のように投稿日8桁を付ける) | `https://yuichi-sato.com/goods/kichijitsu-techo-2027/?utm_source=x&utm_medium=social&utm_campaign=launch&utm_content=kichijitsu_techo` |
| Instagramの告知(2027年 吉日デジタル手帳。ストーリーズのリンクなど) | `https://yuichi-sato.com/goods/kichijitsu-techo-2027/?utm_source=instagram&utm_medium=social&utm_campaign=launch&utm_content=kichijitsu_techo` |
| TikTokのプロフィールのウェブサイト欄(リンク集) | `https://yuichi-sato.com/links/?utm_source=tiktok&utm_medium=social&utm_campaign=profile` |
| Instagramのプロフィールのウェブサイト欄(リンク集) | `https://yuichi-sato.com/links/?utm_source=instagram&utm_medium=social&utm_campaign=profile` |
| Xのプロフィールのウェブサイト欄をリンク集にする場合 | `https://yuichi-sato.com/links/?utm_source=x&utm_medium=social&utm_campaign=profile` |
| Xの投稿からリンク集へ送る(10/22の例) | `https://yuichi-sato.com/links/?utm_source=x&utm_medium=social&utm_campaign=sns_hub_202610&utm_content=20261022` |

リンク集(`/links/`・`/en/links/`・`/zh/links/`)の中のリンクは内部リンクなので、UTMを付けない(GA4はセッションの流入元を入口のURLのUTMで記録するため、サイト内のリンクにUTMを付けると流入元が上書きされる)。
英語・中国語の投稿から送るときは、パスを `/en/links/`・`/zh/links/` に変え、UTMは同じ規則で付ける。

ストア(apps.garmin.com)へのリンクにはUTMを付けても集計できない(GA4が入っていない)ので、
SNSにはなるべくHPの製品ページを載せ、HPからストアへ送る。

## ストアの掲載からHPへ送るURL(2026-10-23 追加。T-049)

| 使う場所 | URL |
|---|---|
| Google Play の各アプリの「ウェブサイト」欄(Play Console のストアの設定 → 連絡先の詳細。アプリごとに設定できる) | `https://yuichi-sato.com/apps/<アプリ>/?utm_source=google_play&utm_medium=store&utm_campaign=developer_site&utm_content=<アプリ>` |
| Google Play・Garmin のストアの説明文の末尾 | `https://yuichi-sato.com/apps/<アプリ>/` または `https://yuichi-sato.com/garmin/<製品>/`(UTMは付けない) |

- `<アプリ>` は `/apps/` の下のフォルダ名(`pdftoolkit`、`mediatoolbox`、`readshot`、`seniorpedometer` など)、`<製品>` は `/garmin/` の下のフォルダ名。
- 英語の説明文(Garmin のストアなど)の末尾には `/en/garmin/<製品>/`・`/en/apps/<アプリ>/` を使う(中国語の掲載なら `/zh/`)。Google Play の「ウェブサイト」欄は言語ごとに分けられないので、日本語のページのままにする。
- 説明文の中のURLは、2026-10-23 に apps.garmin.com で見た範囲ではリンクにならない(文字だけ)。読んだ人が手で打つか写すので、短いURLにする。Google Play の説明文のURLがリンクになるかは未確認。
- 「ウェブサイト」欄にUTMを付けるのは、Play からの流入をアプリごとに分けて見るため。Play のアプリから開かれたときに参照元が残るかは未確認なので、UTMで確実に区別する。

## GA4での見方

- レポート → 集客 → トラフィック獲得 → 主なディメンションを「セッションの参照元 / メディア」にすると `x / social` などで並ぶ。
- 投稿ごとの比較は、ディメンションを「セッションのキャンペーン」や「セッションの手動広告コンテンツ」(= utm_content)に変える。
- ストアへの送客は、製品ページで外部リンクのクリック(拡張計測機能の「離脱クリック」、イベント名 `click`)を見る。拡張計測機能が有効になっているかは未確認(GA4 管理 → データストリーム で確認する)。
