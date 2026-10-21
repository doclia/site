// Liste d'attente : présélectionne le profil indiqué dans l'adresse (« /?profil=aesh#liste-attente », lien de la page AESH).
// Sans ce script, le formulaire s'affiche sans présélection et fonctionne de même.
(function () {
  var profil = new URLSearchParams(window.location.search).get("profil");
  if (!profil || !/^[a-z]+$/.test(profil)) return;
  var choix = document.querySelector('input[name="profile"][value="' + profil + '"]');
  if (choix) choix.checked = true;
})();
