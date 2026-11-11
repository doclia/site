"""Parcours à la touche Tab : ordre, éléments atteints, anneau de focus visible. Usage : python3 controles/clavier.py"""
import os
BASE=os.environ.get("DOCLIA_BASE","http://127.0.0.1:8787")
from playwright.sync_api import sync_playwright
B=BASE
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={"width":1280,"height":800})
    for path in ["/","/aesh","/etablissements"]:
        pg.goto(B+path)
        n=pg.evaluate("""()=>{const els=[...document.querySelectorAll('a[href],button,input:not([type=hidden]),summary,video[controls],select,textarea')].filter(e=>e.tabIndex>=0 && !e.closest('[aria-hidden=true]')&&e.getClientRects().length);
           els.forEach((e,i)=>e.dataset.k=i); return els.length}""")
        order=[];stray=[];noring=[]
        for i in range(n+6):
            pg.keyboard.press("Tab")
            r=pg.evaluate("""()=>{const e=document.activeElement;const s=getComputedStyle(e);return [e.dataset.k??null,e.tagName+'.'+e.className,(s.outlineStyle!=='none'&&parseFloat(s.outlineWidth)>=2)||s.boxShadow!=='none']}""")
            if r[0] is None:
                if r[1].startswith('BODY'): break
                stray.append(r[1]); continue
            order.append(int(r[0]))
            if not r[2]: noring.append(r[1])
        radios=pg.evaluate("document.querySelectorAll('input[type=radio]').length")
        print(path,"focusables",n,"atteints",len(set(order)),"attendu",n-(radios-1 if radios else 0),"croissant",order==sorted(order),"hors liste",stray,"sans anneau",noring)
    b.close()
