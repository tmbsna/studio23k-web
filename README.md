# studio23k.eu

Nova stranica Studio23k na istom sustavu kao tmbingo.com: statički HTML, CSS i JS, bez builda, objava na Netlifyju.

Studio23k je glavni brend za veće projekte po mjeri. Paket za male firme je **TMBingo by Studio23k** (stranica `/tmbingo/`, narudžba ostaje na tmbingo.com).

## Struktura
- `index.html` naslovna (usluge, proces, dva načina suradnje, radovi, pitanja, kontakt)
- `radovi/` svi radovi i klijenti
- `tmbingo/` TMBingo by Studio23k: paketi s baznim cijenama i usporedba s projektom po mjeri
- `assets/studio.css`, `assets/js/studio.js` zajednički stil i skripta
- `sitemap.xml`, `robots.txt`, `llms.txt` za Google i AI pretrage
- `netlify.toml` preusmjerava stare WordPress adrese (/usluge/, /studio/, /kontakt/, /novosti/, /cjenik/)

**Kad se mijenjaju cijene TMBingo paketa** (u `app/cjenik.mjs` na tmbingo-web), promijeni ih i u `tmbingo/index.html`, na naslovnoj (kartica "od 199 €") i u `llms.txt`.

## Objava na Netlify
1. Netlify → Add new site → Import an existing project → GitHub → ovaj repozitorij.
2. Build command prazno, Publish directory `.`.
3. Provjeri testnu adresu (`*.netlify.app`).
4. Domain management → Add domain → `studio23k.eu`, pa kod registra domene prebaci DNS prema uputama Netlifyja. Stari WordPress tek onda ugasi (napravi sigurnosnu kopiju).

## Lokalni pregled
```sh
python3 -m http.server 8000
```

## Izmjene stranica
Naslovna, /radovi/ i /tmbingo/ generiraju se iz `izvor/build.py` (zajedničko zaglavlje i podnožje): `python3 izvor/build.py .`
