# -*- coding: utf-8 -*-
import os, shutil, json, html, sys, re
from urllib.parse import quote
sys.path.insert(0, os.path.dirname(__file__))
from content import *
from deep_pests1 import DEEP_PESTS_1
from deep_pests2 import DEEP_PESTS_2
from deep_cities import CITIES_NEW, DEEP_CITIES
from deep_local import LOCAL
from deep_combos import COMBO_PESTS, COMBO_CITIES, COMBOS
from guides import GUIDES
from deep_services import DEEP_SERVICES
CITIES = CITIES[:-1] + CITIES_NEW + CITIES[-1:]   # "המרכז" נשאר אחרון
DEEP_PESTS = {**DEEP_PESTS_1, **DEEP_PESTS_2}
WA_PHOTO = "https://api.whatsapp.com/send?phone=972559992266&text=" + "שלום! אני שולח/ת תמונה של מזיק לזיהוי (מאתר הדברה 360)"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_ASSETS = os.path.join(ROOT, "site", "assets")
OUT = os.path.join(ROOT, "dist")
VER = "18"

E = html.escape
PEST_BY = {p["path"]: p for p in PESTS}
CITY_BY = {c["path"]: c for c in CITIES}
CITY_BY_ALL = CITY_BY
SERV_BY = {s["path"]: s for s in SERVICES}

I_PHONE = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg>'
I_WA = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 11.5a8.4 8.4 0 0 1-12.3 7.4L3 21l2.1-5.6A8.4 8.4 0 1 1 21 11.5z"/></svg>'
I_MENU = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M4 6h16M4 12h16M4 18h16"/></svg>'
I_LEAF = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.5 19 2c1 2 2 4.2 2 8 0 5.5-4.8 10-10 10z"/><path d="M2 21c0-3 1.9-5.4 5.1-6"/></svg>'
I_AWARD = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="8" r="6"/><path d="M15.5 13 17 22l-5-3-5 3 1.5-9"/></svg>'
I_SHIELD = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></svg>'
I_CLOCK = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>'

def url(path):
    return "/" if not path else "/" + path.strip("/") + "/"

def abs_url(path):
    return DOMAIN + quote(url(path))

def phone_btn(cls="btn btn-g", label="חייגו: "):
    return f'<a class="{cls}" href="tel:{TEL}">{I_PHONE}<span>{label}<span class="ltr">{PHONE}</span></span></a>'

def wa_btn(cls="btn btn-o", label="וואטסאפ"):
    return f'<a class="{cls}" href="{E(WA)}" target="_blank" rel="noopener">{I_WA}{label}</a>'

NAV = [("שירותי הדברה","שירותי-הדברה"),("סוגי מזיקים","הדברת-מזיקים"),("מחירון","מחירון"),("ביקורות","המלצות"),("אזורי שירות","אזורי-שירות"),("מדריכים","בלוג"),("שאלות נפוצות","שאלות-נפוצות"),("אודות","אודות")]

def nav_links():
    return "".join(f'<a href="{url(p)}">{t}</a>' for t, p in NAV)

LB = {
  "@context":"https://schema.org","@type":"PestControl","name":"הדברה 360","url":DOMAIN+"/",
  "telephone":"+972-55-999-2266","email":"hadbara360@gmail.com","image":DOMAIN+"/assets/logo-square.png","logo":DOMAIN+"/assets/logo-square.png","priceRange":"₪₪",
  "areaServed":[c["name"] for c in CITIES if c["path"]!="הדברה-במרכז"],
  "openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Sunday","Monday","Tuesday","Wednesday","Thursday"],"opens":"07:00","closes":"21:00"},{"@type":"OpeningHoursSpecification","dayOfWeek":"Friday","opens":"07:00","closes":"14:00"}],
  "description":"חברת הדברה מקצועית במרכז. רישיון מדביר במבנים ובשטח פתוח מס׳ "+LICENSE+"."
}

def page(path, title, desc, body, schema=None, noindex=False, head_extra=""):
    sch = [LB] + (schema or [])
    sch_html = "".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in sch)
    robots = '<meta name="robots" content="noindex">' if noindex else ''
    return f'''<!doctype html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
{robots}<link rel="canonical" href="{abs_url(path)}">
<meta property="og:type" content="website"><meta property="og:locale" content="he_IL">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{abs_url(path)}"><meta property="og:image" content="{DOMAIN}/assets/photo-sprayer.webp">
<meta name="theme-color" content="#01344A">
<link rel="icon" href="/assets/icon.png?v=2"><link rel="apple-touch-icon" href="/assets/icon.png?v=2">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;700;800&amp;display=swap">
{head_extra or '<link rel="preload" as="image" href="/assets/photo-sprayer.webp" fetchpriority="high">'}
<link rel="stylesheet" href="/assets/style.css?v={VER}">
<script src="/assets/track.js?v={VER}"></script>
{sch_html}
</head>
<body>
<a class="skip" href="#main">דילוג לתוכן</a>
<div class="promo"><b>מבצע</b>{E(PROMO)}, אמרו לנו "ראיתי באתר"</div>
<header class="hdr"><div class="wrap">
<a class="logo" href="/"><img src="/assets/logo.svg" alt="הדברה 360 – לדף הבית" width="348" height="160" fetchpriority="high"></a>
<nav class="nav nav-d" aria-label="ניווט ראשי">{nav_links()}</nav>
<a class="hphone" href="tel:{TEL}">{I_PHONE}<span><small>מענה מהיר · חירום גם בערב ובלילה</small><strong>{PHONE}</strong></span></a>
<details class="menu"><summary aria-label="תפריט">{I_MENU}</summary><nav class="nav" aria-label="תפריט נייד"><a href="/">דף הבית</a>{nav_links()}</nav></details>
</div></header>
<main id="main">
{body}
</main>
{footer()}
<div class="mbar"><a class="c" href="tel:{TEL}">{I_PHONE}חייגו עכשיו</a><a class="w" href="{E(WA)}" target="_blank" rel="noopener">{I_WA}וואטסאפ</a></div>
</body>
</html>'''

def footer():
    pests = "".join(f'<li><a href="{url(p["path"])}">{p["h1"].split(":")[0]}</a></li>' for p in PESTS if p.get("top"))
    cities = "".join(f'<li><a href="{url(c["path"])}">הדברה {c["prep"]}</a></li>' for c in CITIES[:6])
    return f'''<footer class="ftr"><div class="wrap">
<div class="cols">
<div style="max-width:300px;display:flex;flex-direction:column;gap:12px"><span class="lg"><img src="/assets/logo.svg" alt="הדברה 360" width="348" height="160" loading="lazy"></span><span>חברת הדברה מקצועית. רישיון מדביר במבנים ובשטח פתוח מס׳ {LICENSE}. חומרים מאושרים ע״י המשרד להגנת הסביבה.</span></div>
<div><h3>הדברת מזיקים</h3><ul>{pests}<li><a href="{url("הדברת-מזיקים")}">כל המזיקים</a></li></ul></div>
<div><h3>אזורי שירות</h3><ul>{cities}<li><a href="{url("אזורי-שירות")}">כל האזורים</a></li></ul></div>
<div><h3>החברה</h3><ul><li><a href="{url("אודות")}">אודות</a></li><li><a href="{url("מחירון")}">מחירון הדברה</a></li><li><a href="{url("המלצות")}">ביקורות</a></li><li><a href="{url("שאלות-נפוצות")}">שאלות נפוצות</a></li><li><a href="{url("בלוג")}">מדריכים</a></li><li><a href="{url("אחריות")}">אחריות</a></li></ul></div>
<div><h3>צרו קשר</h3><ul><li><a href="tel:{TEL}" class="ltr">{PHONE}</a></li><li><a href="{E(WA)}" target="_blank" rel="noopener">וואטסאפ</a></li><li><a href="mailto:hadbara360@gmail.com">hadbara360@gmail.com</a></li><li>א׳–ה׳ 7:00–21:00 · ו׳ 7:00–14:00</li><li><a href="{E(WA_SOS)}" target="_blank" rel="noopener">חירום בערב ובלילה – וואטסאפ</a></li></ul></div>
</div>
<div class="bottom"><span>© הדברה 360. כל הזכויות שמורות.</span><a href="{url("הצהרת-נגישות")}">הצהרת נגישות</a></div>
</div></footer>'''

WA_SOS = "https://api.whatsapp.com/send?phone=972559992266&text=" + "שלום, יש לי מקרה חירום (מאתר הדברה 360): "
SOS_LINE = f'<p class="sos">🚨 <strong>חירום בערב או בלילה?</strong> חולדה בבית, נחש, קן צרעות – <a href="{E(WA_SOS)}" target="_blank" rel="noopener">שלחו וואטסאפ</a>. נחזור בהקדם לפי זמינות, בתעריף חירום.</p>'

def ctaband(h, p="ייעוץ והצעת מחיר בחינם · מדביר מוסמך עם אחריות בכתב."):
    return f'<section class="ctaband"><div class="wrap"><div style="flex:999 1 420px"><h2>{h}</h2><p>{p}</p>{SOS_LINE}</div>{phone_btn(label="")}</div></section>'

HE_MONTHS = ["ינואר","פברואר","מרץ","אפריל","מאי","יוני","יולי","אוגוסט","ספטמבר","אוקטובר","נובמבר","דצמבר"]
I_G = '<svg class="rev-g" width="20" height="20" viewBox="0 0 48 48" aria-label="Google" role="img"><path fill="#FFC107" d="M43.6 20.1H42V20H24v8h11.3C33.7 32.7 29.2 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 12.9 4 4 12.9 4 24s8.9 20 20 20 20-8.9 20-20c0-1.3-.1-2.6-.4-3.9z"/><path fill="#FF3D00" d="m6.3 14.7 6.6 4.8C14.7 15.1 19 12 24 12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 16.3 4 9.7 8.3 6.3 14.7z"/><path fill="#4CAF50" d="M24 44c5.2 0 9.9-2 13.4-5.2l-6.2-5.2C29.2 35.1 26.7 36 24 36c-5.2 0-9.6-3.3-11.3-8l-6.5 5C9.5 39.6 16.2 44 24 44z"/><path fill="#1976D2" d="M43.6 20.1H42V20H24v8h11.3c-.8 2.2-2.2 4.2-4.1 5.6l6.2 5.2C37 39.2 44 34 44 24c0-1.3-.1-2.6-.4-3.9z"/></svg>'
AV_COLORS = ["#2E7D1A","#01344A","#5DB02B","#0F6E8C","#7A8F2A","#3F5F73"]

def he_date(iso):
    try:
        y, m = iso.split("-")[:2]
        return f"{HE_MONTHS[int(m)-1]} {y}"
    except Exception:
        return ""

def rev_card(r):
    n, t, d, av = (list(r) + ["", ""])[:4]
    initial = E(n.strip()[:1].upper() or "★")
    col = AV_COLORS[sum(map(ord, n)) % len(AV_COLORS)]
    img = (f'<img src="https://lh3.googleusercontent.com{E(av)}=s96-c" alt="" width="48" height="48" loading="lazy" referrerpolicy="no-referrer" onerror="this.remove()">' if av else "")
    body = "<br>".join(E(line) for line in t.split("\n") if line.strip())
    date = f'<span class="rev-d">{he_date(d)}</span>' if d else ""
    return (f'<figure class="rev"><div class="rev-h"><span class="av" style="background:{col}" aria-hidden="true"><b>{initial}</b>{img}</span>'
            f'<div class="rev-who"><figcaption>{E(n)}</figcaption>{date}</div>{I_G}</div>'
            f'<span class="stars" aria-label="5 כוכבים">★★★★★</span><blockquote>{body}</blockquote></figure>')

def reviews_html(items):
    return '<div class="reviews">' + "".join(rev_card(r) for r in items) + '</div>'

def rating_bar(big=False):
    d = REVIEWS_DATA
    return (f'<div class="rbar{" big" if big else ""}"><div class="rbar-s">{I_G}<b>{d["rating"]:.1f}</b><span class="stars" aria-hidden="true">★★★★★</span>'
            f'<span>{d["count"]} ביקורות בגוגל</span></div>'
            f'<a class="btn rbar-w" href="{E(d["write_url"])}" target="_blank" rel="noopener">כתבו לנו ביקורת</a></div>')

def faq_ans(a):  # [[טקסט|נתיב]] או [[טקסט|https://...]] → קישור
    out = E(a)
    return re.sub(r"\[\[([^|\]]+)\|([^\]]+)\]\]", lambda m: (f'<a href="{html.unescape(m.group(2))}" target="_blank" rel="noopener">{m.group(1)}</a>' if m.group(2).startswith("http") else f'<a href="{url(html.unescape(m.group(2)))}">{m.group(1)}</a>'), out)

def faq_plain(a):
    return re.sub(r"\[\[([^|\]]+)\|[^\]]+\]\]", r"\1", a)

def faq_html(items):
    return '<div class="faq">' + "".join(f'<details><summary>{E(q)}</summary><p>{faq_ans(a)}</p></details>' for q, a in items) + '</div>'

def faq_schema(items):
    return {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":faq_plain(a)}} for q, a in items]}

def crumbs_schema(trail):
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":abs_url(p)} for i,(n,p) in enumerate(trail)]}

def crumbs_html(trail, dark=False):
    parts = [f'<a href="{url(p)}">{n}</a>' for n, p in trail[:-1]] + [f'<span aria-current="page">{trail[-1][0]}</span>']
    return f'<nav class="crumbs{" dark" if dark else ""}" aria-label="פירורי לחם">' + " › ".join(parts) + '</nav>'

def nobug(kind="roach", mini=False):
    src = "/assets/no-ant.webp" if kind=="ant" else "/assets/no-roach.svg"
    return f'<div class="{"nobug-mini" if mini else "nobug"}" aria-hidden="true"><img src="{src}" alt="" width="120" height="120" decoding="async"></div>'
NOBUG = nobug()

def sub_hero(trail, h1, lead, img="photo-sprayer", show_price=False, bug="roach", icon=True):
    # מחיר "החל מ־" מוצג רק בעמוד הבית
    price = ''
    return f'''<section class="hero sub" style="background-image:url('/assets/{img}.webp')"><div class="ov">{nobug(bug) if icon else ""}<div class="wrap">
{crumbs_html(trail)}
<h1 style="margin-top:20px">{h1}</h1>
<p class="lead">{lead}</p>
{price}
<div class="ctas">{phone_btn()}{wa_btn()}</div>
</div></div></section>''' + lead_form()

SUPA_ANON = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlsdWJsaGdhd2dmem54cGRyZnJhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODEzMzMwNjAsImV4cCI6MjA5NjkwOTA2MH0.RMUX-pVuO4AGqtyGrAOxbW3RBPvBm6QnNeO0li6SY4E"  # מפתח ציבורי. ההרשאות במסד מאפשרות לאתר רק להוסיף ליד

def lead_form():
    opts = "".join(f"<option>{p['name']}</option>" for p in PESTS if p.get("top")) + "<option>אחר</option>"
    return f'''<div class="leadwrap"><form class="lead-form" id="lead" data-k="{SUPA_ANON}" novalidate>
<div class="t"><strong>מעדיפים שנחזור אליכם?</strong><span>השאירו פרטים וקבלו 10% הנחה</span></div>
<label>שם מלא<input type="text" id="lead-name" autocomplete="name" maxlength="80" required></label>
<label>טלפון<input type="tel" id="lead-phone" autocomplete="tel" inputmode="tel" maxlength="20" required></label>
<label>סוג המזיק<select id="lead-pest">{opts}</select></label>
<p class="hidden"><label>לא למילוי<input id="lead-hp" tabindex="-1" autocomplete="off"></label></p>
<button class="btn btn-n" type="submit" id="lead-btn">חזרו אליי</button>
<p id="lead-msg" role="status" aria-live="polite" style="flex:1 1 100%;margin:0;font-weight:700"></p>
</form></div>
<script src="/assets/lead.js?v={VER}" defer></script>'''

FEAT = f'''<div class="feat">
<div><span class="ico">{I_LEAF}</span><span><strong>הדברה ירוקה</strong><span>חומרים מאושרים ובטוחים</span></span></div>
<div><span class="ico">{I_AWARD}</span><span><strong>מדבירים מוסמכים</strong><span>רישיון מדביר בתוקף</span></span></div>
<div><span class="ico">{I_SHIELD}</span><span><strong>אחריות מלאה</strong><span>אחריות בכתב על כל עבודה</span></span></div>
<div><span class="ico">{I_CLOCK}</span><span><strong>חירום גם בלילה</strong><span>מענה מהיר, גם בערב ובלילה</span></span></div>
</div>
<div class="lic"><a href="/assets/license.webp" target="_blank" rel="noopener" style="flex:none"><img src="/assets/license.webp" alt="רישיון מדביר במבנים ובשטח פתוח מטעם המשרד להגנת הסביבה, מספר רישיון {LICENSE}, על שם זוהר אהרוני" width="150" height="96" loading="lazy" style="display:block;width:150px;height:96px;object-fit:cover;border-radius:8px;border:1px solid var(--line)"></a><span><strong style="display:block;font-size:18px">מדביר מורשה ע״י המשרד להגנת הסביבה</strong><span style="color:var(--muted);font-size:16px;display:block">רישיון מדביר במבנים ובשטח פתוח מס׳ {LICENSE}</span><span style="color:var(--muted);font-size:16px;display:block">בתוקף עד 02/2030 · לחצו להגדלה</span></span></div>'''

STEPS = '''<div class="steps">
<div class="step"><span class="n">1</span><span><strong>מתקשרים אלינו</strong><span>מספרים מה קורה ומקבלים ייעוץ והצעת מחיר בחינם.</span></span></div>
<div class="step"><span class="n">2</span><span><strong>מדביר מוסמך מגיע בזמן</strong><span>אבחון מקור הבעיה וטיפול בשיטה המתאימה.</span></span></div>
<div class="step"><span class="n">3</span><span><strong>אחריות ומעקב</strong><span>אחריות בכתב, ואנחנו זמינים אם משהו חוזר.</span></span></div>
</div>'''

def city_chips(paths=None, cls="chip"):
    paths = paths or [c["path"] for c in CITIES]
    return '<div class="chips">' + "".join(f'<a class="{cls}" href="{url(p)}">{CITY_BY[p]["name"]}</a>' for p in paths) + '</div>'

def pest_tiles(items, more=True):
    t = "".join(f'<a class="tile" href="{url(p["path"])}">{p["name"]}</a>' for p in items)
    if more: t += f'<a class="tile dark" href="{url("הדברת-מזיקים")}">לכל המזיקים</a>'
    return f'<div class="tiles">{t}</div>'

def serv_card(s, desc=None):
    return f'<a class="card" href="{url(s["path"])}"><img src="/assets/{s["img"]}.webp" alt="" loading="lazy" width="786" height="450"><span class="b"><strong>{s["name"]}</strong><span>{desc or s["intro"].split(".")[0]+"."}</span><em>לפרטים ←</em></span></a>'

def toc_html(items):
    return '<nav class="toc" aria-label="תוכן העניינים"><strong>בעמוד הזה</strong><ol>' + "".join(f'<li><a href="#{a}">{E(t)}</a></li>' for a, t in items) + '</ol></nav>'

def photo_id_box():
    return f'''<div class="photoid"><div><strong>לא בטוחים איזה מזיק זה?</strong><span>צלמו ושלחו לנו בוואטסאפ, ונזהה בשבילכם בחינם.</span></div><a class="btn btn-w" href="{E(WA_PHOTO)}" target="_blank" rel="noopener">{I_WA}שליחת תמונה לזיהוי</a></div>'''

def steps_html(steps):
    return '<div class="steps">' + "".join(f'<div class="step"><span class="n">{i+1}</span><span><strong>{E(t)}</strong><span>{E(d)}</span></span></div>' for i,(t,d) in enumerate(steps)) + '</div>'

def ul(items):
    return '<ul class="list">' + "".join(f"<li>{E(x)}</li>" for x in items) + '</ul>'

def price_from_txt(price):
    m = re.search(r'(\d[\d,]*)\s*[–-]', price) or re.search(r'(\d[\d,]*)\s*₪', price)
    return m.group(1) if m else None

def mini_prices():
    rows = PRICE_TABLES[0][1][:6]
    trs = "".join(f"<tr><td><strong>{E(a)}</strong></td><td>{E(b)}</td><td>{E(c)}</td></tr>" for a,b,c,d in rows)
    return f'<div class="tablebox"><table class="prices"><thead><tr><th scope="col">מזיק</th><th scope="col">אופן ביצוע</th><th scope="col">מחיר לדירה</th></tr></thead><tbody>{trs}</tbody></table></div><p style="font-size:15px;color:var(--muted);margin-top:10px">המחירים כוללים מע״מ. בבתים עם חצר וביובים המחיר שונה. <a href="{url("מחירון")}">למחירון המלא</a></p>'

def combo_path(pk, cpath):
    return COMBO_PESTS[pk]["slug"] + "-" + cpath.replace("הדברה-", "", 1)

def H2(anchor, text, extra=""):
    return f'<h2 id="{anchor}" style="scroll-margin-top:90px{extra}">{text}</h2>'

# ---------------- PAGES ----------------
pages = {}

TOP = [p for p in PESTS if p.get("top")]
TOP_TILES = TOP + [SERV_BY["הרחקת-יונים"] | {"name":"הרחקת יונים"}, SERV_BY["לוכד-נחשים"] | {"name":"לכידת נחשים"}]

# Home
HOME_HEAD = '<link rel="preload" as="image" href="/assets/hero-home.webp" media="(min-width:900px)" fetchpriority="high"><link rel="preload" as="image" href="/assets/hero-home-mob.webp" media="(max-width:899px)" fetchpriority="high">\n<style>.hero.home .nobug,.hero.home .nobug-mini{display:none!important}.hero.home .ov{background:linear-gradient(to left,rgba(1,36,52,.85) 0%,rgba(1,36,52,.6) 45%,rgba(1,36,52,.08) 85%)}@media(max-width:899px){.hero.home{background-image:url(\'/assets/hero-home-mob.webp\')!important;background-size:100% auto;background-position:center -15vw;background-color:#012434}.hero.home .ov{background:none}.hero.home .wrap{margin-top:85vw;background:#012434;border-radius:24px 24px 0 0;padding-top:22px;box-shadow:0 -12px 30px rgba(0,0,0,.25)}.hero.home .badge{position:absolute;top:calc(-85vw + 18px);right:20px;left:20px;background:rgba(1,36,52,.82);color:#d9f5b8;text-align:center;font-size:14px}}.hero.home .v4{list-style:none;padding:0;margin:0;display:grid;gap:9px;font-size:clamp(17px,1.7vw,20px);font-weight:600;color:#fff}.hero.home .v4 li{display:flex;gap:10px;align-items:center}.hero.home .v4 li::before{content:"✓";flex:0 0 26px;height:26px;border-radius:50%;background:var(--green);color:var(--navy);display:grid;place-items:center;font-weight:900;font-size:15px}.tcards{max-width:1100px;margin:-70px auto 0;position:relative;z-index:2;display:grid;grid-template-columns:repeat(3,1fr);background:#fff;border-radius:20px;box-shadow:0 14px 40px rgba(1,52,74,.15);padding:22px 10px}.tcards .tc{text-align:center;padding:6px 18px;border-left:1px dashed #cfe5bd}.tcards .tc:last-child{border-left:none}.tcards svg{width:38px;height:38px;display:block;margin:0 auto 6px}.tcards b{display:block;font-size:19px;color:#01344A}.tcards span{color:#4B6472;font-size:15px}.tcards+.leadwrap .lead-form{margin-top:28px}@media(max-width:899px){.hero.home .wrap{padding-bottom:28px!important}.tcards{margin:18px 14px 0;grid-template-columns:1fr;padding:6px 14px}.tcards .tc{border-left:none;border-bottom:1px dashed #cfe5bd;padding:12px 4px;display:grid;grid-template-columns:44px 1fr;text-align:right;align-items:center;column-gap:10px}.tcards .tc svg{grid-row:span 2;margin:0}.tcards .tc:last-child{border-bottom:none}}</style>'
home = f'''<section class="hero home" style="background-image:url('/assets/hero-home.webp')"><div class="ov"><div class="nobug" aria-hidden="true"><img src="/assets/no-roach.svg" alt="" width="120" height="120" decoding="async"></div><div class="wrap">
<span class="badge">רישיון מדביר במבנים ובשטח פתוח מס׳ {LICENSE} · חומרים מאושרים ע״י המשרד להגנת הסביבה</span>
<h1>בית נקי ממזיקים<br>עם אחריות בכתב</h1>
<ul class="v4"><li>מדביר מוסמך עם ניסיון בבתים, בניינים ועסקים</li><li>מחיר ברור מראש, בלי הפתעות בסוף</li><li>פותרים את הבעיה מהשורש, לא רק מרססים</li><li>גם אחרי הטיפול אנחנו כאן, לכל שאלה</li></ul>
<div class="price"><span>הדברה החל מ־</span><strong>250 ₪</strong><div class="nobug-mini" aria-hidden="true"><img src="/assets/no-roach.svg" alt="" width="120" height="120" decoding="async"></div></div>
<div class="ctas"><a class="btn btn-g" href="tel:0559992266"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg><span>חייגו: <span class="ltr">055-9992266</span></span></a><a class="btn btn-o" href="https://api.whatsapp.com/send?phone=972559992266&amp;text=שלום! אני פונה אליכם מאתר הדברה 360, חזרו אליי בבקשה" target="_blank" rel="noopener"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 11.5a8.4 8.4 0 0 1-12.3 7.4L3 21l2.1-5.6A8.4 8.4 0 1 1 21 11.5z"/></svg>וואטסאפ</a></div>
<ul class="checks"><li>ייעוץ והצעת מחיר בחינם</li><li>אחריות מלאה בכתב</li><li>הגעה בזמן שנקבע</li></ul>
</div></div></section>
<div class="tcards"><div class="tc"><svg viewBox="0 0 48 48" aria-hidden="true"><path d="M24 4 8 10v12c0 11 7 19 16 22 9-3 16-11 16-22V10z" fill="#E3F1F7" stroke="#01344A" stroke-width="2.5" stroke-linejoin="round"/><path d="m17 24 5 5 9-10" fill="none" stroke="#80CD29" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/></svg><b>אחריות בכתב</b><span>על כל טיפול, ביומן ביצוע מסודר</span></div>
<div class="tc"><svg viewBox="0 0 48 48" aria-hidden="true"><circle cx="24" cy="24" r="18" fill="#E3F1F7" stroke="#01344A" stroke-width="2.5"/><path d="M24 13v11l7 5" fill="none" stroke="#01344A" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg><b>מגיעים בזמן</b><span>בתיאום מראש, גם בערב</span></div>
<div class="tc"><svg viewBox="0 0 48 48" aria-hidden="true"><path d="M40 8C22 8 10 16 10 30c0 3 1 6 2 8 2-9 9-16 18-20-7 5-12 11-15 21 3 1 6 1 8 1 13 0 17-13 17-32z" fill="#80CD29" stroke="#3f8f12" stroke-width="2" stroke-linejoin="round"/></svg><b>חומרים מאושרים</b><span>בטוח לבית עם ילדים ובעלי חיים</span></div></div>
{lead_form()}
<section class="sec"><div class="wrap split">
<div><span class="eyebrow">למה הדברה 360</span><h2>הדברה מקצועית, ב־360 מעלות</h2>
<p class="intro" style="margin-top:16px">אנחנו לא רק מרססים. מאבחנים את מקור הבעיה, מטפלים בשיטה המתאימה ונשארים זמינים גם אחרי, כדי שהמזיקים לא יחזרו.</p>{FEAT}</div>
<div class="photo"><img src="/assets/photo-window.webp" alt="מדביר מוסמך בעבודה בתוך בית" width="786" height="450"><div class="g"><span class="stars" aria-label="5 כוכבים">★★★★★</span><br>לקוחות ממליצים עלינו בגוגל</div></div>
</div></section>
<section class="sec soft" id="services"><div class="wrap">
<div class="sec-head"><div><span class="eyebrow">שירותי הדברה</span><h2>פתרון מותאם לכל מקום</h2></div><a href="{url("שירותי-הדברה")}" style="font-weight:700">לכל השירותים ←</a></div>
<div class="cards">{serv_card(SERV_BY["הדברה-בדירות"],"טיפול נקי ושקט, כולל הדברה ללא ריסוס בג׳לים ובגרגירים.")}{serv_card(SERV_BY["הדברת-בניינים"],"שטחים משותפים, ביובים ואחזקה שוטפת לוועדי בית.")}{serv_card(SERV_BY["אחזקה-שותפת-למסעדות"],"עמידה בדרישות התברואה, בלי לעצור את העסק.")}</div>
</div></section>
<section class="sec" id="pests"><div class="wrap">
<div class="sec-head"><div><span class="eyebrow">סוגי מזיקים</span><h2>מטפלים בכל סוגי המזיקים</h2></div></div>
{pest_tiles(TOP_TILES)}
{photo_id_box()}
</div></section>
<section class="sec" id="guides" style="padding-top:0"><div class="wrap">
<div class="sec-head"><div><span class="eyebrow">מדריכים</span><h2>מדריכים מועילים</h2></div><a href="{url("בלוג")}" style="font-weight:700">לכל המדריכים ←</a></div>
<div class="gcards">{"".join(f'<a class="gcard" href="{url("בלוג/"+g["slug"])}"><strong>{E(g["h1"])}</strong><span>{E(g["desc"])}</span><em>לקריאה ←</em></a>' for g in GUIDES[:3])}</div>
</div></section>
<section class="sec soft" id="reviews"><div class="wrap">
<div class="sec-head"><div><span class="eyebrow">ביקורות מ־Google</span><h2>לקוחות ממליצים</h2></div><a href="{url("המלצות")}" style="font-weight:700">לכל {REVIEWS_DATA["count"]} הביקורות ←</a></div>
{rating_bar()}{reviews_html(REVIEWS[:3])}
</div></section>
<section class="sec"><div class="wrap split" style="align-items:flex-start">
<div><h2>איך זה עובד</h2>{STEPS}</div>
<div><h2>אזורי שירות</h2><p class="intro" style="margin:16px 0">מגיעים אליכם בכל אזור המרכז:</p>{city_chips()}</div>
</div></section>
{ctaband("יש מזיק בבית? נפתור את זה היום.", f"הדברה החל מ־{PRICE_FROM} ₪ · ייעוץ והצעת מחיר בחינם.")}'''
pages[""] = page("", f"הדברה 360 | חברת הדברה מקצועית במרכז, החל מ־{PRICE_FROM} ₪", "הדברה מקצועית לכל סוגי המזיקים: תיקנים, נמלים, פשפש מיטה, מכרסמים ועוד. מדביר מוסמך, רישיון 2849, אחריות בכתב. חייגו 055-9992266.", home, head_extra=HOME_HEAD)

# ---------------- Guides (blog) ----------------
def gtext(s):
    out = E(s)
    out = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", out)
    return re.sub(r"\[\[([^|\]]+)\|([^\]]+)\]\]", lambda m: f'<a href="{url(html.unescape(m.group(2)))}">{m.group(1)}</a>', out)

def gpath(g):
    return "בלוג/" + g["slug"]

def guides_for(path):
    return [g for g in GUIDES if path in g["related"]]

def guide_box(path):
    gs = guides_for(path)
    if not gs: return ""
    return '<div class="gbox"><strong>מדריך מומלץ:</strong> ' + " · ".join(f'<a href="{url(gpath(g))}">{E(g["h1"])}</a>' for g in gs) + '</div>'

# Pest pages
for p in PESTS:
    d = DEEP_PESTS.get(p["path"], {})
    trail = [("דף הבית",""),("הדברת מזיקים","הדברת-מזיקים"),(p["name"],p["path"])]
    signs = "".join(f"<div>{E(s_)}</div>" for s_ in p["signs"])
    faqs = p["faq"] + d.get("faq", []) + [("יש אחריות על הטיפול?","כן. על כל הדברה ניתנת אחריות בכתב, לפי סוג המזיק.")]
    others = [q for q in PESTS if q["path"] != p["path"]][:8]
    rev = [r for r in REVIEWS if "פשפש" in r[1]] if "פשפש" in p["name"] else REVIEWS[1:3]
    toc = [("about", f"מה צריך לדעת על {p['name']}"), ("signs","סימנים לנגיעות")]
    if d.get("why"): toc.append(("why","למה הם מגיעים"))
    toc += [("treat","איך אנחנו מטפלים"),("price","כמה זה עולה")]
    if p.get("prep"): toc.append(("prep","איך מתכוננים"))
    if d.get("after"): toc.append(("after","אחרי הטיפול"))
    if d.get("prevent"): toc.append(("prevent","איך מונעים חזרה"))
    toc.append(("faq","שאלות נפוצות"))
    about = "".join(f'<p>{E(x)}</p>' for x in d.get("about", []))
    combos_here = [(pk, cp) for (pk, cp) in COMBOS if COMBO_PESTS[pk]["pest"] == p["path"]]
    combo_links = ""
    if combos_here:
        combo_links = '<div class="chips" style="margin-bottom:18px">' + "".join(f'<a class="chip" href="{url(combo_path(pk,cp))}">{COMBO_PESTS[pk]["short"]} {CITY_BY_ALL[cp]["prep"]}</a>' for pk,cp in combos_here) + '</div>'
    body = f'''{sub_hero(trail, p["h1"] + " מקצועית, עם אחריות בכתב", E(p["intro"].split(". ")[0]) + ". מדביר מוסמך מגיע, מאבחן ומטפל עד הסוף.", bug=("ant" if "נמל" in p["name"] else "roach"))}
<section class="sec"><div class="wrap narrow">
{toc_html(toc)}
{H2("about", f"מה צריך לדעת על {p['name']}", ";margin-top:34px")}
<div class="prose" style="margin-top:16px"><p>{E(p["intro"])}</p>{about}</div>
<h3 id="signs" style="font-size:24px;margin-top:34px;scroll-margin-top:90px">סימנים לנגיעות</h3>
<div class="signs">{signs}</div>
{f'{H2("why","למה הם מגיעים",";margin-top:40px;font-size:30px")}<div class="prose" style="margin-top:14px">' + "".join(f"<p>{E(x)}</p>" for x in d["why"]) + (f'<p><strong>למה לא לחכות:</strong> {E(d["risks"])}</p>' if d.get("risks") else "") + '</div>' if d.get("why") else ""}
{photo_id_box()}
{guide_box(p["path"])}
</div></section>
<section class="sec soft"><div class="wrap narrow">
{H2("treat","איך אנחנו מטפלים")}
{steps_html(d["steps"]) if d.get("steps") else STEPS.replace("אבחון מקור הבעיה וטיפול בשיטה המתאימה.", E(p["method"]))}
<div id="price" class="pricebox" style="scroll-margin-top:90px"><span><span style="display:block;color:#C7D8E0;font-size:16px">מחיר משוער</span><strong>{E(p["price"])}</strong></span>{phone_btn(label="")}</div>
<p style="font-size:15px;color:var(--muted);margin-top:10px">המחיר הסופי נקבע לפי גודל הנכס והיקף הנגיעות. <a href="{url("מחירון")}">למחירון המלא</a></p>
</div></section>
{f'<section class="sec"><div class="wrap narrow">{H2("prep","איך מתכוננים להדברה?")}{ul(p["prep"])}</div></section>' if p.get("prep") else ""}
{f'<section class="sec"><div class="wrap narrow split" style="align-items:flex-start"><div>{H2("after","אחרי הטיפול",";font-size:30px")}{ul(d["after"])}</div><div>{H2("prevent","איך מונעים חזרה",";font-size:30px")}{ul(d["prevent"])}</div></div></section>' if d.get("after") else ""}
<section class="sec soft"><div class="wrap narrow"><h2>מה הלקוחות אומרים</h2><div style="margin-top:22px">{reviews_html(rev[:2])}</div></div></section>
<section class="sec"><div class="wrap narrow">{H2("faq", f"שאלות נפוצות על {p['name']}")}{faq_html(faqs)}</div></section>
<section class="sec soft"><div class="wrap narrow"><h2 style="font-size:26px;margin-bottom:16px">{p["h1"].split(":")[0]} באזור שלכם</h2>{combo_links}{city_chips()}
<h2 style="font-size:26px;margin:34px 0 16px">מזיקים נוספים</h2>{pest_tiles(others)}</div></section>
{ctaband(f"{p['name']}? אל תחכו שזה יתפשט.")}'''
    pf = price_from_txt(p["price"])
    title = f'{p["h1"]} ✔ ' + (f'מ־{pf} ₪, ' if pf else '') + 'מדביר מוסמך | הדברה 360'
    desc = f'{p["h1"]} במרכז: {p["intro"].split(". ")[0].rstrip(".")}. אבחון, טיפול בחומרים מאושרים ואחריות בכתב. חייגו {PHONE}.'
    pages[p["path"]] = page(p["path"], title, desc[:300], body, [faq_schema(faqs), crumbs_schema(trail)])

# Pests hub
trail = [("דף הבית",""),("הדברת מזיקים","הדברת-מזיקים")]
body = f'''{sub_hero(trail, "הדברת מזיקים מכל הסוגים", "תיקנים, נמלים, פשפש מיטה, מכרסמים, טרמיטים ועוד. בחרו את המזיק ותגלו איך מזהים אותו ואיך אנחנו מטפלים בו.")}
<section class="sec"><div class="wrap"><h2 style="margin-bottom:24px">בחרו מזיק</h2>{pest_tiles(PESTS, more=False)}
<h2 style="margin:48px 0 24px">שירותים נוספים</h2><div class="tiles"><a class="tile" href="{url("הרחקת-יונים")}">הרחקת יונים</a><a class="tile" href="{url("לוכד-נחשים")}">לכידת נחשים</a></div></div></section>
{ctaband("לא בטוחים מה המזיק? שלחו תמונה ונזהה.")}'''
pages["הדברת-מזיקים"] = page("הדברת-מזיקים", "הדברת מזיקים: כל סוגי המזיקים | הדברה 360", "מדריך הדברת מזיקים: תיקנים, נמלים, פשפש מיטה, מכרסמים, פרעושים, טרמיטים ועוד. מדביר מוסמך עם אחריות בכתב.", body, [crumbs_schema(trail)])

# Services
TRUST_DEEP = '<section class="sec soft"><div class="wrap"><h2 style="text-align:center;margin-bottom:24px">למה אפשר לסמוך עלינו</h2><div class="trust3"><div><span class="ti"><svg viewBox="0 0 24 24" width="30" height="30" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="14" rx="2"/><circle cx="9" cy="10" r="2.2"/><path d="M6 15c.6-1.4 1.7-2 3-2s2.4.6 3 2M14 9h4M14 12h3"/></svg></span><h3>מדביר מוסמך</h3><p>רישיון מדביר במבנים ובשטח פתוח מס׳ ' + str(LICENSE) + ', בתוקף.</p></div><div><span class="ti"><svg viewBox="0 0 24 24" width="30" height="30" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3l7 3v5c0 4.5-3 8-7 10-4-2-7-5.5-7-10V6l7-3z"/><path d="M8.5 12l2.5 2.5 4.5-5"/></svg></span><h3>חומרים מאושרים</h3><p>משתמשים רק בחומרים שמאושרים לשימוש בבתי מגורים, במינון לפי ההוראות.</p></div><div><span class="ti"><svg viewBox="0 0 24 24" width="30" height="30" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 3h8l4 4v14H7z"/><path d="M15 3v4h4M10 12h6M10 16h6"/></svg></span><h3>יומן ביצוע בכתב</h3><p>בסוף כל טיפול מקבלים יומן מפורט: מה נעשה, באילו חומרים, והנחיות ברורות.</p></div></div></div></section>'
SVC_HEAD = '<link rel="preload" as="image" href="/assets/photo-sprayer.webp" fetchpriority="high"><style>.svc-deep h2{font-size:30px;margin-top:26px;color:var(--navy)}.svc-deep h2:first-child{margin-top:0}.svc-deep .list li{margin-bottom:6px}.svc-deep ol.list{padding-right:22px}.svc-deep .tablebox{margin:4px 0}.svc-deep .tiles{margin-top:4px}@media(max-width:899px){.svc-deep h2{font-size:25px}}.svc-deep ul.list{list-style:none;padding-right:0}.svc-deep ul.list li{position:relative;padding-right:30px}.svc-deep ul.list li::before{content:"";position:absolute;right:0;top:.2em;width:20px;height:20px;border-radius:50%;background:#5DB02B url("data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 24 24%27 fill=%27none%27 stroke=%27white%27 stroke-width=%273.2%27 stroke-linecap=%27round%27 stroke-linejoin=%27round%27%3E%3Cpath d=%27M6 12.5l4 4 8-9%27/%3E%3C/svg%3E") center/13px no-repeat}.callout{margin:18px 0;padding:18px 20px;border-radius:14px;background:#EAF6FC;border-right:5px solid #0F6E8C}.callout strong{display:block;color:var(--navy);font-size:19px;margin-bottom:6px}.callout p{margin:0}.trust3{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}.trust3>div{background:#fff;border:1px solid #E3ECEF;border-radius:16px;padding:22px;box-shadow:0 2px 14px rgba(1,52,74,.08);text-align:center}.trust3 .ti{display:inline-flex;width:56px;height:56px;border-radius:50%;background:#EAF6FC;color:#0F6E8C;align-items:center;justify-content:center}.trust3 h3{margin:12px 0 6px;font-size:20px;color:var(--navy)}.trust3 p{margin:0;color:var(--text2)}@media(max-width:899px){.trust3{grid-template-columns:1fr}}.svc-deep td.pr{white-space:nowrap}.svc-fig{margin:26px 0 0}.svc-fig img{width:100%;height:auto;display:block;border-radius:16px;box-shadow:0 6px 24px rgba(1,52,74,.12)}.svc-fig figcaption{margin-top:10px;font-size:15px;color:var(--text2);text-align:center}.svc-deep h2[id],#faq{scroll-margin-top:96px}.tocsec{padding-bottom:0}.tocsec+.sec{padding-top:44px}.toc{background:#fff;border:1px solid #E3ECEF;border-radius:16px;padding:18px 22px;box-shadow:0 2px 14px rgba(1,52,74,.06)}.toc strong,.toc summary{font-size:19px;font-weight:800;color:var(--navy)}.toc ol{margin:10px 0 0;padding-right:22px;columns:2;column-gap:32px}.toc li{margin-bottom:7px;break-inside:avoid}.toc a{color:#0F6E8C;text-decoration:none;font-weight:600}.toc a:hover{text-decoration:underline}.toc-m{display:none}.toc summary{cursor:pointer;list-style:none;display:flex;justify-content:space-between;align-items:center}.toc summary::-webkit-details-marker{display:none}.toc summary::after{content:"+";font-size:26px;color:#5DB02B;line-height:1}.toc details[open] summary::after{content:"−"}@media(max-width:899px){.toc-d{display:none}.toc-m{display:block}.toc ol{columns:1}.toc{padding:14px 18px}}.svc-deep table.prices td:nth-child(3){font-weight:400;white-space:normal}@media(max-width:899px){.svc-deep .tablebox{overflow:visible;border:0;box-shadow:none;background:none}.svc-deep table.prices,.svc-deep table.prices tbody,.svc-deep table.prices tr,.svc-deep table.prices td{display:block;width:auto}.svc-deep table.prices thead{display:none}.svc-deep table.prices tr{background:#fff;border:1px solid #E3ECEF;border-radius:14px;padding:14px 16px;margin-bottom:12px;box-shadow:0 2px 10px rgba(1,52,74,.06)}.svc-deep table.prices td{border:0;padding:4px 0}.svc-deep table.prices td.tp{font-size:19px;color:var(--navy);padding-bottom:8px;margin-bottom:4px;border-bottom:1px solid #E3ECEF}.svc-deep table.prices td[data-l]::before{content:attr(data-l) ": ";font-weight:700;color:var(--navy)}}</style>'
for s in SERVICES:
    trail = [("דף הבית",""),("שירותי הדברה","שירותי-הדברה"),(s["name"],s["path"])]
    pts = "".join(f"<li>{E(x)}</li>" for x in s["points"])
    others = [x for x in SERVICES if x["path"] != s["path"]][:6]
    body = f'''{sub_hero(trail, s["h1"], E(s["intro"].split(". ")[0].rstrip(".")) + ".", s["img"])}
<section class="sec"><div class="wrap split">
<div><h2>{s["h1"]}</h2><p class="intro" style="margin-top:16px">{E(s["intro"])}</p><h3 style="font-size:24px;margin-top:28px">מה כולל השירות</h3><ul class="list">{pts}</ul></div>
<div class="photo"><img src="/assets/{s["img"]}.webp" alt="" width="786" height="450" loading="lazy"></div>
</div></section>
<section class="sec soft"><div class="wrap split" style="align-items:flex-start"><div><h2>איך זה עובד</h2>{STEPS}</div><div><h2>מה הלקוחות אומרים</h2><div style="margin-top:22px">{reviews_html(REVIEWS[2:4])}</div></div></div></section>
<section class="sec"><div class="wrap"><h2 style="font-size:26px;margin-bottom:16px">שירותים נוספים</h2><div class="tiles">{"".join(f'<a class="tile" href="{url(x["path"])}">{x["name"]}</a>' for x in others)}</div>
<h2 style="font-size:26px;margin:34px 0 16px">סוגי מזיקים</h2>{pest_tiles(TOP)}</div></section>
{ctaband(s["name"] + "? דברו איתנו עכשיו.")}'''
    pages[s["path"]] = page(s["path"], f'{s["h1"]} | הדברה 360', f'{s["h1"]} במרכז: {s["intro"][:90]}... חייגו {PHONE}.', body, [crumbs_schema(trail)])
    if s["path"] in DEEP_SERVICES:
        d = DEEP_SERVICES[s["path"]]
        trs = "".join(f"<tr><td class=\"tp\"><strong>{E(a)}</strong></td><td data-l=\"שיטת הטיפול\">{E(b)}</td><td data-l=\"יציאה מהבית\">{E(c)}</td></tr>" for a,b,c in d["table"])
        table = f'<div class="tablebox"><table class="prices"><thead><tr><th scope="col">מזיק</th><th scope="col">שיטת הטיפול</th><th scope="col">יציאה מהבית</th></tr></thead><tbody>{trs}</tbody></table></div>'
        city_links = '<p>אנחנו מבצעים הדברת דירות בכל אזור המרכז. מידע על הדברה בעיר שלכם:</p><div class="tiles">' + "".join(f'<a class="tile" href="{url(c["path"])}">הדברה {c["prep"]}</a>' for c in CITIES if c.get("prep")) + '</div>'
        secs = ""; k = 0; toc = []
        for h, htm in d["sections"]:
            mid = "__TABLE__" in htm
            htm = htm.replace("__TABLE__", table).replace("__CITIES__", city_links)
            htm = re.sub(r"__URL_([^_]+(?:-[^_]+)*)__", lambda m: url(m.group(1)), htm)
            toc.append(h)
            secs += f'<section class="sec{" soft" if k % 2 else ""}"><div class="wrap {"" if mid else "narrow "}prose svc-deep"><h2 id="s{len(toc)}">{E(h)}</h2>{htm}</div></section>'
            if mid:
                secs += ctaband("רוצים הצעת מחיר מדויקת לדירה שלכם?", "שיחה קצרה, ואתם יודעים בדיוק כמה זה עולה — לפני שמתחילים.")
            k += 1
            if h.startswith("אחריות"):
                secs += TRUST_DEEP.replace('class="sec soft"', 'class="sec soft"' if k % 2 else 'class="sec"'); k += 1
        svc_schema = {"@context":"https://schema.org","@type":"Service","serviceType":s["name"],"name":d["h1"],"areaServed":"מרכז הארץ","provider":{"@type":"PestControl","name":"הדברה 360","telephone":"+972-55-999-2266","url":DOMAIN+"/"}}
        lis = "".join(f'<li><a href="#s{i+1}">{E(h)}</a></li>' for i, h in enumerate(toc)) + '<li><a href="#faq">שאלות נפוצות</a></li>'
        toc_box = f'<section class="sec tocsec"><div class="wrap narrow"><nav class="toc" aria-label="תוכן העניינים"><details class="toc-m"><summary>מה בעמוד הזה</summary><ol>{lis}</ol></details><div class="toc-d"><strong>מה בעמוד הזה</strong><ol>{lis}</ol></div></nav></div></section>'
        body = f'''{sub_hero(trail, d["h1"], E(d["lead"]), s["img"], icon=False)}
{toc_box}
{secs}
<section class="sec"><div class="wrap narrow prose svc-deep"><h2 id="faq">שאלות נפוצות על הדברה בדירה</h2>{faq_html(d["faq"])}</div></section>
<section class="sec soft"><div class="wrap"><h2 style="margin-bottom:22px">מה הלקוחות אומרים</h2>{reviews_html(REVIEWS[:3])}</div></section>
<section class="sec"><div class="wrap"><h2 style="font-size:26px;margin-bottom:16px">שירותים נוספים</h2><div class="tiles">{"".join(f'<a class="tile" href="{url(x["path"])}">{x["name"]}</a>' for x in others)}</div>
<h2 style="font-size:26px;margin:34px 0 16px">סוגי מזיקים</h2>{pest_tiles(TOP)}</div></section>
{ctaband(s["name"] + "? דברו איתנו עכשיו.")}'''
        pages[s["path"]] = page(s["path"], d["title"], d["desc"], body, [crumbs_schema(trail), faq_schema(d["faq"]), svc_schema], head_extra=SVC_HEAD)

trail = [("דף הבית",""),("שירותי הדברה","שירותי-הדברה")]
body = f'''{sub_hero(trail, "שירותי הדברה", "הדברה לדירות, לבתים פרטיים, לבניינים, לעסקים ולמוסדות, בשיטה שמתאימה לכל מקום.")}
<section class="sec"><div class="wrap"><div class="cards">{"".join(serv_card(s) for s in SERVICES)}</div></div></section>
{ctaband("לא בטוחים איזה שירות מתאים? נייעץ בחינם.")}'''
pages["שירותי-הדברה"] = page("שירותי-הדברה", "שירותי הדברה לבית ולעסק | הדברה 360", "שירותי הדברה: דירות, בתים פרטיים, בניינים, מסעדות, מוסדות חינוך, הדברה ללא ריסוס, הרחקת יונים ולכידת נחשים.", body, [crumbs_schema(trail)])

# Cities
for ci, c in enumerate(CITIES):
    d = DEEP_CITIES.get(c["path"], {}); L = LOCAL.get(c["path"], {})
    trail = [("דף הבית",""),("אזורי שירות","אזורי-שירות"),(c["name"],c["path"])]
    faqs = [(f"כמה עולה הדברה {c['prep']}?", "המחיר תלוי בסוג המזיק, בגודל הנכס ובהיקף הנגיעות. מתקשרים, מתארים את הבעיה ומקבלים הצעת מחיר בחינם בטלפון."),
            ("אתם עובדים גם עם ועדי בית ועסקים?","כן. אנחנו מבצעים הדברה לשטחים משותפים, אחזקה שוטפת לבניינים ולמסעדות, והדברה למוסדות חינוך."),
            ("כמה זמן צריך לצאת מהבית?","בהדברה בריסוס בדרך כלל צריך לצאת לכשעה. בהדברה בג׳לים אין צורך לצאת. המדביר ייתן הנחיות מדויקות."),
            ("יש אחריות על העבודה?","כן, כל עבודה מקבלת אחריות בכתב.")] + d.get("faq", [])
    if L.get("types"):  # ערים במעגל הראשון: פחות שאלות כלליות, יותר מקומיות
        faqs = [faqs[0], faqs[3]] + L.get("faq", []) + d.get("faq", [])
    elif L.get("faq"):
        faqs = faqs + L["faq"]
    arrive = f'<div style="margin-top:22px;background:#eef7f1;border:1px solid #cfe6d8;border-radius:14px;padding:16px 18px"><b style="font-size:18px">🚐 מדבירים באזור, הגעה מהירה</b><p style="margin:6px 0 0">{E(L["arrive"])}</p></div>' if L.get("arrive") else ""
    season = f'<div class="prose" style="margin:14px 0 22px"><h3>מה אנחנו רואים {c["prep"]} לאורך השנה</h3><p>{E(L["season"])}</p></div>' if L.get("season") else ""
    if L.get("types"):
        types_html = "".join(f"<h3>{E(t)}</h3><p>{E(x)}</p>" for t, x in L["types"])
    else:
        types_html = f"""<h3>דירה בבניין</h3><p>בדירה, רוב המזיקים מגיעים מהביוב, מהשטחים המשותפים או מדירות שכנות. אנחנו מטפלים בניקוזים, בפנלים ובנקודות הכניסה, ומתאימים את השיטה לבית: ריסוס, ג׳לים או מלכודות. בבית עם תינוקות או חיות מחמד אפשר לבחור בטיפול ללא ריסוס.</p>
<h3>בית פרטי או דירת גן</h3><p>בבית עם חצר המזיקים מגיעים בעיקר מבחוץ: מהגינה, מבורות הביוב, מהמחסן ומעצים שנוגעים בבית. לכן הטיפול כולל גם את החצר, את הביובים ואת הצמחייה, ולא רק את הבית עצמו.</p>
<h3>בניין משותף וועד בית</h3><p>הדברה של הלובי, חדרי המדרגות, חדר האשפה, המקלט, החניון ובורות הביוב מונעת מהמזיקים לחזור לדירות. אנחנו מציעים לוועדי בית {c['prep']} גם אחזקה שוטפת בתדירות קבועה.</p>
<h3>עסקים, מסעדות ומשרדים</h3><p>בעסקים אנחנו עובדים בשעות שלא מפריעות לפעילות, בחומרים מאושרים, ומספקים יומן ביצוע מסודר אחרי כל טיפול. למסעדות ולעסקי מזון אנחנו מציעים אחזקה שוטפת.</p>"""
    rv = [REVIEWS[(ci*2) % len(REVIEWS)], REVIEWS[(ci*2+1) % len(REVIEWS)]]
    about = "".join(f'<p>{E(x)}</p>' for x in d.get("about", []))
    hoods = ""
    if d.get("hoods"):
        hoods = f'<h3 style="font-size:22px;margin-top:28px">שכונות שבהן אנחנו עובדים {c["prep"]}</h3><div class="chips" style="margin-top:12px">' + "".join(f'<span class="chip" style="background:#fff;border:1px solid var(--line)">{E(h)}</span>' for h in d["hoods"]) + '<span class="chip" style="background:#fff;border:1px solid var(--line)">וכל שאר השכונות</span></div>'
    pests_list = ""
    if d.get("pests"):
        pests_list = '<div class="signs">' + "".join(f'<div><a href="{url(pp)}" style="font-weight:800;font-size:19px">{E(n)}</a><br><span style="color:var(--text2)">{E(r)}</span></div>' for n, pp, r in d["pests"]) + '</div>'
    combos_here = [pk for (pk, cp) in COMBOS if cp == c["path"]]
    combo_links = ""
    if combos_here:
        combo_links = f'<h3 style="font-size:22px;margin-top:28px">מדריכים מפורטים {c["prep"]}</h3><div class="chips" style="margin-top:12px">' + "".join(f'<a class="chip" href="{url(combo_path(pk,c["path"]))}">{COMBO_PESTS[pk]["h1"]} {c["prep"]}</a>' for pk in combos_here) + '</div>'
    toc = [("about", f"הדברה {c['prep']}"), ("pests", f"המזיקים הנפוצים {c['prep']}"), ("types","לפי סוג הנכס"), ("all","כל סוגי ההדברה"), ("prices","מחירים"), ("how","איך זה עובד"), ("faq","שאלות נפוצות")]
    body = f'''{sub_hero(trail, f"הדברה {c['prep']}: מדביר מוסמך עד הבית", f"הדברה לדירות, לבניינים ולעסקים {c['prep']}. חומרים מאושרים, הגעה בזמן ואחריות בכתב.", "photo-window")}
<section class="sec"><div class="wrap narrow">
{toc_html(toc)}
{H2("about", f"שירותי הדברה {c['prep']}", ";margin-top:34px")}
<div class="prose" style="margin-top:16px"><p>{E(c["local"])}</p>{about}{f"<p>{E(d['homes'])}</p>" if d.get("homes") else ""}</div>
{arrive}
{hoods}
<div class="cards" style="margin-top:28px">{serv_card(SERV_BY["הדברה-בדירות"],"טיפול נקי ושקט, כולל אפשרות להדברה ללא ריסוס.")}{serv_card(SERV_BY["הדברת-בניינים"],"לובי, חדרי אשפה, מקלטים, ביובים ואחזקה שוטפת.")}{serv_card(SERV_BY["אחזקה-שותפת-למסעדות"],"אחזקה שוטפת לעסקי מזון, בשעות שמתאימות לכם.")}</div>
</div></section>
<section class="sec soft"><div class="wrap narrow">{H2("pests", f"המזיקים הנפוצים {c['prep']}")}
{season}
{pests_list}
{combo_links}
</div></section>
<section class="sec"><div class="wrap narrow">{H2("types", f"הדברה {c['prep']} לפי סוג הנכס")}
<div class="prose" style="margin-top:16px">
{types_html}
</div></div></section>
<section class="sec soft"><div class="wrap narrow">{H2("all", f"כל סוגי ההדברה {c['prep']}")}
<div class="chips" style="margin-top:14px">{"".join(f'<a class="chip" href="{url(q["path"])}">{E(q["h1"].split(":")[0])}</a>' for q in PESTS)}</div></div></section>
<section class="sec"><div class="wrap narrow">{H2("prices", f"מחירי הדברה {c['prep']}")}{mini_prices()}
{photo_id_box()}</div></section>
<section class="sec soft"><div class="wrap narrow split" style="align-items:flex-start">
<div>{H2("how","איך זה עובד",";font-size:30px")}{STEPS}</div>
<div>{f'<h2 style="font-size:30px">טיפים {c["prep"]}</h2>' + ul(d["tips"]) if d.get("tips") else ""}</div>
</div></section>
<section class="sec"><div class="wrap narrow"><h2>לקוחות ממליצים</h2><div style="margin-top:22px">{reviews_html(rv)}</div></div></section>
<section class="sec soft"><div class="wrap narrow">{H2("faq", f"שאלות נפוצות: הדברה {c['prep']}")}{faq_html(faqs)}</div></section>
<section class="sec"><div class="wrap narrow"><h2 style="font-size:26px;margin-bottom:16px">מגיעים גם לערים הסמוכות</h2>{city_chips([n for n in c["near"] if n in CITY_BY])}</div></section>
{ctaband(f"צריכים מדביר {c['prep']}? דברו איתנו עכשיו.")}'''
    pages[c["path"]] = page(c["path"], f'הדברה {c["prep"]} ✔ מדביר מוסמך עם אחריות | הדברה 360', f'הדברה {c["prep"]}: מדביר מוסמך לדירות, בניינים ועסקים. חומרים מאושרים, אחריות בכתב והצעת מחיר בחינם. חייגו {PHONE}.', body, [faq_schema(faqs), crumbs_schema(trail)])

# Pest + city pages
for (pk, cp), cd in COMBOS.items():
    P = COMBO_PESTS[pk]; p = PEST_BY[P["pest"]]; d = DEEP_PESTS.get(P["pest"], {}); c = CITY_BY[cp]; dc = DEEP_CITIES.get(cp, {})
    path = combo_path(pk, cp)
    h1 = f'{P["h1"]} {c["prep"]}'
    trail = [("דף הבית",""),("אזורי שירות","אזורי-שירות"),(c["name"],cp),(f'{P["short"]} {c["prep"]}', path)]
    signs = "".join(f"<div>{E(s_)}</div>" for s_ in p["signs"])
    price_q = (f"כמה עולה {P['h1'].split(' (')[0]} {c['prep']}?", f"המחיר מתחיל מכ־{P['price_from']} ₪ לדירה ותלוי בגודל הנכס ובהיקף הנגיעות. מחיר משוער: {p['price']}. הצעת מחיר מדויקת ניתנת בטלפון, בחינם.") if P["price_from"] else (f"כמה עולה {P['h1']} {c['prep']}?", f"{p['price']}.")
    faqs = [price_q, (f"כמה מהר אתם מגיעים {c['prep']}?", f"אנחנו נותנים שירות בכל שכונות {c['name']}, ובדרך כלל אפשר לתאם הגעה באותו יום או למחרת.")] + d.get("faq", [])[:3] + [("יש אחריות?","כן. על כל הדברה ניתנת אחריות בכתב, לפי סוג המזיק.")]
    others_here = [k for k in COMBO_PESTS if k != pk and (k, cp) in COMBOS]
    other_cities = [x for x in COMBO_CITIES if x != cp and (pk, x) in COMBOS]
    hoods = ""
    if dc.get("hoods"):
        hoods = f'<p style="margin-top:18px;color:var(--text2)"><strong>שכונות שבהן אנחנו עובדים:</strong> {E(", ".join(dc["hoods"]))} וכל שאר השכונות.</p>'
    toc = [("about", f"{P['short']} {c['prep']}"), ("signs","איך מזהים"), ("treat","איך מטפלים"), ("price","מחיר"), ("prevent","מניעה"), ("faq","שאלות נפוצות")]
    body = f'''{sub_hero(trail, h1 + ": מדביר מוסמך עם אחריות", E(cd["intro"].split(". ")[0].rstrip(".")) + ".", "photo-window", bug=("ant" if "נמל" in P["short"] else "roach"))}
<section class="sec"><div class="wrap narrow">
{toc_html(toc)}
{H2("about", h1, ";margin-top:34px")}
<div class="prose" style="margin-top:16px"><p>{E(cd["intro"])}</p><p>{E(cd["local"])}</p>{"".join(f"<p>{E(x)}</p>" for x in d.get("about", [])[:2])}</div>
{hoods}
<h3 id="signs" style="font-size:24px;margin-top:34px;scroll-margin-top:90px">איך מזהים {P["short"]}?</h3>
<div class="signs">{signs}</div>
{photo_id_box()}
</div></section>
<section class="sec soft"><div class="wrap narrow">
{H2("treat", f"איך אנחנו מטפלים ב{P['short']} {c['prep']}")}
{steps_html(d["steps"]) if d.get("steps") else ""}
<div id="price" class="pricebox" style="scroll-margin-top:90px"><span><span style="display:block;color:#C7D8E0;font-size:16px">מחיר משוער {c["prep"]}</span><strong>{E(p["price"])}</strong></span>{phone_btn(label="")}</div>
</div></section>
<section class="sec"><div class="wrap narrow split" style="align-items:flex-start"><div>{H2("after","אחרי הטיפול",";font-size:30px")}{ul(d.get("after", []))}</div><div>{H2("prevent","איך מונעים חזרה",";font-size:30px")}{ul(d.get("prevent", []))}</div></div></section>
<section class="sec soft"><div class="wrap narrow"><h2>לקוחות ממליצים</h2><div style="margin-top:22px">{reviews_html(([r for r in REVIEWS if "פשפש" in r[1]]+REVIEWS)[:2] if pk=="פשפש" else REVIEWS[1:3])}</div></div></section>
<section class="sec"><div class="wrap narrow">{H2("faq", f"שאלות נפוצות: {P['short']} {c['prep']}")}{faq_html(faqs)}</div></section>
<section class="sec soft"><div class="wrap narrow">
<h2 style="font-size:26px;margin-bottom:16px">עוד {c["prep"]}</h2><div class="chips"><a class="chip" href="{url(cp)}">הדברה {c["prep"]}</a>{"".join(f'<a class="chip" href="{url(combo_path(k,cp))}">{COMBO_PESTS[k]["h1"]} {c["prep"]}</a>' for k in others_here)}</div>
<h2 style="font-size:26px;margin:30px 0 16px">{P["h1"]} בערים נוספות</h2><div class="chips"><a class="chip" href="{url(P["pest"])}">{P["h1"]}: המדריך המלא</a>{"".join(f'<a class="chip" href="{url(combo_path(pk,x))}">{P["short"]} {CITY_BY[x]["prep"]}</a>' for x in other_cities)}</div>
</div></section>
{ctaband(f"{P['short']} {c['prep']}? נגיע ונפתור.")}'''
    pf = P["price_from"]
    title = f'{h1} ✔ ' + (f'מ־{pf} ₪ · ' if pf else '') + 'מדביר מוסמך | הדברה 360'
    pages[path] = page(path, title, f'{h1}: {cd["intro"].split(". ")[0].rstrip(".")}. מדביר מוסמך, חומרים מאושרים ואחריות בכתב. חייגו {PHONE}.'[:300], body, [faq_schema(faqs), crumbs_schema(trail)])

trail = [("דף הבית",""),("אזורי שירות","אזורי-שירות")]
body = f'''{sub_hero(trail, "אזורי שירות", "אנחנו נותנים שירות הדברה בכל אזור המרכז וגוש דן.")}
<section class="sec"><div class="wrap"><div class="tiles">{"".join(f'<a class="tile" href="{url(c["path"])}">הדברה {c["prep"]}</a>' for c in CITIES)}</div>
<h2 style="margin:48px 0 20px;font-size:30px">מדריכים לפי מזיק ועיר</h2><div class="chips">{"".join(f'<a class="chip" href="{url(combo_path(pk,cp))}">{COMBO_PESTS[pk]["h1"]} {CITY_BY[cp]["prep"]}</a>' for (pk,cp) in COMBOS)}</div></div></section>
{ctaband("לא מצאתם את העיר שלכם? התקשרו, כנראה שנגיע.")}'''
pages["אזורי-שירות"] = page("אזורי-שירות", "אזורי שירות: הדברה במרכז ובגוש דן | הדברה 360", "הדברה בתל אביב, רמת גן, גבעתיים, חולון, בת ים, פתח תקווה, גבעת שמואל, קריית אונו, בני ברק והרצליה.", body, [crumbs_schema(trail)])

# About
trail = [("דף הבית",""),("אודות","אודות")]
body = f'''{sub_hero(trail, "אודות הדברה 360", "מתמחים בהדברת כל סוגי המזיקים, ונותנים מעטפת מלאה לכל צורכי ההדברה בבית ובעסק.", show_price=False)}
<section class="sec"><div class="wrap split" style="align-items:flex-start">
<div class="prose">
<p>הדברה 360 היא חברת הדברה מקצועית שמטפלת בכל סוגי המזיקים: ממזיקים נפוצים כמו נמלים, תיקנים ומכרסמים, ועד בעיות מורכבות יותר כמו טרמיטים ופשפשי מיטה. אנחנו נותנים פתרון מקיף במחיר הוגן, בלי להתפשר על איכות השירות.</p>
<h3>מדבירים עם רישיון הדברה ורישיון לכידת נחשים</h3>
<p>הצוות שלנו מנוסה ומוסמך מטעם המשרד להגנת הסביבה. הניסיון מאפשר לנו להעריך במדויק את חומרת הבעיה ולתת שירות מלא: ניטור, הדברה ואחריות.</p>
<h3>הדברה בטוחה</h3>
<p>הבטיחות של הלקוחות ושל הסביבה קודמת לכל. אנחנו עובדים רק עם חומרים שאושרו ע״י המשרד להגנת הסביבה, כדי לצמצם ככל האפשר את הפגיעה בסביבה.</p>
<h3>פתרון מותאם אישית</h3>
<p>כל בעיה שונה. אנחנו מתחילים בבדיקה יסודית כדי לזהות את שורש הבעיה, ובונים תוכנית טיפול שמתאימה לבית או לעסק שלכם.</p>
<h3>שירות ואחריות</h3>
<p>אנחנו מחויבים לשירות מקצועי ואמין. על כל הדברה ניתנת אחריות בכתב, לפי סוג המזיק.</p>
</div>
<div><img src="/assets/logo-mascot.webp" alt="הדברה 360 - לוגו החברה" width="260" height="260" loading="lazy" style="display:block;margin:0 auto 22px;width:260px;max-width:70%;height:auto">{FEAT}</div>
</div></section>
{ctaband("רוצים להכיר אותנו? התקשרו.")}'''
pages["אודות"] = page("אודות", "אודות הדברה 360 | מדבירים מוסמכים", "הדברה 360: חברת הדברה מקצועית עם מדבירים מוסמכים, רישיון לכידת נחשים, חומרים מאושרים ואחריות בכתב.", body, [crumbs_schema(trail)])

# FAQ
trail = [("דף הבית",""),("שאלות נפוצות","שאלות-נפוצות")]
body = f'''{sub_hero(trail, "שאלות נפוצות על הדברה", "כל מה שצריך לדעת לפני ואחרי הדברה.", show_price=False)}
<section class="sec soft"><div class="wrap narrow">{faq_html(FAQ_GENERAL)}</div></section>
{ctaband("לא מצאתם תשובה? נשמח לענות בטלפון.")}'''
pages["שאלות-נפוצות"] = page("שאלות-נפוצות", "שאלות נפוצות על הדברה | הדברה 360", "איך מתכוננים להדברה, כמה זמן לצאת מהבית, מתי אפשר לשטוף ומה עושים כשיש תינוקות. תשובות ממדביר מוסמך.", body, [faq_schema(FAQ_GENERAL), crumbs_schema(trail)])

# Reviews
ALL_REVIEWS_T = [(r["name"], r["text"], r["date"], r.get("avatar","")) for r in ALL_REVIEWS]
trail = [("דף הבית",""),("ביקורות","המלצות")]
body = f'''{sub_hero(trail, "ביקורות והמלצות", f"כל הביקורות שלנו בגוגל – {REVIEWS_DATA['count']} ביקורות, ממוצע {REVIEWS_DATA['rating']:.1f} כוכבים.", show_price=False)}
<section class="sec soft"><div class="wrap">{rating_bar(True)}{reviews_html(ALL_REVIEWS_T)}</div></section>
{ctaband("מצטרפים ללקוחות המרוצים?")}'''
pages["המלצות"] = page("המלצות", "ביקורות והמלצות לקוחות | הדברה 360", "ביקורות אמיתיות מגוגל על הדברה 360: מקצועיות, אמינות, עמידה בזמנים ומחיר הוגן.", body, [crumbs_schema(trail)])

# Blog
pages_title_short = {p["path"]: p["h1"].split(":")[0] for p in PESTS}
pages_title_short.update({s["path"]: s["h1"] for s in SERVICES})
pages_title_short.update({combo_path(pk, cp): f'{COMBO_PESTS[pk]["short"]} {CITY_BY_ALL[cp]["prep"]}' for pk, cp in COMBOS})
pages_title_short["מחירון"] = "מחירון הדברה"
HE_MONTHS_FULL = HE_MONTHS
def g_date(iso):
    y, m, d = iso.split("-")
    return f"{int(d)} ב{HE_MONTHS[int(m)-1]} {y}"
for g in GUIDES:
    gp = gpath(g)
    trail = [("דף הבית",""),("מדריכים","בלוג"),(g["h1"], gp)]
    secs = ""
    toc = []
    for i,(h, blocks) in enumerate(g["sections"]):
        sid = f"s{i+1}"
        toc.append((sid, h))
        inner = ""
        for bl in blocks:
            if isinstance(bl, tuple) and bl[0] == "ul":
                inner += '<ul class="gul">' + "".join(f"<li>{gtext(x)}</li>" for x in bl[1]) + "</ul>"
            elif isinstance(bl, tuple) and bl[0] == "table":  # טבלת השוואה: כרטיס לכל שורה, נוח גם בטלפון
                hd = bl[1]
                inner += '<div class="cmpcards" style="display:grid;gap:12px;margin:18px 0">' + "".join(
                    '<div style="background:#fff;border:1px solid var(--line);border-radius:14px;padding:14px 16px">'
                    f'<div style="font-weight:800;font-size:19px;margin-bottom:6px">{gtext(r[0])}</div>'
                    + "".join(f'<div style="margin-top:4px"><b style="color:var(--text2);font-weight:700">{E(hd[k])}:</b> {gtext(r[k])}</div>' for k in range(1, len(r)))
                    + '</div>' for r in bl[2]) + '</div>'
            else:
                inner += f"<p>{gtext(bl)}</p>"
        secs += f'{H2(sid, E(h), ";margin-top:38px;font-size:30px")}<div class="prose" style="margin-top:14px">{inner}</div>'
    toc.append(("faq","שאלות נפוצות"))
    rel = "".join(f'<a class="chip" href="{url(r)}">{E(pages_title_short.get(r, r.split("/")[-1].replace("-"," ")))}</a>' for r in g["related"])
    others = [o for o in GUIDES if o is not g]
    more = "".join(f'<li><a href="{url(gpath(o))}">{E(o["h1"])}</a></li>' for o in others)
    body = f'''{sub_hero(trail, E(g["h1"]), E(g["lead"]), show_price=False)}
<article class="sec"><div class="wrap narrow">
<p class="gmeta">מאת זוהר אהרוני, מדביר מוסמך (רישיון {LICENSE}) · {g_date(g["date"])}</p>
{toc_html(toc)}
{secs}
{photo_id_box()}
{H2("faq", "שאלות נפוצות", ";margin-top:40px;font-size:30px")}{faq_html(g["faq"])}
<h2 style="font-size:24px;margin:38px 0 14px">עמודים קשורים</h2><div class="chips">{rel}</div>
<h2 style="font-size:24px;margin:30px 0 10px">מדריכים נוספים</h2><ul class="gul">{more}</ul>
</div></article>
{ctaband("רוצים שמדביר מוסמך יבדוק? חייגו.")}'''
    art = {"@context":"https://schema.org","@type":"Article","headline":g["h1"],"description":g["desc"],"datePublished":g["date"],"dateModified":g["date"],
           "inLanguage":"he","mainEntityOfPage":abs_url(gp),"image":DOMAIN+"/assets/photo-sprayer.webp",
           "author":{"@type":"Person","name":"זוהר אהרוני","jobTitle":"מדביר מוסמך","url":abs_url("אודות")},
           "publisher":{"@type":"Organization","name":"הדברה 360","logo":{"@type":"ImageObject","url":DOMAIN+"/assets/logo-square.png"}}}
    pages[gp] = page(gp, g["title"] + " | הדברה 360", g["desc"], body, [art, faq_schema(g["faq"]), crumbs_schema(trail)])

trail = [("דף הבית",""),("מדריכים","בלוג")]
cards = "".join(f'<a class="gcard" href="{url(gpath(g))}"><strong>{E(g["h1"])}</strong><span>{E(g["desc"])}</span><em>לקריאה ←</em></a>' for g in GUIDES)
body = f'''{sub_hero(trail, "מדריכים וטיפים", "תשובות של מדביר מוסמך לשאלות הכי נפוצות: איך מזהים, מה עושים, כמה זה עולה ואיך מונעים.", show_price=False)}
<section class="sec soft"><div class="wrap"><div class="gcards">{cards}</div></div></section>
{ctaband("לא מצאתם תשובה? שאלו אותנו.")}'''
pages["בלוג"] = page("בלוג", "מדריכים וטיפים להדברה | הדברה 360", "מדריכים של מדביר מוסמך: פשפש מיטה, מחירי הדברה, קן צרעות, ג׳וקים בחורף ועוד.", body, [crumbs_schema(trail)])

# Prices
PRICE_FAQ = [
 ("למה המחיר הוא טווח ולא מחיר קבוע?","כי כל בית שונה: מספר החדרים, חצר, בורות ביוב והיקף הנגיעות משנים את כמות העבודה והחומר. בטלפון נשאל כמה שאלות קצרות וניתן מחיר מדויק."),
 ("המחיר כולל מע״מ?","כן, כל המחירים באתר כוללים מע״מ."),
 ("הייעוץ בטלפון עולה כסף?","לא. ייעוץ והצעת מחיר בטלפון בחינם."),
 ("האם יש אחריות על הטיפול?","כן. על כל הדברה ניתנת אחריות בכתב, לפי סוג המזיק ושיטת הטיפול."),
]
trail = [("דף הבית",""),("מחירון","מחירון")]
tables = ""
for t, rows in PRICE_TABLES:
    trs = "".join(f"<tr><td><strong>{E(a)}</strong></td><td>{E(b)}</td><td>{E(c)}</td><td>{E(d)}</td></tr>" for a,b,c,d in rows)
    tables += f'<h2 style="font-size:28px;margin-top:40px">{E(t)}</h2><div class="tablebox"><table class="prices"><thead><tr><th scope="col">סוג מזיק</th><th scope="col">אופן ביצוע</th><th scope="col">מחיר</th><th scope="col">הערות</th></tr></thead><tbody>{trs}</tbody></table></div>'
body = f'''{sub_hero(trail, "מחירון הדברה", "מחירים שקופים, בלי הפתעות. המחיר הסופי נקבע לפי גודל הנכס והיקף הנגיעות.")}
<section class="sec"><div class="wrap narrow">
<div class="prose"><h2 style="font-size:28px">ממה מורכב המחיר?</h2><p>הדברה מתחילה מ־{PRICE_FROM} ₪ לדירה. המחיר הסופי נקבע לפי סוג המזיק, מספר החדרים, אם יש חצר, כמה בורות ביוב צריך לטפל, והיקף הנגיעות. בדירה רגילה המחיר נע בדרך כלל בין 250 ל־450 ₪, בדירת קרקע או בית עם חצר החל מ־350 ₪, ובווילה החל מ־650 ₪. התקשרו, ספרו מה קורה, ונמסור לכם מחיר מדויק בטלפון, בלי התחייבות.</p></div>
{tables}
<p style="margin-top:24px;color:var(--muted)">כל המחירים כוללים מע״מ. הצעת מחיר מדויקת ניתנת בטלפון, בחינם.</p>
<div class="prose" style="margin-top:30px"><h2 style="font-size:26px">שאלות על המחיר</h2></div>{faq_html(PRICE_FAQ)}</div></section>
{ctaband("רוצים הצעת מחיר מדויקת? חייגו.")}'''
pages["מחירון"] = page("מחירון", "מחירון הדברה 2026: תיקנים, נמלים, מכרסמים ועוד | הדברה 360", f"מחירון הדברה מעודכן: הדברה לדירה החל מ־{PRICE_FROM} ₪, לבית עם חצר החל מ־350 ₪. תיקנים, נמלים, פרעושים, מכרסמים, כיני יונים, צרעות ועוד. הצעת מחיר בחינם.", body, [crumbs_schema(trail), faq_schema(PRICE_FAQ)])

# Warranty
trail = [("דף הבית",""),("אחריות","אחריות")]
body = f'''{sub_hero(trail, "אחריות על ההדברה", "על כל הדברה ניתנת אחריות בכתב.", show_price=False)}
<section class="sec"><div class="wrap narrow prose">
<p>אנחנו עומדים מאחורי העבודה שלנו. על כל הדברה ניתנת אחריות בכתב, ומשך האחריות נקבע לפי סוג המזיק ושיטת הטיפול.</p>
<p>[פירוט תקופות האחריות לפי סוג מזיק]</p>
<p>אם במהלך תקופת האחריות המזיקים חוזרים, פשוט התקשרו אלינו ונחזור לטפל.</p>
</div></section>
{ctaband("שאלה על האחריות? דברו איתנו.")}'''
pages["אחריות"] = page("אחריות", "אחריות על הדברה | הדברה 360", "על כל הדברה של הדברה 360 ניתנת אחריות בכתב לפי סוג המזיק.", body, [crumbs_schema(trail)])

# Accessibility
trail = [("דף הבית",""),("הצהרת נגישות","הצהרת-נגישות")]
body = f'''<section class="sec"><div class="wrap narrow prose">{crumbs_html(trail, dark=True)}
<h1 style="font-size:40px;color:var(--navy)">הצהרת נגישות</h1>
<p>אנחנו רואים חשיבות רבה במתן שירות שוויוני לכלל הלקוחות, ופועלים כדי שהאתר יהיה נגיש לאנשים עם מוגבלות, בהתאם לתקן הישראלי 5568 ולהנחיות WCAG 2.1 ברמה AA.</p>
<h3>מה עשינו באתר</h3>
<ul class="list"><li>האתר מותאם לגלישה במחשב ובטלפון נייד.</li><li>אפשר לנווט באתר באמצעות המקלדת, וקיים קישור "דילוג לתוכן".</li><li>ניגודיות צבעים מספקת וטקסט בגודל קריא.</li><li>לתמונות יש טקסט חלופי, ולטפסים יש תוויות.</li><li>מבנה כותרות היררכי שמתאים לקוראי מסך.</li></ul>
<h3>נתקלתם בבעיה?</h3>
<p>אם נתקלתם בקושי בגלישה באתר, נשמח לשמוע ולתקן. רכז הנגישות: זוהר אהרוני, טלפון: <a href="tel:{TEL}" class="ltr">{PHONE}</a>, דוא״ל: <a href="mailto:hadbara360@gmail.com" class="ltr">hadbara360@gmail.com</a>.</p>
<p>תאריך עדכון ההצהרה: 29.10.2026.</p>
</div></section>'''
pages["הצהרת-נגישות"] = page("הצהרת-נגישות", "הצהרת נגישות | הדברה 360", "הצהרת הנגישות של אתר הדברה 360.", body)

# Thank you
body = f'''<section class="sec"><div class="wrap narrow" style="text-align:center;display:flex;flex-direction:column;gap:18px;align-items:center">
<h1 style="font-size:44px">תודה! קיבלנו את הפרטים</h1><p class="intro">נחזור אליכם בהקדם. רוצים לדבר עכשיו?</p>{phone_btn()}<a href="/">חזרה לדף הבית</a></div></section>'''
pages["thank-you"] = page("thank-you", "תודה | הדברה 360", "תודה על פנייתכם.", body, noindex=True)

# Old WordPress URLs -> home (works on any static host)
for old in ["דוגמא-1", "category/uncategorized"]:
    pages[old] = f'<!doctype html><html lang="he"><head><meta charset="utf-8"><title>הדברה 360</title><link rel="canonical" href="{DOMAIN}/"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0; url=/"></head><body><a href="/">לדף הבית</a></body></html>'

# ---------------- WRITE ----------------
import re
BASE = os.environ.get("BASE", "").rstrip("/")
def fix(h):
    if BASE:
        h = re.sub(r'(href|src)="/(?!/)', lambda m: f'{m.group(1)}="{BASE}/', h)
        h = h.replace("url('/assets", f"url('{BASE}/assets").replace("url=/", f"url={BASE}/")
        if 'name="robots"' not in h:
            h = h.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n<meta name="robots" content="noindex">', 1)
    return h

if os.path.exists(OUT): shutil.rmtree(OUT)
os.makedirs(OUT)
shutil.copytree(SRC_ASSETS, os.path.join(OUT, "assets"))
open(os.path.join(OUT, ".nojekyll"), "w").write("")
# static pages kept as-is (e.g. /d/ short links for customer documents)
_STATIC=os.path.join(os.path.dirname(os.path.abspath(__file__)),"static")
if os.path.isdir(_STATIC) and not BASE:
    for _root,_dirs,_files in os.walk(_STATIC):
        for _f in _files:
            _src=os.path.join(_root,_f); _rel=os.path.relpath(_src,_STATIC); _dst=os.path.join(OUT,_rel)
            os.makedirs(os.path.dirname(_dst),exist_ok=True); shutil.copy2(_src,_dst)
for path, htmltext in pages.items():
    d = os.path.join(OUT, path) if path else OUT
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f: f.write(fix(htmltext))

nf = page("404", "העמוד לא נמצא | הדברה 360", "העמוד לא נמצא.", f'<section class="sec"><div class="wrap narrow" style="text-align:center;display:flex;flex-direction:column;gap:18px;align-items:center"><h1 style="font-size:44px">העמוד לא נמצא</h1><p class="intro">אבל המזיקים כן? אנחנו כאן.</p>{phone_btn()}<a href="/">לדף הבית</a></div></section>', noindex=True)
open(os.path.join(OUT, "404.html"), "w", encoding="utf-8").write(fix(nf))

redirects = """/דוגמא-1/  /  301
/category/*  /  301
/author/*  /  301
/feed/*  /  301
/wp-admin/*  /  301
/home  /  301
"""
open(os.path.join(OUT, "_redirects"), "w", encoding="utf-8").write(redirects)

sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"<url><loc>{abs_url(p)}</loc></url>\n" for p in pages if p not in ("thank-you","דוגמא-1","category/uncategorized")) + "</urlset>\n"
open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8").write(sm)
open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nDisallow: /thank-you/\nDisallow: /_src/\nSitemap: {DOMAIN}/sitemap.xml\n")
print("pages:", len(pages))
