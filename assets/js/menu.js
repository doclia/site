// Menu replié (mobile) : amélioration seulement. Sans ce fichier, le menu <details> fonctionne, il reste juste ouvert après un clic.
// Referme le menu quand on choisit un lien, ou avec la touche Échap (le focus revient sur le bouton « Menu »).
(function () {
  var menu = document.querySelector(".menu");
  if (!menu) return;
  var toggle = menu.querySelector("summary");
  menu.addEventListener("click", function (e) {
    if (e.target.closest("a")) menu.open = false;
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && menu.open) {
      menu.open = false;
      toggle.focus();
    }
  });
})();
