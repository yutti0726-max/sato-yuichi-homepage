const translations = {
  ja: {
    nav_profile: 'プロフィール',
    nav_apps: 'アプリ',
    nav_books: '書籍',

    hero_eyebrow: '実業家 ・ アプリケーション開発者 ・ ビジネスコンサルタント',
    hero_lead: '現場で培った顧客心理分析力とテクノロジーへの知見を融合し、<br class="hero-break">日常の不便を解消する「ありそうでなかった」アプリケーションを開発しています。',

    profile_title: 'プロフィール',
    profile_lead: '北海道を拠点に活動する実業家／アプリケーション開発者／ビジネスコンサルタント。通信インフラ領域における光回線やビジネスフォンの現場営業、携帯キャリアショップの統括マネジメントに加え、保険領域において高度なコンサルティング営業を経験。かんぽ生命での個人向け生命保険・第三分野（医療・がん等）から、東京海上日動の自動車保険をはじめとする損害保険、さらには法人向け生命保険のソリューション提案に至るまで、多岐にわたる金融・保険商品の販売現場で顧客心理の分析と成約ノウハウを体系化してきた。',
    profile_subhead: '経歴・実績',

    career1_tag: '通信・インフラ・店舗マネジメント',
    career1_desc: '光回線（フレッツ光・au光・TEPCO光）の訪問営業やビジネスフォン販売、マンション設備交渉を経験。携帯キャリアショップの店長・統括として組織運営および販売戦略を主導。',
    career2_tag: '保険・金融コンサルティング',
    career2_desc: 'かんぽ生命における生命保険・第三分野保険の提案、東京海上日動における自動車保険等の損害保険、および法人向け生命保険営業を担当。個人のライフプランニングから法人の財務対策まで、複雑なニーズに対するソリューション営業に従事。',
    career3_tag: 'テクノロジー・開発',
    career3_desc: '100台を超える自作PC構築実績とハードウェア／ソフトウェアの知見をベースに、ユーザーの潜在ニーズを形にする実用アプリケーションの企画・開発を行う。',

    profile_closing: '現場最前線で培った「顧客の本質的な課題抽出能力」と、100台以上の自作PC構築やガジェット検証で培ったハード・ソフト双方の知見を融合し、誰もが恩恵を受けられる、実用性と独自性を兼ね備えたアプリケーションを企画・開発・公開しています。',

    works_title: 'アプリ',

    app1_tagline: '動画・画像・音声・PDFをまとめて変換できる、シンプルなマルチメディア変換ツール。',
    app1_feat1: '【動画リサイズ】1080p/720p/360pなど好きな解像度を指定してMP4形式に変換・保存',
    app1_feat2: '【画像リサイズ】幅・高さを自由に指定してリサイズ（アスペクト比固定にも対応）',
    app1_feat3: '【音声抽出】動画から音声だけを取り出してM4A形式で保存',
    app1_feat4: '【PDFを画像に変換】PDFの各ページをJPEG/PNGとして書き出し',
    app1_feat5: '【画像をPDFに変換】カメラ撮影や保存済みの画像からPDFを作成',
    app1_note: '※ 現在テスト公開準備中のため、公開までリンク先が表示されない場合があります。',

    app2_tagline: 'スキャン・結合・分割・圧縮まで、PDFのよくある作業をこれ1つで。',
    app2_feat1: '【スキャンしてPDF化】カメラで書類を撮影して自動補正しPDFに',
    app2_feat2: '【画像からPDF作成】複数の写真を1つのPDFにまとめる',
    app2_feat3: '【PDFを結合】複数のPDFを1つに結合する',
    app2_feat4: '【PDFを分割】ページ範囲や間隔でPDFを分割する',
    app2_feat5: '【PDFを圧縮】ファイルサイズを縮小する（画像化されます）',

    app3_name: 'らくらく歩数計',
    app3_tagline: 'ボタン操作は不要。自動で歩数を記録する、シニアにやさしい歩数計アプリ。',
    app3_feat1: '【自動歩数カウント】アプリを開かなくても、バックグラウンドで自動的に歩数を記録',
    app3_feat2: '【ホーム画面ウィジェット】今日の歩数・カロリーを大きな文字で表示、サイズも調整可能',
    app3_feat3: '【称号システム】歩いた距離に応じて称号がアップ。東京から日本列島制覇を目指す、ゲーム感覚の仕掛け',
    app3_feat4: '【目標達成通知】3,000／5,000／8,000／10,000／15,000歩など、その日の目標達成をお知らせ',

    price_free: '無料',
    lang_badge: '🌐 日本語 / English 対応',
    cta_download: '📲 無料でダウンロード',
    note_pending: '※ 現在公開準備中のため、公開までリンク先が表示されない場合があります。',

    books_title: '書籍',
    books_lead: 'Kindleにて、ダイビングログブックと自作PCに関する実用書を出版しています。',

    book_tag_diving: 'ダイビングログブック',
    book_tag_pcguide: '自作PCガイド',
    book_tag_lease: '自作PC × コスト削減',

    book1_title: 'MY 100 DIVES: スキューバダイビング・ログブック（100本の記録と、その先へ）',
    book1_desc: '経験本数の証明に必要な項目（水深・水温・残圧・ウェイト・透視度・サイン欄）をあらかじめ網羅した記入式ログブック。100ダイブ分の記録ページに加え、節目（1・10・25・40・50・60・75・100本）ごとのMILESTONEページ、ダイバープロフィールや器材リスト、和英併記の生物チェックリストも収録。プロコースを目指す方から、趣味として記録を残したい方まで。',
    book1_cta: '📖 ¥1,628 でKindleを読む',

    book2_title: 'パソコンの黄金構成比で自作できるパーツ構成&神ガジェット最適化バイブル【2026年最新版】',
    book2_desc: '100台以上の自作実績を持つ著者が、2026年最新パーツで「予算を1円も無駄にしない」黄金構成を徹底解説。予算10万円台・20万円未満・30万円台前半の3つの黄金ルートを紹介し、作業効率を上げる神周辺機器も解説。BTOパソコンの歪なスペックバランスに予算をドブに捨てる前に。',
    book2_cta: '📖 ¥480 でKindleを読む',

    book3_title: 'パーツ寿命を2倍に伸ばす「自作PCメンテナンス&トラブルシューティング」徹底解説',
    book3_desc: '100台以上のPCを自作してきたプロが、愛機の寿命を2倍に引き延ばす「物理メンテナンス」と、突然の不具合を自己解決する「トラブルシューティング」を徹底解説。CPUグリスの塗り替え技術、温度・電圧・ストレージ寿命の読み解き方、電源が入らない時の切り分けフローやエラーコード解析まで実務的にカバー。',
    book3_cta: '📖 ¥480 でKindleを読む',

    book4_title: 'リースは、もう終わりにしよう。：スタートアップ・個人事業主のための自作PC×自己保守 完全コスト削減バイブル',
    book4_desc: '毎月のPCリース料金をやめ、自作PC×自己保守でコストを削減する実務バイブル。リースと購入のTCO比較や少額減価償却資産の特例を活用した節税テクニック、失敗しない黄金パーツ構成表、予防保守の手順、NASを活用したデータ保護（3-2-1ルール）までを1冊で網羅。',
    book4_cta: '📖 ¥480 でKindleを読む',

    page_title: '佐藤雄一 | 実業家・アプリ開発者・ビジネスコンサルタント',
    meta_description: '実業家・アプリ開発者・ビジネスコンサルタントの佐藤雄一の公式サイト。Androidアプリ「MediaToolbox」「PDFツールキット」「らくらく歩数計」とKindle書籍を紹介しています。',
    back_to_top: 'トップに戻る',
  },
  en: {
    nav_profile: 'Profile',
    nav_apps: 'Apps',
    nav_books: 'Books',

    hero_eyebrow: 'Entrepreneur · App Developer · Business Consultant',
    hero_lead: 'Combining frontline customer-psychology insight with a passion for technology,<br class="hero-break"> I build apps that solve everyday frustrations nobody else quite got around to.',

    profile_title: 'Profile',
    profile_lead: 'Yuichi Sato is an entrepreneur, application developer, and business consultant based in Hokkaido, Japan. He built his career in telecom infrastructure sales &mdash; door-to-door fiber-optic internet (Flet&rsquo;s Hikari, au Hikari, TEPCO Hikari) and business phone sales &mdash; before moving into advanced insurance consulting: individual life and third-sector (medical, cancer) insurance at Japan Post Insurance, auto and other property insurance at Tokio Marine Nichido, and corporate life insurance solutions. Across this wide range of financial and insurance products, he has systematized an approach to reading customer psychology and closing deals.',
    profile_subhead: 'Career & Achievements',

    career1_tag: 'Telecom, Infrastructure & Store Management',
    career1_desc: 'Door-to-door sales of fiber-optic internet (Flet&rsquo;s Hikari, au Hikari, TEPCO Hikari) and business phone systems, including negotiating equipment installation in apartment buildings. Led store operations and sales strategy as a store manager and area supervisor for mobile carrier shops.',
    career2_tag: 'Insurance & Financial Consulting',
    career2_desc: 'Proposed life and third-sector insurance at Japan Post Insurance, handled auto and other property insurance at Tokio Marine Nichido, and led corporate life insurance sales. Worked solution-based sales addressing complex needs, from individual life planning to corporate financial strategy.',
    career3_tag: 'Technology & Development',
    career3_desc: 'Drawing on experience building over 100 custom PCs and deep hardware/software knowledge, he plans and develops practical applications that turn users&rsquo; latent needs into real products.',

    profile_closing: 'By combining the ability to identify customers&rsquo; underlying problems &mdash; honed on the front lines &mdash; with the hardware and software insight gained from building and testing 100+ custom PCs and gadgets, he plans, builds, and ships applications that are both genuinely useful and distinctly his own.',

    works_title: 'Apps',

    app1_tagline: 'A simple multimedia conversion tool that handles video, images, audio, and PDFs all in one place.',
    app1_feat1: '[Resize Video] Convert to MP4 at your choice of resolution &mdash; 1080p, 720p, 360p, and more',
    app1_feat2: '[Resize Image] Freely set width and height, with an optional aspect-ratio lock',
    app1_feat3: '[Extract Audio] Pull just the audio track out of a video and save it as M4A',
    app1_feat4: '[PDF to Images] Export every page of a PDF as JPEG or PNG',
    app1_feat5: '[Images to PDF] Build a PDF from photos taken with the camera or already saved on your phone',
    app1_note: '* Still in closed testing &mdash; this link may not work until the app goes live.',

    app2_tagline: 'Scan, merge, split, and compress &mdash; the everyday PDF tasks, all in one app.',
    app2_feat1: '[Scan to PDF] Photograph a document and it&rsquo;s auto-corrected into a PDF',
    app2_feat2: '[Images to PDF] Combine multiple photos into a single PDF',
    app2_feat3: '[Merge PDFs] Combine multiple PDF files into one',
    app2_feat4: '[Split PDF] Split a PDF by page range or interval',
    app2_feat5: '[Compress PDF] Shrink file size (pages are converted to images)',

    app3_name: 'Rakuraku Step Counter',
    app3_tagline: 'No buttons to press &mdash; automatic step tracking designed to be easy for seniors.',
    app3_feat1: '[Automatic Step Counting] Tracks your steps in the background &mdash; no need to even open the app',
    app3_feat2: '[Home-Screen Widget] Shows today&rsquo;s steps and calories in large, easy-to-read text, resizable to fit your screen',
    app3_feat3: '[Rank System] Your rank climbs with the distance you&rsquo;ve walked &mdash; a game-like journey from Tokyo toward conquering the length of Japan',
    app3_feat4: '[Daily Goal Alerts] Get notified on hitting 3,000 / 5,000 / 8,000 / 10,000 / 15,000 steps in a day',

    price_free: 'Free',
    lang_badge: '🌐 Japanese / English',
    cta_download: '📲 Free Download',
    note_pending: '* Still preparing for release &mdash; this link may not work until it goes live.',

    books_title: 'Books',
    books_lead: 'Published on Kindle: a scuba diving logbook and practical guides to building your own PC.',

    book_tag_diving: 'Diving Logbook',
    book_tag_pcguide: 'PC Build Guide',
    book_tag_lease: 'Custom PC &times; Cost Cutting',

    book1_title: 'MY 100 DIVES: Scuba Diving Logbook (100 Dives Recorded &mdash; and Beyond)',
    book1_desc: 'A fill-in dive logbook that already covers everything needed to prove your experience level &mdash; depth, water temperature, remaining pressure, weight, visibility, and a sign-off column. Includes 100 dive-log pages, milestone pages at key counts (1, 10, 25, 40, 50, 60, 75, 100 dives), a diver profile, a gear checklist, and a bilingual (Japanese/English) marine-life checklist. For anyone working toward a pro rating, or simply keeping a personal record.',
    book1_cta: '📖 Read on Kindle &mdash; ¥1,628',

    book2_title: 'The &ldquo;Golden Ratio&rdquo; PC Build Bible: Parts & Gadget Optimization From Someone Who&rsquo;s Built 100+ PCs [2026 Edition]',
    book2_desc: 'Written by someone who has personally built over 100 PCs, this guide lays out a &ldquo;golden ratio&rdquo; build that wastes not a single yen of your 2026 budget. Covers three build routes by budget &mdash; under ¥100K, under ¥200K, and the ¥300K range &mdash; plus the peripherals worth investing in to work faster. For anyone about to overpay for a lopsided pre-built PC.',
    book2_cta: '📖 Read on Kindle &mdash; ¥480',

    book3_title: 'Double Your PC&rsquo;s Lifespan: A Complete Guide to Custom-PC Maintenance & Troubleshooting',
    book3_desc: 'From a builder who&rsquo;s assembled over 100 PCs: the physical maintenance that doubles your machine&rsquo;s lifespan, and the troubleshooting skills to solve sudden problems yourself. Covers reapplying CPU thermal paste, reading temperature/voltage/storage health, a step-by-step flowchart for when the PC won&rsquo;t boot, and decoding error codes &mdash; all in hands-on, practical detail.',
    book3_cta: '📖 Read on Kindle &mdash; ¥480',

    book4_title: 'No More Leasing: The Complete Cost-Cutting Bible for Startups and Freelancers &mdash; Custom PCs & Self-Maintenance',
    book4_desc: 'A practical playbook for cutting costs by ditching monthly PC leases in favor of building and maintaining your own. Covers a lease-vs-buy total cost comparison, tax-saving techniques using Japan&rsquo;s small-value depreciable-asset rules, a proven parts-selection formula, preventive-maintenance steps, and NAS-based data protection (the 3-2-1 rule).',
    book4_cta: '📖 Read on Kindle &mdash; ¥480',

    page_title: 'Yuichi Sato | Entrepreneur, App Developer & Business Consultant',
    meta_description: 'Official site of Yuichi Sato — entrepreneur, app developer, and business consultant. Featuring the Android apps MediaToolbox, PDF Toolkit, and Rakuraku Step Counter, plus books on Kindle.',
    back_to_top: 'Back to top',
  },
};

(function () {
  const STORAGE_KEY = 'site-lang';

  function applyLang(lang) {
    const dict = translations[lang] || translations.ja;
    document.querySelectorAll('[data-i18n]').forEach((el) => {
      const key = el.getAttribute('data-i18n');
      if (dict[key] !== undefined) {
        el.innerHTML = dict[key];
      }
    });

    document.documentElement.lang = lang;
    if (dict.page_title) document.title = dict.page_title;
    const metaDesc = document.querySelector('meta[name="description"]');
    if (metaDesc && dict.meta_description) metaDesc.setAttribute('content', dict.meta_description);
    const backToTop = document.getElementById('backToTop');
    if (backToTop && dict.back_to_top) backToTop.setAttribute('aria-label', dict.back_to_top);

    const switchBtn = document.getElementById('langSwitch');
    if (switchBtn) {
      switchBtn.classList.toggle('is-en', lang === 'en');
      switchBtn.setAttribute('aria-pressed', lang === 'en' ? 'true' : 'false');
    }

    localStorage.setItem(STORAGE_KEY, lang);
  }

  document.addEventListener('DOMContentLoaded', () => {
    let saved = 'ja';
    try {
      saved = localStorage.getItem(STORAGE_KEY) || 'ja';
    } catch (e) {
      saved = 'ja';
    }
    applyLang(saved);

    const switchBtn = document.getElementById('langSwitch');
    if (switchBtn) {
      switchBtn.addEventListener('click', () => {
        const current = document.documentElement.lang === 'en' ? 'en' : 'ja';
        applyLang(current === 'en' ? 'ja' : 'en');
      });
    }
  });
})();
