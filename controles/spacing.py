"""Espacement du texte agrandi (WCAG 1.4.12) à 390 et 1280 px : débordement et textes rognés. Usage : python3 controles/spacing.py"""
import os
BASE=os.environ.get("DOCLIA_BASE","http://127.0.0.1:8787")
from playwright.sync_api import sync_playwright
B=BASE
with sync_playwright() as p:
    b=p.chromium.launch()
    for w in (390,1280):
        ctx=b.new_context(bypass_csp=True, viewport={"width":w,"height":800}); pg=ctx.new_page()
        for path in ["/","/etablissements","/aesh","/erreur","/inscription-confirmee","/reponse-enregistree","/demande-envoyee","/demande-erreur","/conditions","/familles","/confidentialite","/mentions-legales"]:
            pg.goto(B+path)
            pg.add_style_tag(content="*{line-height:1.5!important;letter-spacing:.12em!important;word-spacing:.16em!important}p{margin-bottom:2em!important}")
            o=pg.evaluate("document.documentElement.scrollWidth-document.documentElement.clientWidth")
            clip=pg.evaluate("""()=>[...document.querySelectorAll('a,button,label,summary,h1,h2,h3,p,li')].filter(e=>e.scrollWidth>e.clientWidth+1 && getComputedStyle(e).overflow!=='visible' && !e.closest('.site-nav') && !e.classList.contains('visually-hidden')).length""")
            print(w,path,"débord",o,"textes rognés",clip)
        ctx.close()
    b.close()
