# -*- coding: utf-8 -*-
# compare-pair.py — extrae metricas de calidad de pares duplicados
import os, re

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)))

def metrics(slug):
    p = os.path.join(BASE, 'posts', slug, 'index.html')
    h = open(p, encoding='utf-8', errors='replace').read()
    txt = re.sub(r'<[^>]+>', ' ', re.sub(r'<script[\s\S]*?</script>', ' ', h, flags=re.I))
    palabras = len(txt.split())
    img = len(re.findall(r'<img', h, flags=re.I))
    h2 = len(re.findall(r'<h2', h, flags=re.I))
    h3 = len(re.findall(r'<h3', h, flags=re.I))
    title = re.search(r'<title>([^<]*)</title>', h, flags=re.I)
    return {
        'size': os.path.getsize(p),
        'palabras': palabras,
        'imgs': img, 'h2': h2, 'h3': h3,
        'title': title.group(1)[:90] if title else '?'
    }

print("=== SUELDO MINIMO ===")
for s in ['sueldo-minimo-2026-aumento-s1300-dos-etapas', 'sueldo-minimo-2026-dos-aumentos-rmv-s1300-pymes']:
    m = metrics(s)
    print(f"{s}: {m}")

print("\n=== PAPA LEON XIV ===")
for s in ['papa-leon-xiv-visita-peru-noviembre-2026', 'papa-leon-xiv-peru-agenda-visita-actividades']:
    m = metrics(s)
    print(f"{s}: {m}")
