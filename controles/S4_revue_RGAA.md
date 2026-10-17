# S4 — Accessibilité et performance : revue critère par critère
**DEV-Site — 17/10/2026 — référence : brief DEV-Site §2.9 et §4 (S4), RGAA 4.1.**
Doclia est conçu pour être accessible et vise la conformité au RGAA ; il n'a pas encore fait l'objet d'un audit. Ce document est une revue interne, pas une déclaration de conformité.

Outils (tous locaux, aucun service tiers) : serveur statique appliquant `vercel.json` ; Chromium sans tête ; axe-core 4 (WCAG 2.2 A/AA + bonnes pratiques) ; Lighthouse 12 ; scripts de contrôle (contraste calculé, reflux, clavier, titres, espacement).

| Thème RGAA | Critère (brief §2.9 / S4) | Constat | État |
|---|---|---|---|
| 1. Images | `alt` sur chaque image (1.1) ; décoratives en `alt=""` (1.2) | 0 image sans `alt` sur 8 pages. Logo : « Doclia — accueil ». IMG-1 à 4 et portrait : `alt` validés CMO. Pictogrammes et zones IMG-6/7 : décoratifs ou provisoires (`alt=""`) ; IMG-6/7 à rédiger à l'arrivée des captures. | OK (IMG-6/7 ouvert) |
| 3. Couleurs | Information jamais par la couleur seule (3.1) | Liens soulignés ; états de formulaire natifs ; aucune information portée par la seule couleur. | OK |
| 3. Couleurs | Contraste texte ≥ 4,5:1 (3.2) | Texte 13,45 ; secondaire 5,49 (5,25 sur fond clair) ; menthe texte `#1F7F7A` 4,80 ; bleu/blanc et blanc/bleu 8,90 ; © sur bleu 8,05. axe et Lighthouse : 0 défaut. | OK |
| 3. Couleurs | Contraste des composants ≥ 3:1 (3.3) | **Corrigé en S4** : bordure du champ e-mail 1,73 → 5,49 (`#5E6B73`). Anneau de focus 4,80. | OK |
| 6. Liens | Liens explicites hors contexte (6.1) | Libellés explicites (« Voir la page Établissements », « Revenir au formulaire », « politique de confidentialité ») ; aucun « cliquez ici ». | OK |
| 8. Éléments obligatoires | `lang="fr"` (8.3), titre de page pertinent (8.5-8.6) | `lang="fr"` partout ; titres d'onglet distincts « <titre> — Doclia ». | OK |
| 9. Structuration | Hiérarchie de titres (9.1) | Un `h1` par page, aucun saut de niveau (8 pages). Repères `header`, `nav` nommée, `main`, `footer`. | OK |
| 10. Présentation | Zoom 200 % sans perte ni défilement horizontal (10.4, 10.11) | Aucun débordement à 1280, 640 (= 200 %) et 320 px (= 400 %), 8 pages. Zoom non verrouillé (`width=device-width, initial-scale=1`). En-tête non collant sur écran bas. | OK |
| 10. Présentation | Espacement du texte (10.12) | Surcharge WCAG 1.4.12 injectée à 390 et 1280 px : aucun débordement, aucun texte rogné. | OK |
| 10. Présentation | Focus visible (10.7) | Anneau de 3 px `#1F7F7A` ; vérifié sur chaque élément focusable des 8 pages (clair sur bleu dans le pied de page). | OK |
| 11. Formulaires | Champs étiquetés (11.1-11.2), regroupés (11.5-11.6), obligatoires signalés (11.10) | `label` pour chaque champ ; profil en `fieldset`/`legend` ; ligne « Tous les champs sont obligatoires… » + `required` ; `autocomplete="email"` (11.13). | OK |
| 11. Formulaires | Erreurs annoncées en texte (11.10-11.11) | Avant envoi : messages natifs du navigateur, en texte. Après envoi : page `/erreur` (texte explicite). Parcours réel vérifié en S3. | OK, à revérifier S3 |
| 12. Navigation | Lien d'évitement (12.7), navigation clavier complète, ordre logique (12.8) | « Aller au contenu » en premier tab, mène à `main`. Tab : tous les éléments atteints dans l'ordre du document sur 8 pages (liens des volets FAQ fermés atteints une fois le volet ouvert). Volets FAQ ouvrables à Entrée. Piège à robots hors tabulation. | OK |
| 13. Consultation | Mouvement réduit (13.8) | Aucune animation sur le site ; règle `prefers-reduced-motion` présente pour toute animation future. | OK |
| — | Cibles tactiles ≥ 48 px (charte §8) | Boutons, liens de navigation, choix du formulaire, liens du pied : `min-height: 48px`. | OK |

## Lighthouse (local, hôte `doclia.fr` simulé pour lever le `noindex`)
| Page | Mobile (Perf / Acc / BP / SEO) | Ordinateur |
|---|---|---|
| `/` | 100 / 100 / 100 / 100 | 100 / 100 / 100 / 100 |
| `/etablissements` | 100 / 100 / 100 / **91** | 100 / 100 / 100 / **91** |
| `/merci`, `/inscription-confirmee`, `/erreur`, `/mentions-legales`, `/confidentialite` | 100 / 100 / 100 / **91** | idem |
| 404 | non évaluable (Lighthouse refuse un statut 404, attendu) | — |

Seul audit en échec : **méta-description absente** des pages secondaires (texte non fourni). Captures des rapports : `controles/s4/lighthouse_*.png`.
Poids de la page principale avec ses ressources : 115 Ko (images provisoires) ; LCP mobile 1,7 s, CLS 0, TBT 0 ms.
