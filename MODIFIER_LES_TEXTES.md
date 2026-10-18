# Modifier un texte du site, sans développeur

1. **Où est le texte** : une page = un fichier HTML à la racine (`index.html` = page principale, `etablissements.html`, `merci.html`, `inscription-confirmee.html`, `404.html`, `mentions-legales.html`, `confidentialite.html`, `erreur.html`). L'en-tête et le pied de page sont recopiés dans chaque fichier : un changement s'y fait dans les huit. Dans l'en-tête, les cinq liens de navigation figurent deux fois (liste pour ordinateur, menu replié pour mobile) : changer les deux.
2. **Repérer le bloc** : chaque texte est précédé d'un commentaire `<!-- Texte 4.1 — … -->` qui porte le numéro de section de `docs/Doclia_Site_Textes_V1.md`. Chercher ce numéro avec Ctrl+F.
3. **Modifier sur github.com** : ouvrir le fichier, cliquer sur le crayon (« Edit this file »), changer uniquement le texte entre les balises, sans toucher aux `<…>`.
4. **Enregistrer** : « Commit changes… », choisir **« Create a new branch… and start a pull request »**, puis « Propose changes » et « Create pull request ».
5. **Voir l'aperçu** : dans la demande de fusion, Vercel publie en une minute un lien « Preview » : le site modifié, non indexé.
6. **Publier** : si l'aperçu convient, « Merge pull request ». La fusion sur `main` publie le site.
7. **Ensuite** : le CMO reporte le texte modifié dans `Doclia_Site_Textes_V1.md` (le site fait foi, pas l'inverse).
8. Un doute, une balise cassée : ne pas fusionner, le signaler au relais `docs/Doclia_Site_Relais.md`.
