# -*- coding: utf-8 -*-
# inspect-dupe.py — compara los 2 entries del slug duplicado y verifica carpetas
import json, os

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)))
SLUG = 'por-que-me-siento-cansado-frank-suarez'

for j in ['posts/home.json', 'posts/salud.json']:
    data = json.load(open(os.path.join(BASE, j), encoding='utf-8'))
    for e in data:
        if e.get('slug') == SLUG:
            print(f"--- {j} ---")
            for k, v in e.items():
                print(f"  {k}: {str(v)[:120]}")
            print()

# carpetas existentes
print("CARPETAS EN posts/:", len(os.listdir(os.path.join(BASE, 'posts'))))
for d in sorted(os.listdir(os.path.join(BASE, 'posts'))):
    if os.path.isdir(os.path.join(BASE, 'posts', d)):
        print(" ", d)
