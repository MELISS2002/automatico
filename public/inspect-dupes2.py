# -*- coding: utf-8 -*-
# inspect-dupes2.py — compara pares sospechosos (sueldo minimo, papa)
import json, os, re, unicodedata

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)))
JSONS = ['posts/home.json', 'posts/salud.json', 'posts/gana.json']

# cargar todos
todo = []
for j in JSONS:
    data = json.load(open(os.path.join(BASE, j), encoding='utf-8'))
    for e in data:
        todo.append({**e, '_json': j})

PARES = [
    ('sueldo-minimo-2026-aumento-s1300-dos-etapas', 'sueldo-minimo-2026-dos-aumentos-rmv-s1300-pymes'),
    ('papa-leon-xiv-visita-peru-noviembre-2026', 'papa-leon-xiv-peru-agenda-visita-actividades'),
]

for a, b in PARES:
    print(f"===== {a} vs {b} =====")
    for slug in (a, b):
        # buscar en JSON
        found = [t for t in todo if t.get('slug') == slug]
        if found:
            e = found[0]
            print(f"\n[JSON {e['_json']}] slug={slug}")
            print(f"  title: {e.get('title','')}")
            print(f"  date: {e.get('date','')}")
            print(f"  htmlPath: {e.get('htmlPath','')}")
        else:
            print(f"\n[NO ESTA EN NINGUN JSON] slug={slug}")
        # verificar carpeta
        carpeta = os.path.join(BASE, 'posts', slug)
        idx = os.path.join(carpeta, 'index.html')
        if os.path.exists(idx):
            sz = os.path.getsize(idx)
            print(f"  CARPETA: existe, index.html {sz} bytes")
        else:
            print(f"  CARPETA: NO existe ({carpeta})")
    print()
