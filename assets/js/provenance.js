/*
 * Provenance de l'inscription à la liste d'attente (CTO n° 8, 08/11/2026 19:34 et 19:42 ; demande du CMO, 06/11 ; règle 6 du COS).
 *
 * 1. Report dans les liens (toutes les pages) : au chargement d'une page dont l'adresse porte un `utm_source`
 *    valide, les liens internes qui mènent à l'accueil (« / », « /#… », « /?profil=…#liste-attente ») reçoivent
 *    `utm_source` et `landing`. `landing` = celui déjà présent dans l'adresse s'il est valide (la première page
 *    d'arrivée l'emporte), sinon le chemin de la page courante. Les paramètres propres au lien (`profil`) restent ;
 *    rien d'autre n'est ajouté. Liens externes et
 *    liens vers d'autres pages : non touchés.
 * 2. Formulaire de la liste d'attente (`form[data-provenance]`, accueil) : à l'envoi, deux champs cachés,
 *    `utm_source` et `landing` (celui de l'adresse s'il est valide, sinon le chemin de la page).
 *
 * Aucun cookie, aucun localStorage ni sessionStorage, aucun Referer, jamais l'adresse complète.
 * Valeur invalide → champ vide (formulaire) ou rien (liens). Sans JS : rien n'est ajouté, le formulaire fonctionne.
 */
(function () {
  'use strict';

  var SOURCE = /^[a-z0-9._-]{1,64}$/;
  var LANDING = /^\/[a-z0-9\/-]{0,63}$/;

  function lire(nom) {
    try {
      return (new URLSearchParams(window.location.search).get(nom) || '').trim();
    } catch (e) {
      return '';
    }
  }

  function source() {
    var s = lire('utm_source').toLowerCase();
    return SOURCE.test(s) ? s : '';
  }

  function chemin(valeur) {
    // « //evil » passerait le motif seul : on refuse aussi toute double barre.
    return LANDING.test(valeur) && valeur.indexOf('//') === -1 ? valeur : '';
  }

  function arrivee() {
    return chemin(lire('landing')) || chemin(window.location.pathname);
  }

  // 0. Profil de la page (CMO 09/11 22:33) : sur une page qui porte <body data-profil="…"> (/familles : « parent »),
  //    les liens vers le formulaire (« /#liste-attente », dont le bouton de l'en-tête commun) présélectionnent ce profil,
  //    comme le bouton du bas. L'en-tête reste identique sur toutes les pages. Sans JS : formulaire sans présélection.
  var profilPage = (document.body && document.body.getAttribute('data-profil')) || '';
  if (/^[a-z]+$/.test(profilPage)) {
    var versFormulaire = document.querySelectorAll('a[href="/#liste-attente"]');
    for (var k = 0; k < versFormulaire.length; k++) {
      versFormulaire[k].setAttribute('href', '/?profil=' + profilPage + '#liste-attente');
    }
  }

  var utm = source();

  // 1. Report dans les liens internes vers l'accueil
  if (utm) {
    var landing = arrivee();
    // Sur l'accueil, `landing` ne figure dans l'adresse que s'il y était déjà (sinon le formulaire prend « / »).
    var qa = new URLSearchParams();
    qa.set('utm_source', utm);
    if (chemin(lire('landing'))) qa.set('landing', chemin(lire('landing')));
    var actuels = new URLSearchParams(window.location.search);
    var n = 0;
    actuels.forEach(function (v, k) { if (k !== 'profil') n++; });
    // L'adresse courante ne porte que nos deux paramètres, valides (quel que soit l'encodage de « / »),
    // plus éventuellement `profil` (présélection du profil, profil.js).
    var accueilPropre = n === Array.from(qa.keys()).length &&
      actuels.get('utm_source') === qa.get('utm_source') &&
      (actuels.get('landing') || '') === (qa.get('landing') || '');
    var liens = document.querySelectorAll('a[href]');
    for (var i = 0; i < liens.length; i++) {
      var a = liens[i];
      var brut = a.getAttribute('href');
      // Ancres de la page (« #contenu », « #liste-attente ») : l'adresse courante est déjà gardée, rien à faire.
      if (brut.charAt(0) === '#') continue;
      var cible;
      try {
        cible = new URL(brut, window.location.href);
      } catch (e) {
        continue;
      }
      if (cible.origin !== window.location.origin || cible.pathname !== '/') continue;
      // Sur l'accueil même, « /#tarifs » doit rester un saut dans la page, sans rechargement :
      // si l'adresse courante est déjà exactement la nôtre, le lien ne garde que l'ancre.
      if (window.location.pathname === '/' && !cible.search && accueilPropre) {
        a.setAttribute('href', window.location.search + cible.hash);
        continue;
      }
      // Les paramètres déjà portés par le lien (ex. « ?profil=aesh ») sont gardés ; seuls les deux nôtres s'ajoutent.
      var q = cible.searchParams;
      q.set('utm_source', utm);
      if (landing && !chemin(q.get('landing') || '')) q.set('landing', landing);
      a.setAttribute('href', '/?' + q.toString() + cible.hash);
    }
  }

  // 2. Champs ajoutés au formulaire de la liste d'attente, à l'envoi
  var form = document.querySelector('form[data-provenance]');
  if (!form) return;

  function champ(nom, valeur) {
    var input = form.querySelector('input[type="hidden"][name="' + nom + '"]');
    if (!input) {
      input = document.createElement('input');
      input.type = 'hidden';
      input.name = nom;
      form.appendChild(input);
    }
    input.value = valeur;
  }

  form.addEventListener('submit', function () {
    champ('utm_source', source());
    champ('landing', arrivee());
  });
})();
