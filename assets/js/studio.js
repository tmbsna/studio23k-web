/* Studio23k v2: izbornik, skrivanje trake pri skrolanju, glatko skrolanje, pojavljivanje sekcija, plutajuće slike,
   kursor, chat oblačić, povlačenje kartica i naljepnica. */
(function () {
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = matchMedia('(hover: hover) and (min-width: 901px)').matches;

  var lenis = null;
  if (!reduce && window.Lenis) {
    lenis = new Lenis({ lerp: 0.09 });
    (function raf(t) { lenis.raf(t); requestAnimationFrame(raf); })(performance.now());
  }

  /* menu */
  var menu = document.getElementById('menu');
  function openMenu() { menu.classList.add('open'); menu.setAttribute('aria-hidden', 'false'); if (lenis) lenis.stop(); }
  function closeMenu() { menu.classList.remove('open'); menu.setAttribute('aria-hidden', 'true'); if (lenis) lenis.start(); }
  document.querySelectorAll('.open-menu').forEach(function (b) { b.addEventListener('click', openMenu); });
  document.getElementById('closeMenu').addEventListener('click', closeMenu);
  addEventListener('keydown', function (e) { if (e.key === 'Escape') { closeMenu(); chat && chat.classList.remove('open'); } });

  document.querySelectorAll('a[href*="#"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var u = new URL(a.href, location.href);
      if (u.pathname !== location.pathname || !u.hash) return;
      var t = document.querySelector(u.hash); if (!t) return;
      e.preventDefault(); closeMenu();
      if (lenis) lenis.scrollTo(t, { offset: -20 }); else t.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth' });
    });
  });

  /* nav hides on scroll down */
  var nav = document.querySelector('.nav'), lastY = 0;
  var floats = document.querySelectorAll('[data-float]');
  function onScroll() {
    var y = scrollY;
    if (nav) nav.classList.toggle('hide', y > 300 && y > lastY && !menu.classList.contains('open'));
    lastY = y;
    if (!reduce) floats.forEach(function (f) { f.style.transform = 'translate3d(0,' + (y * (+f.dataset.float)) + 'px,0)'; });
  }
  addEventListener('scroll', onScroll, { passive: true }); onScroll();

  /* reveal */
  var rv = document.querySelectorAll('.rv');
  if (!reduce && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }); }, { rootMargin: '0px 0px -8% 0px' });
    rv.forEach(function (el) { io.observe(el); });
  } else rv.forEach(function (el) { el.classList.add('in'); });

  /* lazy video */
  var vids = document.querySelectorAll('video[data-lazyplay]');
  if (!reduce && 'IntersectionObserver' in window) {
    var vio = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { var p = e.target.play(); if (p && p.catch) p.catch(function () {}); } else e.target.pause(); }); }, { rootMargin: '200px' });
    vids.forEach(function (v) { vio.observe(v); });
  }

  /* cards: drag to scroll on desktop */
  document.querySelectorAll('.cards').forEach(function (c) {
    var down = false, sx = 0, sl = 0;
    c.addEventListener('pointerdown', function (e) { if (e.pointerType !== 'mouse') return; down = true; sx = e.clientX; sl = c.scrollLeft; c.style.scrollSnapType = 'none'; });
    addEventListener('pointerup', function () { if (!down) return; down = false; c.style.scrollSnapType = ''; });
    c.addEventListener('pointermove', function (e) { if (down) c.scrollLeft = sl - (e.clientX - sx); });
  });

  /* stickers: drag them around (desktop) */
  if (fine) document.querySelectorAll('.stk').forEach(function (s) {
    var d = null;
    s.addEventListener('pointerdown', function (e) { d = { x: e.clientX, y: e.clientY, tx: +(s.dataset.tx || 0), ty: +(s.dataset.ty || 0) }; s.setPointerCapture(e.pointerId); s.style.cursor = 'grabbing'; });
    s.addEventListener('pointermove', function (e) { if (!d) return; var tx = d.tx + e.clientX - d.x, ty = d.ty + e.clientY - d.y; s.dataset.tx = tx; s.dataset.ty = ty; s.style.translate = tx + 'px ' + ty + 'px'; });
    s.addEventListener('pointerup', function () { d = null; s.style.cursor = ''; });
  });

  /* cursor */
  var cur = document.querySelector('.cur');
  if (cur && fine && !reduce) {
    var mx = -100, my = -100, cx = -100, cy = -100;
    addEventListener('pointermove', function (e) { mx = e.clientX; my = e.clientY; });
    (function loop() { cx += (mx - cx) * .2; cy += (my - cy) * .2; cur.style.transform = 'translate(' + cx + 'px,' + cy + 'px)'; requestAnimationFrame(loop); })();
    document.querySelectorAll('[data-cur]').forEach(function (el) {
      el.addEventListener('pointerenter', function () { cur.classList.add('big'); cur.textContent = el.dataset.cur; });
      el.addEventListener('pointerleave', function () { cur.classList.remove('big'); cur.textContent = ''; });
    });
  } else if (cur) cur.remove();

  /* chat bubble */
  var chat = document.getElementById('chat');
  if (chat) {
    chat.querySelector('.btn').addEventListener('click', function () { chat.classList.toggle('open'); this.setAttribute('aria-expanded', chat.classList.contains('open')); });
    var seen = false; try { seen = sessionStorage.getItem('s23k-chat') === '1'; } catch (e) {}
    if (!seen && !reduce) setTimeout(function () { chat.classList.add('open'); try { sessionStorage.setItem('s23k-chat', '1'); } catch (e) {} }, 6000);
  }
})();

/* Society-ideje: uvodna zavjesa, svijetla/tamna tema, filteri radova */
(function () {
  var d = document.documentElement;
  var pre = document.getElementById('pre');
  if (pre && !d.classList.contains('no-pre') && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    var go = function () { setTimeout(function () { pre.classList.add('out'); setTimeout(function () { pre.remove(); }, 1100); }, 650); };
    if (document.readyState === 'complete') go(); else addEventListener('load', go);
    setTimeout(function () { pre.classList.add('out'); }, 2500);
  } else if (pre) pre.remove();

  var tb = document.getElementById('theme');
  if (tb) tb.addEventListener('click', function () {
    var dark = d.dataset.theme !== 'dark';
    if (dark) d.dataset.theme = 'dark'; else delete d.dataset.theme;
    try { localStorage.setItem('s23k-tema', dark ? 'dark' : ''); } catch (e) {}
  });

  var grid = document.getElementById('radoviGrid');
  document.querySelectorAll('.filt button').forEach(function (b, _, all) {
    b.addEventListener('click', function () {
      var f = b.dataset.f;
      all.forEach(function (x) { x.setAttribute('aria-pressed', x === b); });
      grid.classList.toggle('f', !!f);
      grid.querySelectorAll('li').forEach(function (li) { li.classList.toggle('out', !!f && li.dataset.cat.split(' ').indexOf(f) < 0); li.classList.add('in'); });
    });
  });
})();
