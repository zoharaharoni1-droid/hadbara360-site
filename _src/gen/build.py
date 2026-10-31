# -*- coding: utf-8 -*-
import os, shutil, json, html, sys, re
from urllib.parse import quote
sys.path.insert(0, os.path.dirname(__file__))
from content import *
from deep_pests1 import DEEP_PESTS_1
from deep_pests2 import DEEP_PESTS_2
from deep_cities import CITIES_NEW, DEEP_CITIES
from deep_combos import COMBO_PESTS, COMBO_CITIES, COMBOS
CITIES = CITIES[:-1] + CITIES_NEW + CITIES[-1:]   # "המרכז" נשאר אחרון
DEEP_PESTS = {**DEEP_PESTS_1, **DEEP_PESTS_2}
WA_PHOTO = "https://api.whatsapp.com/send?phone=972559992266&text=" + "שלום! אני שולח/ת תמונה של מזיק לזיהוי (מאתר הדברה 360)"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_ASSETS = os.path.join(ROOT, "site", "assets")
OUT = os.path.join(ROOT, "dist")
VER = "12"

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

NAV = [("שירותי הדברה","שירותי-הדברה"),("סוגי מזיקים","הדברת-מזיקים"),("מחירון","מחירון"),("ביקורות","המלצות"),("אזורי שירות","אזורי-שירות"),("שאלות נפוצות","שאלות-נפוצות"),("אודות","אודות")]

def nav_links():
    return "".join(f'<a href="{url(p)}">{t}</a>' for t, p in NAV)

LB = {
  "@context":"https://schema.org","@type":"PestControl","name":"הדברה 360","url":DOMAIN+"/",
  "telephone":"+972-55-999-2266","email":"hadbara360@gmail.com","image":DOMAIN+"/assets/logo.png","priceRange":"₪₪",
  "areaServed":[c["name"] for c in CITIES if c["path"]!="הדברה-במרכז"],
  "openingHours":"Mo-Su 00:00-23:59",
  "description":"חברת הדברה מקצועית במרכז. רישיון מדביר ראשי מס׳ "+LICENSE+"."
}

def page(path, title, desc, body, schema=None, noindex=False):
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
<link rel="icon" href="/assets/icon.png"><link rel="apple-touch-icon" href="/assets/icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;700;800&amp;display=swap">
<link rel="stylesheet" href="/assets/style.css?v={VER}">
{sch_html}
</head>
<body>
<a class="skip" href="#main">דילוג לתוכן</a>
<div class="promo"><b>מבצע</b>{E(PROMO)}, אמרו לנו "ראיתי באתר"</div>
<header class="hdr"><div class="wrap">
<a class="logo" href="/"><img src="/assets/logo.png" alt="הדברה 360 – לדף הבית" width="369" height="170"></a>
<nav class="nav nav-d" aria-label="ניווט ראשי">{nav_links()}</nav>
<a class="hphone" href="tel:{TEL}">{I_PHONE}<span><small>חייגו עכשיו, זמינים 24/7</small><strong>{PHONE}</strong></span></a>
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
<div style="max-width:300px;display:flex;flex-direction:column;gap:12px"><span class="lg"><img src="/assets/logo.png" alt="הדברה 360" width="369" height="170"></span><span>חברת הדברה מקצועית. רישיון מדביר ראשי מס׳ {LICENSE}. חומרים מאושרים ע״י המשרד להגנת הסביבה.</span></div>
<div><h3>הדברת מזיקים</h3><ul>{pests}<li><a href="{url("הדברת-מזיקים")}">כל המזיקים</a></li></ul></div>
<div><h3>אזורי שירות</h3><ul>{cities}<li><a href="{url("אזורי-שירות")}">כל האזורים</a></li></ul></div>
<div><h3>החברה</h3><ul><li><a href="{url("אודות")}">אודות</a></li><li><a href="{url("מחירון")}">מחירון הדברה</a></li><li><a href="{url("המלצות")}">ביקורות</a></li><li><a href="{url("שאלות-נפוצות")}">שאלות נפוצות</a></li><li><a href="{url("אחריות")}">אחריות</a></li></ul></div>
<div><h3>צרו קשר</h3><ul><li><a href="tel:{TEL}" class="ltr">{PHONE}</a></li><li><a href="{E(WA)}" target="_blank" rel="noopener">וואטסאפ</a></li><li><a href="mailto:hadbara360@gmail.com">hadbara360@gmail.com</a></li><li>זמינים 24/7</li></ul></div>
</div>
<div class="bottom"><span>© הדברה 360. כל הזכויות שמורות.</span><a href="{url("הצהרת-נגישות")}">הצהרת נגישות</a></div>
</div></footer>'''

def ctaband(h, p="הדברה החל מ־249 ₪ · ייעוץ והצעת מחיר בחינם."):
    return f'<section class="ctaband"><div class="wrap"><div style="flex:999 1 420px"><h2>{h}</h2><p>{p}</p></div>{phone_btn(label="")}</div></section>'

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

def faq_html(items):
    return '<div class="faq">' + "".join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in items) + '</div>'

def faq_schema(items):
    return {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q, a in items]}

def crumbs_schema(trail):
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":abs_url(p)} for i,(n,p) in enumerate(trail)]}

def crumbs_html(trail, dark=False):
    parts = [f'<a href="{url(p)}">{n}</a>' for n, p in trail[:-1]] + [f'<span aria-current="page">{trail[-1][0]}</span>']
    return f'<nav class="crumbs{" dark" if dark else ""}" aria-label="פירורי לחם">' + " › ".join(parts) + '</nav>'

NOBUG = '''<div class="nobug" aria-hidden="true"><svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
<g fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" class="bug">
<path d="M52 34 Q44 20 34 16"/><path d="M68 34 Q76 20 86 16"/>
<path d="M45 52 L30 46 L22 36"/><path d="M44 64 L28 66 L18 60"/><path d="M46 76 L32 86 L28 98"/>
<path d="M75 52 L90 46 L98 36"/><path d="M76 64 L92 66 L102 60"/><path d="M74 76 L88 86 L92 98"/>
</g>
<ellipse class="bug" cx="60" cy="40" rx="9" ry="7" fill="currentColor"/>
<ellipse class="bug" cx="60" cy="68" rx="16" ry="25" fill="currentColor"/>
<path class="bug" d="M60 46 V92" stroke="rgba(1,36,52,.55)" stroke-width="2"/>
<circle cx="60" cy="60" r="52" fill="none" class="ring" stroke-width="9"/>
<path d="M23 23 L97 97" class="ring" stroke-width="9" stroke-linecap="round"/>
</svg></div>'''

def sub_hero(trail, h1, lead, img="photo-sprayer", show_price=True):
    price = f'<div class="price"><span>הדברה החל מ־</span><strong>{PRICE_FROM} ₪</strong>{NOBUG.replace('class="nobug"','class="nobug-mini"')}</div>' if show_price else ''
    return f'''<section class="hero sub" style="background-image:url('/assets/{img}.webp')"><div class="ov">{NOBUG}<div class="wrap">
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
<div><span class="ico">{I_CLOCK}</span><span><strong>שירות 24/7</strong><span>מענה מהיר לחירום</span></span></div>
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
home = f'''<section class="hero" style="background-image:url('/assets/photo-sprayer.webp')"><div class="ov">{NOBUG}<div class="wrap">
<span class="badge">רישיון מדביר ראשי מס׳ {LICENSE} · חומרים מאושרים ע״י המשרד להגנת הסביבה</span>
<h1>אנחנו באים לפתור לכם את הבעיה!</h1>
<p class="lead">הדברה מקצועית לכל סוגי המזיקים, לבתים, לבניינים ולעסקים. מדביר מוסמך מגיע אליכם בזמן, עם אחריות בכתב.</p>
<div class="price"><span>הדברה החל מ־</span><strong>{PRICE_FROM} ₪</strong>{NOBUG.replace('class="nobug"','class="nobug-mini"')}</div>
<div class="ctas">{phone_btn()}{wa_btn()}</div>
<ul class="checks"><li>ייעוץ והצעת מחיר בחינם</li><li>אחריות מלאה בכתב</li><li>הגעה בזמן שנקבע</li></ul>
</div></div></section>
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
<section class="sec soft" id="reviews"><div class="wrap">
<div class="sec-head"><div><span class="eyebrow">ביקורות מ־Google</span><h2>לקוחות ממליצים</h2></div><a href="{url("המלצות")}" style="font-weight:700">לכל {REVIEWS_DATA["count"]} הביקורות ←</a></div>
{rating_bar()}{reviews_html(REVIEWS[:3])}
</div></section>
<section class="sec"><div class="wrap split" style="align-items:flex-start">
<div><h2>איך זה עובד</h2>{STEPS}</div>
<div><h2>אזורי שירות</h2><p class="intro" style="margin:16px 0">מגיעים אליכם בכל אזור המרכז:</p>{city_chips()}</div>
</div></section>
{ctaband("יש מזיק בבית? נפתור את זה היום.")}'''
pages[""] = page("", "הדברה 360 | חברת הדברה מקצועית במרכז, החל מ־249 ₪", "הדברה מקצועית לכל סוגי המזיקים: תיקנים, נמלים, פשפש מיטה, מכרסמים ועוד. מדביר מוסמך, רישיון 2849, אחריות בכתב. חייגו 055-9992266.", home)

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
    body = f'''{sub_hero(trail, p["h1"] + " מקצועית, עם אחריות בכתב", E(p["intro"].split(". ")[0]) + ". מדביר מוסמך מגיע, מאבחן ומטפל עד הסוף.")}
<section class="sec"><div class="wrap narrow">
{toc_html(toc)}
{H2("about", f"מה צריך לדעת על {p['name']}", ";margin-top:34px")}
<div class="prose" style="margin-top:16px"><p>{E(p["intro"])}</p>{about}</div>
<h3 id="signs" style="font-size:24px;margin-top:34px;scroll-margin-top:90px">סימנים לנגיעות</h3>
<div class="signs">{signs}</div>
{f'{H2("why","למה הם מגיעים",";margin-top:40px;font-size:30px")}<div class="prose" style="margin-top:14px">' + "".join(f"<p>{E(x)}</p>" for x in d["why"]) + (f'<p><strong>למה לא לחכות:</strong> {E(d["risks"])}</p>' if d.get("risks") else "") + '</div>' if d.get("why") else ""}
{photo_id_box()}
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

trail = [("דף הבית",""),("שירותי הדברה","שירותי-הדברה")]
body = f'''{sub_hero(trail, "שירותי הדברה", "הדברה לדירות, לבתים פרטיים, לבניינים, לעסקים ולמוסדות, בשיטה שמתאימה לכל מקום.")}
<section class="sec"><div class="wrap"><div class="cards">{"".join(serv_card(s) for s in SERVICES)}</div></div></section>
{ctaband("לא בטוחים איזה שירות מתאים? נייעץ בחינם.")}'''
pages["שירותי-הדברה"] = page("שירותי-הדברה", "שירותי הדברה לבית ולעסק | הדברה 360", "שירותי הדברה: דירות, בתים פרטיים, בניינים, מסעדות, מוסדות חינוך, הדברה ללא ריסוס, הרחקת יונים ולכידת נחשים.", body, [crumbs_schema(trail)])

# Cities
for c in CITIES:
    d = DEEP_CITIES.get(c["path"], {})
    trail = [("דף הבית",""),("אזורי שירות","אזורי-שירות"),(c["name"],c["path"])]
    faqs = [(f"כמה עולה הדברה {c['prep']}?", f"הדברה מתחילה מ־{PRICE_FROM} ₪. המחיר הסופי תלוי בסוג המזיק ובגודל הנכס, ואנחנו נותנים הצעת מחיר בחינם בטלפון."),
            ("אתם עובדים גם עם ועדי בית ועסקים?","כן. אנחנו מבצעים הדברה לשטחים משותפים, אחזקה שוטפת לבניינים ולמסעדות, והדברה למוסדות חינוך."),
            ("כמה זמן צריך לצאת מהבית?","בהדברה בריסוס בדרך כלל צריך לצאת לכשעה. בהדברה בג׳לים אין צורך לצאת. המדביר ייתן הנחיות מדויקות."),
            ("יש אחריות על העבודה?","כן, כל עבודה מקבלת אחריות בכתב.")] + d.get("faq", [])
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
{hoods}
<div class="cards" style="margin-top:28px">{serv_card(SERV_BY["הדברה-בדירות"],"טיפול נקי ושקט, כולל אפשרות להדברה ללא ריסוס.")}{serv_card(SERV_BY["הדברת-בניינים"],"לובי, חדרי אשפה, מקלטים, ביובים ואחזקה שוטפת.")}{serv_card(SERV_BY["אחזקה-שותפת-למסעדות"],"אחזקה שוטפת לעסקי מזון, בשעות שמתאימות לכם.")}</div>
</div></section>
<section class="sec soft"><div class="wrap narrow">{H2("pests", f"המזיקים הנפוצים {c['prep']}")}
{pests_list}
{combo_links}
</div></section>
<section class="sec"><div class="wrap narrow">{H2("types", f"הדברה {c['prep']} לפי סוג הנכס")}
<div class="prose" style="margin-top:16px">
<h3>דירה בבניין</h3><p>בדירה, רוב המזיקים מגיעים מהביוב, מהשטחים המשותפים או מדירות שכנות. אנחנו מטפלים בניקוזים, בפנלים ובנקודות הכניסה, ומתאימים את השיטה לבית: ריסוס, ג׳לים או מלכודות. בבית עם תינוקות או חיות מחמד אפשר לבחור בטיפול ללא ריסוס.</p>
<h3>בית פרטי או דירת גן</h3><p>בבית עם חצר המזיקים מגיעים בעיקר מבחוץ: מהגינה, מבורות הביוב, מהמחסן ומעצים שנוגעים בבית. לכן הטיפול כולל גם את החצר, את הביובים ואת הצמחייה, ולא רק את הבית עצמו.</p>
<h3>בניין משותף וועד בית</h3><p>הדברה של הלובי, חדרי המדרגות, חדר האשפה, המקלט, החניון ובורות הביוב מונעת מהמזיקים לחזור לדירות. אנחנו מציעים לוועדי בית {c['prep']} גם אחזקה שוטפת בתדירות קבועה.</p>
<h3>עסקים, מסעדות ומשרדים</h3><p>בעסקים אנחנו עובדים בשעות שלא מפריעות לפעילות, בחומרים מאושרים, ומספקים יומן ביצוע מסודר אחרי כל טיפול. למסעדות ולעסקי מזון אנחנו מציעים אחזקה שוטפת.</p>
</div></div></section>
<section class="sec soft"><div class="wrap narrow">{H2("all", f"כל סוגי ההדברה {c['prep']}")}
<div class="signs">{"".join(f'<div><a href="{url(q["path"])}" style="font-weight:800">{E(q["h1"].split(":")[0])}</a><br><span style="color:var(--text2)">{E(q["intro"].split(". ")[0].rstrip("."))}.</span></div>' for q in PESTS)}</div></div></section>
<section class="sec"><div class="wrap narrow">{H2("prices", f"מחירי הדברה {c['prep']}")}{mini_prices()}
{photo_id_box()}</div></section>
<section class="sec soft"><div class="wrap narrow split" style="align-items:flex-start">
<div>{H2("how","איך זה עובד",";font-size:30px")}{STEPS}</div>
<div>{f'<h2 style="font-size:30px">טיפים {c["prep"]}</h2>' + ul(d["tips"]) if d.get("tips") else ""}</div>
</div></section>
<section class="sec"><div class="wrap narrow"><h2>לקוחות ממליצים</h2><div style="margin-top:22px">{reviews_html([REVIEWS[2], REVIEWS[3]])}</div></div></section>
<section class="sec soft"><div class="wrap narrow">{H2("faq", f"שאלות נפוצות: הדברה {c['prep']}")}{faq_html(faqs)}</div></section>
<section class="sec"><div class="wrap narrow"><h2 style="font-size:26px;margin-bottom:16px">מגיעים גם לערים הסמוכות</h2>{city_chips([n for n in c["near"] if n in CITY_BY])}</div></section>
{ctaband(f"צריכים מדביר {c['prep']}? דברו איתנו עכשיו.")}'''
    pages[c["path"]] = page(c["path"], f'הדברה {c["prep"]} ✔ מדביר מוסמך מ־{PRICE_FROM} ₪ | הדברה 360', f'הדברה {c["prep"]}: מדביר מוסמך לדירות, בניינים ועסקים. חומרים מאושרים, אחריות בכתב והצעת מחיר בחינם. חייגו {PHONE}.', body, [faq_schema(faqs), crumbs_schema(trail)])

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
    body = f'''{sub_hero(trail, h1 + ": מדביר מוסמך עם אחריות", E(cd["intro"].split(". ")[0].rstrip(".")) + ".", "photo-window")}
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
<div>{FEAT}</div>
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

# Prices
trail = [("דף הבית",""),("מחירון","מחירון")]
tables = ""
for t, rows in PRICE_TABLES:
    trs = "".join(f"<tr><td><strong>{E(a)}</strong></td><td>{E(b)}</td><td>{E(c)}</td><td>{E(d)}</td></tr>" for a,b,c,d in rows)
    tables += f'<h2 style="font-size:28px;margin-top:40px">{E(t)}</h2><div class="tablebox"><table class="prices"><thead><tr><th scope="col">סוג מזיק</th><th scope="col">אופן ביצוע</th><th scope="col">מחיר</th><th scope="col">הערות</th></tr></thead><tbody>{trs}</tbody></table></div>'
body = f'''{sub_hero(trail, "מחירון הדברה", "מחירים שקופים, בלי הפתעות. המחיר הסופי נקבע לפי גודל הנכס והיקף הנגיעות.")}
<section class="sec"><div class="wrap narrow">{tables}
<p style="margin-top:24px;color:var(--muted)">כל המחירים כוללים מע״מ. הצעת מחיר מדויקת ניתנת בטלפון, בחינם.</p></div></section>
{ctaband("רוצים הצעת מחיר מדויקת? חייגו.")}'''
pages["מחירון"] = page("מחירון", "מחירון הדברה 2026: תיקנים, נמלים, מכרסמים ועוד | הדברה 360", "מחירון הדברה מעודכן לדירות ולבתים: תיקנים, נמלים, פרעושים, מכרסמים, כיני יונים, צרעות ועוד. הצעת מחיר בחינם.", body, [crumbs_schema(trail)])

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
for old in ["בלוג", "דוגמא-1", "category/uncategorized"]:
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

redirects = """/בלוג/  /  301
/בלוג  /  301
/דוגמא-1/  /  301
/category/*  /  301
/author/*  /  301
/feed/*  /  301
/wp-admin/*  /  301
/home  /  301
"""
open(os.path.join(OUT, "_redirects"), "w", encoding="utf-8").write(redirects)

sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"<url><loc>{abs_url(p)}</loc></url>\n" for p in pages if p not in ("thank-you","בלוג","דוגמא-1","category/uncategorized")) + "</urlset>\n"
open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8").write(sm)
open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nDisallow: /thank-you/\nDisallow: /_src/\nSitemap: {DOMAIN}/sitemap.xml\n")
print("pages:", len(pages))
