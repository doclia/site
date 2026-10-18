#!/usr/bin/env python3
"""Contrôle des marqueurs bloquants (relais, CMO 18/10/2026 18:32) — conditionne S6.

Échoue (code de sortie 1) si une page servie contient encore :
  - « [EN ATTENTE — … » ou « [CONDITIONNEL — … » ;
  - le champ « 06 XX XX XX XX » ;
  - un élément class="marqueur".
Les commentaires HTML sont ignorés (ils ne s'affichent pas). Les fichiers exclus
du déploiement par .vercelignore ne sont pas servis et ne sont pas lus.

Usage : python3 controles/marqueurs.py
Le site ne se publie jamais sur doclia.fr tant que ce contrôle échoue.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
ignores = [l.strip().rstrip("/") for l in (ROOT / ".vercelignore").read_text(encoding="utf-8").splitlines() if l.strip()]

def servi(p: pathlib.Path) -> bool:
    rel = p.relative_to(ROOT).as_posix()
    return not any(rel == i or rel.startswith(i + "/") for i in ignores)

MOTIFS = [
    ("[EN ATTENTE", re.compile(r"\[\s*EN ATTENTE", re.I)),
    ("[CONDITIONNEL", re.compile(r"\[\s*CONDITIONNEL", re.I)),
    ("06 XX XX XX XX", re.compile(r"0\d(?:[\s.]*XX){4}", re.I)),
    ('class="marqueur"', re.compile(r'class="[^"]*\bmarqueur\b')),
]
COMMENTAIRE = re.compile(r"<!--.*?-->", re.S)

trouves = []
for page in sorted(ROOT.rglob("*.html")):
    if not servi(page):
        continue
    html = COMMENTAIRE.sub("", page.read_text(encoding="utf-8"))
    for n, ligne in enumerate(html.splitlines(), 1):
        for nom, rx in MOTIFS:
            if rx.search(ligne):
                trouves.append((page.relative_to(ROOT).as_posix(), nom))

if trouves:
    synthese = {}
    for page, nom in trouves:
        synthese.setdefault(page, {}).setdefault(nom, 0)
        synthese[page][nom] += 1
    print("ÉCHEC — marqueurs bloquants dans des pages servies (S6 impossible) :")
    for page, noms in synthese.items():
        print(f"  {page} : " + ", ".join(f"{k} ×{v}" for k, v in noms.items()))
    sys.exit(1)
print("OK — aucun marqueur bloquant dans les pages servies.")
