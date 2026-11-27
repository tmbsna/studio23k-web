// Ilustracije za podstranice usluga Studio23k (1600x1000). Pokretanje: node izvor/usluge_slike.js <mapa-stranice>
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path');
const root = path.resolve(process.argv[2] || '.');
const types = { '.css': 'text/css', '.jpg': 'image/jpeg', '.png': 'image/png', '.woff2': 'font/woff2' };
const srv = http.createServer((q, r) => { const f = path.join(root, decodeURIComponent(q.url.split('?')[0])); if (!fs.existsSync(f)) { r.writeHead(404); return r.end(); } r.writeHead(200, { 'Content-Type': types[path.extname(f)] || 'application/octet-stream', 'Access-Control-Allow-Origin': '*' }); fs.createReadStream(f).pipe(r); }).listen(8768);
const B = 'http://localhost:8768';

const base = `<link rel="stylesheet" href="${B}/assets/fonts/fonts.css"><style>
*{box-sizing:border-box;margin:0}body{width:1600px;height:1000px;overflow:hidden;position:relative;font-family:Manrope;color:#0d1512}
.syne{font-family:Manrope;font-weight:800;letter-spacing:-.04em}
.card{position:absolute;border-radius:36px;box-shadow:0 40px 80px rgba(13,21,18,.22);overflow:hidden;background:#fbf8f2}
.stk{position:absolute;display:grid;place-items:center;text-align:center;font:800 40px/1 Manrope;letter-spacing:-.03em}
.round{border-radius:50%}
.pill{position:absolute;border-radius:999px;padding:18px 30px;font:700 28px/1 Manrope}
.bar{display:flex;gap:10px;padding:18px 22px;background:#efe9dc}.bar i{width:16px;height:16px;border-radius:50%;background:#d6cfbf}
.tag{font:700 20px/1 Manrope;letter-spacing:.14em;text-transform:uppercase}
.num{position:absolute;left:70px;bottom:60px}
</style>`;

const S = {
  'web-platforme': `<body style="background:#9ad1ff">
    <div class="card" style="left:140px;top:150px;width:880px;height:660px;rotate:-3deg"><img src="${B}/assets/radovi/frida.jpg" style="width:100%;height:100%;object-fit:cover"></div>
    <div class="card" style="left:900px;top:300px;width:600px;height:450px;rotate:4deg"><img src="${B}/assets/radovi/ldesign.jpg" style="width:100%;height:100%;object-fit:cover"></div>
    <div class="pill" style="left:110px;top:70px;background:#0d1512;color:#f4efe4;rotate:-6deg">HR · EN · DE</div>
    <div class="pill" style="left:820px;top:840px;background:#ff5a1f;rotate:4deg">Rezervacije ✓</div>
    <div class="stk round" style="right:70px;top:60px;width:200px;height:200px;background:#ffd23f;rotate:-12deg">po<br>mjeri</div></body>`,
  'web-trgovine': `<body style="background:#ffb3c7">
    <div class="card" style="left:120px;top:170px;width:860px;height:645px;rotate:2deg"><img src="${B}/assets/radovi/goveer.jpg" style="width:100%;height:100%;object-fit:cover"></div>
    <div class="card" style="left:930px;top:110px;width:520px;height:330px;padding:34px;rotate:-4deg"><p class="tag" style="opacity:.6">Košarica</p><p class="syne" style="font-size:96px;margin-top:20px">3 × ✦</p><p style="font:700 34px Manrope;margin-top:16px">Ukupno 249,00 €</p></div>
    <div class="card" style="left:1010px;top:500px;width:440px;height:300px;padding:34px;background:#0d1512;color:#f4efe4;rotate:3deg"><p class="tag" style="opacity:.6">Plaćanje</p><div style="margin-top:34px;height:120px;border-radius:22px;background:linear-gradient(135deg,#ff5a1f,#ffd23f);position:relative"><span style="position:absolute;left:24px;bottom:20px;font:700 26px Manrope;color:#0d1512">•••• 2323</span></div></div>
    <div class="pill" style="left:80px;top:80px;background:#ffd23f;rotate:-5deg">Dostava sutra 📦</div>
    <div class="stk round" style="left:60px;bottom:50px;width:180px;height:180px;background:#3faf7f;rotate:10deg;font-size:34px">+1<br>narudžba</div></body>`,
  'web-aplikacije': `<body style="background:#0f3b2e">
    <div class="card" style="left:150px;top:120px;width:1300px;height:760px;padding:40px;display:grid;grid-template-columns:260px 1fr;gap:34px">
      <div style="background:#0d1512;border-radius:24px;padding:30px;color:#f4efe4;display:grid;align-content:start;gap:22px;font:700 24px Manrope"><span class="syne" style="font-size:36px">crm<span style="color:#ff5a1f">.</span></span><span style="opacity:.5">Upiti</span><span>Klijenti</span><span style="opacity:.5">Zadaci</span><span style="opacity:.5">Računi</span></div>
      <div style="display:grid;grid-template-rows:auto 1fr;gap:28px">
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:20px">
          ${[['Novi upiti','24','#ffd23f'],['Otvoreni zadaci','7','#9ad1ff'],['Riješeno','132','#3faf7f']].map(([a,b,c])=>`<div style="background:${c};border-radius:24px;padding:24px"><p class="tag" style="font-size:16px">${a}</p><p class="syne" style="font-size:88px;margin-top:10px">${b}</p></div>`).join('')}
        </div>
        <div style="background:#f4efe4;border-radius:24px;padding:30px;display:flex;align-items:flex-end;gap:22px">
          ${[40,62,48,80,66,92,74,100,86,70].map((h,i)=>`<div style="flex:1;height:${h*3.2}px;border-radius:14px 14px 4px 4px;background:${i==7?'#ff5a1f':'#0f3b2e'}"></div>`).join('')}
        </div>
      </div>
    </div>
    <div class="pill" style="right:90px;top:60px;background:#ff5a1f;rotate:6deg">Automatski ⚡</div>
    <div class="stk round" style="left:70px;bottom:50px;width:190px;height:190px;background:#ffb3c7;rotate:-10deg;font-size:30px">manje<br>ručnog<br>posla</div></body>`,
  'brend-identitet': `<body style="background:#f4efe4">
    <div class="card" style="left:120px;top:120px;width:640px;height:640px;background:#0f3b2e;display:grid;place-items:center;rotate:-4deg"><img src="${B}/assets/logo-icon.png" style="height:440px"></div>
    <div style="position:absolute;left:840px;top:130px;display:grid;grid-template-columns:repeat(2,300px);gap:24px">
      ${[['#0f3b2e','#f4efe4','Borovina'],['#ff5a1f','#0d1512','Narančasta'],['#ffd23f','#0d1512','Sunce'],['#ffb3c7','#0d1512','Ruža']].map(([b,c,n],i)=>`<div style="height:200px;border-radius:30px;background:${b};color:${c};padding:24px;display:grid;align-content:space-between;rotate:${[3,-2,-3,2][i]}deg;box-shadow:0 30px 60px rgba(13,21,18,.15)"><span class="tag">${n}</span><span style="font:700 24px Manrope">${b.toUpperCase()}</span></div>`).join('')}
    </div>
    <div class="card" style="left:840px;top:620px;width:624px;height:260px;padding:34px;rotate:-1deg"><p class="syne" style="font-size:110px;line-height:.9">Aa</p><p style="font:700 26px Manrope;margin-top:14px">Manrope Bold</p></div>
    <div class="stk round" style="left:620px;top:690px;width:200px;height:200px;background:#ffd23f;rotate:12deg;font-size:30px">knjiga<br>standarda</div></body>`,
  'foto-video': `<body style="background:#ffd23f">
    <div class="card" style="left:180px;top:120px;width:1240px;height:760px;rotate:-2deg"><img src="${B}/assets/img/hero-3.jpg" style="width:100%;height:100%;object-fit:cover">
      <div style="position:absolute;inset:40px;border:4px solid rgba(255,255,255,.9);border-radius:20px"></div>
      <div style="position:absolute;left:70px;top:66px;display:flex;align-items:center;gap:14px;color:#fff;font:700 28px Manrope"><i style="width:22px;height:22px;border-radius:50%;background:#ff3b30"></i>REC 00:23</div>
      <div style="position:absolute;right:70px;bottom:66px;color:#fff;font:700 26px Manrope">4K · 25 fps</div>
      <div style="position:absolute;left:50%;top:50%;width:110px;height:110px;margin:-55px 0 0 -55px;border:4px solid #fff;border-radius:50%"></div>
    </div>
    <div class="pill" style="left:110px;top:70px;background:#0d1512;color:#f4efe4;rotate:-5deg">Proizvodi · Prostori · Događaji</div>
    <div class="stk round" style="right:80px;bottom:50px;width:200px;height:200px;background:#ff5a1f;rotate:10deg;font-size:34px">akcija!</div></body>`,
  'kampanje-tisak': `<body style="background:#9ad1ff">
    <div style="position:absolute;left:150px;top:120px;width:1080px;height:520px;border-radius:24px;background:#0f3b2e;box-shadow:0 40px 80px rgba(13,21,18,.25);display:grid;align-content:center;padding:60px;rotate:-2deg"><p class="syne" style="font-size:150px;line-height:.86;color:#f4efe4">Kreiramo<br><span style="color:#ff5a1f">doživljaj.</span></p></div>
    <div style="position:absolute;left:640px;top:640px;width:26px;height:300px;background:#0d1512;rotate:-2deg"></div>
    <div class="card" style="left:1180px;top:300px;width:320px;height:450px;padding:30px;rotate:7deg;background:#f4efe4"><p class="tag" style="opacity:.6">Meni A5</p><p class="syne" style="font-size:56px;margin-top:22px;line-height:.95">Fritule<br>Uštipci<br>Kava</p><p style="font:700 24px Manrope;margin-top:30px">· · · · · · 3 €</p></div>
    <div class="pill" style="left:110px;top:60px;background:#ffd23f;rotate:-5deg">Jumbo 504 × 238</div>
    <div class="stk round" style="left:90px;bottom:60px;width:190px;height:190px;background:#ffb3c7;rotate:-12deg;font-size:30px">spremno<br>za tisak</div></body>`,
  'seo-ai-vidljivost': `<body style="background:#3faf7f">
    <div class="card" style="left:200px;top:120px;width:1200px;height:150px;border-radius:999px;display:flex;align-items:center;padding:0 60px;gap:30px;rotate:-1deg"><svg width="56" height="56" viewBox="0 0 24 24" fill="none" stroke="#0d1512" stroke-width="2.6"><circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/></svg><span style="font:600 46px Manrope">izrada web trgovine zadar</span></div>
    <div class="card" style="left:200px;top:330px;width:1200px;height:240px;padding:40px 60px;rotate:1deg;box-shadow:0 0 0 6px #ff5a1f,0 40px 80px rgba(13,21,18,.22)"><p style="font:600 26px Manrope;opacity:.6">studio23k.eu</p><p class="syne" style="font-size:64px;margin-top:10px">Studio23k · Web, brend i aplikacije</p><p style="font:500 28px Manrope;margin-top:12px;opacity:.7">Zadar · Web, trgovine i aplikacije po mjeri</p></div>
    <div class="card" style="left:200px;top:620px;width:1200px;height:200px;padding:40px 60px;opacity:.55;rotate:-1deg"><p style="font:600 26px Manrope;opacity:.6">neki-drugi.hr</p><p class="syne" style="font-size:54px;margin-top:10px">Netko drugi</p></div>
    <div class="stk round" style="right:70px;top:250px;width:210px;height:210px;background:#ffd23f;rotate:12deg;font-size:90px">#1</div>
    <div class="pill" style="left:90px;bottom:60px;background:#0d1512;color:#f4efe4;rotate:-4deg">AI asistenti nas spominju ✦</div></body>`,
  'odrzavanje': `<body style="background:#ffb3c7">
    <div class="card" style="left:160px;top:140px;width:760px;height:720px;padding:50px;display:grid;align-content:space-between;rotate:-3deg"><p class="tag" style="opacity:.6">Stanje weba</p><p class="syne" style="font-size:150px;line-height:.9">Sve<br>radi ✓</p><div style="display:flex;gap:8px">${Array.from({length:30},(_, i)=>`<i style="flex:1;height:70px;border-radius:8px;background:${i==17?'#ffd23f':'#3faf7f'}"></i>`).join('')}</div></div>
    <div class="card" style="left:980px;top:180px;width:460px;height:300px;padding:40px;background:#0f3b2e;color:#f4efe4;rotate:4deg"><p class="tag" style="opacity:.6">Sigurnosna kopija</p><p class="syne" style="font-size:66px;margin-top:30px">redovito</p></div>
    <div class="card" style="left:1000px;top:540px;width:440px;height:280px;padding:40px;rotate:-2deg"><p class="tag" style="opacity:.6">Izmjena</p><p style="font:700 40px/1.2 Manrope;margin-top:20px">Novi cjenik na webu ✓</p></div>
    <div class="stk round" style="left:70px;bottom:50px;width:190px;height:190px;background:#ffd23f;rotate:-10deg;font-size:30px">mirni<br>ste</div></body>`,
};

(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1600, height: 1000 } });
  fs.mkdirSync(path.join(root, 'assets/usluge'), { recursive: true });
  for (const [k, html] of Object.entries(S)) {
    await p.setContent(base + html, { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    await p.screenshot({ path: path.join(root, 'assets/usluge', k + '.jpg'), type: 'jpeg', quality: 82 });
    console.log(k);
  }
  await b.close(); srv.close();
})();
