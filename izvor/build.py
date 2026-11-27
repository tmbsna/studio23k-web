#!/usr/bin/env python3
"""Generira statičke stranice za studio23k.eu (v2, razigrani stil). Pokretanje: python3 izvor/build.py ."""
import json, os, re, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
ADRESA = "Jakova Gotovca 18"
MAIL = "tonci@studio23k.eu"
W3F_KEY = "4082dd29-6008-4e96-a629-a279cee98721"  # Web3Forms (javni ključ, šalje upite na tonci@studio23k.eu)
TEL = "+385 92 405 0600"
TMB = "https://tmbingo.com"
UPIT = f"mailto:{MAIL}?subject=Upit%20za%20projekt"

# Vesele tekstualne face (emotikoni) kroz cijelu stranicu
EMO = {"web-platforme": ":)", "web-trgovine": ":D", "web-aplikacije": "B)", "brend-identitet": "<3", "foto-video": ":O", "kampanje-tisak": "xD", "seo-ai-vidljivost": ";)", "odrzavanje": "^^"}
EMO_KARTICE = [":)", "xD", "^^", ";)", ":O", "B)"]
EMO_KORACI = [":)", ";)", ":P", ":D"]


def emo(t, cls=""):
    t = t.replace("<", "&lt;")
    return f'<span class="emo{(" " + cls) if cls else ""}" aria-hidden="true">{t}</span>'


NAV = [("/usluge/", "Usluge"), ("/radovi/", "Radovi"), ("/#studio", "Studio"), ("/tmbingo/", "TMBingo")]

SCHEMA_ORG = {
    "@context": "https://schema.org", "@type": "ProfessionalService", "@id": "https://studio23k.eu/#studio",
    "name": "Studio23k", "slogan": "Mi prodajemo ideje. Usluge su samo alat.",
    "description": "Kreativni i digitalni studio iz Zadra za veće projekte: web platforme i trgovine po mjeri, web aplikacije, brend identitet, foto i video te kampanje. Paket za male firme je TMBingo by Studio23k.",
    "url": "https://studio23k.eu/", "logo": "https://studio23k.eu/assets/apple-touch-icon.png", "image": "https://studio23k.eu/assets/og-image.jpg",
    "email": MAIL, "telephone": TEL, "taxID": "13393375189",
    "address": {"@type": "PostalAddress", "streetAddress": ADRESA, "postalCode": "23000", "addressLocality": "Zadar", "addressRegion": "Zadarska županija", "addressCountry": "HR"},
    "areaServed": [{"@type": "City", "name": "Zadar"}, {"@type": "Country", "name": "Hrvatska"}],
    "founder": {"@type": "Person", "name": "Tonći Morić", "jobTitle": "Dizajner i programer"},
    "subOrganization": {"@type": "ProfessionalService", "@id": "https://tmbingo.com/#posao", "name": "TMBingo", "url": "https://tmbingo.com/"},
    "knowsAbout": ["izrada web stranica", "web trgovine", "web aplikacije", "brend identitet", "grafički dizajn", "fotografija proizvoda", "video produkcija", "SEO", "održavanje web stranica"],
}


def head(title, desc, path, extra=None, noindex=False):
    url = "https://studio23k.eu" + path
    sc = [SCHEMA_ORG] + (extra or [])
    return f"""<!doctype html>
<html lang="hr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">{'\n<meta name="robots" content="noindex">' if noindex else ""}
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
<link rel="stylesheet" href="/assets/studio.css?v=10">
<script>(function(){{var d=document.documentElement;try{{var s=localStorage.getItem('s23k-tema');if(s)d.dataset.theme=s;if(sessionStorage.getItem('s23k-pre'))d.classList.add('no-pre');sessionStorage.setItem('s23k-pre','1')}}catch(e){{}}}})();</script>
<script type="application/ld+json">
{json.dumps(sc if len(sc) > 1 else sc[0], ensure_ascii=False, indent=1)}
</script>
</head>
<body>
<div class="pre" id="pre" aria-hidden="true"><i></i><b><span class="lg"></span></b><i></i></div>
<div class="cur" aria-hidden="true"></div>
"""


def nav(cur):
    lis = "".join(f'<li><a href="{h}"{" class=\"tmb\"" if t == "TMBingo" else ""}{" aria-current=\"page\"" if h == cur else ""}>{t}</a></li>' for h, t in NAV)
    links = "".join(f'<a href="{h}"{" class=\"tmb\"" if t == "TMBingo" else ""}>{t}</a>' for h, t in NAV)
    return f"""<header class="nav">
  <a class="logo" href="/" aria-label="Studio23k, naslovna"><span class="lg"></span></a>
  <nav aria-label="Glavna navigacija"><ul>{lis}</ul></nav>
  <div class="end">
    <button class="theme" type="button" id="theme" aria-label="Svijetla ili tamna tema" title="Svijetla / tamna tema"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 3a9 9 0 0 0 0 18z" fill="currentColor"/></svg></button>
    <a class="pill" href="/upit/">Opišite projekt <span class="ar">→</span></a>
    <button class="burger open-menu" type="button" aria-label="Otvori izbornik"><span><i></i><i></i></span></button>
  </div>
</header>
<div class="menu" id="menu" aria-hidden="true">
  <div class="row"><a class="logo" href="/" aria-label="Studio23k, naslovna"><span class="lg"></span></a><button class="close" type="button" id="closeMenu">Zatvori</button></div>
  <nav class="links" aria-label="Izbornik">{links}<a href="/upit/">Upit</a></nav>
  <div class="row tag"><span>{MAIL}</span><span class="dim">Zadar</span></div>
</div>
"""


def round_sticker(text, big, cls, rot=-12):
    return f'<div class="stk round {cls}" style="rotate:{rot}deg" aria-hidden="true"><svg viewBox="0 0 128 128"><defs><path id="c{cls}" d="M64,64 m-48,0 a48,48 0 1,1 96,0 a48,48 0 1,1 -96,0"/></defs><text><textPath href="#c{cls}" textLength="301" lengthAdjust="spacing">{text}</textPath></text></svg><b>{big}</b></div>'


def marquee(words, cls="", href=None, n=6):
    one = "".join(f"<span>{w}<i>✦</i></span>" for w in words)
    inner = f'<div class="tr">{one * n}</div>'
    if href:
        return f'<a class="mq {cls}" href="{href}" aria-label="{words[0]}" data-cur="Klik">{inner}</a>'
    return f'<div class="mq {cls}" aria-hidden="true">{inner}</div>'


def footer(cta=True):
    return (f"""<section class="cta" id="kontakt">
  {round_sticker("bez sastanaka · bez sastanaka · ", "✍", "s9", 10)}
  <h2 class="rv">Imate ideju?<br>Napišite <span class="o">je ;)</span></h2>
  <p class="lead rv">Bez kave, poziva i sastanaka. Opišite projekt svojim riječima, a pisanu ponudu dobivate na mail.</p>
  <div class="row rv">
    <a class="mail" href="{UPIT}" data-cur="Pišite">{MAIL}</a>
    <div style="display:flex;gap:10px;flex-wrap:wrap"><a class="pill o" href="/upit/">Opišite projekt <span class="ar">→</span></a></div>
  </div>
</section>
""" if cta else "") + f"""<footer class="ft">
  <div><span class="tag">Studio</span><p>Obrt Studio23k<br>vl. Tonći Morić<br>{ADRESA}<br>23000 Zadar</p></div>
  <div><span class="tag">Kontakt</span><p><a href="mailto:{MAIL}">{MAIL}</a><br><a href="/upit/">Obrazac za upit</a></p></div>
  <div><span class="tag">Stranice</span><ul><li><a href="/usluge/">Usluge</a></li><li><a href="/radovi/">Radovi</a></li><li><a href="/#studio">Studio</a></li><li><a class="g" href="/tmbingo/">TMBingo by Studio23k</a></li></ul></div>
  <div><span class="tag">Mala firma?</span><p>Web, dizajn i mreže od 199 € mjesečno.<br><a class="g" href="{TMB}/" target="_blank" rel="noopener">tmbingo.com ↗</a></p></div>
  <p class="big" aria-hidden="true"><span class="lg"></span></p>
  <div class="bottom"><span>© 2026 Studio23k · OIB 13393375189 · obrt nije u sustavu PDV-a</span><span>Dosadno, ali važno :| <a href="{TMB}/privatnost.html">Privatnost</a> · <a href="{TMB}/uvjeti.html">Uvjeti</a> · <a href="{TMB}/cjenik/">Cjenik</a></span></div>
</footer>

<div class="chat" id="chat">
  <div class="win" role="dialog" aria-label="Poruka Studio23k">
    <div class="top"><i></i><b>Studio23k</b><span class="dim">· Zadar</span></div>
    <div class="msgs"><p class="msg">Bok! :)</p><p class="msg">Imate projekt na umu ili vam treba nešto manje za firmu? Napišite, odgovaramo pisano.</p></div>
    <div class="opts"><a href="/upit/">Opisat ću projekt</a><a class="g" href="/tmbingo/">Mala sam firma</a><a href="{UPIT}">Pišem mail</a></div>
  </div>
  <button class="btn" type="button" aria-label="Otvori poruke" aria-expanded="false"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/></svg></button>
</div>

<script src="/assets/js/lenis.min.js"></script>
<script src="/assets/js/studio.js?v=5" defer></script>
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


KAT = {"Web": "web", "Web trgovina": "trgovina", "Identitet": "identitet"}


def work_item(r):
    f, n, u, tags = r
    chips = "".join(f"<span>{t}</span>" for t in tags)
    cats = " ".join(sorted({KAT[t] for t in tags if t in KAT}))
    return f'<li class="rv" data-cat="{cats}"><a href="{u}" target="_blank" rel="noopener" data-cur="Pogledaj"><span class="thumb"><img src="/assets/radovi/{f}.jpg" alt="Web stranica {n} na laptopu i mobitelu" width="1200" height="900" loading="lazy"><span class="go">↗</span></span><span class="cap"><h3>{n}</h3><span class="chips">{chips}</span></span></a></li>'


USLUGE = [
    ("web-platforme", "Web platforme po mjeri", "Višejezični webovi, rezervacije, prijave i integracije s alatima koje već koristite."),
    ("web-trgovine", "Web trgovine", "Katalog, košarica, kartice, dostava i veza na skladište ili knjigovodstvo."),
    ("web-aplikacije", "Web aplikacije i sustavi", "CRM, portali za klijente, narudžbe i automatizacija posla koji se danas radi ručno."),
    ("brend-identitet", "Brend identitet", "Ime, znak, boje i tipografija. Jedan sustav za web, tisak i mreže."),
    ("foto-video", "Foto i video", "Proizvodi, prostori i događaji, snimljeni za web, kampanje i mreže."),
    ("kampanje-tisak", "Kampanje i tisak", "Jumbo plakati, katalozi, meniji i oglasi, spremni za tisak i objavu."),
    ("seo-ai-vidljivost", "SEO i AI vidljivost", "Da vas nađu Google, karte i AI asistenti kad netko pita za ono što radite."),
    ("odrzavanje", "Održavanje i podrška", "Hosting, sigurnost i izmjene, s jednom osobom koja zna vaš projekt."),
]

KARTICE = [
    ("20+", "godina", "Dizajna i koda. Prvi web smo radili dok je internet još škripao na modemu."),
    ("100+", "projekata", "Od lokalnih obrta do web trgovina i turističkih brendova."),
    ("1", "osoba", "Od prvog upita do lansiranja dopisujete se s istim čovjekom. Bez prosljeđivanja."),
    ("0", "predložaka", "Sve crtamo od nule, prvo u Figmi. Kod kreće tek kad kažete da je to to."),
    ("7 Bf", "bura", "Radimo i kad puše. Rok je rok, makar se laptop držao s obje ruke."),
    ("0", "sastanaka", "Upit, ponuda, dizajn i izmjene idu pisano. Vi radite svoj posao, mi svoj, a sve ostaje zapisano."),
]

FAQ = [
    ("Koja je razlika između Studio23k i TMBingo?", "Studio23k radi veće projekte po mjeri, s ponudom za svaki projekt. <a href=\"/tmbingo/\">TMBingo by Studio23k</a> je paket za male firme, obrte i apartmane: web, dizajn i društvene mreže za jednu mjesečnu cijenu, bez obveze trajanja. Iza oba stoji isti tim."),
    ("Koliko košta projekt?", f"Ovisi o opsegu. Kad opišete projekt u <a href=\"/upit/\">obrascu</a> ili mailu, dobivate pisanu ponudu s cijenom, rokom i popisom onoga što ulazi u cijenu. Za manje stvari cijene su javne na <a href=\"{TMB}/cjenik/\">TMBingo cjeniku</a>."),
    ("Koliko traje izrada?", "Rok pišemo u ponudu prema opsegu. Dizajn prvo vidite u Figmi, a izrada kreće tek kad ga odobrite."),
    ("Radite li s firmama izvan Zadra?", "Da, s klijentima iz cijele Hrvatske i inozemstva. Sve ide online i pisano, pa udaljenost nije važna."),
    ("Moramo li se naći ili imati sastanak?", "Ne. Upit, ponuda, dizajn i povratne informacije idu pisano: obrazac, mail i komentari izravno u Figmi. Tako nitko ne gubi vrijeme na usklađivanje termina, a svaka odluka ostaje zapisana."),
    ("Tko radi na projektu?", "Svaki projekt vodi Tonći Morić, dizajner i programer s 20 godina iskustva. Za veće projekte uključujemo suradnike za fotografiju, video i sadržaj."),
]


def faq_html(items):
    return "\n    ".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in items)


def faq_schema(items):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}} for q, a in items]}


def index():
    svc = "\n      ".join(f'<li class="rv"><span class="tag">{i:02d}</span><h3><a href="/usluge/{slug}/" data-cur="Više">{n}</a></h3><p>{d}</p><span class="ic" aria-hidden="true">{EMO[slug].replace("<", "&lt;")}</span></li>' for i, (slug, n, d) in enumerate(USLUGE, 1))
    cards = "\n      ".join(f'<article class="card"><div class="n tag"><span>{i:02d} / {len(KARTICE):02d}</span>{emo(EMO_KARTICE[i - 1])}</div><b>{big}<small>{small}</small></b><p>{p}</p></article>' for i, (big, small, p) in enumerate(KARTICE, 1))
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
  <div class="stk tape s2" aria-hidden="true">Figma prije koda :P</div>
  <p class="kick rv">Digitalni koncept partner za <i>vizionare</i> :)</p>
  <h1><span class="l"><span>Mi prodajemo <em>ideje</em><span class="o">.</span></span></span><span class="l"><span class="b2">Usluge su samo alat.</span></span></h1>
  <div class="sub">
    <p>Dajemo vam strategiju, doživljaj i hrabrost za rast. Web, brend, aplikacije, foto i video su samo alati kojima vašu ideju pretvaramo u nešto stvarno.</p>
    <div class="acts"><a class="pill o" href="#radovi">Pogledajte radove <span class="ar">↓</span></a><a class="pill line" href="/tmbingo/">Mala firma? TMBingo</a></div>
  </div>
</section>

{marquee(["Web platforme", "Web trgovine", "Aplikacije", "Brend identitet", "Foto i video", "SEO"], "o")}

<section class="stmt" id="studio">
  <span class="tag rv">( Studio )</span>
  <h2 class="rv">Spajamo strategiju, dizajn i kod u <span class="hl">jednom timu</span>. Projekte shvaćamo ozbiljno, a vaše vrijeme još ozbiljnije.</h2>
  <div class="ps rv">
    <p>Studio23k vodi Tonći Morić, dizajner i programer s dvadeset godina iskustva. Za veće projekte okupljamo suradnike za fotografiju, video i sadržaj, ali vi se uvijek dopisujete s istom osobom.</p>
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
  <div class="more"><a class="pill" href="/usluge/">Sve usluge <span class="ar">→</span></a></div>
</section>

{steps_html()}

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

{recenzije_html("", SVE_RECENZIJE)}

<section class="ways" id="nacini">
  <div class="way s23 rv">
    <span class="tag">Studio23k</span>
    <h3>Projekt<br>po mjeri</h3>
    <ul><li>Web platforme, trgovine i aplikacije</li><li>Brend identitet od nule</li><li>Foto, video i kampanje</li><li>Integracije i automatizacija</li></ul>
    <div><p class="pr">Ponuda<small>po projektu, pisano, nakon vašeg opisa</small></p><div class="acts"><a class="pill o" href="/upit/">Opišite projekt <span class="ar">→</span></a></div></div>
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

{marquee(["Opišite projekt", "Bez sastanaka"], "", href="/upit/")}
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
  <div class="filt" role="group" aria-label="Filtriraj radove">
    <button type="button" data-f="" aria-pressed="true">Sve<span>{len(RADOVI)}</span></button>
    <button type="button" data-f="web" aria-pressed="false">Web stranice<span>{sum(1 for r in RADOVI if "Web" in r[3])}</span></button>
    <button type="button" data-f="trgovina" aria-pressed="false">Web trgovine<span>{sum(1 for r in RADOVI if "Web trgovina" in r[3])}</span></button>
    <button type="button" data-f="identitet" aria-pressed="false">Identitet<span>{sum(1 for r in RADOVI if "Identitet" in r[3])}</span></button>
  </div>
  <ul class="grid2" id="radoviGrid">
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
  <div class="b rv"><h3>Studio23k</h3><dl><div><dt>Za koga</dt><dd>Tvrtke, turizam, trgovine, brendovi</dd></div><div><dt>Cijena</dt><dd>Ponuda po projektu</dd></div><div><dt>Narudžba</dt><dd>Pisani upit, pa pisana ponuda</dd></div><div><dt>Obveza</dt><dd>Ugovor za projekt, održavanje po dogovoru</dd></div></dl><p style="margin-top:24px"><a class="pill o" href="/upit/">Opišite projekt →</a></p></div>
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
<main><section class="phead"><h1>Ups <span class="o">:(</span></h1><p>Ova stranica je negdje odlutala. <a class="pill" href="/" style="margin-top:20px">Natrag na naslovnu →</a></p></section></main>
""" + footer(False)


PROCES = [
    ("Opišete projekt", "U obrascu ili mailu napišete što trebate, za koga i do kada. Ako nešto nedostaje, pitamo pisano."),
    ("Dobijete pisanu ponudu", "Cijena, rok i popis onoga što ulazi u cijenu. Crno na bijelo, bez iznenađenja."),
    ("Komentirate u Figmi", "Dizajn i prijedloge gledate kad vama odgovara i ostavljate komentare izravno na njima. Bez usklađivanja termina."),
    ("Izrada i predaja", "Napredak javljamo pisano. Kad sve odobrite, projekt ide van, a mi ostajemo uz njega."),
]


def steps_html(h="Kako radimo.<br>Bez sastanaka."):
    li = "".join(f'<li class="rv"><span class="tag">{i:02d}</span>{emo(EMO_KORACI[i - 1], "big")}<h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(PROCES, 1))
    return f"""<section class="steps" id="proces">
  <div class="sec-h"><h2 class="rv">{h}</h2><p class="rv">Sve ide online i pisano. Manje kave i poziva, više vremena za sam projekt.</p></div>
  <ol>{li}</ol>
</section>"""


# Podstranice usluga: (h1/naslov, meta title, meta opis, uvod, naljepnica, što dobivate, za koga, povezani radovi, FAQ)
USLUGE_DETALJI = {
    "web-platforme": dict(
        title="Izrada web stranica po mjeri, Zadar · Studio23k",
        desc="Višejezične web stranice i platforme po mjeri: rezervacije, prijave i integracije s alatima koje već koristite. Studio23k iz Zadra, dizajn prvo u Figmi.",
        lead="Za firme kojima predložak nije dovoljan: više jezika, rezervacije, prijave i veza s alatima koje već koristite. Dizajn crtamo od nule i prvo ga odobrite u Figmi.",
        stk="po mjeri · po mjeri · ", big="",
        dob=["Dizajn od nule, prvo u Figmi", "Više jezika (HR, EN, DE i drugi)", "Rezervacije, upiti i prijave", "Integracije s CRM-om, kalendarom ili ERP-om", "Brz web, pripremljen za Google i AI asistente", "Testirano na mobitelu, tabletu i računalu"],
        za="Turizam, nekretnine, usluge i firme s više jezika ili s procesom koji gotovi predlošci ne pokrivaju.",
        radovi=["frida", "ldesign", "dalmatica", "protex"],
        faq=[("Koliko traje izrada web platforme?", "Ovisi o opsegu. Rok pišemo u ponudu nakon što opišete projekt, a izrada kreće kad odobrite dizajn."),
             ("Možete li povezati web s alatima koje već koristimo?", "Najčešće da. U upitu navedite koje alate koristite, pa u ponudi pišemo kako i što ulazi u cijenu."),
             ("Treba li mi platforma ili mi je dovoljan manji web?", "Ako vam treba web na jednoj ili nekoliko stranica, pogledajte <a href=\"/tmbingo/\">TMBingo paket</a>: landing page od 299 €, bazna cijena 299 € (25. 11. 2026.).")]),
    "web-trgovine": dict(
        title="Izrada web trgovine po mjeri, Zadar · Studio23k",
        desc="Web trgovine po mjeri: katalog, košarica, plaćanje karticama, dostava i veza sa skladištem ili knjigovodstvom. Studio23k iz Zadra.",
        lead="Trgovina koja prodaje i kad ste offline: pregledan katalog, jednostavna košarica, plaćanje karticama i dostava. Povezujemo je sa skladištem ili knjigovodstvom kad to ima smisla.",
        stk="+1 narudžba · +1 narudžba · ", big="",
        dob=["Katalog s filterima i varijantama", "Košarica i plaćanje karticama", "Dostava, kuponi i obavijesti kupcima", "Veza sa skladištem ili knjigovodstvom", "SEO za kategorije i proizvode", "Fotografije proizvoda, po dogovoru"],
        za="Trgovci koji prodaju online ili tek kreću, od par desetaka do tisuća proizvoda.",
        radovi=["goveer", "focx", "dizajnpro"],
        faq=[("Na kojoj platformi radite trgovine?", "Biramo prema projektu: broju proizvoda, načinu plaćanja i tome kako vodite skladište. Prijedlog i obrazloženje dobivate u ponudi."),
             ("Možete li prebaciti postojeću trgovinu?", "Da. U upitu navedite adresu trgovine i približan broj proizvoda, pa u ponudi pišemo kako ide prijenos."),
             ("Snimate li i proizvode?", "Možemo. <a href=\"/usluge/foto-video/\">Fotografiju i video</a> proizvoda dodajemo u ponudu ako vam treba.")]),
    "web-aplikacije": dict(
        title="Web aplikacije i poslovni sustavi po mjeri · Studio23k Zadar",
        desc="CRM, portali za klijente, sustavi narudžbi i automatizacija ručnog posla. Web aplikacije po mjeri iz Zadra.",
        lead="Kad se posao vodi u deset tablica i stotinu mailova, vrijeme je za sustav. Radimo CRM-ove, portale za klijente i narudžbe, i automatiziramo ono što se danas radi ručno.",
        stk="manje ručnog posla · ", big="",
        dob=["Pisana analiza posla koji želite olakšati", "CRM, portal za klijente ili sustav narudžbi", "Uloge i prava pristupa", "Automatske obavijesti i izvještaji", "Integracije s postojećim alatima", "Održavanje i nadogradnje nakon lansiranja"],
        za="Firme koje rastu brže od svojih tablica i žele manje ručnog prepisivanja.",
        radovi=[],
        faq=[("Što je bolje: gotovi alat ili aplikacija po mjeri?", "Ako gotovi alat radi ono što trebate, preporučit ćemo ga. Aplikacija po mjeri ima smisla kad gotova rješenja traže previše zaobilaženja."),
             ("Kako opisati što trebam?", "Napišite kako posao ide danas, korak po korak, i gdje gubite vrijeme. To je dovoljno za prvi pisani prijedlog."),
             ("Može li se krenuti s manjom verzijom?", "Može, i to preporučujemo. Prvo radi ono najvažnije, a nadograđujemo prema stvarnom korištenju.")]),
    "brend-identitet": dict(
        title="Brend identitet i dizajn loga, Zadar · Studio23k",
        desc="Logo, boje, tipografija i knjiga standarda: brend identitet koji jednako radi na webu, u tisku i na mrežama. Studio23k iz Zadra.",
        lead="Ime, znak, boje i tipografija koji drže zajedno na webu, ambalaži, plakatu i Instagramu. Na kraju dobivate sustav, a ne samo logo.",
        stk="knjiga standarda · ", big="",
        dob=["Logo i njegove varijante", "Paleta boja i tipografija", "Knjiga standarda (PDF)", "Posjetnice, memorandum i predlošci", "Predlošci za društvene mreže", "Sve datoteke za tisak i web"],
        za="Novi brendovi, firme pred redizajnom i svi kojima logo izgleda drukčije na svakom mjestu.",
        radovi=["antuntun"],
        faq=[("Radite li i redizajn postojećeg loga?", "Da. Ponekad je dovoljno osvježiti znak i složiti pravila, a ponekad treba krenuti ispočetka. To pišemo u ponudi."),
             ("Koliko prijedloga dobijem?", "Broj prijedloga i krugova izmjena piše u ponudi, tako da unaprijed znate što ulazi u cijenu."),
             ("Kako komentiram prijedloge?", "Izravno u Figmi ili mailom, kad vam odgovara. Sve ostaje zapisano.")]),
    "foto-video": dict(
        title="Fotografija proizvoda i video produkcija, Zadar · Studio23k",
        desc="Fotografija i video proizvoda, prostora i događaja za web, kampanje i društvene mreže. Studio23k iz Zadra.",
        lead="Proizvodi, prostori i događaji, snimljeni tako da rade na webu, u kampanji i na mrežama. Plan snimanja dogovaramo pisano, da na dan snimanja nema iznenađenja.",
        stk="akcija! · akcija! · ", big="",
        dob=["Pisani plan snimanja (popis kadrova)", "Fotografija proizvoda i prostora", "Kratki video za mreže i web", "Obrada i prilagodba formata", "Datoteke spremne za web i tisak"],
        za="Trgovine, turizam, ugostitelji i brendovi kojima trebaju vlastite fotografije umjesto fotografija s interneta. Za veća snimanja uključujemo suradnike za fotografiju i video.",
        radovi=[],
        faq=[("Gdje snimate?", "Kod vas, na lokaciji ili u prostoru koji dogovorimo. Detalji idu u pisani plan snimanja."),
             ("Koje formate dobijem?", "Formate prilagođene mjestu gdje ćete ih koristiti: web, tisak, Instagram, TikTok ili oglasi."),
             ("Možete li snimiti proizvode za web trgovinu?", "Da, i to je često dio projekta <a href=\"/usluge/web-trgovine/\">web trgovine</a>.")]),
    "kampanje-tisak": dict(
        title="Dizajn kampanja, jumbo plakata i tiskovina · Studio23k Zadar",
        desc="Jumbo plakati, katalozi, meniji, letci i oglasi: dizajn kampanja spreman za tisak i objavu. Studio23k iz Zadra.",
        lead="Jumbo plakati, katalozi, meniji i oglasi koji izgledaju kao dio istog brenda. Pripremamo ih za tiskaru i za objavu, u svim formatima koje trebate.",
        stk="spremno za tisak · ", big="",
        dob=["Ideja i ključni vizual kampanje", "Jumbo plakati i vanjsko oglašavanje", "Katalozi, meniji i letci", "Oglasi za mreže i web", "Priprema za tisak (CMYK, napust za rez)", "Komunikacija s tiskarom, po dogovoru"],
        za="Ugostitelji, trgovine, nekretnine i brendovi pred sezonom, otvorenjem ili novom ponudom.",
        radovi=[],
        faq=[("Je li tisak uključen u cijenu?", "Dizajn i priprema su u ponudi, a tisak se obično plaća posebno. Ako želite, uz ponudu pošaljemo i ponudu tiskare."),
             ("Koliko formata dobijem?", "Sve formate koje navedete u upitu, od jumbo plakata do priče za Instagram. Popis piše u ponudi."),
             ("Možete li raditi prema našem postojećem brendu?", "Naravno. Pošaljite knjigu standarda ili postojeće materijale, pa radimo prema njima.")]),
    "seo-ai-vidljivost": dict(
        title="SEO i AI vidljivost, Zadar · Studio23k",
        desc="SEO, Google Business profil i vidljivost u AI asistentima kao što su ChatGPT, Gemini i Claude. Tehnički SEO, strukturirani podaci i sadržaj. Studio23k iz Zadra.",
        lead="Da vas nađu kad netko traži ono što radite: na Googleu, na kartama i u AI asistentima, koji sve češće odgovaraju umjesto tražilice.",
        stk="google · karte · AI · ", big="",
        dob=["Tehnički pregled i popravci", "Strukturirani podaci (schema.org)", "Google Business profil", "Sadržaj za stranice i usluge", "llms.txt i pristup AI botovima", "Pisani izvještaj o napretku, po dogovoru"],
        za="Firme koje imaju dobar web, ali ih ljudi ne nalaze kad traže ono što rade.",
        radovi=[],
        faq=[("Garantirate li prvo mjesto na Googleu?", "Ne, i to nitko pošten ne može garantirati. Ono za što odgovaramo jest da tehnička strana, sadržaj i podaci budu složeni kako treba."),
             ("Što je AI vidljivost?", "Sve više ljudi traži preporuke od ChatGPT-a, Geminija ili Claudea. AI vidljivost znači da ti alati mogu pročitati točne i jasne podatke o vama."),
             ("Kad se vide rezultati?", "Tehnički popravci djeluju brže, a sadržaj i ugled grade se mjesecima. U ponudi pišemo što radimo i kako pratimo napredak.")]),
    "odrzavanje": dict(
        title="Održavanje web stranica i podrška, Zadar · Studio23k",
        desc="Hosting, sigurnosne kopije, ažuriranja i izmjene sadržaja. Održavanje web stranica, s jednom osobom koja zna vaš projekt i zahtjevima koji idu pisano.",
        lead="Web nije gotov na dan lansiranja. Brinemo za hosting, sigurnost, kopije i izmjene, a zahtjeve šaljete pisano i pratite ih bez telefoniranja.",
        stk="mirni ste · mirni ste · ", big="",
        dob=["Hosting i domena", "Redovite sigurnosne kopije", "Ažuriranja i sigurnost", "Izmjene sadržaja po zahtjevu", "Praćenje rada weba", "Svaki zahtjev pisano i zapisan"],
        za="Firme kojima web mora raditi, a nemaju vremena ni volje baviti se njime.",
        radovi=[],
        faq=[("Održavate li i webove koje niste vi radili?", "Da, nakon pregleda. Pošaljite adresu weba u upitu, pa vam pisano javimo u kakvom je stanju i što predlažemo."),
             ("Kako šaljem izmjene?", "Mailom ili kroz obrazac. Svaki zahtjev ostaje zapisan, s rokom i potvrdom kad je gotov."),
             ("Mala sam firma. Ima li nešto jednostavnije?", "Ima: <a href=\"/tmbingo/\">TMBingo by Studio23k</a> uključuje održavanje u mjesečni paket od 199 €, bazna cijena 199 € (31. 10. 2026.).")]),
}
USLUGE_ALT = {
    "web-platforme": "Ilustracija: web stranice Frida i L-Design na računalu i mobitelu, s oznakama za više jezika i rezervacije",
    "web-trgovine": "Ilustracija: web trgovina Goveer s karticama košarice i plaćanja",
    "web-aplikacije": "Ilustracija: nadzorna ploča CRM aplikacije s brojem upita, zadataka i grafom",
    "brend-identitet": "Ilustracija: znak 23k, paleta boja i tipografija iz knjige standarda",
    "foto-video": "Ilustracija: tražilo kamere iznad majstora u radionici",
    "kampanje-tisak": "Ilustracija: jumbo plakat Kreiramo doživljaj i meni A5",
    "seo-ai-vidljivost": "Ilustracija: tražilica s upitom i Studio23k kao prvim rezultatom",
    "odrzavanje": "Ilustracija: kartica Sve radi, sigurnosna kopija i izmjena cjenika",
}
RAD = {r[0]: r for r in RADOVI}

# Recenzije klijenata po usluzi: samo stvarne, doslovno od klijenta. (citat, ime, firma/uloga, poveznica ili "")
_SNAAP = ("Snažna arhitektura platforme i jasan koncept koji je Studio23k postavio bili su presudni da u prvom krugu osiguramo investicije. Sada smo spremni skalirati i preuzeti tržište. Nisu odradili samo tehnički posao, bili su naši pravi strateški partneri.", "Tonći", "Snaap", "")
_FRIDA = ("Prije suradnje, mislili smo da su društvene mreže samo usputna stavka bez pravog dosega. Studio23k nam je potpuno promijenio perspektivu. Pokazali su nam kako se gradi stvarna digitalna prisutnost i gdje se zapravo kriju naši najvrjedniji klijenti.", "Šime", "Frida", "https://frida-zadar.hr/")
_INES = ("Uvijek smo vjerovali da je kvaliteta naše usluge dovoljna. Studio23k nas je naučio da vrhunski rad zaslužuje jednako snažan vizualni doživljaj. Sada naš koncept i dizajn jasno komuniciraju našu vrijednost i prije nego što klijent uopće uđe kroz vrata.", "Matea", "Frizerski salon Ines", "")
_FOCX = ("Redizajn našeg web shopa nije donio samo novi izgled, donio je opipljive rezultate. Kupci nam se sami javljaju kako bi pohvalili besprijekorno i intuitivno iskustvo kupovine. Studio23k je od našeg weba napravio našeg najboljeg prodavača.", "Serkan", "Focx", "https://focx.store/")
RECENZIJE = {s: [] for s in USLUGE_DETALJI}
RECENZIJE.update({"web-platforme": [_SNAAP], "web-aplikacije": [_SNAAP], "web-trgovine": [_FOCX], "brend-identitet": [_INES], "seo-ai-vidljivost": [_FRIDA], "kampanje-tisak": [_FRIDA]})
# naslovna: sve četiri recenzije
SVE_RECENZIJE = [_SNAAP, _FOCX, _INES, _FRIDA]


def recenzije_html(slug, rs=None):
    rs = rs if rs is not None else (RECENZIJE.get(slug) or [])
    if not rs:
        return ""
    cards = "".join(f'<figure class="rev rv"><span class="q" aria-hidden="true">“</span>{emo(":)")}<blockquote><p>{q}</p></blockquote><figcaption><b>{n}</b>{(" · " + (f'<a href="{u}" target="_blank" rel="noopener">{f}</a>' if u else f)) if f else ""}</figcaption></figure>' for q, n, f, u in rs)
    return f"""<section class="revs">
  <div class="sec-h"><h2 class="rv">Što kažu<br>klijenti<span class="o">.</span></h2></div>
  <div class="rg">{cards}</div>
</section>"""


def crumbs(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i, "name": n, "item": "https://studio23k.eu" + u} for i, (n, u) in enumerate(items, 1)]}


def usluga(i, slug, name, short):
    d = USLUGE_DETALJI[slug]
    path = f"/usluge/{slug}/"
    svc_schema = {"@context": "https://schema.org", "@type": "Service", "name": name, "serviceType": name, "description": d["desc"],
                  "url": "https://studio23k.eu" + path, "image": f"https://studio23k.eu/assets/usluge/{slug}.jpg",
                  "provider": {"@id": "https://studio23k.eu/#studio"}, "areaServed": [{"@type": "City", "name": "Zadar"}, {"@type": "Country", "name": "Hrvatska"}]}
    dob = "".join(f"<li>{emo(EMO[slug])}<span>{x}</span></li>" for x in d["dob"])
    rad = ""
    if d["radovi"]:
        rad = f"""<section class="work" style="padding-top:0">
  <div class="sec-h"><h2 class="rv">Iz naših<br>radova<span class="o">.</span></h2><p class="rv">Klik vodi na stvarnu stranicu.</p></div>
  <ul class="grid2">{"".join(work_item(RAD[k]) for k in d["radovi"])}</ul>
</section>"""
    ostale = "".join(f'<a class="pill line" href="/usluge/{s}/">{n}</a>' for s, n, _ in USLUGE if s != slug)
    return head(d["title"], d["desc"], path, [svc_schema, faq_schema(d["faq"]), crumbs([("Studio23k", "/"), ("Usluge", "/usluge/"), (name, path)])]) + nav("/usluge/") + f"""
<main>
<section class="phead uhead">
  {round_sticker(d["stk"], EMO[slug].replace("<", "&lt;"), "s8", 8)}
  <p class="crumb tag"><a href="/usluge/">Usluge</a> / {i:02d}</p>
  <h1>{name}<span class="o">.</span></h1>
  <p>{d["lead"]}</p>
  <div class="acts"><a class="pill o" href="/upit/?usluga={slug}">Opišite projekt <span class="ar">→</span></a><a class="pill line" href="#proces">Kako radimo</a></div>
</section>
<figure class="uimg rv"><img src="/assets/usluge/{slug}.jpg" alt="{USLUGE_ALT[slug]}" width="1600" height="1000" fetchpriority="high"></figure>
<section class="ugrid">
  <div class="rv"><span class="tag">( Što dobivate )</span><ul class="dob">{dob}</ul></div>
  <aside class="za rv"><span class="tag">Za koga</span><p>{d["za"]}</p><span class="tag" style="margin-top:22px">Cijena</span><p>Pisana ponuda po projektu, nakon što opišete što trebate.</p></aside>
</section>
{recenzije_html(slug)}
{steps_html("Kako ide.<br>Bez sastanaka.")}
{rad}
<section class="faq">
  <h2 class="rv">Pitanja</h2>
  <div class="rv">
    {faq_html(d["faq"])}
  </div>
</section>
<section class="ost"><span class="tag">( Ostale usluge )</span><div>{ostale}</div></section>
</main>
""" + footer()


def usluge_index():
    li = "\n  ".join(f'<li class="rv"><a href="/usluge/{s}/" data-cur="Više"><span class="im"><img src="/assets/usluge/{s}.jpg" alt="" width="1600" height="1000" loading="lazy">{emo(EMO[s], "on")}</span><span class="tag">{i:02d}</span><h2>{n}</h2><p>{dsc}</p></a></li>' for i, (s, n, dsc) in enumerate(USLUGE, 1))
    lst = {"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [
        {"@type": "ListItem", "position": i, "name": n, "url": f"https://studio23k.eu/usluge/{s}/"} for i, (s, n, _) in enumerate(USLUGE, 1)]}
    return head("Usluge · Studio23k, Zadar: web, trgovine, aplikacije, brend",
                "Usluge Studio23k: web platforme i trgovine po mjeri, web aplikacije, brend identitet, foto i video, kampanje i tisak, SEO i AI vidljivost te održavanje.",
                "/usluge/", [lst, crumbs([("Studio23k", "/"), ("Usluge", "/usluge/")])]) + nav("/usluge/") + f"""
<main>
<section class="phead">
  {round_sticker("osam načina · jedan tim · ", "8", "s6", 8)}
  <h1>Usluge<span class="o">.</span></h1>
  <p>Od weba i trgovine do brenda, kampanje i održavanja. Odaberite što vam treba ili opišite projekt, pa složimo kombinaciju.</p>
</section>
<ul class="ulist">
  {li}
</ul>
{steps_html()}
</main>
""" + footer()


BUDZET = ["Do 2.000 €", "2.000 do 5.000 €", "5.000 do 10.000 €", "Više od 10.000 €", "Još ne znam"]
ROK = ["Što prije", "U idućih 1 do 3 mjeseca", "Nije hitno"]


def upit():
    chk = "".join(f'<label class="chip"><input type="checkbox" name="Usluga: {n}" value="da" data-slug="{s}"><span>{n}</span></label>' for s, n, _ in USLUGE)
    bud = "".join(f'<label class="chip"><input type="radio" name="budzet" value="{b}"><span>{b}</span></label>' for b in BUDZET)
    rok = "".join(f'<label class="chip"><input type="radio" name="rok" value="{b}"><span>{b}</span></label>' for b in ROK)
    return head("Opišite projekt · Studio23k, Zadar",
                "Pošaljite pisani upit Studio23k: opišite projekt svojim riječima i dobijte pisanu ponudu s cijenom i rokom. Bez sastanaka i poziva.",
                "/upit/", [crumbs([("Studio23k", "/"), ("Upit", "/upit/")])]) + nav("/upit/") + f"""
<main>
<section class="phead">
  {round_sticker("bez sastanaka · bez sastanaka · ", "✍", "s6", 8)}
  <h1>Opišite<br>projekt<span class="o">.</span></h1>
  <p>Svojim riječima, koliko god kratko ili dugo želite. Odgovaramo pisano, a kad imamo dovoljno podataka, šaljemo pisanu ponudu s cijenom i rokom.</p>
</section>
<section class="upit">
  <form class="fm rv" name="upit" method="POST" action="https://api.web3forms.com/submit">
    <input type="hidden" name="access_key" value="{W3F_KEY}">
    <input type="hidden" name="subject" value="Novi upit sa studio23k.eu">
    <input type="hidden" name="from_name" value="Studio23k web">
    <input type="hidden" name="redirect" value="https://studio23k.eu/upit/hvala/">
    <input type="checkbox" name="botcheck" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
    <div class="two">
      <label class="f"><span>Ime i prezime *</span><input name="ime" required autocomplete="name"></label>
      <label class="f"><span>E-mail *</span><input type="email" name="email" required autocomplete="email"></label>
      <label class="f"><span>Firma</span><input name="firma" autocomplete="organization"></label>
      <label class="f"><span>Postojeći web (ako ga imate)</span><input name="web" inputmode="url" placeholder="www."></label>
    </div>
    <fieldset><legend>Što vam treba?</legend><div class="chips">{chk}</div></fieldset>
    <label class="f"><span>Opišite projekt *</span><textarea name="opis" rows="7" required placeholder="Što radite, što želite postići i što vam danas smeta. Primjeri i poveznice su dobrodošli."></textarea></label>
    <fieldset><legend>Okvirni budžet</legend><div class="chips">{bud}</div></fieldset>
    <fieldset><legend>Rok</legend><div class="chips">{rok}</div></fieldset>
    <div class="send"><button class="pill o" type="submit">Pošalji upit <span class="ar">→</span></button><p class="dim">Podatke koristimo samo za odgovor na upit. <a href="{TMB}/privatnost.html">Privatnost</a></p></div>
  </form>
  <aside class="za rv">
    <span class="tag">Radije mail?</span><p><a class="u" href="{UPIT}">{MAIL}</a></p>
    <span class="tag" style="margin-top:22px">Što slijedi</span>
    <ol class="nx"><li>Pročitamo upit i, ako nešto nedostaje, pitamo pisano.</li><li>Šaljemo pisanu ponudu s cijenom, rokom i popisom onoga što ulazi u cijenu.</li><li>Kad je prihvatite, krećemo. Dizajn komentirate u Figmi.</li></ol>
    <span class="tag" style="margin-top:22px">Mala firma?</span><p>Za web, dizajn i mreže po javnim cijenama pogledajte <a class="u" href="/tmbingo/">TMBingo paket</a>.</p>
  </aside>
</section>
</main>
""" + footer(False)


def hvala():
    return head("Hvala na upitu · Studio23k", "Upit je poslan.", "/upit/hvala/", noindex=True) + nav("") + f"""
<main><section class="phead">
  {round_sticker("hvala · hvala · hvala · ", "✓", "s6", 8)}
  <h1>Hvala <span class="o">:)</span></h1>
  <p>Upit je stigao. Pročitat ćemo ga i javiti se pisano na vaš e-mail. Ako se sjetite još nečega, samo odgovorite na naš mail ili pišite na <a class="u" href="mailto:{MAIL}">{MAIL}</a>.</p>
  <div class="acts" style="margin-top:30px"><a class="pill" href="/radovi/">Pogledajte radove <span class="ar">→</span></a></div>
</section></main>
""" + footer(False)


def w(p, s):
    p = os.path.join(OUT, p)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(s)


w("index.html", index())
w("radovi/index.html", radovi())
w("tmbingo/index.html", tmbingo())
w("404.html", nf())
w("usluge/index.html", usluge_index())
for i, (slug, name, short) in enumerate(USLUGE, 1):
    w(f"usluge/{slug}/index.html", usluga(i, slug, name, short))
w("upit/index.html", upit())
w("upit/hvala/index.html", hvala())
print("ok")
