# -*- coding: utf-8 -*-
# check-dupes-content.py — detecta duplicados por SIMILITUD DE CONTENIDO (HTML)
import json, os, re, unicodedata, hashlib

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)))
JSONS = ['posts/home.json', 'posts/salud.json', 'posts/gana.json']

def norm(s):
    s = s.lower()
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
    s = re.sub(r'[^a-z0-9\s]', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()

def texto_html(p):
    try:
        h = open(p, encoding='utf-8', errors='replace').read()
    except Exception:
        return ''
    h = re.sub(r'<script[\s\S]*?</script>', ' ', h, flags=re.I)
    h = re.sub(r'<style[\s\S]*?</style>', ' ', h, flags=re.I)
    h = re.sub(r'<[^>]+>', ' ', h)
    h = re.sub(r'&[a-z]+;', ' ', h)
    return norm(h)

def sim_jaccard(a, b):
    wa, wb = set(a.split()), set(b.split())
    if not wa or not wb: return 0
    return len(wa & wb) / len(wa | wb)

# cargar todos los posts con su contenido
posts = []  # (slug, json, htmlPath, titulo, texto)
for j in JSONS:
    data = json.load(open(os.path.join(BASE, j), encoding='utf-8'))
    for e in data:
        slug = e.get('slug', '')
        hp = e.get('htmlPath', '') or f'/posts/{slug}/index.html'
        p = os.path.join(BASE, hp.lstrip('/'))
        txt = texto_html(p) if os.path.exists(p) else ''
        posts.append((slug, j, hp, e.get('title', ''), txt))

print(f"{len(posts)} posts cargados\n")

# comparar pares por contenido (primeras 2000 palabras normalizadas)
print("=== PARES CON SIMILITUD DE CONTENIDO >= 0.45 ===")
vistos = set()
for i in range(len(posts)):
    for j in range(i + 1, len(posts)):
        a, b = posts[i], posts[j]
        if not a[4] or not b[4]: continue
        # comparar sobre muestras de 800 palabras
        ta = ' '.join(a[4].split()[:800])
        tb = ' '.join(b[4].split()[:800])
        s = sim_jaccard(ta, tb)
        if s >= 0.45:
            key = tuple(sorted([a[0], b[0]]))
            if key in vistos: continue
            vistos.add(key)
            print(f"\n[{s:.2f}] {a[0]} <=> {b[0]}")
            print(f"    A({a[1]}): {a[3][:80]}")
            print(f"    B({b[1]}): {b[3][:80]}")
