#!/usr/bin/env python3
"""Contrôle avant commit (brief DEV-Site §2.3, §2.6, §2.7).

- En-tête et pied de page strictement identiques sur toutes les pages.
- Aucun <style>, aucun <script> en ligne, aucun attribut style= ni on…= (CSP sans 'unsafe-inline').
- lang="fr", <title> non vide, un seul <h1>, <main id="contenu">.
- Aucune ressource externe chargée (src=/href= de feuille, script, image, police hors du site).

Usage : python3 outils/verifier.py   (code de sortie 1 en cas d'écart)
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = ["index.html", "etablissements.html", "aesh.html", "merci.html", "inscription-confirmee.html", "reponse-enregistree.html", "demande-envoyee.html", "demande-erreur.html",
         "404.html", "mentions-legales.html", "confidentialite.html", "erreur.html", "confirmer.html", "lien-expire.html"]
BLOCS = {
    "en-tête": re.compile(r'<a class="skip-link".*?<!-- FIN EN-TÊTE -->', re.S),
    "pied de page": re.compile(r'<!-- PIED DE PAGE.*?<!-- FIN PIED DE PAGE -->', re.S),
}
erreurs = []
reference = {}
for nom in PAGES:
    p = ROOT / nom
    if not p.exists():
        erreurs.append(f"{nom} : page absente"); continue
    html = p.read_text(encoding="utf-8")
    for bloc, rx in BLOCS.items():
        m = rx.search(html)
        if not m:
            erreurs.append(f"{nom} : {bloc} introuvable"); continue
        reference.setdefault(bloc, (nom, m.group(0)))
        if m.group(0) != reference[bloc][1]:
            erreurs.append(f"{nom} : {bloc} différent de {reference[bloc][0]}")
    # Typographie française (CMO 18/10 19:37) : espace fine insécable U+202F avant : ; ? ! et dans « », jamais une espace ordinaire ;
    # apostrophe typographique (CEO 18/10 16:59). Texte visible et attributs alt/content/aria-label/title seulement.
    visible = re.sub(r"<!--.*?-->|<script\b.*?</script>|<style\b.*?</style>", "", html, flags=re.S)
    textes = re.sub(r"<[^>]+>", "\n", visible)
    textes += "\n" + "\n".join(re.findall(r'\s(?:alt|content|aria-label|title)="([^"]*)"', visible))
    for motif, quoi in ((r"[ \u00a0][:;?!»]", "espace ordinaire avant : ; ? ! ou »"), (r"«[ \u00a0]", "espace ordinaire après «"), (r"[A-Za-zÀ-ÿ]'[A-Za-zÀ-ÿ]", "apostrophe droite")):
        for m in re.finditer(motif, textes):
            erreurs.append(f"{nom} : {quoi} — « {textes[max(0,m.start()-25):m.end()+5].strip()} »")
    if re.search(r"<style\b", html, re.I): erreurs.append(f"{nom} : balise <style>")
    for s in re.findall(r"<script\b[^>]*>", html, re.I):
        if "src=" not in s: erreurs.append(f"{nom} : script en ligne")
    if re.search(r"\sstyle\s*=", html, re.I): erreurs.append(f"{nom} : attribut style=")
    if re.search(r"\son[a-z]+\s*=", html, re.I): erreurs.append(f"{nom} : attribut on…=")
    if '<html lang="fr">' not in html: erreurs.append(f"{nom} : lang=\"fr\" absent")
    t = re.search(r"<title>(.*?)</title>", html, re.S)
    if not t or not t.group(1).strip(): erreurs.append(f"{nom} : <title> vide")
    if len(re.findall(r"<h1\b", html)) != 1: erreurs.append(f"{nom} : il faut exactement un <h1>")
    if '<main id="contenu"' not in html: erreurs.append(f"{nom} : <main id=\"contenu\"> absent")
    for tag in re.findall(r"<(?:script|img|link|source|iframe|video|audio)\b[^>]*>", html, re.I):
        for url in re.findall(r'(?:src|href)="([^"]+)"', tag):
            if re.match(r"(https?:)?//", url): erreurs.append(f"{nom} : ressource externe {url}")
for css in ROOT.glob("assets/css/*.css"):
    for url in re.findall(r"url\(([^)]+)\)", css.read_text(encoding="utf-8")):
        if re.match(r"['\"]?(https?:)?//", url): erreurs.append(f"{css.name} : ressource externe {url}")
    if "@import" in css.read_text(encoding="utf-8"): erreurs.append(f"{css.name} : @import")
if erreurs:
    print("ÉCARTS :"); [print(" -", e) for e in erreurs]; sys.exit(1)
print(f"OK — {len(PAGES)} pages, en-tête et pied de page identiques, aucune ressource externe ni code en ligne.")
