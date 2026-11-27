const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path');
const root = process.argv[2], out = process.argv[3];
const types = { '.html':'text/html; charset=utf-8', '.css':'text/css', '.js':'text/javascript', '.jpg':'image/jpeg', '.png':'image/png', '.woff2':'font/woff2', '.mp4':'video/mp4', '.svg':'image/svg+xml' };
const srv = http.createServer((q, r) => { let p = decodeURIComponent(q.url.split('?')[0]); if (p.endsWith('/')) p += 'index.html'; const f = path.join(root, p); if (!fs.existsSync(f)) { r.writeHead(404); return r.end(); } r.writeHead(200, { 'Content-Type': types[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(r); }).listen(8765);
(async () => {
  const b = await chromium.launch();
  // favicon + og
  const p0 = await b.newPage({ viewport: { width: 512, height: 512 } });
  await p0.goto('http://localhost:8765/');
  await p0.setContent(`<link rel="stylesheet" href="http://localhost:8765/assets/fonts/fonts.css"><style>html,body{margin:0}body{width:512px;height:512px;background:#0f3b2e;display:grid;place-items:center}</style><img src="http://localhost:8765/assets/logo-icon.png" style="height:400px">`);
  await p0.waitForTimeout(500);
  await p0.screenshot({ path: path.join(root, 'assets/apple-touch-icon.png') });
  await p0.setViewportSize({ width: 64, height: 64 });
  await p0.setContent(`<link rel="stylesheet" href="http://localhost:8765/assets/fonts/fonts.css"><style>html,body{margin:0}body{width:64px;height:64px;background:#0f3b2e;display:grid;place-items:center}</style><img src="http://localhost:8765/assets/logo-icon.png" style="height:56px">`);
  await p0.waitForTimeout(300);
  await p0.screenshot({ path: path.join(root, 'assets/favicon.png') });
  await p0.setViewportSize({ width: 1200, height: 630 });
  await p0.setContent(`<link rel="stylesheet" href="http://localhost:8765/assets/fonts/fonts.css"><style>html,body{margin:0}body{width:1200px;height:630px;background:#f4efe4;color:#0d1512;position:relative;overflow:hidden}main{position:absolute;inset:56px;display:grid;grid-template-rows:auto 1fr auto}p{margin:0;font:700 17px/1.4 Manrope;letter-spacing:.12em;text-transform:uppercase}h1{margin:0;align-self:center;font:800 104px/1 Manrope;letter-spacing:-.045em}h1 span{color:transparent;-webkit-text-stroke:2.5px #0d1512}em{font-style:normal;background:#0f3b2e;color:#f4efe4;padding:0 .12em;border-radius:.35em;display:inline-block;transform:rotate(-2deg)}b{color:#ff5a1f}.s{position:absolute;right:70px;top:56px;height:150px;padding:26px 30px;background:#0f3b2e;border-radius:28px;transform:rotate(-6deg)}.lg{height:44px}.g{color:#1f7a52}</style><img class="s" src="http://localhost:8765/assets/logo-icon.png"><main><p><img class="lg" src="http://localhost:8765/assets/logo.png"></p><h1>Mi prodajemo <em>ideje</em><b>.</b><br><span>Usluge su samo alat.</span></h1><p>Web · Brend · Aplikacije · Foto i video · <span class="g">TMBingo by Studio23k</span></p></main>`);
  await p0.waitForTimeout(800);
  await p0.screenshot({ path: path.join(root, 'assets/og-image.jpg'), type: 'jpeg', quality: 85 });
  for (const [u, n] of [['/', 'naslovna'], ['/tmbingo/', 'tmbingo'], ['/radovi/', 'radovi']]) {
    for (const [w, h, s] of [[1440, 900, 'desk'], [390, 844, 'mob']]) {
      const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1, reducedMotion: 'reduce' });
      await p.goto('http://localhost:8765' + u, { waitUntil: 'networkidle' });
      await p.evaluate(async () => { for (const i of document.querySelectorAll('img[loading=lazy]')) i.loading = 'eager'; await new Promise(r => setTimeout(r, 800)); });
      const sw = await p.evaluate(() => document.documentElement.scrollWidth);
      console.log(n, s, 'scrollWidth', sw);
      await p.screenshot({ path: path.join(out, `${n}-${s}.jpg`), fullPage: true, type: 'jpeg', quality: 70 });
      await p.close();
    }
  }
  await b.close(); srv.close();
})();
