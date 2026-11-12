/* Bouton d’inscription fixe de /familles, sur téléphone (mandat du CMO, 11/11 11:17 ; conditions du CTO, 11/11 12:13).
   Visible par défaut. Ce script le cache tant que le premier bouton n’est pas dépassé au défilement,
   et quand le bouton final est à l’écran. Il pose ou retire une classe, rien d’autre :
   aucune requête, aucun stockage, aucun style en ligne. Sans script, sans IntersectionObserver
   ou sur une erreur, le bouton reste visible. */
(function () {
  'use strict';
  try {
    if (!('IntersectionObserver' in window)) { return; }
    var fixe = document.querySelector('.cta-fixe');
    if (!fixe) { return; }
    /* Boutons du texte seulement : ceux du bouton fixe sont écartés (fragilité relevée par le CTO, 11/11 14:10). */
    var boutons = Array.prototype.filter.call(document.querySelectorAll('main .btn--lg'), function (b) {
      return !fixe.contains(b);
    });
    if (boutons.length < 2) { return; }
    var premier = boutons[0];
    var dernier = boutons[boutons.length - 1];
    var premierDepasse = false;
    var dernierVisible = false;
    function appliquer() {
      fixe.classList.toggle('cta-fixe--cache', !premierDepasse || dernierVisible);
    }
    new IntersectionObserver(function (entrees) {
      var e = entrees[entrees.length - 1];
      premierDepasse = !e.isIntersecting && e.boundingClientRect.bottom <= 0;
      appliquer();
    }).observe(premier);
    /* Marge basse : la hauteur du bouton fixe, pour ne compter le bouton final que lorsqu’il est vraiment lisible. */
    new IntersectionObserver(function (entrees) {
      dernierVisible = entrees[entrees.length - 1].isIntersecting;
      appliquer();
    }, { rootMargin: '0px 0px -72px 0px' }).observe(dernier);
  } catch (erreur) {
    /* Le bouton reste visible. */
  }
})();
