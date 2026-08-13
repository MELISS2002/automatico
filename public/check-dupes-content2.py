# -*- coding: utf-8 -*-
# check-dupes-content2.py — umbral 0.35 para detectar duplicados tematicos
import json, os, re, unicodedata

BASE = os.path.dirname(os.path.abspath(__file__))

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
    return norm(h)

def sim(a, b):
    wa, wb = set(a.split()), set(b.split())
    if not wa or not wb: return 0
    return len(wa & wb) / len(wa | wb)

posts = []
for j in ['posts/home.json', 'posts/salud.json', 'posts/gana.json']:
    data = json.load(open(os.path.join(BASE, j), encoding='utf-8'))
    for e in data:
        slug = e.get('slug', '')
        hp = e.get('htmlPath', '') or f'/posts/{slug}/index.html'
        p = os.path.join(BASE, hp.lstrip('/'))
        posts.append((slug, j, e.get('title', ''), texto_html(p) if os.path.exists(p) else ''))

print(f"{len(posts)} posts\n")
vistos = set()
for i in range(len(posts)):
    for j in range(i + 1, len(posts)):
        a, b = posts[i], posts[j]
        if not a[3] or not b[3]: continue
        ta = ' '.join(a[3].split()[:600])
        tb = ' '.join(b[3].split()[:600])
        s = sim(ta, tb)
        if s >= 0.35:
            key = tuple(sorted([a[0], b[0]]))
            if key in vistos: continue
            vistos.add(key)
            print(f"[{s:.2f}] {a[0]} <=> {b[0]}")
            print(f"    A: {a[2][:75]}")
            print(f"    B: {b[2][:75]}")
