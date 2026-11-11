"""axe-core (WCAG 2.0 à 2.2 A et AA, bonnes pratiques) sur les 16 pages, à 390 px. Usage : python3 controles/axe_run.py <chemin/axe.min.js>"""
import sys
import os
BASE=os.environ.get("DOCLIA_BASE","http://127.0.0.1:8787")
from playwright.sync_api import sync_playwright
AXE=open(sys.argv[1]).read()  # chemin de axe.min.js (npm install axe-core)
PAGES=["/","/etablissements","/aesh","/merci","/inscription-confirmee","/reponse-enregistree","/demande-envoyee","/demande-erreur","/n-existe-pas","/mentions-legales","/confidentialite","/conditions","/familles","/erreur","/confirmer","/lien-expire"]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_context(bypass_csp=True, viewport={"width":390,"height":900}).new_page()
    for path in PAGES:
        pg.goto(BASE+path)
        pg.add_script_tag(content=AXE)  # injection de test, hors CSP du site (bypass dans le contexte de test)
        r=pg.evaluate("axe.run(document,{runOnly:['wcag2a','wcag2aa','wcag21aa','wcag22aa','best-practice']})")
        v=r["violations"]
        print(path, "violations:", len(v))
        for x in v: print("   ", x["id"], x["impact"], len(x["nodes"]), x["nodes"][0]["target"])
    b.close()
