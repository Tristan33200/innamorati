// Menu mobile, visionneuse photo, protection des images, parallaxe et apparitions.
(function () {
  var reduit = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var burger = document.querySelector(".burger"), menu = document.getElementById("menu");
  if (burger) burger.addEventListener("click", function () {
    var open = menu.hidden; menu.hidden = !open; burger.setAttribute("aria-expanded", String(open));
  });

  // Pas de clic droit ni de glisser-déposer sur les photos
  document.addEventListener("contextmenu", function (e) { if (e.target.closest(".ph, .lb-img, img")) e.preventDefault(); });
  document.addEventListener("dragstart", function (e) { if (e.target.closest(".ph, .lb-img, img")) e.preventDefault(); });

  // ---------- Mouvement ----------
  if (!reduit && "IntersectionObserver" in window) {
    document.documentElement.classList.add("fx");
    var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

    // Titres : mot par mot
    $$(".head h1, .head h2, .intro h2, .family h2, .contact h1, .band blockquote p, .hero .big, .album-hero h1, .litter h2, .art h2").forEach(function (h) {
      if (h.querySelector("a")) return;
      var mots = h.textContent.trim().split(/\s+/);
      h.innerHTML = mots.map(function (m, i) { return '<span class="w"><span style="--i:' + i + '">' + m + "</span></span>"; }).join(" ");
      h.classList.add("split");
    });
    // Blocs qui apparaissent en glissant
    $$(".head p, .head .label, .intro p, .intro .label, .litter span, .card .t, .door h3, .door .label, .family .text p, .birman-grid .text > p, .std > div, .steps li, .incl li, .verify-grid > div, .titles-list li, .facts > div, .recap-t tr, .recap-regles > div, .note, .years, .price, .band cite, .results, .art p, .faq details, .sommaire").forEach(function (el) { el.classList.add("rv"); });
    // Photos qui se dévoilent comme un rideau
    $$(".card .ph, .door .ph, .g-item .ph, .mosaic .ph, .family .ph, .birman-grid > .ph, .palm-grid > .ph").forEach(function (el) { el.classList.add("rv", "ph-rv"); });
    // Décalage en cascade dans les grilles
    $$(".grid, .gallery, .doors, .steps, .incl, .verify-grid, .std, .titles-list, .facts, .mosaic, .articles").forEach(function (g) {
      Array.prototype.forEach.call(g.children, function (c, i) {
        var d = (i % 8) * 90 + "ms";
        c.style.setProperty("--d", d);
        $$(".rv", c).forEach(function (x) { x.style.setProperty("--d", d); });
      });
    });
    // Une photo masquée par clip-path n'est jamais « visible » : on observe son parent à la place
    var cibles = new Map();
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (en) {
        if (!en.isIntersecting) return;
        (cibles.get(en.target) || [en.target]).forEach(function (t) { t.classList.add("in"); });
        io.unobserve(en.target);
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0 });
    $$(".rv, .split").forEach(function (el) {
      if (el.classList.contains("ph-rv")) {
        var p = el.parentNode, l = cibles.get(p);
        if (l) l.push(el); else { cibles.set(p, [el]); io.observe(p); }
      } else io.observe(el);
    });

    // Parallaxe : seulement les éléments visibles
    var vus = new Set();
    var io2 = new IntersectionObserver(function (es) {
      es.forEach(function (en) { if (en.isIntersecting) vus.add(en.target); else vus.delete(en.target); });
      onScroll();
    }, { rootMargin: "20% 0px" });
    $$(".ph:not(.vide)").filter(function (p) { return !p.closest(".film"); }).concat($$(".ribbon")).forEach(function (el) { io2.observe(el); });
    var hero = document.querySelector(".hero"), heroTxt = hero && hero.querySelector(".wrap"), heroImg = hero && hero.querySelector(".ph img");
    var DERIVE = [0, 240, -110, 320, -60, 180], MOSA = [-9, 6, -10, 8, -5, 9];

    // Défilé horizontal : la page descend, les photos glissent de droite à gauche
    var films = $$(".film").map(function (f) { return { f: f, t: f.querySelector(".film-track"), d: 0, im: $$(".f-item img", f) }; });
    function mesure() {
      films.forEach(function (o) {
        o.d = Math.max(0, o.t.scrollWidth - window.innerWidth + 32);
        o.f.style.height = (o.d + window.innerHeight) + "px";
      });
    }
    films.forEach(function (o) { o.im.forEach(function (im) { im.addEventListener("load", function () { mesure(); onScroll(); }); }); });
    mesure();

    var ticking = false;
    function frame() {
      ticking = false;
      var vh = window.innerHeight, y = window.scrollY, vw = window.innerWidth;
      films.forEach(function (o) {
        var top = o.f.getBoundingClientRect().top;
        if (top > vh || top < -o.d - vh) return;
        var k = Math.min(1, Math.max(0, -top / (o.d || 1)));
        o.t.style.transform = "translate3d(" + (-k * o.d).toFixed(1) + "px,0,0)";
        o.im.forEach(function (im) {
          var r = im.parentNode.getBoundingClientRect();
          im.style.translate = (((r.left + r.width / 2 - vw / 2) / vw) * -9).toFixed(2) + "% 0";
        });
      });
      if (hero && y < vh * 1.2) {
        heroImg.style.setProperty("--py", (y * 0.38).toFixed(1) + "px");
        heroTxt.style.transform = "translate3d(0," + (y * -0.22).toFixed(1) + "px,0)";
        heroTxt.style.opacity = Math.max(0, 1 - y / (vh * 0.65)).toFixed(3);
      }
      var rects = new Map();
      vus.forEach(function (el) {
        var r = el.getBoundingClientRect();
        var p = (r.top + r.height / 2 - vh / 2) / vh; // négatif en haut de l'écran, positif en bas
        if (el.classList.contains("ribbon")) {
          el.firstElementChild.style.transform = "translate3d(" + (p * 28 - 22).toFixed(2) + "%,0,0)";
        } else if (el.classList.contains("g-item")) {
          // Colonnes qui glissent d'un bloc, chacune à sa vitesse (avancement de toute la galerie)
          var g = el.parentNode, gr = rects.get(g);
          if (!gr) { gr = g.getBoundingClientRect(); rects.set(g, gr); }
          var k = Math.min(1, Math.max(0, (vh - gr.top) / (vh + gr.height)));
          var col = Math.round(el.offsetLeft / (el.offsetWidth + 12));
          el.style.translate = "0 " + ((0.5 - k) * DERIVE[col % 6]).toFixed(1) + "px";
        } else if (el.parentNode.classList.contains("mosaic")) {
          // Chaque photo glisse dans son cadre, à sa propre vitesse (sans chevauchement)
          var i = Array.prototype.indexOf.call(el.parentNode.children, el);
          var m = el.querySelector("img"); if (m) m.style.setProperty("--py", (p * MOSA[i % 6]).toFixed(2) + "%");
        } else if (!el.parentNode.classList.contains("hero")) {
          var img = el.querySelector("img");
          if (img) img.style.setProperty("--py", (p * (el.parentNode.classList.contains("band") ? -16 : -7)).toFixed(2) + "%");
        }
      });
    }
    function onScroll() { if (!ticking) { ticking = true; requestAnimationFrame(frame); } }
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", function () { mesure(); onScroll(); });
    frame();
  }

  // ---------- Visionneuse ----------
  var items = Array.prototype.slice.call(document.querySelectorAll(".g-item"));
  var lb = document.getElementById("lb"); if (!lb || !items.length) return;
  var im = lb.querySelector("img"), cap = lb.querySelector("figcaption"), cur = 0;
  function show(i) {
    cur = (i + items.length) % items.length;
    im.src = items[cur].getAttribute("href");
    cap.textContent = items[cur].dataset.cap + "  ·  " + (cur + 1) + " / " + items.length;
  }
  items.forEach(function (a, i) {
    a.addEventListener("click", function (e) { e.preventDefault(); show(i); lb.hidden = false; document.body.style.overflow = "hidden"; lb.querySelector(".lb-x").focus(); });
  });
  function close() { lb.hidden = true; document.body.style.overflow = ""; im.removeAttribute("src"); }
  lb.querySelector(".lb-x").onclick = close;
  lb.querySelector(".lb-p").onclick = function () { show(cur - 1); };
  lb.querySelector(".lb-n").onclick = function () { show(cur + 1); };
  document.addEventListener("keydown", function (e) {
    if (lb.hidden) return;
    if (e.key === "Escape") close(); else if (e.key === "ArrowLeft") show(cur - 1); else if (e.key === "ArrowRight") show(cur + 1);
  });
  var x0 = null;
  lb.addEventListener("touchstart", function (e) { x0 = e.touches[0].clientX; }, { passive: true });
  lb.addEventListener("touchend", function (e) { if (x0 === null) return; var dx = e.changedTouches[0].clientX - x0; if (Math.abs(dx) > 50) show(cur + (dx < 0 ? 1 : -1)); x0 = null; });
})();

// Vitesse : polices chargées juste après le premier affichage, photos du bas de page après la photo du haut
(function () {
  var moi = document.currentScript && document.currentScript.src;
  requestAnimationFrame(function () { setTimeout(function () {
    if (!moi) return;
    var l = document.createElement("link"); l.rel = "stylesheet"; l.href = moi.replace(/site\.js.*$/, "fonts.css"); document.head.appendChild(l);
  }, 0); });
  function photos() {
    Array.prototype.forEach.call(document.querySelectorAll("img[data-src]"), function (i) {
      if (i.dataset.srcset) i.srcset = i.dataset.srcset;
      i.src = i.dataset.src; i.removeAttribute("data-src");
    });
  }
  if (document.readyState === "complete") photos(); else window.addEventListener("load", function () { setTimeout(photos, 0); });
})();
