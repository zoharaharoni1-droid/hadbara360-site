// הדברה 360 — מעקב המרות: מאיפה הגיע כל לקוח (גוגל ממומן / אורגני / פייסבוק / ישיר...)
// 1) שומר את מקור ההגעה (UTM, gclid, אתר מפנה) בדפדפן של הגולש ל-90 יום.
// 2) כל ליד מהטופס נשלח ל-CRM יחד עם המקור; בוואטסאפ מצורף המקור לסוף ההודעה.
// 3) לחיצה על טלפון / וואטסאפ / שליחת טופס נשלחות ל-Google Analytics ול-Google Ads — ברגע שיוכנסו הקודים למטה.
(function () {
  // ─── קודי חיבור (ריק = כבוי). מוכנסים כשנפתחים החשבונות ───
  var GA4_ID = '';                 // לדוגמה: 'G-XXXXXXXXXX'
  var ADS_ID = '';                 // לדוגמה: 'AW-1234567890'
  var ADS_LABELS = { lead: '', whatsapp: '', call: '' }; // תוויות ההמרה מ-Google Ads

  var KEY = 'h360_attr', DAYS = 90;
  function now() { return Date.now(); }
  function qs(n) { try { return new URLSearchParams(location.search).get(n) || ''; } catch (e) { return ''; } }
  function host(u) { try { return new URL(u).hostname.replace(/^www\./, ''); } catch (e) { return ''; } }
  function path() { var p = location.pathname; try { p = decodeURIComponent(p); } catch (e) {} return p; }
  function load() { try { var a = JSON.parse(localStorage.getItem(KEY) || 'null'); if (a && a.t && now() - a.t < DAYS * 864e5) return a; } catch (e) {} return null; }
  function save(a) { try { localStorage.setItem(KEY, JSON.stringify(a)); } catch (e) {} }

  // מקור ההגעה הנוכחי
  function classify(src, med, gclid, ref) {
    var s = (src || '').toLowerCase(), m = (med || '').toLowerCase(), r = host(ref);
    if (gclid || /cpc|ppc|paid/.test(m) && /google/.test(s)) return 'גוגל ממומן';
    if (/cpc|ppc|paid/.test(m)) return (s || 'פרסום') + ' ממומן';
    if (s) return s + (m ? ' / ' + m : '');
    if (!r || r === location.hostname.replace(/^www\./, '')) return '';
    if (/google\./.test(r)) return 'גוגל אורגני';
    if (/bing\.|duckduckgo|yahoo/.test(r)) return 'חיפוש אחר';
    if (/facebook|fb\.|instagram/.test(r)) return 'פייסבוק / אינסטגרם';
    if (/b144|d\.co\.il|easy\.co\.il|midrag|zap\.co\.il/.test(r)) return 'אינדקס: ' + r;
    return 'אתר מפנה: ' + r;
  }
  var gclid = qs('gclid') || qs('gbraid') || qs('wbraid');
  var cur = {
    s: classify(qs('utm_source'), qs('utm_medium'), gclid, document.referrer),
    c: qs('utm_campaign'), k: qs('utm_term'), g: gclid, l: path(), r: host(document.referrer), t: now()
  };
  var a = load();
  if (cur.s) { // הגעה ממקור חיצוני — מתעדכן (ושומרים את המקור הראשון)
    a = { first: (a && a.first) || cur.s, s: cur.s, c: cur.c, k: cur.k, g: cur.g || (a && a.g) || '', l: cur.l, r: cur.r, t: now() };
    save(a);
  } else if (!a) {
    a = { first: 'ישיר', s: 'ישיר', c: '', k: '', g: '', l: cur.l, r: '', t: now() };
    save(a);
  }

  // מה נשלח ל-CRM (בשדה referrer — עד 300 תווים)
  window.h360Attr = function () {
    var x = load() || a || {};
    var o = { src: x.s || 'ישיר', first: x.first || '', camp: x.c || '', kw: x.k || '', gclid: (x.g || '').slice(0, 100), land: (x.l || '').slice(0, 80), ref: x.r || '' };
    var j = 'H360:' + JSON.stringify(o);
    while (j.length > 300 && o.gclid) { o.gclid = ''; j = 'H360:' + JSON.stringify(o); }
    return j.slice(0, 300);
  };
  window.h360Source = function () { var x = load() || a || {}; return x.s || 'ישיר'; };

  // ─── Google Analytics / Ads ───
  var on = !!(GA4_ID || ADS_ID);
  if (on) {
    var sc = document.createElement('script'); sc.async = true;
    sc.src = 'https://www.googletagmanager.com/gtag/js?id=' + (GA4_ID || ADS_ID); document.head.appendChild(sc);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { dataLayer.push(arguments); };
    gtag('js', new Date());
    if (GA4_ID) gtag('config', GA4_ID);
    if (ADS_ID) gtag('config', ADS_ID);
  }
  window.h360Conv = function (kind, extra) {
    if (!on || !window.gtag) return;
    var ev = kind === 'lead' ? 'generate_lead' : kind === 'whatsapp' ? 'click_whatsapp' : 'click_call';
    gtag('event', ev, Object.assign({ page_path: path(), lead_source: window.h360Source() }, extra || {}));
    if (ADS_ID && ADS_LABELS[kind]) gtag('event', 'conversion', { send_to: ADS_ID + '/' + ADS_LABELS[kind] });
  };

  // לחיצות על טלפון / וואטסאפ בכל האתר
  document.addEventListener('click', function (e) {
    var el = e.target && e.target.closest ? e.target.closest('a[href]') : null; if (!el) return;
    var h = el.getAttribute('href') || '';
    if (/^tel:/i.test(h)) { window.h360Conv('call'); return; }
    if (/api\.whatsapp\.com|wa\.me/i.test(h)) {
      window.h360Conv('whatsapp');
      // מוסיפים את המקור לסוף ההודעה (פעם אחת), כדי שבמשרד יידעו מאיפה הגיע
      try {
        var u = new URL(h, location.href), t = u.searchParams.get('text') || '', src = window.h360Source();
        if (src && t.indexOf('הגעתי דרך') < 0) {
          var nt = encodeURIComponent(t + '\n(הגעתי דרך: ' + src + ')');
          el.setAttribute('href', /[?&]text=/.test(h) ? h.replace(/([?&]text=)[^&#]*/, '$1' + nt) : h + (h.indexOf('?') < 0 ? '?' : '&') + 'text=' + nt);
        }
      } catch (er) {}
    }
  }, true);
})();
