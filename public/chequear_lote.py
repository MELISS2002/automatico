# -*- coding: utf-8 -*-
"""chequear_lote.py - verifica los posts del lote_diario.json (imagenes locales, 0 pollinations,
titulos, thumbnails locales, JSON actualizados). No hardcodea slugs, lee el lote.
Uso: python chequear_lote.py  |  python chequear_lote.py --slug abc"""
import os, re, json, sys

HERE = os.path.dirname(os.path.abspath(__file__))
POSTS = os.path.join(os.path.dirname(HERE), "public", "posts")
# POSTS apunta a automatico-main\public\posts (este script vive en public/ o en raiz segun despliegue)
if not os.path.isdir(POSTS):
    # compat: script actual dentro de public/
    POSTS = os.path.join(HERE, "posts")

lote = json.load(open(os.path.join(HERE, "lote_diario.json"), encoding="utf-8"))
solo = None
if "--slug" in sys.argv:
    solo = sys.argv[sys.argv.index("--slug") + 1]

all_ok = True
for art in lote:
    slug = art["slug"]
    if solo and solo not in slug:
        continue
    carpeta = os.path.join(POSTS, slug)
    if not os.path.isdir(carpeta):
        print(f"FAIL {slug}: no existe carpeta")
        all_ok = False
        continue
    hp = os.path.join(carpeta, "index.html")
    if not os.path.isfile(hp):
        print(f"FAIL {slug}: sin index.html (no generado)")
        all_ok = False
        continue
    html = open(hp, encoding="utf-8", errors="replace").read()
    n_poll = len(re.findall(r"pollinations", html, re.I))
    n_refs = len(re.findall(r"imagen[123]\.jpg", html))
    imgs = [f for f in os.listdir(carpeta) if f.endswith((".jpg", ".png", ".jpeg", ".webp"))]
    n_emoji = len(re.findall(r"[\U0001F000-\U0001FAFF\u2600-\u27BF]", html))
    t = re.search(r"<title>(.*?)</title>", html, re.S)
    title = t.group(1).strip() if t else "SIN TITLE"
    srcs = re.findall(r'<img[^>]+src="([^"]+)"', html)
    print(f"\n{slug}")
    print(f"  title: {title[:80]}")
    print(f"  size: {len(html)} | pollinations: {n_poll} | refs imagen*.jpg: {n_refs} | emojis: {n_emoji}")
    print(f"  imgs en carpeta: {sorted(imgs)}")
    print(f"  srcs en HTML: {srcs}")
    if n_poll > 0 or n_emoji > 0 or n_refs < 2 or len(imgs) < 1:
        all_ok = False

# JSON de las categorias del lote
cats = sorted({a["cat"] for a in lote})
for cat in cats:
    jp = os.path.join(POSTS, f"{cat}.json")
    if not os.path.isfile(jp):
        print(f"\nFAIL: falta {cat}.json")
        all_ok = False
        continue
    data = json.load(open(jp, encoding="utf-8"))
    print(f"\n=== {cat}.json (primeros 5) ===")
    for x in data[:5]:
        print(f"  {x['slug'][:45]} | thumb={x['thumbnail'][:55]}")

print("\n" + ("TODO OK" if all_ok else "HAY PROBLEMAS"))