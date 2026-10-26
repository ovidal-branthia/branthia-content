#!/usr/bin/env python3
"""Visuales de Branthia (estilo branthia.com: Satoshi 900 + JetBrains Mono, papel #F1ECE2).

Uso: python3 render.py piezas.json out/

Tarjeta: {"id","tipo":"tarjeta","section":"§ II","label":"Criterio","meta":"MMXXVI — 06",
          "quote":"Texto con <q>parte gris</q>","sub":"opcional, con <b>énfasis</b>","dark":false}
Carrusel: {"id","tipo":"carrusel","section","label","pages":[{"kind":"cover","text","sub"},
          {"kind":"point","n":"01","title","body"},{"kind":"end","text"}]}
"""
import json, sys, pathlib, html, re
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).parent
CSS = (ROOT / "templates" / "base.css").resolve().as_uri()
# base.css referencia ../fonts/, relativo a templates/
LOGO = (ROOT / "fonts" / "logo.svg").read_text().replace("<svg ", '<svg class="logo" ', 1)

def esc(s):
    s = html.escape(s or "")
    for t in ("q", "b"):
        s = s.replace(f"&lt;{t}&gt;", f'<span class="{t}">' if t == "q" else "<b>").replace(f"&lt;/{t}&gt;", "</span>" if t == "q" else "</b>")
    return s

def size(text, big, mid, small):
    n = len(re.sub(r"<[^>]+>", "", text))
    return big if n <= 34 else mid if n <= 70 else small

def doc(body, dark=False):
    return f'<!doctype html><html lang="es"><head><meta charset="utf-8"><link rel="stylesheet" href="{CSS}"></head><body class="{"dark" if dark else ""}">{body}</body></html>'

def top(section, label, right):
    return f'<div class="top mono"><span>{esc(section)}</span><span>{esc(label)}</span><span>{esc(right)}</span></div><div class="rule"></div>'

def bottom(right="branthia.com"):
    return f'<div class="bottom">{LOGO}<span class="mono">{esc(right)}</span></div>'

def tarjeta(item):
    fs = size(item["quote"], 132, 104, 84)
    sub = f'<p class="sub">{esc(item["sub"])}</p>' if item.get("sub") else ""
    body = f'<div class="page" style="width:1080px;height:1080px">{top(item.get("section","§"), item.get("label",""), item.get("meta","MMXXVI"))}<div class="mid"><p class="h" style="font-size:{fs}px">{esc(item["quote"])}</p>{sub}</div>{bottom()}</div>'
    return doc(body, item.get("dark", False))

def pantalla(item):
    """Captura enmarcada. item: section, label, meta, img (ruta local o URL), caption."""
    img = item["img"]
    if not re.match(r"^https?://", img):
        img = (pathlib.Path(img).resolve()).as_uri()
    cap = f'<p class="h" style="font-size:{size(item["caption"],72,60,52)}px;margin-top:40px">{esc(item["caption"])}</p>'
    shot = f'<div style="flex:1;display:flex;align-items:center;justify-content:center;min-height:0;margin-top:40px"><img src="{img}" style="max-width:100%;max-height:100%;border-radius:8px;box-shadow:0 8px 32px rgba(10,10,10,.14);object-fit:contain"></div>'
    body = f'<div class="page" style="width:1080px;height:1080px">{top(item.get("section","§ I"), item.get("label","Construido"), item.get("meta",""))}{shot}{cap}<div style="height:40px"></div>{bottom()}</div>'
    return doc(body, item.get("dark", False))

def carrusel(item):
    pages, total = [], len(item["pages"])
    for i, p in enumerate(item["pages"], 1):
        num = f"{i:02d} / {total:02d}"
        dark = p["kind"] in ("cover", "end") and item.get("dark_ends", True)
        cls = "page dark" if dark else "page"
        if p["kind"] == "point":
            mid = f'<div class="mid"><p class="h" style="font-size:200px;margin-bottom:48px">{esc(p["n"])}</p><p class="h" style="font-size:{size(p["title"],96,80,68)}px">{esc(p["title"])}</p><p class="sub">{esc(p.get("body",""))}</p></div>'
        else:
            sub = f'<p class="sub">{esc(p["sub"])}</p>' if p.get("sub") else ""
            mid = f'<div class="mid"><p class="h" style="font-size:{size(p["text"],140,112,92)}px">{esc(p["text"])}</p>{sub}</div>'
        pages.append(f'<section class="{cls}" style="width:1080px;height:1350px;break-after:page">{top(item["section"], item["label"], num)}{mid}{bottom()}</section>')
    return doc("".join(pages))

def main():
    src, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page()
        for it in json.loads(src.read_text()):
            f = out / f'{it["id"]}-{it["tipo"]}.html'
            if it["tipo"] in ("tarjeta", "pantalla"):
                f.write_text(tarjeta(it) if it["tipo"] == "tarjeta" else pantalla(it)); pg.set_viewport_size({"width":1080,"height":1080})
                pg.goto(f.resolve().as_uri()); pg.evaluate("document.fonts.ready")
                pg.screenshot(path=str(f.with_suffix(".png")))
            else:
                f.write_text(carrusel(it)); pg.set_viewport_size({"width":1080,"height":1350})
                pg.goto(f.resolve().as_uri()); pg.evaluate("document.fonts.ready")
                pg.pdf(path=str(f.with_suffix(".pdf")), width="1080px", height="1350px", print_background=True)
                n = len(it["pages"])
                for i in range(n):
                    pg.screenshot(path=str(out / f'{it["id"]}-carrusel-{i+1:02d}.png'), full_page=True, clip={"x":0,"y":1350*i,"width":1080,"height":1350})
            print(f.stem)
        b.close()

if __name__ == "__main__":
    main()
