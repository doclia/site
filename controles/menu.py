"""En-tête et menu de 320 à 1440 px, menu au clavier et sans JavaScript. Usage : python3 controles/menu.py <dossier_captures>"""
import sys
import os
BASE=os.environ.get("DOCLIA_BASE","http://127.0.0.1:8787")
from playwright.sync_api import sync_playwright
B=BASE; S=sys.argv[1]  # dossier des captures du menu
with sync_playwright() as p:
    b=p.chromium.launch()
    for w in (320,390,820,1023,1024,1087,1088,1184,1280,1440):
        pg=b.new_page(viewport={"width":w,"height":844}); errs=[]
        pg.on("console", lambda m: errs.append(m.text) if m.type=="error" else None)
        pg.goto(B+"/")
        r=pg.evaluate("""()=>{const q=s=>{const e=document.querySelector(s);const r=e.getBoundingClientRect();return [Math.round(r.width),Math.round(r.height), getComputedStyle(e).display!=='none' && r.width>0]};
          return {hdr:Math.round(document.querySelector('.site-header').getBoundingClientRect().height),logo:q('.site-header__logo img'),
          menu:q('.menu'),liste:q('.site-nav__list'),cta:q('.site-header__cta .btn'),label:document.querySelector('.site-header__cta .btn').innerText,
          over:document.documentElement.scrollWidth-document.documentElement.clientWidth}}""")
        print(w, r, errs)
        if w==390:
            pg.screenshot(path=f"{S}/m390_ferme.png", clip={"x":0,"y":0,"width":390,"height":844})
            pg.click(".menu__toggle"); pg.wait_for_timeout(200)
            print("  ouvert:", pg.evaluate("document.querySelector('.menu').open"), "liens visibles:", pg.evaluate("[...document.querySelectorAll('.menu__panel a')].filter(a=>a.getBoundingClientRect().height>0).map(a=>a.innerText)"))
            pg.screenshot(path=f"{S}/m390_ouvert.png", clip={"x":0,"y":0,"width":390,"height":844})
            pg.click(".menu__panel a[href='/#tarifs']"); pg.wait_for_timeout(500)
            top=pg.evaluate("document.getElementById('tarifs').getBoundingClientRect().top")
            print("  après clic Tarifs: ouvert=", pg.evaluate("document.querySelector('.menu').open"), "titre Tarifs à", round(top),"px du haut")
            # clavier
            pg.goto(B+"/"); pg.keyboard.press("Tab"); pg.keyboard.press("Tab"); pg.keyboard.press("Tab")
            print("  3e tab:", pg.evaluate("document.activeElement.className"))
            pg.keyboard.press("Enter"); print("  Entrée → ouvert:", pg.evaluate("document.querySelector('.menu').open"))
            pg.keyboard.press("Tab"); print("  tab suivant:", pg.evaluate("document.activeElement.innerText"))
            pg.keyboard.press("Escape"); print("  Échap → ouvert:", pg.evaluate("document.querySelector('.menu').open"), "focus:", pg.evaluate("document.activeElement.className"))
        pg.close()
    # sans JavaScript
    ctx=b.new_context(java_script_enabled=False, viewport={"width":390,"height":844}); pg=ctx.new_page(); pg.goto(B+"/")
    pg.click(".menu__toggle"); print("sans JS, ouvert:", pg.evaluate("1") if False else pg.locator(".menu__panel a").first.is_visible())
    pg.click(".menu__panel a[href='/etablissements']"); pg.wait_for_load_state(); print("sans JS, lien Établissements →", pg.url)
    b.close()
