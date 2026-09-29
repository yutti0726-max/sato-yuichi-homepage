# Android アプリ 収益化状況の調査(読み取りのみ)

調査日: 2026-09-29
対象: MediaToolbox / PDFツールキット / らくらく歩数計 / Readshot / ハグログ

- 各アプリのローカルリポジトリ(`C:\Users\yutti\<アプリ名>`)のソースを読んだだけで、コードの変更・ビルド・ストアへのアップロードはしていません。
- 広告ユニットIDなどの値そのものは記載しません。「本番ID / テストID / なし」の区分だけを書きます。
- 認証情報・keystore・`local.properties`・`google-services.json` は読んでいません。
- **このリポジトリは公開リポジトリです。** 収益額などの非公開の数字はここには書いていません。
- ローカルの値と、Play Console で実際に公開中のバージョンは一致しないことがあります(過去にも食い違いがありました)。公開中の状態は Play Console で確認してください。

---

## 1. 一覧

| アプリ | AdMob 依存 | UMP(同意) | Play Billing | リリースビルドの広告ID | デバッグビルド | versionCode / versionName | targetSdk |
|---|---|---|---|---|---|---|---|
| MediaToolbox | あり | あり | **あり**(広告削除の買い切り) | バナー: 本番ID / インタースティシャル: 本番ID | テストIDに自動切替 | 16 / 1.5.0 | 36 |
| PDFツールキット | あり | あり | なし | バナー・インタースティシャル・リワード: すべて本番ID | テストIDに自動切替 | 9 / 1.2.2 | 36 |
| らくらく歩数計 | あり | あり | なし | バナー: 本番ID | テストIDに自動切替 | 14 / 1.7.1(※未コミット)。コミット済みは 7 / 1.3.3 | 36 |
| Readshot | あり | あり | なし | バナー・インタースティシャル: 本番ID | テストIDに自動切替 | 6 / 1.3.0(※未コミット)。コミット済みは 4 / 1.1.2 | 36 |
| ハグログ | あり | あり | なし | インタースティシャル: 本番ID / バナー: テストID(未使用) | テストIDに自動切替 | 10 / 1.2.1 | 36 |

全アプリ共通: `minSdk = 26`、`compileSdk = 36`。AdMob のアプリID(`AndroidManifest.xml` の meta-data)は5本とも本番IDです。

**リリースビルドでテストIDのまま広告を出している箇所はありませんでした。**
ハグログのバナー用定数だけテストIDですが、バナーの表示部品(`BannerAd`)はどの画面からも呼ばれておらず、実際には使われていません。

---

## 2. アプリ別の詳細

### 2-1. MediaToolbox(`C:\Users\yutti\Media Toolbox`)

- 依存: `gradle/libs.versions.toml` に `play-services-ads`、`user-messaging-platform`、`com.android.billingclient:billing`(9.1.0)
- 配布フレーバーが2つ: `play`(広告あり、Google Play 向け)と `full`(広告なし、`applicationIdSuffix = ".full"`)。広告と課金のコードは `app/src/play/` にだけ入っている。
- 広告の実装箇所
  - ID の定義: `app/src/play/java/com/example/mediatoolbox/ads/AdConfig.kt`(`BuildConfig.DEBUG` ならテストID、リリースなら本番ID。本番IDが `TODO_` のままならテストIDに戻す安全策つき)
  - バナー: `ads/AdBanner.kt`
  - インタースティシャル: `ads/InterstitialAdManager.kt`
  - 同意(UMP): `ads/AdsController.kt`
  - 表示している画面: `ui/screens/` の HomeScreen・VideoResizeScreen・ImageResizeScreen・AudioExtractScreen・PdfToImageScreen・ImageToPdfScreen
- 課金: `billing/BillingManager.kt`(商品ID `remove_ads`、買い切り `INAPP`)、`billing/BillingController.kt`、`billing/EntitlementCache.kt`、購入導線は `ui/home/RemoveAdsCardProvider.kt`
- 所見: 5本の中で唯一、広告と課金の両方がそろっている。**他のアプリに課金を入れる場合の見本はこのアプリ。**

### 2-2. PDFツールキット(`C:\Users\yutti\PdfToolkit`)

- 依存: `play-services-ads`、`user-messaging-platform`。Billing なし。
- 広告の実装箇所
  - ID の定義: `app/src/main/java/com/snaptools/pdfkit/ads/AdConfig.kt`(デバッグはテストID、リリースは本番ID。本番IDが `YOUR_` のままならテストIDに戻す)
  - インタースティシャル・リワード: `ads/AdManager.kt`(PDF操作3回ごとにインタースティシャル: `INTERSTITIAL_EVERY_N_ACTIONS = 3`)
  - バナー: `ui/components/BannerAdView.kt`、表示は `ui/screens/LibraryScreen.kt`・`ui/screens/DocumentDetailScreen.kt`、`ui/navigation/NavGraph.kt`
  - 同意(UMP): `ads/ConsentManager.kt`

### 2-3. らくらく歩数計(`C:\Users\yutti\SeniorPedometer`)

- 依存: `play-services-ads`、`user-messaging-platform`。Billing なし。
- 広告の実装箇所
  - ID の定義: `app/src/main/java/com/yutti/seniorpedometer/AdConfig.kt`(デバッグはテストID、リリースは本番ID)
  - バナー: `MainActivity.kt` がコードで `adUnitId` を設定して読み込み、`AdsController.kt` が同意(UMP)と読み込みを管理
- **注意: 作業ツリーに未コミットの変更が33件あります**(`app/build.gradle.kts`・`AndroidManifest.xml`・`AdsController.kt`・`MainActivity.kt` など)。コミット済みの版は versionCode 7 / 1.3.3、作業ツリーは 14 / 1.7.1。HP に掲載している新機能(歩数貯金・家族に送るなど)は未コミット側に入っている可能性が高く、**GitHub にバックアップされていない状態**です。コミットと push を推奨します(TODO(要確認))。

### 2-4. Readshot(`C:\Users\yutti\Readshot`)

- 依存: `play-services-ads`、`user-messaging-platform`。Billing なし。
- 広告の実装箇所
  - ID の定義: `app/src/main/java/com/snaptools/readshot/ads/AdIds.kt`(デバッグはテストID、リリースは本番ID)
  - バナー: `ads/AdBanner.kt`、表示は `ui/home/HomeScreen.kt`
  - インタースティシャル: `ads/InterstitialAdManager.kt`
  - 同意(UMP): `ads/AdsController.kt`
- **注意: 作業ツリーに未コミットの変更が18件あります**(`app/build.gradle.kts` で versionCode 6 / 1.3.0 に更新済み、OCR・オーバーレイ・サービス周りのファイル)。コミット済みは 4 / 1.1.2。クローズドテストに出している版がどちらかを確認してください(TODO(要確認))。

### 2-5. ハグログ(`C:\Users\yutti\HagLog`)

- 依存: `play-services-ads`、`user-messaging-platform`。Billing なし。
- 広告の実装箇所
  - ID の定義: `app/src/main/java/com/snaptools/haglog/ads/AdConfig.kt`(インタースティシャルはデバッグでテストID・リリースで本番ID。バナー用定数はテストIDだが未使用)
  - インタースティシャル: `ads/InterstitialAdManager.kt`、呼び出しは `feature/diary/DiaryEntryViewModel.kt`(日記の保存後)と `MainActivity.kt`
  - 同意(UMP): `ads/ConsentManager.kt`
  - 広告はユーザーが設定でオフにできる(`data/prefs/Settings.adsEnabled`)。表示間隔は最短2分(`INTERSTITIAL_MIN_GAP_MS`)。
- `CLAUDE.md` / `TODO.md` がこのリポジトリだけありません(他の4本にはある)。

---

## 3. 課金(Google Play Billing)が未実装の4本に入れる場合

### 3-1. 入れるとしたら何を売るか

MediaToolbox と同じ「広告削除の買い切り(`INAPP`、商品ID `remove_ads`)」が、実装量・審査リスクともに最も小さい方法です。サブスクリプションや機能の有料化は、画面設計と Play Console 側の設定が増えるため今回は対象外とします。

### 3-2. 作業手順(ファイル単位)

MediaToolbox の実装をそのまま移植する前提です。パッケージ名だけ各アプリに合わせます。

1. `gradle/libs.versions.toml` — `billingClient` のバージョンと `billing` ライブラリを追加(MediaToolbox と同じ行)
2. `app/build.gradle.kts` — `implementation(libs.billing)` を追加し、versionCode / versionName を上げる
3. `.../billing/BillingManager.kt` — MediaToolbox からコピー。接続・商品情報の取得・購入・購入の承認(acknowledge)・購入状態の再確認を担当
4. `.../billing/EntitlementCache.kt` — コピー。購入済みかどうかを端末に保存し、起動直後やオフラインでも広告を出さないようにする
5. `.../billing/BillingController.kt` — コピー。アプリ起動時と画面復帰時(`onResume`)に購入状態を更新
6. 広告の表示箇所 — 購入済みなら広告を読み込まない分岐を追加
   - PDFツールキット: `ads/AdManager.kt`、`ui/components/BannerAdView.kt`
   - らくらく歩数計: `AdsController.kt`、`MainActivity.kt`
   - Readshot: `ads/AdBanner.kt`、`ads/InterstitialAdManager.kt`
   - ハグログ: `ads/InterstitialAdManager.kt`
7. 購入ボタンの画面 — MediaToolbox の `ui/home/RemoveAdsCardProvider.kt` を参考に、設定画面かホーム画面にカードを追加。文言は `res/values*/strings.xml`(翻訳版があるアプリは各言語)に追加
8. `AndroidManifest.xml` — Billing ライブラリが `com.android.vending.BILLING` 権限を自動で追加するため、通常は変更不要(ビルド後のマージ済みマニフェストで確認)
9. 人が行う作業: Play Console でアプリ内アイテム `remove_ads` を作成・価格設定・有効化 → ライセンステスターで購入テスト → 新バージョンを審査に提出

### 3-3. 想定工数(1アプリあたり、目安)

| 作業 | 目安 |
|---|---|
| 1〜5(依存追加・課金クラスの移植) | 1〜2時間 |
| 6(広告表示の分岐) | 0.5〜1時間 |
| 7(購入ボタンと文言、多言語分) | 1〜2時間 |
| ビルド・ライセンステスターでの購入/復元テスト | 1〜2時間 |
| Play Console の設定と提出(人の作業) | 0.5〜1時間 |
| **合計** | **4〜8時間** |

### 3-4. 優先度の所見

- 広告収益の規模が小さい現状では、課金を入れても売上への影響は小さく、**インストール数を増やす施策のほうが効果が大きい**と考えます。
- 入れるなら、作業のたびに広告が出る実用系の **PDFツールキット** が最有力です(リワード広告もあり、広告を消したい動機が生まれやすい)。
- ハグログは広告を設定でオフにできるため、広告削除の課金は価値が小さいです。らくらく歩数計はバナーのみで、利用者層を考えると購入の見込みは低めです。
- 先に片付けるべきこと: らくらく歩数計と Readshot の**未コミットの変更をコミット・push すること**(2-3・2-4)。
