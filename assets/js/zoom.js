// Captures d'écran : un clic ouvre une vue agrandie dans une fenêtre modale (<dialog> natif : focus gardé, Échap ferme).
// Sans ce script (ou sans <dialog>) : le lien ouvre simplement l'image en grand.
(function () {
  var liens = document.querySelectorAll("a.zoom");
  if (!liens.length || typeof HTMLDialogElement !== "function") return;

  var dialog = document.createElement("dialog");
  dialog.className = "zoom-dialog";
  var fermer = document.createElement("button");
  fermer.type = "button";
  fermer.className = "zoom-dialog__fermer";
  fermer.textContent = "Fermer";
  var cadre = document.createElement("div");
  cadre.className = "zoom-dialog__cadre";
  var image = document.createElement("img");
  cadre.appendChild(image);
  dialog.appendChild(fermer);
  dialog.appendChild(cadre);
  document.body.appendChild(dialog);

  var origine = null;
  fermer.addEventListener("click", function () { dialog.close(); });
  // Un clic hors de l'image (fond sombre, marges) ferme aussi.
  dialog.addEventListener("click", function (e) { if (e.target !== image) dialog.close(); });
  dialog.addEventListener("close", function () {
    image.removeAttribute("src");
    if (origine) origine.focus();
    origine = null;
  });

  Array.prototype.forEach.call(liens, function (lien) {
    lien.addEventListener("click", function (e) {
      if (e.button !== 0 || e.ctrlKey || e.metaKey || e.shiftKey || e.altKey) return;
      e.preventDefault();
      var source = lien.querySelector("img");
      image.alt = source ? source.alt : "";
      image.src = lien.getAttribute("href");
      dialog.setAttribute("aria-label", image.alt);
      // Variante d’affichage (data-zoom) : « bandeau » (très allongé), « tel » (écran de téléphone, en hauteur).
      dialog.className = "zoom-dialog" + (lien.dataset.zoom ? " zoom-dialog--" + lien.dataset.zoom : "");
      origine = lien;
      dialog.showModal();
      fermer.focus();
    });
  });
})();
