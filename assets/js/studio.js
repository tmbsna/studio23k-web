/* Studio23k: izbornik, gumb Kontakt pri skrolanju, izmjena fotografija u naslovu, glatko skrolanje, paralaksa, veliki natpis u podnožju. */
(function () {
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  var hs = document.querySelectorAll('#heroBg img'), hi = 0;
  if (!reduce && hs.length > 1) setInterval(function () { hs[hi].classList.remove('on'); hi = (hi + 1) % hs.length; hs[hi].classList.add('on'); }, 6000);

  var lenis = null;
  if (!reduce && window.Lenis) {
    lenis = new Lenis({ lerp: 0.09 });
    (function raf(t) { lenis.raf(t); requestAnimationFrame(raf); })(performance.now());
  }

  var menu = document.getElementById('menu');
  function openMenu() { menu.classList.add('open'); menu.setAttribute('aria-hidden', 'false'); if (lenis) lenis.stop(); }
  function closeMenu() { menu.classList.remove('open'); menu.setAttribute('aria-hidden', 'true'); if (lenis) lenis.start(); }
  document.querySelectorAll('.open-menu').forEach(function (b) { b.addEventListener('click', openMenu); });
  document.getElementById('closeMenu').addEventListener('click', closeMenu);
  addEventListener('keydown', function (e) { if (e.key === 'Escape') closeMenu(); });

  document.querySelectorAll('a[href*="#"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var u = new URL(a.href, location.href);
      if (u.pathname !== location.pathname || !u.hash) return;
      var target = document.querySelector(u.hash);
      if (!target) return; e.preventDefault(); closeMenu();
      if (lenis) lenis.scrollTo(target, { offset: 0 }); else target.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth' });
    });
  });

  var chip = document.getElementById('chip'), top = document.querySelector('.hero, .top');
  var par = document.querySelectorAll('[data-parallax]');
  function onScroll() {
    var vh = innerHeight;
    if (chip && top) chip.classList.toggle('on', top.getBoundingClientRect().bottom < 60);
    if (!reduce) par.forEach(function (im) { var r = im.parentNode.getBoundingClientRect(); if (r.bottom < 0 || r.top > vh) return; var p = (r.top + r.height / 2 - vh / 2) / vh; im.style.transform = 'translate3d(0,' + (p * -6) + '%,0)'; });
  }
  addEventListener('scroll', onScroll, { passive: true }); addEventListener('resize', onScroll); onScroll();

  var giant = document.querySelector('.giant'), gspan = giant && giant.querySelector('span');
  function fitGiant() { if (!gspan) return; giant.style.fontSize = '100px'; var w = giant.clientWidth, sw = gspan.getBoundingClientRect().width; if (sw) giant.style.fontSize = Math.floor(100 * w / sw * 0.99) + 'px'; }
  fitGiant(); if (document.fonts && document.fonts.ready) document.fonts.ready.then(fitGiant); addEventListener('resize', fitGiant);

  var vids = document.querySelectorAll('video[data-lazyplay]');
  if (!reduce && 'IntersectionObserver' in window) {
    var vio = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { var pr = e.target.play(); if (pr && pr.catch) pr.catch(function () {}); } else e.target.pause(); }); }, { rootMargin: '200px' });
    vids.forEach(function (v) { vio.observe(v); });
  }
})();
