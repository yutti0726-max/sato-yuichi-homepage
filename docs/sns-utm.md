# SNSからのリンクにUTMを付けるルール

SNSやフォーラムに yuichi-sato.com へのリンクを載せるときは、URLの末尾にUTMパラメータを付ける。
GA4(測定ID G-KVFRTBGBBQ)は追加設定なしでUTMを読み取るので、「どの投稿から来たか」を区別できる。
全ページに canonical が入っているため、UTM付きのURLが検索結果で重複ページ扱いになることはない。

## パラメータの決め方

| パラメータ | 値 | 例 |
|---|---|---|
| `utm_source` | 媒体 | `x` / `reddit` / `garmin_forum` / `instagram` / `threads` |
| `utm_medium` | 種類 | `social`(SNS)/ `forum`(掲示板) |
| `utm_campaign` | 投稿の種類 | `profile`(プロフィール欄)/ `pinned`(固定ポスト)/ `kaiunbi`(開運日の定期投稿)/ `launch`(新製品の告知) |
| `utm_content` | 個別の投稿 | 日付 `20261005` や製品名 `kichijitsu` |

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

ストア(apps.garmin.com)へのリンクにはUTMを付けても集計できない(GA4が入っていない)ので、
SNSにはなるべくHPの製品ページを載せ、HPからストアへ送る。

## GA4での見方

- レポート → 集客 → トラフィック獲得 → 主なディメンションを「セッションの参照元 / メディア」にすると `x / social` などで並ぶ。
- 投稿ごとの比較は、ディメンションを「セッションのキャンペーン」や「セッションの手動広告コンテンツ」(= utm_content)に変える。
- ストアへの送客は、製品ページで外部リンクのクリック(拡張計測機能の「離脱クリック」、イベント名 `click`)を見る。拡張計測機能が有効になっているかは未確認(GA4 管理 → データストリーム で確認する)。
