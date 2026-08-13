# -*- coding: utf-8 -*-
# check-dupes.py — detecta articulos duplicados en home.json / salud.json / gana.json
# Criterios: slug duplicado, titulo normalizado duplicado, o titulo casi identico (similitud > 0.85)
import json, re, unicodedata, os

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)))
JSONS = ['posts/home.json', 'posts/salud.json', 'posts/gana.json']

def norm(s):
    s = s.lower()
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
    s = re.sub(r'[^a-z0-9\s]', '', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def sim(a, b):
    # Jaccard de palabras
    wa, wb = set(a.split()), set(b.split())
    if not wa or not wb: return 0
    return len(wa & wb) / len(wa | wb)

todo = []  # (cat, slug, titulo_norm, titulo_orig)
for j in JSONS:
    p = os.path.join(BASE, j)
    if not os.path.exists(p):
        print(f"NO EXISTE: {j}")
        continue
    data = json.load(open(p, encoding='utf-8'))
    print(f"{j}: {len(data)} articulos")
    for e in data:
        slug = e.get('slug', '')
        tit = e.get('title', '') or e.get('titulo', '') or ''
        todo.append((j, slug, norm(tit), tit))

print(f"\nTotal: {len(todo)} articulos\n")

# 1) slugs duplicados
from collections import Counter
slugs = Counter(t[1] for t in todo)
print("=== SLUGS DUPLICADOS ===")
dup_slugs = {s: c for s, c in slugs.items() if c > 1}
if dup_slugs:
    for s, c in dup_slugs.items():
        print(f"  [{c}x] {s}")
        for t in todo:
            if t[1] == s: print(f"    -> {t[0]}")
else:
    print("  ninguno")

# 2) titulos normalizados duplicados exactos
print("\n=== TITULOS NORMALIZADOS DUPLICADOS (exactos) ===")
tn = Counter(t[2] for t in todo if t[2])
dup_tn = {s: c for s, c in tn.items() if c > 1}
if dup_tn:
    for s, c in dup_tn.items():
        print(f"  [{c}x] {s}")
        for t in todo:
            if t[2] == s: print(f"    -> {t[0]} | {t[1]} | {t[3][:60]}")
else:
    print("  ninguno")

# 3) similitud alta entre pares (mismo tema, titulo distinto)
print("\n=== PARES CON SIMILITUD ALTA (>= 0.70) ===")
vistos = set()
for i in range(len(todo)):
    for j in range(i + 1, len(todo)):
        a, b = todo[i], todo[j]
        if not a[2] or not b[2]: continue
        s = sim(a[2], b[2])
        if s >= 0.70:
            key = tuple(sorted([a[1], b[1]]))
            if key in vistos: continue
            vistos.add(key)
            print(f"  [{s:.2f}] {a[1]} <=> {b[1]}")
            print(f"      A: {a[3][:90]}")
            print(f"      B: {b[3][:90]}")
