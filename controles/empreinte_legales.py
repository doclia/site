"""Empreinte du texte de /conditions et /confidentialite comparée à la source du COS. Usage : python3 controles/empreinte_legales.py <Doclia_Pages_Legales_Application.md> [adresse]"""
import re, hashlib, pathlib, sys
from playwright.sync_api import sync_playwright
SRC = pathlib.Path(sys.argv[1]).read_text()  # docs/Doclia_Pages_Legales_Application.md du dépôt doclia/doclia
def norm(s):
    s = s.replace("’","'").replace(" "," ").replace(" "," ")
    s = re.sub(r"Dernière mise à jour ?: ?[^\n]*", "", s)
    s = re.sub(r"^>\s?", "", s, flags=re.M)
    s = re.sub(r"^\s*- ", " ", s, flags=re.M)
    s = re.sub(r"[*#]", "", s)
    return re.sub(r"\s+", " ", s).strip()
def src(title):
    s = SRC.index(title); s = SRC.index("\n", s)+1; e = SRC.index("\n---", s); return SRC[s:e]
base = sys.argv[2] if len(sys.argv)>2 else "http://127.0.0.1:8787"
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    for path, t in [("/conditions","## Texte 1 — `/conditions`"),("/confidentialite","## Texte 2 — `/confidentialite`")]:
        pg.goto(base+path); txt = pg.inner_text("main")
        a, c = norm(src(t)), norm(txt)
        print(path, "source", hashlib.sha256(a.encode()).hexdigest()[:16], "publié", hashlib.sha256(c.encode()).hexdigest()[:16], "identiques" if a==c else "DIFFÉRENTS")
        if a!=c:
            import difflib
            for i,(x,y) in enumerate(zip(a,c)):
                if x!=y: print("  écart:", repr(a[max(0,i-60):i+60]), "|", repr(c[max(0,i-60):i+60])); break
    b.close()
