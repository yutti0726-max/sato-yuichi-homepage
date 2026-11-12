/* ---------------------------------------------------------------
   お問い合わせフォーム(Google フォーム)の設定。ここ1か所だけを書き換える。
   - url: フォームの「回答用」の URL(https://docs.google.com/forms/d/e/…/viewform)。
     短縮の URL(forms.gle)では製品名・種類をあらかじめ入れられないので、長い URL を使う。
   - entryType・entryProduct: あらかじめ入れる項目の番号(「entry.123456789」の形。
     フォームの「事前入力した URL を取得」で作った URL の中にある)。
   - typeCustom: 「種類」の選択肢の文字(フォームの選択肢と1字も違わないこと)。
   url が 'FORM_URL_TODO' のままのあいだは、ボタンは /contact/ に行くだけ(差し替えない)。
   --------------------------------------------------------------- */
const CONTACT_FORM = {
  url: 'https://docs.google.com/forms/d/e/1FAIpQLSf29FyllDEjyIAHg73Zc94-iTohRqeNSxmC-XIxQWw3koIBLQ/viewform',
  entryType: 'entry.1070849450',
  entryProduct: 'entry.505538422',
  typeCustom: '受託制作の相談 / Custom work request / 定制委托咨询'
};

document.addEventListener('DOMContentLoaded', () => {
  /* お問い合わせフォームのボタン(<a class="contact-form-link" href="/contact/">)の href を、
     CONTACT_FORM から組み立てたフォームの URL に差し替え、新しいタブで開くようにする。
     JS が動かないときや、設定がまだのときは /contact/ に行く。 */
  const contactTypes = { custom: CONTACT_FORM.typeCustom };
  const isSet = (v) => typeof v === 'string' && v !== '' && !/_TODO$/.test(v);
  const isEntry = (v) => isSet(v) && /^entry\.[0-9]+$/.test(v);

  const buildContactFormUrl = (product, type) => {
    if (!isSet(CONTACT_FORM.url)) return null;
    let u;
    try { u = new URL(CONTACT_FORM.url); } catch (e) { return null; }
    const typeText = contactTypes[type] || '';
    const fills = [];
    if (product && isEntry(CONTACT_FORM.entryProduct)) fills.push([CONTACT_FORM.entryProduct, product]);
    if (typeText && isEntry(CONTACT_FORM.entryType)) fills.push([CONTACT_FORM.entryType, typeText]);
    if (fills.length) {
      u.searchParams.set('usp', 'pp_url');
      fills.forEach(([k, v]) => u.searchParams.set(k, v));
    }
    return u.href;
  };

  document.querySelectorAll('a.contact-form-link').forEach((a) => {
    const href = buildContactFormUrl(a.dataset.contactProduct || '', a.dataset.contactType || '');
    if (!href) return;
    a.href = href;
    a.target = '_blank';
    a.rel = 'noopener';
  });

  const revealEls = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    const revealObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          revealObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15 });
    revealEls.forEach((el) => revealObserver.observe(el));
  } else {
    revealEls.forEach((el) => el.classList.add('is-visible'));
  }

  const navLinks = Array.from(document.querySelectorAll('.site-header nav a'));

  const navToggle = document.getElementById('navToggle');
  const siteNav = document.getElementById('siteNav');

  if (navToggle && siteNav) {
    navToggle.addEventListener('click', () => {
      const isOpen = siteNav.classList.toggle('is-open');
      navToggle.classList.toggle('is-open', isOpen);
      navToggle.setAttribute('aria-expanded', String(isOpen));
    });

    navLinks.forEach((link) => {
      link.addEventListener('click', () => {
        siteNav.classList.remove('is-open');
        navToggle.classList.remove('is-open');
        navToggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  const sections = navLinks
    .filter((a) => a.getAttribute('href').startsWith('#'))
    .map((a) => document.querySelector(a.getAttribute('href')))
    .filter(Boolean);

  if ('IntersectionObserver' in window && sections.length) {
    const spyObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        const link = navLinks.find((a) => a.getAttribute('href') === `#${entry.target.id}`);
        if (!link) return;
        navLinks.forEach((a) => a.classList.remove('is-active'));
        link.classList.add('is-active');
      });
    }, { rootMargin: '-40% 0px -50% 0px', threshold: 0 });
    sections.forEach((s) => spyObserver.observe(s));
  }

  const progressBar = document.getElementById('scrollProgress');
  const backToTop = document.getElementById('backToTop');

  const onScroll = () => {
    const scrollTop = window.scrollY;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const pct = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
    if (progressBar) progressBar.style.width = `${pct}%`;
    if (backToTop) backToTop.classList.toggle('is-visible', scrollTop > 400);
  };

  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  if (backToTop) {
    backToTop.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  /* ---------------------------------------------------------------
     アウトバウンドクリック計測（GA4）
     Google Play / Kindle / Amazon物販 / 楽天 / Garmin Connect IQ / BOOTH /
     お問い合わせフォーム(Google フォーム)への遷移を記録する。全ページで共通の script.js なので、ページ側の
     変更は不要。
     --------------------------------------------------------------- */
  const APP_NAMES = {
    'com.satoyuichi.mediatoolbox': 'MediaToolbox',
    'com.snaptools.pdfkit': 'PDF Toolkit',
    'com.yutti.seniorpedometer': 'らくらく歩数計',
    'com.snaptools.readshot': 'Readshot',
    'com.snaptools.haglog': 'ハグログ'
  };

  const BOOK_NAMES = {
    '0fyPEuUH': 'MY 100 DIVES',
    '03SI9M8q': '黄金構成比バイブル',
    '0cEq9G5i': 'パーツ寿命2倍',
    '0jjHObPt': 'リースはもう終わりにしよう'
  };

  const GARMIN_NAMES = {
    'd5c391f0-82a1-4c79-8c82-18deb2cb31b3': 'Aurum',
    'ff485586-320b-4c73-87ee-4d2094541278': 'Cairn',
    'c2cb128d-3a5c-4b8f-a9bc-aefa42c488cf': 'Cairn Pro',
    '527bc0eb-6b1a-42a5-9f47-47aabd270082': 'Overwatch',
    '5c206dca-7ac0-43f8-adea-3a816f3213ed': 'Empress',
    '3083dfc3-3605-4818-8c74-130cc0c643b7': 'Cairn Cycle',
    '3b996aba-1782-47a2-a85c-458716340547': 'Cairn Cycle Pro',
    'fe029fb8-c6b1-4b6e-b3d2-3ac25c13a2d4': 'Multitime',
    '737315f9-223d-4f3d-b7d3-1bc78ac2b70f': 'Multitime Pro',
    '735866ea-b92b-45f6-a148-a1b6a345e642': 'Platina',
    '49a04616-6cd6-49b3-8333-a86bfda44905': 'Tide Phase',
    'c35a01ea-2d30-4a48-8047-d9c9c92620f8': 'Tide Phase Lite',
    'c26d9468-9a73-4932-aadd-7ce45b962118': 'Kichijitsu',
    'eea677ed-f063-4f2d-ba0d-63d464e12072': 'Kichijitsu Calendar'
  };

  const BOOTH_NAMES = {
    '9032113': '2027 Kichijitsu Techo'
  };

  const isCustomFacesPage = () => /^\/(en\/)?garmin\/custom\//.test(location.pathname);

  /* 返す値は、送るイベントの配列(なければ null)。 */
  const classifyOutbound = (url, link) => {
    let u;
    try { u = new URL(url); } catch (e) { return null; }
    const host = u.hostname;
    const path = u.pathname;

    /* オリジナル ウォッチフェイスの制作のページ(/garmin/custom/・/en/garmin/custom/)の
       問い合わせのメールのリンク。ほかのページの mailto は数えない。
       GA4 にメールアドレスを送らないよう、link_url・link_text を固定の値で上書きする。 */
    if (u.protocol === 'mailto:') {
      if (!isCustomFacesPage()) return null;
      return [{ event: 'custom_faces_mail_click', params: { link_url: 'mailto', link_text: 'contact_email' } }];
    }

    /* お問い合わせフォーム(Google フォーム)へのリンク。
       制作のページでは、問い合わせの数(T-136 の E-021)を続けて数えるため、
       メールのときと同じ custom_faces_mail_click も送る(link_url・link_text で、メールとフォームを分けられる)。 */
    if ((host === 'docs.google.com' && path.startsWith('/forms/')) || host === 'forms.gle') {
      const data = (link && link.dataset) || {};
      const hits = [{
        event: 'contact_form_click',
        params: {
          contact_product: data.contactProduct || '',
          contact_type: data.contactType || '',
          page_path: location.pathname,
          page_lang: document.documentElement.lang || 'ja'
        }
      }];
      if (isCustomFacesPage()) {
        hits.push({ event: 'custom_faces_mail_click', params: { link_url: 'contact_form', link_text: 'contact_form' } });
      }
      return hits;
    }

    const hit = classifyStore(host, path, u);
    return hit ? [hit] : null;
  };

  /* ストア・販売先へのリンク(1つのイベント。なければ null) */
  const classifyStore = (host, path, u) => {
    if (host.endsWith('play.google.com')) {
      const id = u.searchParams.get('id') || '';
      return { event: 'play_store_click', params: { app_id: id, app_name: APP_NAMES[id] || id } };
    }
    /* ペーパーバック（MY 100 DIVES）を含む、amzn.asia の本のリンクすべて。
       イベント名は過去の集計とそろえるため kindle_click のまま。 */
    if (host.endsWith('amzn.asia')) {
      const key = (path.match(/\/d\/([A-Za-z0-9]+)/) || [])[1] || '';
      return { event: 'kindle_click', params: { book_id: key, book_name: BOOK_NAMES[key] || key } };
    }
    if (host.endsWith('amazon.co.jp') || host.endsWith('amzn.to')) {
      const asin = (path.match(/\/dp\/([A-Z0-9]{10})/) || [])[1] || '';
      return { event: 'amazon_click', params: { asin: asin } };
    }
    if (host.endsWith('rakuten.co.jp')) {
      return { event: 'rakuten_click', params: {} };
    }
    if (host.endsWith('apps.garmin.com')) {
      const id = (path.match(/\/apps\/([0-9a-f-]{36})/) || [])[1] || '';
      return { event: 'garmin_click', params: { app_id: id, app_name: GARMIN_NAMES[id] || id } };
    }
    /* BOOTH(デジタル商品。吉日デジタル手帳など) */
    if (host === 'booth.pm' || host.endsWith('.booth.pm')) {
      const item = (path.match(/\/items\/([0-9]+)/) || [])[1] || '';
      return { event: 'booth_click', params: { item_id: item, item_name: BOOTH_NAMES[item] || item } };
    }
    return null;
  };

  document.addEventListener('click', (e) => {
    const link = e.target.closest && e.target.closest('a[href]');
    if (!link) return;

    const hits = classifyOutbound(link.href, link);
    if (!hits) return;

    if (typeof gtag !== 'function') return;

    hits.forEach((hit) => {
      gtag('event', hit.event, Object.assign({
        link_url: link.href,
        link_text: (link.textContent || '').trim().slice(0, 100),
        page_path: location.pathname,
        page_lang: document.documentElement.lang || 'ja'
      }, hit.params));
    });
  }, { capture: true });
});
