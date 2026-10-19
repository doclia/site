// Page /confirmer (S3, contrat CTO du 19/10/2026) : copie le jeton « t » de l’adresse dans le champ caché du formulaire.
// Sans ce script, la confirmation est impossible : une page statique ne peut pas lire l’adresse autrement.
(function () {
  var champ = document.getElementById("jeton");
  if (!champ) return;
  var jeton = new URLSearchParams(window.location.search).get("t");
  if (jeton) champ.value = jeton;
})();
