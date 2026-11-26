#!/usr/bin/env python3
"""Generira statičke stranice za studio23k.eu (v2, razigrani stil). Pokretanje: python3 izvor/build.py ."""
import json, os, re, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
ADRESA = "Jakova Gotovca 18"
MAIL = "hello@studio23k.eu"
TEL = "+385 92 405 0600"
KAL = "https://calendar.app.google/jx4eBT3Tn9bsoiSt9"
TMB = "https://tmbingo.com"
UPIT = f"mailto:{MAIL}?subject=Upit%20za%20projekt"

NAV = [("/#usluge", "Usluge"), ("/radovi/", "Radovi"), ("/#studio", "Studio"), ("/tmbingo/", "TMBingo")]

SCHEMA_ORG = {
    "@context": "https://schema.org", "@type": "ProfessionalService", "@id": "https://studio23k.eu/#studio",
    "name": "Studio23k", "slogan": "Kreiramo doživljaj",
    "description": "Kreativni i digitalni studio iz Zadra za veće projekte: web platforme i trgovine po mjeri, web aplikacije, brend identitet, foto i video te kampanje. Paket za male firme je TMBingo by Studio23k.",
    "url": "https://studio23k.eu/", "logo": "https://studio23k.eu/assets/apple-touch-icon.png", "image": "https://studio23k.eu/assets/og-image.jpg",
    "email": MAIL, "telephone": TEL, "taxID": "13393375189",
    "address": {"@type": "PostalAddress", "streetAddress": ADRESA, "postalCode": "23000", "addressLocality": "Zadar", "addressRegion": "Zadarska županija", "addressCountry": "HR"},
    "areaServed": [{"@type": "City", "name": "Zadar"}, {"@type": "Country", "name": "Hrvatska"}],
    "founder": {"@type": "Person", "name": "Tonći Morić", "jobTitle": "Dizajner i programer"},
    "subOrganization": {"@type": "ProfessionalService", "@id": "https://tmbingo.com/#posao", "name": "TMBingo", "url": "https://tmbingo.com/"},
    "knowsAbout": ["izrada web stranica", "web trgovine", "web aplikacije", "brend identitet", "grafički dizajn", "fotografija proizvoda", "video produkcija", "SEO", "održavanje web stranica"],
}


def head(title, desc, path, extra=None):
    url = "https://studio23k.eu" + path
    sc = [SCHEMA_ORG] + (extra or [])
    return f"""<!doctype html>
<html lang="hr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#f4efe4">
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
<link rel="stylesheet" href="/assets/studio.css?v=2">
<script type="application/ld+json">
{json.dumps(sc if len(sc) > 1 else sc[0], ensure_ascii=False, indent=1)}
</script>
</head>
<body>
<div class="cur" aria-hidden="true"></div>
"""


def nav(cur):
    lis = "".join(f'<li><a href="{h}"{" class=\"tmb\"" if t == "TMBingo" else ""}{" aria-current=\"page\"" if h == cur else ""}>{t}</a></li>' for h, t in NAV)
    links = "".join(f'<a href="{h}"{" class=\"tmb\"" if t == "TMBingo" else ""}>{t}</a>' for h, t in NAV)
    return f"""<header class="nav">
  <a class="logo" href="/" aria-label="Studio23k, naslovna">studio23<b>k</b></a>
  <nav aria-label="Glavna navigacija"><ul>{lis}</ul></nav>
  <a class="pill" href="/#kontakt">Javite se <span class="ar">→</span></a>
  <button class="burger open-menu" type="button" aria-label="Otvori izbornik"><span><i></i><i></i></span></button>
</header>
<div class="menu" id="menu" aria-hidden="true">
  <div class="row"><a class="logo" href="/">studio23<b>k</b></a><button class="close" type="button" id="closeMenu">Zatvori</button></div>
  <nav class="links" aria-label="Izbornik">{links}<a href="/#kontakt">Kontakt</a></nav>
  <div class="row tag"><span>{MAIL}</span><span class="dim">Zadar</span></div>
</div>
"""


def round_sticker(text, big, cls, rot=-12):
    return f'<div class="stk round {cls}" style="rotate:{rot}deg" aria-hidden="true"><svg viewBox="0 0 128 128"><defs><path id="c{cls}" d="M64,64 m-48,0 a48,48 0 1,1 96,0 a48,48 0 1,1 -96,0"/></defs><text><textPath href="#c{cls}">{text}</textPath></text></svg><b>{big}</b></div>'


def marquee(words, cls="", href=None, n=6):
    one = "".join(f"<span>{w}<i>✦</i></span>" for w in words)
    inner = f'<div class="tr">{one * n}</div>'
    if href:
        return f'<a class="mq {cls}" href="{href}" aria-label="{words[0]}" data-cur="Klik">{inner}</a>'
    return f'<div class="mq {cls}" aria-hidden="true">{inner}</div>'


def footer():
    return f"""<section class="cta" id="kontakt">
  {round_sticker("javite se · javite se · javite se · ", "☕", "s9", 10)}
  <h2 class="rv">Imate ideju?<br>Popijmo <span class="o">kavu.</span></h2>
  <div class="row rv">
    <a class="mail" href="{UPIT}" data-cur="Pišite">{MAIL}</a>
    <div style="display:flex;gap:10px;flex-wrap:wrap"><a class="pill o" href="{UPIT}">Pošaljite upit <span class="ar">→</span></a><a class="pill line" href="{KAL}" target="_blank" rel="noopener">Video poziv 30 min</a></div>
  </div>
</section>
<footer class="ft">
  <div><span class="tag">Studio</span><p>Obrt Studio23k<br>vl. Tonći Morić<br>{ADRESA}<br>23000 Zadar</p></div>
  <div><span class="tag">Kontakt</span><p><a href="mailto:{MAIL}">{MAIL}</a><br><a href="tel:+385924050600">{TEL}</a></p></div>
  <div><span class="tag">Stranice</span><ul><li><a href="/#usluge">Usluge</a></li><li><a href="/radovi/">Radovi</a></li><li><a href="/#studio">Studio</a></li><li><a class="g" href="/tmbingo/">TMBingo by Studio23k</a></li></ul></div>
  <div><span class="tag">Mala firma?</span><p>Web, dizajn i mreže od 199 € mjesečno.<br><a class="g" href="{TMB}/" target="_blank" rel="noopener">tmbingo.com ↗</a></p></div>
  <p class="big" aria-hidden="true">studio23<b>k</b></p>
  <div class="bottom"><span>© 2026 Studio23k · OIB 13393375189 · obrt nije u sustavu PDV-a</span><span><a href="{TMB}/privatnost.html">Privatnost</a> · <a href="{TMB}/uvjeti.html">Uvjeti</a> · <a href="{TMB}/cjenik/">Cjenik</a></span></div>
</footer>

<div class="chat" id="chat">
  <div class="win" role="dialog" aria-label="Poruka Studio23k">
    <div class="top"><i></i><b>Studio23k</b><span class="dim">· Zadar</span></div>
    <div class="msgs"><p class="msg">Bok! 👋</p><p class="msg">Imate projekt na umu ili vam treba nešto manje za firmu?</p></div>
    <div class="opts"><a href="{UPIT}">Imam veći projekt</a><a class="g" href="/tmbingo/">Mala sam firma</a><a href="{KAL}" target="_blank" rel="noopener">Dogovorimo poziv</a></div>
  </div>
  <button class="btn" type="button" aria-label="Otvori poruke" aria-expanded="false"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/></svg></button>
</div>

<script src="/assets/js/lenis.min.js"></script>
<script src="/assets/js/studio.js?v=2" defer></script>
</body>
</html>
"""


RADOVI = [
    ("antuntun", "Antuntun", "https://antuntun-zadar.com/", ["Identitet", "Web"]),
    ("frida", "Frida", "https://frida-zadar.hr/", ["Web", "Upravljanje zgradama"]),
    ("focx", "Focx", "https://focx.store/", ["Web trgovina"]),
    ("dalmatica", "Dalmatica Mobility", "https://dalmaticamobility.com/", ["Web", "Selidbe"]),
    ("goveer", "Goveer", "https://goveer.com/", ["Web trgovina"]),
    ("ldesign", "L-Design", "https://l-design.hr/en/", ["Web", "Nautika"]),
    ("protex", "Protex", "https://protexzadar.hr/", ["Web", "Videonadzor"]),
    ("dizajnpro", "DizajnPro", "https://dizajnpro.net/", ["Web trgovina"]),
]
KLIJENTI = ["Frida", "Antuntun", "Riva Rafting Centar", "Zrmanja Adventures", "Mićanovi Dvori", "DizajnPro", "LanaMar", "ZadarSub", "Goveer", "Focx", "Skroće", "Malta", "Lastavica", "Protex", "SolHome", "L-Design", "Dalmatica Mobility", "Calimero Sport", "Rildo", "Marco Polo's", "Manhatta", "Zadar Region Guide", "Mile", "TST Group"]


def work_item(r):
    f, n, u, tags = r
    chips = "".join(f"<span>{t}</span>" for t in tags)
    return f'<li class="rv"><a href="{u}" target="_blank" rel="noopener" data-cur="Pogledaj"><span class="thumb"><img src="/assets/radovi/{f}.jpg" alt="Web stranica {n} na laptopu i mobitelu" width="1200" height="900" loading="lazy"><span class="go">↗</span></span><span class="cap"><h3>{n}</h3><span class="chips">{chips}</span></span></a></li>'


USLUGE = [
    ("Web platforme po mjeri", "Višejezični webovi, rezervacije, prijave i integracije s alatima koje već koristite."),
    ("Web trgovine", "Katalog, košarica, kartice, dostava i veza na skladište ili knjigovodstvo."),
    ("Web aplikacije i sustavi", "CRM, portali za klijente, narudžbe i automatizacija posla koji se danas radi ručno."),
    ("Brend identitet", "Ime, znak, boje i tipografija. Jedan sustav za web, tisak i mreže."),
    ("Foto i video", "Proizvodi, prostori i događaji, snimljeni za web, kampanje i mreže."),
    ("Kampanje i tisak", "Jumbo plakati, katalozi, meniji i oglasi, spremni za tisak i objavu."),
    ("SEO i AI vidljivost", "Da vas nađu Google, karte i AI asistenti kad netko pita za ono što radite."),
    ("Održavanje i podrška", "Hosting, sigurnost i izmjene, s jednom osobom koja zna vaš projekt."),
]

KARTICE = [
    ("20+", "godina", "Dizajna i koda. Prvi web smo radili dok je internet još škripao na modemu."),
    ("100+", "projekata", "Od lokalnih obrta do web trgovina i turističkih brendova."),
    ("1", "osoba", "Od prve kave do lansiranja razgovarate s istim čovjekom. Bez prosljeđivanja."),
    ("0", "predložaka", "Sve crtamo od nule, prvo u Figmi. Kod kreće tek kad kažete da je to to."),
    ("7 Bf", "bura", "Radimo i kad puše. Rok je rok, makar se laptop držao s obje ruke."),
    ("ZST", "Zadarsko standardno vrijeme", "Ponuda stiže brzo, ali tek nakon prve kave. Neke stvari se ne mijenjaju."),
]

FAQ = [
    ("Koja je razlika između Studio23k i TMBingo?", "Studio23k radi veće projekte po mjeri, s ponudom za svaki projekt. <a href=\"/tmbingo/\">TMBingo by Studio23k</a> je paket za male firme, obrte i apartmane: web, dizajn i društvene mreže za jednu mjesečnu cijenu, bez obveze trajanja. Iza oba stoji isti tim."),
    ("Koliko košta projekt?", f"Ovisi o opsegu. Nakon prvog razgovora dobivate pisanu ponudu s cijenom, rokom i popisom onoga što ulazi u cijenu. Za manje stvari cijene su javne na <a href=\"{TMB}/cjenik/\">TMBingo cjeniku</a>."),
    ("Koliko traje izrada?", "Rok pišemo u ponudu prema opsegu. Dizajn prvo vidite u Figmi, a izrada kreće tek kad ga odobrite."),
    ("Radite li s firmama izvan Zadra?", "Da, s klijentima iz cijele Hrvatske i inozemstva. Kava je uživo u Zadru ili na video pozivu."),
    ("Tko radi na projektu?", "Svaki projekt vodi Tonći Morić, dizajner i programer s 20 godina iskustva. Za veće projekte uključujemo suradnike za fotografiju, video i sadržaj."),
]


def faq_html(items):
    return "\n    ".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in items)


def faq_schema(items):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}} for q, a in items]}


def index():
    svc = "\n      ".join(f'<li class="rv"><span class="tag">{i:02d}</span><h3>{n}</h3><p>{d}</p><span class="ic" aria-hidden="true">→</span></li>' for i, (n, d) in enumerate(USLUGE, 1))
    cards = "\n      ".join(f'<article class="card"><div class="n tag"><span>{i:02d} / {len(KARTICE):02d}</span><span>✦</span></div><b>{big}<small>{small}</small></b><p>{p}</p></article>' for i, (big, small, p) in enumerate(KARTICE, 1))
    work = "\n      ".join(work_item(r) for r in RADOVI[:4])
    cloud = "".join(f"<span>{k}</span>" for k in KLIJENTI)
    return head("Studio23k · Digitalni studio iz Zadra: web, brend, aplikacije",
                "Studio23k iz Zadra radi veće projekte: web platforme i trgovine po mjeri, web aplikacije, brend identitet, foto i video. Za male firme tu je TMBingo by Studio23k.",
                "/", [faq_schema(FAQ)]) + nav("/") + f"""
<main>
<section class="hero" id="vrh">
  <figure class="float f1" data-float="-0.12"><img src="/assets/radovi/antuntun.jpg" alt="" width="1200" height="900"></figure>
  <figure class="float f2" data-float="-0.22"><img src="/assets/radovi/focx.jpg" alt="" width="1200" height="900"></figure>
  <figure class="float f3" data-float="-0.06"><img src="/assets/radovi/frida.jpg" alt="" width="1200" height="900"></figure>
  {round_sticker("iz zadra s ljubavlju · iz zadra s ljubavlju · ", "23k", "s1")}
  <div class="stk tape s2" aria-hidden="true">Figma prije koda ✍️</div>
  <h1><span class="l"><span>Kreiramo</span></span><span class="l"><span><em>doživljaj</em><span class="o">.</span></span></span></h1>
  <div class="sub">
    <p>Digitalni studio iz Zadra za projekte kojima ne treba predložak, nego netko tko će ih stvarno razumjeti.</p>
    <div class="acts"><a class="pill o" href="#radovi">Pogledajte radove <span class="ar">↓</span></a><a class="pill line" href="/tmbingo/">Mala firma? TMBingo</a></div>
  </div>
</section>

{marquee(["Web platforme", "Web trgovine", "Aplikacije", "Brend identitet", "Foto i video", "SEO"], "o")}

<section class="stmt" id="studio">
  <span class="tag rv">( Studio )</span>
  <h2 class="rv">Spajamo strategiju, dizajn i kod u <span class="hl">jednom timu</span>. Projekte shvaćamo ozbiljno, a kavu još ozbiljnije.</h2>
  <div class="ps rv">
    <p>Studio23k vodi Tonći Morić, dizajner i programer s dvadeset godina iskustva. Za veće projekte okupljamo suradnike za fotografiju, video i sadržaj, ali vi uvijek razgovarate s istom osobom.</p>
    <p>Svaki dizajn prvo vidite i odobrite u Figmi. Tek onda pišemo kod, testiramo na svim uređajima i pripremamo za Google. I ostajemo uz projekt nakon lansiranja.</p>
  </div>
</section>

<section class="deck">
  <div class="hd"><h2 class="rv">Par stvari<br>o nama</h2><p class="rv">Povucite kartice. Brojke su stvarne, bura isto.</p></div>
  <div class="cards" data-cur="Povuci">
      {cards}
  </div>
</section>

<section class="svc" id="usluge">
  <div class="sec-h"><h2 class="rv">Što<br>radimo<span class="o">.</span></h2><p class="rv">Za tvrtke, turizam, trgovine i brendove kojima treba rješenje po mjeri.</p></div>
  <ol class="svl">
      {svc}
  </ol>
</section>

<div class="reel rv"><figure><video data-lazyplay muted loop playsinline preload="none" poster="/assets/img/team-2.jpg"><source src="/assets/img/studio.mp4" type="video/mp4"></video><figcaption class="tag">Iza kulisa ✦ Zadar</figcaption></figure></div>

<section class="work" id="radovi">
  <div class="sec-h"><h2 class="rv">Izdvojeni<br>radovi<span class="o">.</span></h2><p class="rv">Klik vodi na stvarnu stranicu. Neka sami kažu kako rade.</p></div>
  <ul class="grid2">
      {work}
  </ul>
  <div class="more"><a class="pill" href="/radovi/">Svi radovi <span class="ar">→</span></a></div>
</section>

{marquee(["Radili smo s", "Radili smo s"], "s rev", n=4)}
<section class="cl"><span class="tag" style="padding-top:60px">( Klijenti )</span><div class="cloud rv">{cloud}</div></section>

<section class="ways" id="nacini">
  <div class="way s23 rv">
    <span class="tag">Studio23k</span>
    <h3>Projekt<br>po mjeri</h3>
    <ul><li>Web platforme, trgovine i aplikacije</li><li>Brend identitet od nule</li><li>Foto, video i kampanje</li><li>Integracije i automatizacija</li></ul>
    <div><p class="pr">Ponuda<small>po projektu, nakon prve kave</small></p><div class="acts"><a class="pill o" href="{UPIT}">Pošaljite upit <span class="ar">→</span></a></div></div>
  </div>
  <div class="way tmb rv">
    {round_sticker("za male firme · za male firme · ", "TMB", "s5", 12)}
    <span class="tag">TMBingo by Studio23k</span>
    <h3>Paket za<br>male firme</h3>
    <ul><li>Web stranica od 299 € (landing page)</li><li>Logo, dizajn i tiskovine</li><li>Vođenje društvenih mreža</li><li>Bez obveze trajanja</li></ul>
    <div><p class="pr">od 199 €<small>mjesečno · bazna cijena 199 € (31. 10. 2026.)</small></p><div class="acts"><a class="pill" href="/tmbingo/">Više o paketu <span class="ar">→</span></a><a class="pill line" href="{TMB}/" target="_blank" rel="noopener">tmbingo.com ↗</a></div></div>
  </div>
</section>

<section class="faq" id="pitanja">
  <h2 class="rv">Pitanja<br>koja često<br>čujemo</h2>
  <div class="rv">
    {faq_html(FAQ)}
  </div>
</section>
</main>

{marquee(["Javite se", "Popijmo kavu"], "", href="#kontakt")}
""" + footer()


def radovi():
    work = "\n      ".join(work_item(r) for r in RADOVI)
    cloud = "".join(f"<span>{k}</span>" for k in KLIJENTI)
    return head("Radovi · Studio23k, Zadar",
                "Odabrani radovi Studio23k: web stranice, web trgovine i vizualni identiteti za tvrtke i turizam u Zadru i Hrvatskoj.",
                "/radovi/") + nav("/radovi/") + f"""
<main>
<section class="phead">
  {round_sticker("klik vodi na stvarni web · ", "↗", "s6", 8)}
  <h1>Radovi<span class="o">.</span></h1>
  <p>Web stranice, trgovine i identiteti za tvrtke, turizam i lokalne brendove.</p>
</section>
<section class="work" style="padding-top:20px">
  <ul class="grid2">
      {work}
  </ul>
</section>
{marquee(["Radili smo s", "Radili smo s"], "s rev", n=4)}
<section class="cl"><span class="tag" style="padding-top:60px">( Klijenti i projekti )</span><div class="cloud rv">{cloud}</div></section>
</main>
""" + footer()


PLANS = [
    ("start", "Start", "199 €", "mjesečno · bazna cijena 199 € (31. 10. 2026.)", ["8 objava mjesečno", "Održavanje postojećeg weba", "Jedan zadatak u isto vrijeme"], False),
    ("tmbingo", "TMBingo paket", "399 €", "mjesečno · bazna cijena 399 € (29. 10. 2026.)", ["Web, hosting i održavanje", "Logo, branding, tiskovine", "Društvene mreže"], True),
    ("pro", "Pro", "749 €", "mjesečno · bazna cijena 749 € (31. 10. 2026.)", ["Sve iz TMBingo paketa", "Dva zadatka u isto vrijeme", "Prednost i mjesečni plan"], False),
    ("web", "Web za 14 dana", "1.490 €", "jednokratno · bazna cijena 1.490 € (31. 10. 2026.)", ["Nova web stranica", "Dizajn prvo u Figmi", "Plaća se jednom"], False),
]
TMB_FAQ = [
    ("Zašto TMBingo ima svoju stranicu?", "Zato što je to drukčiji način rada: gotovi paketi s javnim cijenama, narudžba online i pretplata bez obveze trajanja. Iza njega stoji isti tim i isti obrt Studio23k."),
    ("Gdje se paket naručuje?", f"Na <a href=\"{TMB}/paket/\">tmbingo.com/paket</a>. Tamo su svi detalji, kalkulator i cjenik s baznim cijenama."),
    ("Mogu li krenuti s paketom pa prijeći na veći projekt?", "Naravno. Kad firma naraste i treba joj trgovina, aplikacija ili novi brend, projekt preuzima Studio23k, s istim ljudima koji već znaju vaš posao."),
]


def tmbingo():
    plans = "\n  ".join(
        f'<a class="plan{" feat" if feat else ""} rv" href="{TMB}/paket/?p={k}" target="_blank" rel="noopener" data-cur="Odaberi"><span class="tag">{n}{" ✦ najčešći" if feat else ""}</span><b class="amt">{a}</b><small>{s}</small><ul>{"".join(f"<li>{x}</li>" for x in lis)}</ul><span class="go">Odaberi na tmbingo.com ↗</span></a>'
        for k, n, a, s, lis, feat in PLANS)
    return head("TMBingo by Studio23k · Paket za male firme",
                "TMBingo by Studio23k: web, dizajn i društvene mreže za male firme, obrte i apartmane od 199 € mjesečno, bez obveze trajanja. Web stranica od 299 €.",
                "/tmbingo/", [faq_schema(TMB_FAQ)]) + nav("/tmbingo/") + f"""
<main>
<section class="phead">
  {round_sticker("bez obveze trajanja · bez obveze · ", "199", "s7", -8)}
  <h1>TMBingo<br><span class="g">by Studio23k</span></h1>
  <p>Kreativni tim u jednom paketu za male firme, obrte, kafiće i apartmane. Iste ruke kao za velike projekte, samo u paketu i za mjesečnu cijenu.</p>
</section>
<section class="plans">
  {plans}
  <p class="note">Web na jednoj stranici (landing page) je od 299 €, bazna cijena od 299 € (25. 11. 2026.). Sve cijene i bazne cijene su u <a href="{TMB}/cjenik/">cjeniku na tmbingo.com</a>. Obrt nije u sustavu PDV-a.</p>
</section>
{marquee(["Mala firma", "Veliki dojam"], "o")}
<section class="vs" style="padding-top:110px">
  <div class="a rv"><h3>TMBingo</h3><dl><div><dt>Za koga</dt><dd>Male firme, obrti, kafići, apartmani</dd></div><div><dt>Cijena</dt><dd>Javna, od 199 € mjesečno ili od 299 € jednokratno</dd></div><div><dt>Narudžba</dt><dd>Online na tmbingo.com</dd></div><div><dt>Obveza</dt><dd>Bez obveze trajanja</dd></div></dl><p style="margin-top:24px"><a class="pill" href="{TMB}/paket/" target="_blank" rel="noopener">Odaberi paket ↗</a></p></div>
  <div class="b rv"><h3>Studio23k</h3><dl><div><dt>Za koga</dt><dd>Tvrtke, turizam, trgovine, brendovi</dd></div><div><dt>Cijena</dt><dd>Ponuda po projektu</dd></div><div><dt>Narudžba</dt><dd>Razgovor, pa pisana ponuda</dd></div><div><dt>Obveza</dt><dd>Ugovor za projekt, održavanje po dogovoru</dd></div></dl><p style="margin-top:24px"><a class="pill o" href="{UPIT}">Upit za projekt →</a></p></div>
</section>
<section class="faq">
  <h2 class="rv">Pitanja</h2>
  <div class="rv">
    {faq_html(TMB_FAQ)}
  </div>
</section>
</main>
""" + footer()


def nf():
    return head("Stranica nije pronađena · Studio23k", "Ova stranica ne postoji.", "/404.html") + nav("") + f"""
<main><section class="phead"><h1>Ups<span class="o">.</span></h1><p>Ova stranica je otišla na kavu i nije se vratila. <a class="pill" href="/" style="margin-top:20px">Natrag na naslovnu →</a></p></section></main>
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
