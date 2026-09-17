document.addEventListener('DOMContentLoaded', () => {
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
     Google Play / Kindle / Amazon物販 / 楽天 / Garmin Connect IQ への
     遷移を記録する。全ページで共通の script.js なので、ページ側の
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
    '527bc0eb-6b1a-42a5-9f47-47aabd270082': 'Overwatch'
  };

  const classifyOutbound = (url) => {
    let u;
    try { u = new URL(url); } catch (e) { return null; }
    const host = u.hostname;
    const path = u.pathname;

    if (host.endsWith('play.google.com')) {
      const id = u.searchParams.get('id') || '';
      return { event: 'play_store_click', params: { app_id: id, app_name: APP_NAMES[id] || id } };
    }
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
    return null;
  };

  document.addEventListener('click', (e) => {
    const link = e.target.closest && e.target.closest('a[href]');
    if (!link) return;

    const hit = classifyOutbound(link.href);
    if (!hit) return;

    if (typeof gtag !== 'function') return;

    gtag('event', hit.event, Object.assign({
      link_url: link.href,
      link_text: (link.textContent || '').trim().slice(0, 100),
      page_path: location.pathname,
      page_lang: document.documentElement.lang || 'ja'
    }, hit.params));
  }, { capture: true });
});
