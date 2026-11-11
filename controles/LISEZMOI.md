# Contrôles du site — à lancer avant chaque commit

Ces scripts ne sont pas servis : `.vercelignore` exclut le dossier `controles/` du déploiement. Ils ont été écrits par DEV-Site n° 1 et versés ici le 11/11/2026, avec l'accord du CTO (Relais du site, 11/11 17:29).

## Installer

- Python 3 et Playwright pour Python, avec Chromium (`pip install playwright`, puis `playwright install chromium` si le navigateur manque).
- Pour axe-core, dans un dossier hors du dépôt : `npm install axe-core`, puis donner le chemin de `node_modules/axe-core/axe.min.js`.
- L'adresse testée est `http://127.0.0.1:8787` par défaut. La variable `DOCLIA_BASE` la change.

## Ordre et commandes (depuis la racine du dépôt)

| Script | Commande | Ce qu'il prouve |
|---|---|---|
| `serve.py` | `python3 -I controles/serve.py . 8787` (en arrière-plan) | Le site servi comme sur Vercel : adresses sans `.html`, page 404, en-têtes et CSP lus dans `vercel.json`. **Contrôle bloquant : il doit répondre 200.** |
| `../outils/verifier.py` | `python3 outils/verifier.py` | 16 pages, en-tête et pied identiques, aucun code en ligne, aucune ressource externe, aucune entité HTML cassée. |
| `marqueurs.py` | `python3 controles/marqueurs.py` | Aucun marqueur bloquant dans les pages servies. |
| `check.py` | `python3 controles/check.py <dossier>` | À 390, 820 et 1440 px : console vide (CSP comprise), aucune requête externe, aucun échec, débordement nul, police chargée. Une capture pleine page par page. « PROBLÈMES: 3 » est normal : ce sont les trois largeurs de `/n-existe-pas`, qui répond 404 exprès. |
| `axe_run.py` | `python3 controles/axe_run.py <axe.min.js>` | axe-core (WCAG 2.0 à 2.2, A et AA, bonnes pratiques) sur les 16 pages : 0 violation attendue. |
| `spacing.py` | `python3 controles/spacing.py` | Espacement du texte agrandi (WCAG 1.4.12) : aucun débordement, aucun texte rogné. |
| `clavier.py` | `python3 controles/clavier.py` | Touche Tab sur l'accueil, `/aesh` et `/etablissements` : ordre croissant, éléments atteints, anneau de focus. Écarts connus : le lecteur vidéo n'a pas d'anneau propre, et `/etablissements` compte des champs cachés tant que le formulaire de rappel est fermé. |
| `menu.py` | `python3 controles/menu.py <dossier>` | En-tête et menu de 320 à 1440 px, menu au clavier (Entrée, Échap) et sans JavaScript. |
| `empreinte_legales.py` | `python3 controles/empreinte_legales.py <chemin>/docs/Doclia_Pages_Legales_Application.md` | Le texte de `/conditions` et de `/confidentialite` est identique à la source du COS (hors date) ; sinon, il affiche le premier écart. |

## Captures

Elles se rangent dans `captures/<sujet>/`, à 390 et à 1440 px.
