# Garmin Connect IQ ストア掲載 改善提案

作成日: 2026-09-29
対象: Aurum / Overwatch / Empress / Cairn / Cairn Pro / Cairn Cycle / Cairn Cycle Pro / Multitime / Multitime Pro

## この文書の根拠

| 情報 | 取得元 |
|---|---|
| 各アプリの対応機種(現状) | 各 Garmin プロジェクトの `manifest.xml` / `manifest-pro.xml` の `<iq:product>` |
| 最新デバイス一覧 | ローカルの Connect IQ SDK 9.2.0 に入っているデバイス定義 (`%APPDATA%\Garmin\ConnectIQ\Devices\*\compiler.json`、173機種) |
| 現在のストア説明文 | Connect IQ ストアの公開API(ログイン不要)から 2026-09-29 に取得した掲載文 |
| 無料版と Pro 版の機能差 | 各プロジェクトのソース(`src-free/` `src-pro/` `Config.mc` `CairnFieldPro.mc` など) |

SDK のデバイス定義は「ローカルにダウンロード済みの定義」だけを見ています。SDK Manager で未取得のデバイスがあれば、それは一覧に出てきません(下記で「不明」としたもの)。
販売台数・人気の順位はこの調査では確認していません。

---

## 1. 対応機種の現状

| アプリ | 種別 | minApiLevel | 機種数 | 画面 |
|---|---|---|---|---|
| Aurum | watchface | 5.0.0 | 14 | AMOLED 円形のみ |
| Overwatch | watchface | 5.0.0 | 13 | AMOLED 円形のみ |
| Empress | watchface | 5.0.0 | 14 | AMOLED 円形のみ |
| Cairn / Cairn Pro | datafield | 3.2.0 | 30(無料・Pro 同一) | AMOLED・MIP 円形 |
| Cairn Cycle / Cairn Cycle Pro | datafield | 3.2.0 | 30(無料・Pro 同一) | AMOLED・MIP 円形 |
| Multitime / Multitime Pro | watch-app | 3.2.0 | 25(無料・Pro 同一) | AMOLED・MIP 円形、Instinct(セミオクタゴン) |

ストア側の「対応デバイス数」は、1つの product ID に複数モデルがまとまっている関係で manifest の数より多く表示されます(例: Cairn は manifest 30 → ストア 54)。

### 1-1. 文字盤3本(Aurum / Overwatch / Empress)

共通の13機種:
Forerunner 265 (`fr265`) / Forerunner 265S (`fr265s`) / Forerunner 965 (`fr965`) / Venu 3 (`venu3`) / Venu 3S (`venu3s`) / fēnix 8 43mm (`fenix843mm`) / fēnix 8 47mm・51mm(tactix 8・quatix 8 含む)(`fenix847mm`) / fēnix 9 43mm (`fenix943mm`) / fēnix 9 47mm・51mm (`fenix947mm`) / fēnix 9 Pro 43mm (`fenix9pro43mm`) / fēnix 9 Pro 47mm (`fenix9pro47mm`) / fēnix 9 Pro 51mm (`fenix9pro51mm`) / epix Pro (Gen 2) 47mm (`epix2pro47mm`)

- Aurum と Empress はこれに `quatix847mm` を加えた14機種。
- `quatix847mm` はローカル SDK にデバイス定義がありません(SDK 9.2.0 では quatix 8 47mm は `fenix847mm` に統合されて表示)。**ストアでの扱いは不明**。ビルドが通っているなら問題はない可能性が高いものの、次回ビルド時に警告が出ていないか確認してください。

### 1-2. Cairn / Cairn Pro / Cairn Cycle / Cairn Cycle Pro(4本とも同じ30機種)

上記13機種 + fēnix 7 / 7S / 7X / 7 Pro / 7S Pro / 7X Pro、fēnix 6 / 6S / 6 Pro / 6S Pro / 6X Pro、epix (Gen 2)、Enduro、Enduro 3、fēnix 8 Solar 47mm / 51mm、Forerunner 955

### 1-3. Multitime / Multitime Pro(25機種)

上記13機種 + fēnix 7 / 7S / 7X、fēnix 8 Solar 47mm / 51mm、Instinct 2 / 2S、Instinct 3 Solar、vívoactive 4、Forerunner 255 / 255S / 955

---

## 2. 追加できそうな機種(ローカル SDK のデバイス定義から確認できた範囲)

判定条件: 「アプリ種別に対応」「minApiLevel 以上の Connect IQ に対応」「現在の manifest に未登録」。
以下は **Connect IQ 5.0 以上の現行世代のみ**を載せています(Connect IQ 3.x〜4.x の旧機種は、データフィールドで45機種、Multitime で47機種がさらに条件を満たしますが、優先度が低いため省略)。
「実機での表示確認」はしていません。追加する場合は各プロジェクトの `build.ps1` で全機種ビルド → シミュレーターで目視、の通常手順が必要です。

### 2-1. 文字盤3本: 35機種(すべて既存と同じ解像度・同じメモリ上限)

既存13機種と同じ解像度(360/390/416/454/466 の円形 AMOLED)で、文字盤のメモリ上限も既存機と同じ128KB。既存のリソース(`resources-round-<解像度>`)をそのまま使える可能性が高く、**追加コストが最も低い候補**です。Overwatch は機種別リソース(`resources-venu3` など)も持っているため、レイアウトの目視確認は必須です。

| 解像度 | 機種(product ID) |
|---|---|
| 360×360 | Venu 2S (`venu2s`) |
| 390×390 | Forerunner 165 / 165 Music (`fr165` `fr165m`)、Forerunner 170 / 170 Music (`fr170` `fr170m`)、Forerunner 70 (`fr70`)、Forerunner 570 42mm (`fr57042mm`)、vívoactive 5 (`vivoactive5`)、vívoactive 6 (`vivoactive6`)、Venu 4 41mm (`venu441mm`)、epix Pro (Gen 2) 42mm (`epix2pro42mm`)、Instinct 3 AMOLED 45mm (`instinct3amoled45mm`)、Instinct Crossover AMOLED (`instinctcrossoveramoled`)、MARQ (Gen 2) 各種 (`marq2` `marq2aviator`)、Approach S50 (`approachs50`)、Approach S70 42mm (`approachs7042mm`)、Descent G2 (`descentg2`)、Descent Mk3 43mm (`descentmk343mm`) |
| 416×416 | epix (Gen 2) (`epix2`)、fēnix E (`fenixe`)、Venu 2 / 2 Plus (`venu2` `venu2plus`)、Instinct 3 AMOLED 50mm (`instinct3amoled50mm`)、D2 Air X10 (`d2airx10`)、D2 Mach 1 (`d2mach1`) |
| 454×454 | Forerunner 970 (`fr970`)、Forerunner 570 47mm (`fr57047mm`)、fēnix 8 Pro 47mm / 51mm (`fenix8pro47mm`)、Venu 4 45mm (`venu445mm`)、epix Pro (Gen 2) 51mm (`epix2pro51mm`)、Approach S70 47mm (`approachs7047mm`)、Descent Mk3i 51mm (`descentmk351mm`)、D2 Mach 2 / 2 Pro (`d2mach2` `d2mach2pro`) |

優先度の提案(根拠: 同シリーズの既存対応機との近さ。販売台数データは未確認):
1. Forerunner 970 / 570、fēnix 8 Pro、Venu 4、vívoactive 6 — 既存対応機の後継・同世代
2. epix (Gen 2)、epix Pro 42mm / 51mm、Forerunner 165、Venu 2 系 — 既存と同じ解像度で旧世代のユーザー層
3. MARQ、Approach、Descent、D2、Instinct AMOLED — 用途特化機

### 2-2. Cairn / Cairn Cycle(無料・Pro 共通): 58機種(同じ解像度40・新しい解像度18)

| 区分 | 機種(product ID) |
|---|---|
| 既存と同じ解像度(円形) | 上記 2-1 の文字盤候補のうち、既に対応済みの `epix2` を除く34機種 + fēnix 7 Pro / 7X Pro Solar Edition (no Wi-Fi) (`fenix7pronowifi` `fenix7xpronowifi`)、fēnix 9 Pro Solar 47mm / 51mm (`fenix9prosolar47mm` `fenix9prosolar51mm`)、Forerunner 255 / 255 Music (`fr255` `fr255m`) |
| 新しい解像度(レイアウト調整が必要) | **Edge 1040 / 1050 / 540 / 550 / 840 / 850 / Explore 2 / MTB**(`edge1040` `edge1050` `edge540` `edge550` `edge840` `edge850` `edgeexplore2` `edgemtb`、長方形 LCD)、Forerunner 255S / 255S Music(218×218)、Instinct 3 Solar / Instinct E(セミオクタゴン)、Venu Sq 2 / Sq 2 Music / Venu X1(長方形)、GPSMAP H1、eTrex Touch |

**特に Cairn Cycle は Edge(サイクルコンピューター)が未対応**です。自転車用データフィールドの主要な利用先は Edge のため、長方形レイアウトの追加は Cairn Cycle / Cairn Cycle Pro の最優先候補と考えます(Edge 向けのレイアウト作業と実機に近いシミュレーター確認が必要)。

### 2-3. Multitime / Multitime Pro: 60機種(同じ解像度46・新しい解像度14)

既存と同じ解像度の候補: 文字盤候補の35機種 + fēnix 7 Pro / 7S Pro / 7X Pro 系(`fenix7pro` `fenix7spro` `fenix7xpro` `fenix7pronowifi` `fenix7xpronowifi`)、fēnix 9 Pro Solar(`fenix9prosolar47mm` `fenix9prosolar51mm`)、Enduro 3 (`enduro3`)、Forerunner 255 Music / 255S Music (`fr255m` `fr255sm`)、Instinct E 45mm (`instincte45mm`)
新しい解像度: Edge 各種、Instinct E 40mm、Venu Sq 2 系、Venu X1、GPSMAP H1、eTrex Touch

### 2-4. 参考: 吉日(Kichijitsu)リポジトリの対応機種

同じ作者の `garmin-kichijitsu` は、文字盤で38機種・アプリで59機種を manifest に登録しています(Venu 2 系、vívoactive 5 / 6、Forerunner 165 / 570 / 970、Instinct 3 AMOLED、MARQ、Approach S70、Descent Mk3、D2 など)。上記候補の多くは、既に別アプリでビルド実績があることになります。

---

## 3. 無料版の説明文の冒頭に入れる「Pro 版の案内文」

現在の無料版の説明文には「WANT MORE?」の段落で Pro の案内が既にありますが、**説明文の中ほど**にあり、ストアの一覧・プレビューでは見えません。冒頭(アプリ名の直後の1段落目)に短い案内を入れる案です。価格・機能はすべて現行の Pro 版と同じ内容です。

### Cairn(無料)

英語:
```
Free, with no ads and no permissions. Want twelve metrics instead of six? Cairn Pro adds climb rate (VAM), total descent, distance to your ascent goal, time until sunset, temperature and watch battery. Free for your first 5 activities, then a one-time US$2.49.
```
日本語:
```
無料・広告なし・権限なし。6項目では足りない方へ:上位版の Cairn Pro は、昇降レート(VAM)・累積下降・登坂目標までの残り・日没までの時間・気温・時計のバッテリーを加えた12項目を1画面に表示します。最初の5アクティビティは無料、その後は買い切り US$2.49 です。
```

### Cairn Cycle(無料)

英語:
```
Free, with no ads and no permissions. Want twelve metrics instead of six? Cairn Cycle Pro adds average speed, average power, elevation, grade, temperature and watch battery. Free for your first 5 activities, then a one-time US$2.49.
```
日本語:
```
無料・広告なし・権限なし。6項目では足りない方へ:上位版の Cairn Cycle Pro は、平均速度・平均パワー・標高・勾配・気温・時計のバッテリーを加えた12項目を1画面に表示します。最初の5アクティビティは無料、その後は買い切り US$2.49 です。
```

### Multitime(無料)

英語:
```
Free forever for up to 3 timers at once. Need more? Multitime Pro runs up to 20 timers at once, gives each timer its own vibration pattern and saves your own presets. One-time US$2.49, no subscription.
```
日本語:
```
タイマー3個までならずっと無料。もっと使いたい方へ:上位版の Multitime Pro は、最大20個のタイマーの同時実行、タイマーごとの振動パターン、自分だけのプリセット保存に対応します。買い切り US$2.49(サブスクなし)です。
```

> 注意: 現在の Multitime / Multitime Pro の説明文は「UNLIMITED TIMERS / タイマー数が無制限」と書いていますが、ソース(`garmin-multitime/src-pro/Config.mc`)では `MAX_TIMERS = 20` が上限です。上の案は「最大20個」に直しています。HP の Multitime 個別ページ(`garmin/multitime/index.html` と en/zh)とトップの Multitime Pro カードも「無制限」表記のままなので、あわせて直すかどうかを判断してください(TODO(要確認))。

---

## 4. 有料版のストア説明文 改善案(英語)

### 改善の方針(全アプリ共通)

1. **1〜3行目で「何が得られるか」と「無料で試せること」を言い切る。** ストアの一覧・検索結果で見えるのは冒頭だけのため。現在は多くのアプリで試用の説明が3〜4段落目にあります。
2. **試用と購入の段落(TRIAL & PURCHASE)は必ず残す。** Garmin の審査で「試用後に課金するアプリはその旨を説明文に書く」ことが求められているため(Aurum リポジトリの `output/store/description-en.md` の注記)。
3. **無料版がある Pro 版は、無料版との違いを1行で示す。**
4. 対応機種の列挙はストアが自動表示するため短くする(追加機種が出たときの更新漏れも防げる)。
5. 末尾の SIGN フッター(`MORE FROM THE DEVELOPER`)はそのまま残す。

以下の本文は、現在の掲載文と各リポジトリのソースで確認できた事実だけで書いています。

### 4-1. Aurum(US$5.99、24時間無料お試し)

```
AURUM — six gold watch faces in one, free for 24 hours.

A gold watch face built the way a fine watch dial is built: layered, lit and finished, never a flat gold fill. Frameless, so the dial runs to the very edge of your screen. Try every finish free for 24 hours, then keep them all with a single one-time unlock of US$5.99. No subscription.

THE SIX FINISHES
  Onyx & Gold: grand Roman numerals in polished gold, a railway minute track at the edge, a date window at 3 and a power-reserve style battery gauge at 6.
  Rose Gold, Champagne, Gunmetal & Gold: the same Roman dial in pink gold, pale champagne gold, and brushed steel with a single gold second hand.
  Chronometer: minute numerals printed to the edge, applied gold batons and four round gauges.
  Digital Luxe: huge polished-gold digits, a ring of 60 dots that light with the seconds, and a 2 x 2 grid of your data.
Switch finishes any time in the watch face settings. No second download, no second purchase.

WHAT IT SHOWS
Hours, minutes and seconds, day and date, battery, and up to four data fields you choose: heart rate, steps, calories, floors climbed, distance, Body Battery, watch battery or notification count.

ALWAYS-ON
In low-power mode Aurum drops to a thin outlined dial with a small per-minute pixel shift, for less battery drain and no AMOLED burn-in.

TRIAL & PURCHASE
Everything is free for 24 hours after you install it. When the trial ends, the dial shows a 6-digit code and the URL www.kzl.io/code. Open that URL on your phone, enter the code and pay; the face unlocks within a few minutes. Payment is processed by KiezelPay, not Garmin (card or PayPal). Other supported watches on the same Garmin account do not need a second purchase.

PRIVACY
Aurum only talks to the KiezelPay server to check the unlock status. It never sends step, heart-rate or other personal data anywhere.

English and Japanese. (The unlock screen is English only.)

MORE FROM THE DEVELOPER
Made by SIGN (Yuichi Sato).
More watch faces, apps and news:
https://yuichi-sato.com
```

### 4-2. Overwatch(US$3.99、24時間無料お試し)

```
OVERWATCH — five data layouts in one watch face, and it picks the right one for you. Free for 24 hours.

Most data faces give you one fixed screen. Overwatch carries five, each tuned for a different part of your day, and in Auto mode it switches between them on its own: a running dashboard when you start a run, an altitude dashboard on a hike, a calm dark screen in your sleep window, recovery data after you wake, and everything at once the rest of the day. Or pick one layout and stay there.

Try it free for 24 hours, then keep it with a one-time US$3.99 unlock. No subscription.

THE FIVE LAYOUTS
  Cockpit: big time, your Body Battery trend for the last hour, and six fields (heart rate, steps, calories, Body Battery, watch battery, notifications), with edge gauges for battery and step goal.
  Track: live pace, heart rate, distance, elapsed time, cadence, average pace and calories while you record an activity.
  Trail: altitude, time until sunset, temperature, heart rate, floors climbed, steps and battery.
  Recovery: Body Battery with its last-hour trend, stress, resting heart rate and watch battery.
  Night: the time at the largest size the screen can draw, with date and battery. Built for bed and always-on.

BUILT TO BE READ
The largest number font each watch can render. Units follow your watch (km/mi, m/ft). Four accent colours: white, green, amber, cyan.

ALWAYS-ON
A single dimmed time readout that shifts one pixel every minute, to protect AMOLED screens.

TRIAL & PURCHASE
Free for 24 hours after install. After that the face shows a 6-digit code and www.kzl.io/code; open it on your phone, enter the code and pay, and the face unlocks within minutes. Payment is processed by KiezelPay, not Garmin (card or PayPal). No second purchase for other watches on the same Garmin account.

PRIVACY
Overwatch only talks to the KiezelPay server to check the unlock status. It never sends personal data anywhere.

English and Japanese. (The unlock screen is English only.)

MORE FROM THE DEVELOPER
Made by SIGN (Yuichi Sato).
More watch faces, apps and news:
https://yuichi-sato.com
```

### 4-3. Empress(US$6.99、24時間無料お試し)

```
EMPRESS — a jewelled chronograph watch face in five gemstone finishes. Free for 24 hours.

Each finish is set the way a jewellery watch is set, not tinted with a colour fill: cabochon and baguette-cut stones, three sunburst subdials ringed with pavé micro-stones, and a brushed-metal cartouche for the digital time. Frameless, so the whole screen is dial.

Try all five free for 24 hours, then keep them with a one-time US$6.99 unlock. No subscription.

THE FIVE FINISHES
  Sapphire, Emerald and Ruby on gold subdials.
  Amethyst and Diamond White on platinum subdials.
Switch any time in the watch face settings. No second download, no second purchase.

WHAT IT SHOWS
  Analog hours and minutes with polished faceted hands
  Large digital time with seconds, weekday and date
  12 o'clock: heart-rate gauge with a moon-phase window
  9 o'clock: watch battery
  6 o'clock: steps against your daily goal
  One data field of your choice: calories, floors climbed, distance, Body Battery, notifications and more

SETTINGS
Finish, dial tone (black or charcoal), seconds style (digital, sweep hand or off), moon phase on/off, and the data field.

ALWAYS-ON
In low-power mode Empress drops to a thin outlined dial with a per-minute pixel shift, for less battery drain and no AMOLED burn-in.

TRIAL & PURCHASE
Free for 24 hours after install. After that the dial shows a 6-digit code and www.kzl.io/code; open it on your phone, enter the code and pay, and the face unlocks within minutes. Payment is processed by KiezelPay, not Garmin (card or PayPal). No second purchase for other watches on the same Garmin account.

PRIVACY
Empress only talks to the KiezelPay server to check the unlock status. It never sends personal data anywhere.

English and Japanese. (The unlock screen is English only.)

MORE FROM THE DEVELOPER
Made by SIGN (Yuichi Sato).
More watch faces, apps and news:
https://yuichi-sato.com
```

### 4-4. Cairn Pro(US$2.49、5アクティビティ無料)

```
CAIRN PRO — twelve climbing metrics on one screen. Free for your first 5 activities.

The full-screen hiking data field for people who climb. Cairn Pro shows everything the free Cairn shows, plus the numbers that decide a peak day: how fast you are climbing, how far to your ascent goal, and how long until sunset.

  ELEV · VAM · GRADE
  ASCENT · DESCENT · TO GO
  DIST · TIME · DAYLIGHT
  HR · TEMP · BATTERY

VAM is your live climb rate in metres per hour. TO GO counts down to an ascent goal you set (for example 1000 m). DAYLIGHT is the time until sunset, calculated on the watch from your GPS position, so it works with no phone and no weather data. If twelve cells are too dense for your screen, the Focus layout switches to six large ones.

Add it to any Hike, Walk, Mountaineering or Trail Run activity as a single full-screen field. Metric or imperial follows your watch.

FREE VS PRO
The free Cairn shows six of these metrics (ELEV, ASCENT, GRADE, DIST, TIME, HR) at no cost, forever. Cairn Pro adds VAM, DESCENT, TO GO, DAYLIGHT, TEMP and BATTERY, the ascent goal and the Focus layout.

TRIAL & PURCHASE
Cairn Pro is listed free but is the paid edition. Your first 5 activities are a full free trial. After that the field shows a 6-digit code and www.kzl.io/code until you unlock it with a one-time US$2.49 (no subscription). Open the URL on your phone, enter the code and pay; the field unlocks within minutes. Payment is processed by KiezelPay, not Garmin (card or PayPal). No second purchase for other watches on the same Garmin account.

PRIVACY
Cairn Pro only talks to the KiezelPay server to check the unlock status. It never sends altitude, heart-rate, location or any other data anywhere.

English and Japanese. (The unlock screen is English only.)

MORE FROM THE DEVELOPER
Made by SIGN (Yuichi Sato).
More watch faces, apps and news:
https://yuichi-sato.com
```

### 4-5. Cairn Cycle Pro(US$2.49、5アクティビティ無料)

```
CAIRN CYCLE PRO — twelve ride metrics on one screen. Free for your first 5 activities.

The full-screen cycling data field that shows live values next to your ride averages, so you can pace an effort without switching screens, and keeps elevation and grade in view for the climbs.

  SPEED · AVG SPD · POWER
  AVG PWR · CADENCE · HR
  DIST · TIME · ELEV
  GRADE · TEMP · BATTERY

If twelve cells are too dense for your screen, the Focus layout switches to six large ones (speed, power, cadence, heart rate, distance, time). Add it to any Cycling activity as a single full-screen field. Metric or imperial follows your watch. Power and cadence need the matching sensors.

FREE VS PRO
The free Cairn Cycle shows SPEED, DIST, TIME, HR, POWER and CADENCE at no cost, forever. Cairn Cycle Pro adds average speed, average power, elevation, grade, temperature and watch battery, plus the Focus layout.

TRIAL & PURCHASE
Cairn Cycle Pro is listed free but is the paid edition. Your first 5 activities are a full free trial. After that the field shows a 6-digit code and www.kzl.io/code until you unlock it with a one-time US$2.49 (no subscription). Open the URL on your phone, enter the code and pay; the field unlocks within minutes. Payment is processed by KiezelPay, not Garmin (card or PayPal). No second purchase for other watches on the same Garmin account.

PRIVACY
Cairn Cycle Pro only talks to the KiezelPay server to check the unlock status. It never sends speed, power, location or any other ride data anywhere.

English and Japanese. (The unlock screen is English only.)

MORE FROM THE DEVELOPER
Made by SIGN (Yuichi Sato).
More watch faces, apps and news:
https://yuichi-sato.com
```

### 4-6. Multitime Pro(US$2.49、タイマー3個までは無料)

```
MULTITIME PRO — up to 20 named timers at once, each with its own vibration. The first 3 timers are free forever.

Pasta, dough and the oven, all on one screen: every timer has its own name and counts down on its own line. Swipe to move between them, tap to start, pause or restart. When one finishes it shows DONE right in the list, so you never lose track of which one rang.

WHAT PRO ADDS
  UP TO 20 TIMERS      run as many at once as you need, up to 20
  PER-TIMER VIBRATION  a distinct pattern for each timer, so you know which one finished without looking
  SAVED PRESETS        save your own durations (for example "risotto 18:00") for one-tap reuse

Quick presets (1/3/5/10/15/20/30 min, Pomodoro 25+5, HIIT 30s/10s) and any custom minutes:seconds work in both editions.

TRIAL & PURCHASE
Multitime Pro is listed free but is the paid edition. Up to 3 timers with the default vibration work forever, with no time limit. The moment you use a Pro feature (a 4th timer, a non-default vibration pattern or a saved preset) you will see a 6-digit code and www.kzl.io/code. Open the URL on your phone, enter the code and pay a one-time US$2.49 (no subscription); Pro unlocks within minutes. Payment is processed by KiezelPay, not Garmin (card or PayPal). No second purchase for other watches on the same Garmin account.

A NOTE ON BACKGROUND ALERTS
Connect IQ lets an app reserve one background wake-up at a time, so Multitime Pro always schedules the nearest timer and reschedules the next as each finishes. If two timers end within 5 minutes of each other, the second may not alert the instant it finishes; open the app and it shows DONE correctly. This is a platform limit, not a bug.

PRIVACY
Multitime Pro only talks to the KiezelPay server to check the unlock status.

English and Japanese. (The unlock screen is English only.)

MORE FROM THE DEVELOPER
Made by SIGN (Yuichi Sato).
More watch faces, apps and news:
https://yuichi-sato.com
```

> Multitime Pro の現在の掲載は**英語版のみで、日本語の説明文がありません**(公開APIの `appLocalizations` が `en` のみ)。他の8本は英日両方あります。日本語版の追加を推奨します(文面は無料版 Multitime の日本語説明文と、上の英語案をもとに作成可能)。

### 4-7. 日本語版について

日本語の説明文は、上の英語案と同じ構成(冒頭で価値と無料お試し → 機能 → 試用と購入 → プライバシー → フッター)に並べ替えることを推奨します。文言は現在の日本語掲載文をそのまま流用でき、新しい事実の追加はありません。

---

## 5. 反映時のチェックリスト

- [ ] 説明文の変更は「詳細を編集」から行う(再審査なしで即時反映された実績あり: 2026-09-29 の SIGN フッター追加時)
- [ ] 各言語(en / ja)の両方を更新する
- [ ] TRIAL & PURCHASE の段落が残っていることを確認する
- [ ] Multitime の「無制限」表記を「最大20個」に直す(ストア・HP の両方)
- [ ] 対応機種を追加する場合は、manifest 追加 → 全機種ビルド → シミュレーター目視 → 署名 `.iq` を新バージョンとしてアップロード(こちらは再審査が必要)
