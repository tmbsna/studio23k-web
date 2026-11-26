#!/usr/bin/env python3
"""Generira statičke stranice za studio23k.eu (zajednički header i footer)."""
import json, os, sys

OUT = sys.argv[1]
ADRESA = "Jakova Gotovca 18"
MAIL = "hello@studio23k.eu"
TEL = "+385 92 405 0600"
KAL = "https://calendar.app.google/jx4eBT3Tn9bsoiSt9"
TMB = "https://tmbingo.com"

NAV = [("/#usluge", "Usluge"), ("/#proces", "Proces"), ("/radovi/", "Radovi"), ("/tmbingo/", "TMBingo"), ("/#kontakt", "Kontakt")]

SCHEMA_ORG = {
    "@context": "https://schema.org",
    "@type": "ProfessionalService",
    "@id": "https://studio23k.eu/#studio",
    "name": "Studio23k",
    "slogan": "Kreiramo doživljaj",
    "description": "Kreativni i digitalni studio iz Zadra za veće projekte: web platforme i trgovine po mjeri, web aplikacije, brend identitet, foto i video te kampanje. Paket za male firme je TMBingo by Studio23k.",
    "url": "https://studio23k.eu/",
    "logo": "https://studio23k.eu/assets/apple-touch-icon.png",
    "image": "https://studio23k.eu/assets/og-image.jpg",
    "email": MAIL,
    "telephone": TEL,
    "taxID": "13393375189",
    "address": {"@type": "PostalAddress", "streetAddress": ADRESA, "postalCode": "23000", "addressLocality": "Zadar", "addressRegion": "Zadarska županija", "addressCountry": "HR"},
    "areaServed": [{"@type": "City", "name": "Zadar"}, {"@type": "Country", "name": "Hrvatska"}],
    "founder": {"@type": "Person", "name": "Tonći Morić", "jobTitle": "Dizajner i programer"},
    "subOrganization": {"@type": "ProfessionalService", "@id": "https://tmbingo.com/#posao", "name": "TMBingo", "url": "https://tmbingo.com/"},
    "knowsAbout": ["izrada web stranica", "web trgovine", "web aplikacije", "brend identitet", "grafički dizajn", "fotografija proizvoda", "video produkcija", "SEO", "održavanje web stranica"],
}


def head(title, desc, path, extra_schema=None):
    url = "https://studio23k.eu" + path
    schemas = [SCHEMA_ORG] + (extra_schema or [])
    return f"""<!doctype html>
<html lang="hr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#050505">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:locale" content="hr_HR">
<meta property="og:site_name" content="Studio23k">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://studio23k.eu/assets/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" href="/assets/favicon.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="stylesheet" href="/assets/fonts/fonts.css">
<link rel="stylesheet" href="/assets/studio.css">
<script type="application/ld+json">
{json.dumps(schemas if len(schemas) > 1 else schemas[0], ensure_ascii=False, indent=1)}
</script>
</head>
<body>
"""


def menu():
    links = "".join(f'<a href="{h}"{" class=\"tmb\"" if t == "TMBingo" else ""}>{t}</a>' for h, t in NAV)
    return f"""<div class="chip" id="chip"><a href="/#kontakt">Kontakt</a><button type="button" class="open-menu" aria-label="Otvori izbornik"><span><i></i><i></i></span></button></div>

<div class="menu" id="menu" aria-hidden="true">
  <div class="grid"><span class="lbl c1">Studio23k</span><span class="lbl c3">Izbornik</span><button class="lbl close c11" type="button" id="closeMenu">Zatvori</button></div>
  <nav class="grid" aria-label="Izbornik"><div class="links full">{links}</div></nav>
  <div class="grid"><span class="lbl c1">{MAIL}</span><span class="lbl c3 dim">Paket za male firme: TMBingo by Studio23k</span></div>
</div>
"""


def topbar(cur, ink=False):
    lis = "".join(f'<li><a href="{h}"{" aria-current=\"page\"" if h == cur else ""}>{t}</a></li>' for h, t in NAV)
    return f"""  <div class="top grid{' ink' if ink else ''}">
    <a class="lbl c1 brand" href="/"><b>studio23k</b></a>
    <span class="lbl c3">Kreativni i digitalni studio · Zadar</span>
    <nav class="lbl c7" aria-label="Glavna navigacija"><ul>{lis}</ul></nav>
    <button class="burger c11 open-menu" type="button" aria-label="Otvori izbornik"><i></i><i></i></button>
  </div>
"""


def footer():
    return f"""<footer class="foot-wrap" id="kontakt">
  <div class="ft grid">
    <p class="lbl c1">Studio23k</p>
    <p class="lbl c3">Obrt Studio23k<br>vl. Tonći Morić<br>OIB 13393375189<br>{ADRESA}, 23000 Zadar<br>© 2026 Studio23k</p>
    <div class="c7w">
      <p class="lbl dim">Novi projekt</p>
      <a class="mail" href="mailto:{MAIL}?subject=Upit%20za%20projekt">{MAIL}</a>
      <div class="acts">
        <a class="btn" href="mailto:{MAIL}?subject=Upit%20za%20projekt">Pošaljite upit</a>
        <a class="btn ghost" href="{KAL}" target="_blank" rel="noopener">Video poziv 30 min</a>
      </div>
    </div>
    <dl class="lbl c3">
      <div><dt>Telefon</dt><dd><a href="tel:+385924050600">{TEL}</a></dd></div>
      <div><dt>Ponuda</dt><dd>Pisana, nakon prvog razgovora</dd></div>
    </dl>
    <dl class="lbl c7">
      <div><dt>Za male firme</dt><dd><a class="g" href="/tmbingo/">TMBingo by Studio23k</a> · <a class="g" href="{TMB}/" target="_blank" rel="noopener">tmbingo.com ↗</a></dd></div>
      <div><dt>Vodi</dt><dd>Tonći Morić · 20 godina dizajna i programiranja</dd></div>
    </dl>
    <p class="giant" aria-hidden="true"><span>studio23<span class="a">k</span></span></p>
    <div class="bottom lbl"><span>Kreiramo doživljaj.</span><span class="dim">Obrt nije u sustavu PDV-a</span><span class="links"><a href="/radovi/">Radovi</a><a href="/tmbingo/">TMBingo</a><a href="{TMB}/cjenik/">Cjenik</a><a href="{TMB}/privatnost.html">Privatnost</a><a href="{TMB}/uvjeti.html">Uvjeti</a></span></div>
  </div>
</footer>

<script src="/assets/js/lenis.min.js"></script>
<script src="/assets/js/studio.js" defer></script>
</body>
</html>
"""


RADOVI = [
    ("antuntun", "Antuntun", "https://antuntun-zadar.com/", "Identitet · Web"),
    ("frida", "Frida", "https://frida-zadar.hr/", "Web · upravljanje zgradama"),
    ("focx", "Focx", "https://focx.store/", "Web trgovina"),
    ("dalmatica", "Dalmatica Mobility", "https://dalmaticamobility.com/", "Web · selidbe"),
    ("goveer", "Goveer", "https://goveer.com/", "Web trgovina"),
    ("ldesign", "L-Design", "https://l-design.hr/en/", "Web · tapeciranje i nautika"),
    ("protex", "Protex", "https://protexzadar.hr/", "Web · videonadzor"),
    ("dizajnpro", "DizajnPro", "https://dizajnpro.net/", "Web trgovina"),
]
KLIJENTI = "Frida, Antuntun, Riva Rafting Centar, Zrmanja Adventures, Mićanovi Dvori, DizajnPro, LanaMar, ZadarSub, Goveer, Focx, Skroće, Malta, Lastavica, Protex, SolHome, L-Design, Dalmatica Mobility, Calimero Sport, Rildo, Marco Polo's, Manhatta."


def case(r):
    f, n, u, t = r
    return f'<li><a href="{u}" target="_blank" rel="noopener"><span class="case-img"><img src="/assets/radovi/{f}.jpg" alt="Web stranica {n} na laptopu i mobitelu" width="1200" height="900" loading="lazy"></span><span class="case-t">{n}</span><span class="lbl">{t}</span></a></li>'


USLUGE = [
    ("Web platforme po mjeri", "Višejezični webovi, rezervacije, prijave i integracije s alatima koje već koristite. Sadržaj uređujete sami.", "Web"),
    ("Web trgovine", "Katalog, košarica, kartično plaćanje, dostava i veza na skladište ili knjigovodstvo.", "E-commerce"),
    ("Web aplikacije i sustavi", "CRM, portali za klijente, narudžbe i automatizacija posla koji se danas radi ručno.", "Sustavi"),
    ("Brend identitet", "Ime, znak, boje, tipografija i pravila korištenja. Jedan sustav za web, tisak i mreže.", "Branding"),
    ("Foto i video", "Proizvodi, prostori i događaji, snimljeni za web, kampanje i društvene mreže.", "Produkcija"),
    ("Kampanje i tisak", "Jumbo plakati, katalozi, meniji i oglasi, pripremljeni za tisak i objavu.", "Kampanje"),
    ("SEO i AI vidljivost", "Tehnički i lokalni SEO, strukturirani podaci i sadržaj koji Google i AI asistenti razumiju.", "Vidljivost"),
    ("Održavanje i podrška", "Hosting, sigurnost, sigurnosne kopije i izmjene, s jednom osobom koja zna vaš projekt.", "Podrška"),
]

FAQ = [
    ("Koja je razlika između Studio23k i TMBingo?", f"Studio23k radi veće projekte po mjeri, s ponudom za svaki projekt. <a href=\"/tmbingo/\">TMBingo by Studio23k</a> je paket za male firme, obrte i apartmane: web, dizajn i društvene mreže za jednu mjesečnu cijenu, bez obveze trajanja. Iza oba stoji isti tim i isti obrt."),
    ("Koliko košta projekt?", f"Ovisi o opsegu. Nakon prvog razgovora dobivate pisanu ponudu s cijenom, rokom i popisom onoga što ulazi u cijenu. Ako vam treba manji web ili samo logo, cijene su javne na <a href=\"{TMB}/cjenik/\">TMBingo cjeniku</a>."),
    ("Koliko traje izrada?", "Rok pišemo u ponudu prema opsegu projekta. Dizajn prvo dobivate na pregled u Figmi, pa tek kad ga odobrite kreće izrada."),
    ("Radite li s firmama izvan Zadra?", "Da. Radimo s klijentima iz cijele Hrvatske i inozemstva. Sastanci su uživo u Zadru ili na video pozivu."),
    ("Tko radi na projektu?", "Svaki projekt vodi Tonći Morić, dizajner i programer s 20 godina iskustva. Za veće projekte uključujemo suradnike za fotografiju, video i sadržaj."),
]


def faq_html(items):
    out = []
    for i, (q, a) in enumerate(items, 1):
        out.append(f'<details><summary><span class="lbl">{i:02d}</span>{q}</summary><p>{a}</p></details>')
    return "\n      ".join(out)


def faq_schema(items):
    import re
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}} for q, a in items]}


def index():
    rows = "\n      ".join(f'<li><span class="n">{i:02d}</span><h3>{n}</h3><p>{d}</p><span class="lbl t">{t}</span></li>' for i, (n, d, t) in enumerate(USLUGE, 1))
    cases = "\n      ".join(case(r) for r in RADOVI[:4])
    return head("Studio23k · Web, brend i digitalni projekti po mjeri, Zadar",
                "Studio23k iz Zadra radi veće projekte: web platforme i trgovine po mjeri, web aplikacije, brend identitet, foto i video. Za male firme tu je paket TMBingo by Studio23k.",
                "/", [faq_schema(FAQ)]) + menu() + f"""
<header class="hero" id="vrh">
  <div class="bg" id="heroBg" aria-hidden="true">
    <img class="on" src="/assets/img/hero-3.jpg" alt="">
    <img src="/assets/img/hero-1.jpg" alt="">
    <img src="/assets/img/hero-4.jpg" alt="">
    <img src="/assets/img/hero-2.jpg" alt="">
  </div>
{topbar('/')}  <div class="grid stage">
    <h1>Kreiramo doživljaj<span class="a">.</span></h1>
    <p class="side lbl">Web platforme, trgovine, aplikacije i brendovi po mjeri. Za tvrtke, turizam i brendove kojima treba više od predloška.</p>
    <div class="foot"><span class="lbl">Studio iz Zadra · 20 godina iskustva</span><a class="lbl" href="#nacini">Mala firma? TMBingo paket →</a></div>
  </div>
</header>

<main>
  <section class="intro grid" id="studio">
    <p class="lbl c1">Studio</p>
    <p class="lbl c3">Tonći Morić<br>dizajn i programiranje</p>
    <h2 class="large">Studio23k spaja strategiju, dizajn i programiranje u jednom timu. Od prvog razgovora do lansiranja imate <span class="a">jednu osobu</span> koja zna cijeli projekt, a svaki dizajn prvo vidite i odobrite u Figmi.</h2>
    <div class="stats">
      <div><b>20+</b><span class="lbl dim">godina iskustva</span></div>
      <div><b>100+</b><span class="lbl dim">završenih projekata</span></div>
      <div><b>2</b><span class="lbl dim">načina suradnje: projekt ili paket</span></div>
      <div><b>1</b><span class="lbl dim">kontakt od prvog dana</span></div>
    </div>
  </section>

  <div class="bleed" aria-hidden="true"><span class="lbl">Studio</span><video data-parallax data-lazyplay muted loop playsinline preload="none" poster="/assets/img/team-2.jpg"><source src="/assets/img/studio.mp4" type="video/mp4"></video></div>

  <section class="svc grid" id="usluge">
    <div class="head"><p class="lbl">Usluge</p><p class="lbl">Za projekte kojima treba rješenje po mjeri.</p></div>
    <ol class="rows">
      {rows}
    </ol>
  </section>

  <div class="dark" id="proces">
    <section class="proc grid">
      <div class="head"><p class="lbl">Proces</p><p class="lbl dim">Četiri koraka, bez iznenađenja na kraju.</p></div>
      <ol class="steps">
        <li><span class="lbl dim">01</span><b>Upoznavanje</b><p>Razgovaramo o ciljevima, publici i opsegu. Dobivate pisanu ponudu s cijenom i rokom.</p></li>
        <li><span class="lbl dim">02</span><b>Strategija i dizajn</b><p>Struktura, tekstovi i dizajn u Figmi. Ništa se ne programira dok ne odobrite.</p></li>
        <li><span class="lbl dim">03</span><b>Izrada</b><p>Programiranje, sadržaj, testiranje na svim uređajima i priprema za Google.</p></li>
        <li><span class="lbl dim">04</span><b>Lansiranje i podrška</b><p>Objava, mjerenje i održavanje. Ostajemo uz projekt i nakon lansiranja.</p></li>
      </ol>
    </section>
  </div>

  <section class="ways grid" id="nacini">
    <div class="head"><p class="lbl">Dva načina suradnje</p><p class="lbl">Isti tim. Veliki projekt po mjeri ili mjesečni paket za male firme.</p></div>
    <div class="pair">
      <div class="way s23">
        <span class="lbl">Studio23k</span>
        <h3>Projekt po mjeri<small>Tvrtke, turizam, trgovine, brendovi</small></h3>
        <ul>
          <li>Web platforme, trgovine i aplikacije po mjeri</li>
          <li>Brend identitet od nule</li>
          <li>Foto, video i kampanje</li>
          <li>Integracije, sustavi i automatizacija</li>
          <li>Jedan voditelj projekta od početka do kraja</li>
        </ul>
        <div>
          <p class="amt">Ponuda<small>po projektu, nakon prvog razgovora</small></p>
          <p class="cta" style="margin-top:18px"><a class="btn light" href="mailto:{MAIL}?subject=Upit%20za%20projekt">Pošaljite upit</a><a class="btn ghost light" href="{KAL}" target="_blank" rel="noopener">Video poziv 30 min</a></p>
        </div>
      </div>
      <div class="way tmb">
        <span class="lbl tag-g">TMBingo by Studio23k</span>
        <h3>Paket za male firme<small>Obrti, kafići, apartmani, lokalne firme</small></h3>
        <ul>
          <li>Web stranica od 299 € (landing page)</li>
          <li>Logo, dizajn i tiskovine</li>
          <li>Vođenje društvenih mreža</li>
          <li>Jedna mjesečna cijena, bez obveze trajanja</li>
        </ul>
        <div>
          <p class="amt">od 199 €<small>mjesečno · bazna cijena 199 € (31. 10. 2026.)</small></p>
          <p class="cta" style="margin-top:18px"><a class="btn tmb" href="/tmbingo/">Više o paketu</a><a class="btn ghost" href="{TMB}/" target="_blank" rel="noopener">tmbingo.com ↗</a></p>
        </div>
      </div>
    </div>
  </section>

  <section class="work grid" id="radovi">
    <div class="head"><p class="lbl">Radovi</p><p class="lbl">Izdvojeni projekti</p></div>
    <ul class="cases">
      {cases}
    </ul>
    <p class="lbl more"><a class="u" href="/radovi/">Svi radovi i klijenti →</a></p>
  </section>

  <section class="faq grid" id="pitanja">
    <p class="lbl">Česta pitanja</p>
    <div class="qs">
      {faq_html(FAQ)}
    </div>
  </section>
</main>

""" + footer()


def radovi():
    cases = "\n      ".join(case(r) for r in RADOVI)
    return head("Radovi · Studio23k, Zadar",
                "Odabrani radovi Studio23k: web stranice, web trgovine i vizualni identiteti za tvrtke i turizam u Zadru i Hrvatskoj.",
                "/radovi/") + menu() + topbar('/radovi/', ink=True) + f"""
<main>
  <section class="phead grid">
    <h1>Radovi<span class="a">.</span></h1>
    <p class="lead">Web stranice, trgovine i identiteti koje smo napravili za tvrtke, turizam i lokalne brendove. Klik vodi na stvarnu stranicu.</p>
  </section>
  <section class="work grid">
    <ul class="cases">
      {cases}
    </ul>
    <div class="clients">
      <p class="lbl dim">Klijenti</p>
      <p>{KLIJENTI}</p>
    </div>
    <ul class="projects">
      <li><a href="https://antuntun-zadar.com/" target="_blank" rel="noopener">Antuntun</a><span>Identitet · Web</span></li>
      <li><a href="https://zdguide.com" target="_blank" rel="noopener">Zadar Region Guide</a><span>Identitet · Web</span></li>
      <li>Mile<span>Identitet</span></li>
      <li>TST Group<span>Identitet</span></li>
    </ul>
    <p class="lbl more"><a class="btn" href="mailto:{MAIL}?subject=Upit%20za%20projekt">Pošaljite upit za projekt</a></p>
  </section>
</main>

""" + footer()


PLANS = [
    ("start", "Start", "199 €", "mjesečno", "Bazna cijena 199 € (31. 10. 2026.)", "Društvene mreže i održavanje weba", ["8 objava mjesečno", "Održavanje postojećeg weba", "Jedan zadatak u isto vrijeme"], False),
    ("tmbingo", "TMBingo paket", "399 €", "mjesečno", "Bazna cijena 399 € (29. 10. 2026.)", "Web, dizajn i društvene mreže", ["Web, hosting i održavanje", "Logo, branding, tiskovine", "Zadaci redom, jedan po jedan"], True),
    ("pro", "Pro", "749 €", "mjesečno", "Bazna cijena 749 € (31. 10. 2026.)", "Kad treba više i brže", ["Sve iz TMBingo paketa", "Dva zadatka u isto vrijeme", "Prednost i mjesečni plan"], False),
    ("web", "Web za 14 dana", "1.490 €", "jednokratno", "Bazna cijena 1.490 € (31. 10. 2026.)", "Nova web stranica, bez pretplate", ["Gotovo za 14 dana", "Dizajn prvo u Figmi", "Plaća se jednom"], False),
]

TMB_FAQ = [
    ("Zašto TMBingo ima svoju stranicu?", "Zato što je to drukčiji način rada: gotovi paketi s javnim cijenama, narudžba online i pretplata bez obveze trajanja. Studio23k je za projekte po mjeri. Iza oba stoji isti tim i isti obrt Studio23k."),
    ("Gdje se paket naručuje?", f"Na <a href=\"{TMB}/paket/\">tmbingo.com/paket</a>. Tamo su i svi detalji, kalkulator i cjenik s baznim cijenama."),
    ("Mogu li krenuti s paketom pa prijeći na veći projekt?", "Možete. Kad firma naraste i treba joj trgovina, aplikacija ili novi brend, projekt preuzima Studio23k, s istim ljudima koji već znaju vaš posao."),
]


def tmbingo():
    cards = []
    for key, name, amt, per, bz, sub, lis, feat in PLANS:
        li = "".join(f"<li>{x}</li>" for x in lis)
        em = " <em>Najčešći izbor</em>" if feat else ""
        href = f"{TMB}/paket/?p={key}"
        cards.append(f'<a class="card{" featured" if feat else ""}" href="{href}" target="_blank" rel="noopener"><span class="lbl">{name}{em}</span><b class="amt">{amt}</b><small class="lbl dim">{per}</small><small class="lbl dim">{bz}</small><span>{sub}</span><ul>{li}</ul><span class="lbl go">Odaberi na tmbingo.com ↗</span></a>')
    cards = "\n        ".join(cards)
    return head("TMBingo by Studio23k · Paket za male firme",
                "TMBingo by Studio23k: web, dizajn i društvene mreže za male firme, obrte i apartmane od 199 € mjesečno, bez obveze trajanja. Web stranica od 299 €.",
                "/tmbingo/", [faq_schema(TMB_FAQ)]) + menu() + topbar('/tmbingo/', ink=True) + f"""
<main>
  <section class="phead grid">
    <h1>TMBingo <span class="g">by Studio23k</span></h1>
    <p class="lead">Kreativni tim u jednom paketu za male firme, obrte, kafiće i apartmane. Web, dizajn i društvene mreže za jednu mjesečnu cijenu, bez obveze trajanja. Iste ruke kao i za velike projekte, samo u paketu.</p>
  </section>

  <div class="dark">
    <section class="tmb-plans grid">
      <div class="head" style="margin-bottom:24px;padding-top:16px"><p class="lbl">Paketi</p><p class="lbl dim">Pauza ili otkaz bilo kada. Narudžba na tmbingo.com.</p></div>
      <div class="cards">
        {cards}
      </div>
      <p class="note">Web stranica na jednoj stranici (landing page) je od 299 €, bazna cijena od 299 € (25. 11. 2026.). Sve cijene i bazne cijene su u <a href="{TMB}/cjenik/">cjeniku na tmbingo.com</a>. Obrt nije u sustavu PDV-a.</p>
    </section>
  </div>

  <section class="compare grid">
    <div class="head"><p class="lbl">Što odabrati</p><p class="lbl">Kratka usporedba</p></div>
    <table class="cmp">
      <thead><tr><th></th><th class="g">TMBingo by Studio23k</th><th class="a">Studio23k projekt</th></tr></thead>
      <tbody>
        <tr><th>Za koga</th><td data-k="TMBingo">Male firme, obrti, kafići, apartmani</td><td data-k="Studio23k">Tvrtke, turizam, trgovine, brendovi</td></tr>
        <tr><th>Cijena</th><td data-k="TMBingo">Javna, od 199 € mjesečno ili od 299 € jednokratno</td><td data-k="Studio23k">Ponuda po projektu</td></tr>
        <tr><th>Opseg</th><td data-k="TMBingo">Gotovi paketi i usluge s cjenika</td><td data-k="Studio23k">Po mjeri: platforme, trgovine, aplikacije, identitet</td></tr>
        <tr><th>Narudžba</th><td data-k="TMBingo">Online na tmbingo.com</td><td data-k="Studio23k">Razgovor, pa pisana ponuda</td></tr>
        <tr><th>Obveza</th><td data-k="TMBingo">Bez obveze trajanja</td><td data-k="Studio23k">Ugovor za projekt, održavanje po dogovoru</td></tr>
      </tbody>
    </table>
    <p class="lbl more" style="display:flex;gap:8px;flex-wrap:wrap"><a class="btn tmb" href="{TMB}/paket/" target="_blank" rel="noopener">Odaberi paket na tmbingo.com ↗</a><a class="btn ghost" href="mailto:{MAIL}?subject=Upit%20za%20projekt">Upit za veći projekt</a></p>
  </section>

  <section class="faq grid">
    <p class="lbl">Pitanja</p>
    <div class="qs">
      {faq_html(TMB_FAQ)}
    </div>
  </section>
</main>

""" + footer()


def nf():
    return head("Stranica nije pronađena · Studio23k", "Ova stranica ne postoji.", "/404.html") + menu() + topbar('', ink=True) + f"""
<main><section class="phead grid"><h1>Ova stranica ne postoji<span class="a">.</span></h1><p class="lead">Možda je premještena. <a class="u" href="/">Natrag na naslovnu</a> ili <a class="u" href="/radovi/">pogledajte radove</a>.</p></section></main>
""" + footer()


def w(p, s):
    p = os.path.join(OUT, p)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(s)


w("index.html", index())
w("radovi/index.html", radovi())
w("tmbingo/index.html", tmbingo())
w("404.html", nf())
print("ok")
