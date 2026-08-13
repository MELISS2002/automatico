# -*- coding: utf-8 -*-
# check-dupes-temas.py — busca duplicados tematicos por palabras clave de slug
import json, os, re
from collections import defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))
JSONS = ['posts/home.json', 'posts/salud.json', 'posts/gana.json']

posts = []
for j in JSONS:
    data = json.load(open(os.path.join(BASE, j), encoding='utf-8'))
    for e in data:
        posts.append((e.get('slug', ''), j, e.get('title', ''), e.get('date', '')))

# palabras clave del slug (3+ letras, sin stopwords)
STOP = set('de la el los las y o u a al del en un una unos unas con sin por para que es no si ya se su sus como mas muy entre sobre tambien tras contra desde hasta durante ante segun este esta estos estas ese esa esos sus les lo le e i ni pero aunque cual cuales quien cuyo donde cuando cuanto que quienes como cuando cuanto cuantas cuantos'.split())

grupos = defaultdict(list)
for slug, j, t, d in posts:
    palabras = [w for w in slug.split('-') if len(w) > 3 and w not in STOP and not w.isdigit()]
    for p in set(palabras):
        grupos[p].append((slug, j, t, d))

print("=== PALABRAS CLAVE CON >1 POST (posibles duplicados tematicos) ===")
for kw, items in sorted(grupos.items()):
    if len(items) > 1:
        print(f"\n[{kw}] {len(items)} posts:")
        for slug, j, t, d in items:
            print(f"  {d} | {j} | {slug}")
            print(f"      {t[:85]}")
