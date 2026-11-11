"""Pages du site à 390, 820 et 1440 px : console, CSP, requêtes externes, échecs, débordement, police ; une capture par page. Usage : python3 controles/check.py <dossier_captures>"""
import os
BASE=os.environ.get("DOCLIA_BASE","http://127.0.0.1:8787")
import sys
from playwright.sync_api import sync_playwright
OUT=sys.argv[1]  # dossier des captures pleine page
PAGES=["/","/etablissements","/aesh","/merci","/inscription-confirmee","/reponse-enregistree","/demande-envoyee","/demande-erreur","/n-existe-pas","/mentions-legales","/confidentialite","/conditions","/familles","/erreur","/confirmer","/lien-expire"]
pb=0
with sync_playwright() as p:
    b=p.chromium.launch()
    for w in (390,820,1440):
        ctx=b.new_context(viewport={"width":w,"height":900})
        for path in PAGES:
            pg=ctx.new_page(); logs=[]; ext=[]; fails=[]
            pg.on("console", lambda m: logs.append(f"{m.type}: {m.text}") if "_vercel/insights" not in (m.location or {}).get("url","") and "insights/script.js" not in m.text else None)
            pg.on("pageerror", lambda e: logs.append(f"pageerror: {e}"))
            pg.on("request", lambda r: ext.append(r.url) if not r.url.startswith(BASE) else None)
            pg.on("requestfailed", lambda r: fails.append(r.url) if "/_vercel/" not in r.url else None)
            pg.goto(BASE+path, wait_until="networkidle")
            over=pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
            font=pg.evaluate("document.fonts.check('16px Inter') && [...document.fonts].some(f=>f.status==='loaded')")
            bad = logs or ext or fails or over>0 or not font
            if bad: pb+=1
            print(f"{w:>5} {path:<24} console={logs} externes={ext} échecs={fails} débord={over}px police={font}")
            if True:
                name=(path.strip('/') or 'accueil').replace('/','_')
                pg.screenshot(path=f"{OUT}/s0_{name}_{w}.png", full_page=True)
            pg.close()
        ctx.close()
    b.close()
print("PROBLÈMES:", pb)
