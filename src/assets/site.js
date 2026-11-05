// Menu mobile, visionneuse photo, protection des images.
(function () {
  var burger = document.querySelector(".burger"), menu = document.getElementById("menu");
  if (burger) burger.addEventListener("click", function () {
    var open = menu.hidden; menu.hidden = !open; burger.setAttribute("aria-expanded", String(open));
  });

  // Pas de clic droit ni de glisser-déposer sur les photos
  document.addEventListener("contextmenu", function (e) { if (e.target.closest(".ph, .lb-img, img")) e.preventDefault(); });
  document.addEventListener("dragstart", function (e) { if (e.target.closest(".ph, .lb-img, img")) e.preventDefault(); });

  // Visionneuse
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
