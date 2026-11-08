/*
 * Provenance de l'inscription à la liste d'attente (CTO n° 8, 08/11/2026 19:34 ; demande du CMO, 06/11 ; règle 6 du COS).
 * À l'envoi du formulaire seulement : `utm_source` lu dans l'adresse de la page et le chemin de la page,
 * ajoutés au formulaire en deux champs cachés, `utm_source` et `landing`.
 * Aucun cookie, aucun localStorage ni sessionStorage, aucun Referer, jamais l'adresse complète.
 * Une valeur hors de [a-z0-9._-]{1,64} part vide : rien de saisi par un tiers dans l'adresse
 * (une adresse e-mail, un nom) ne doit atteindre la base.
 * Sans JS, le formulaire fonctionne et n'envoie pas ces champs.
 */
(function () {
  'use strict';
  var form = document.querySelector('form[data-provenance]');
  if (!form) return;

  function propre(valeur, motif) {
    return motif.test(valeur) ? valeur : '';
  }

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
    var source = '';
    try {
      source = (new URLSearchParams(window.location.search).get('utm_source') || '').trim().toLowerCase();
    } catch (e) {
      source = '';
    }
    champ('utm_source', propre(source, /^[a-z0-9._-]{1,64}$/));
    champ('landing', propre(window.location.pathname, /^\/[a-z0-9\/_-]{0,63}$/));
  });
})();
