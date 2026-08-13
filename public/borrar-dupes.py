# -*- coding: utf-8 -*-
# borrar-dupes.py — borra los 3 duplicados detectados (carpeta + entrada JSON)
import json, os, shutil

BASE = os.path.dirname(os.path.abspath(__file__))

def quitar_de_json(jpath, slug):
    p = os.path.join(BASE, jpath)
    data = json.load(open(p, encoding='utf-8'))
    antes = len(data)
    data = [e for e in data if e.get('slug') != slug]
    json.dump(data, open(p, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
    print(f"  {jpath}: {antes} -> {len(data)} (quitado '{slug}')")

# 1) frank-suarez: quitar entrada de home.json (queda en salud.json, mismo htmlPath)
print("1) DUPLICADO EXACTO: por-que-me-siento-cansado-frank-suarez (home + salud, mismo archivo)")
quitar_de_json('posts/home.json', 'por-que-me-siento-cansado-frank-suarez')

# 2) sueldo minimo batch 1 (duplicado tematico del batch 3)
print("\n2) DUPLICADO TEMATICO: sueldo-minimo-2026-dos-aumentos-rmv-s1300-pymes")
carpeta = os.path.join(BASE, 'posts', 'sueldo-minimo-2026-dos-aumentos-rmv-s1300-pymes')
if os.path.isdir(carpeta):
    shutil.rmtree(carpeta)
    print(f"  carpeta borrada: {carpeta}")
quitar_de_json('posts/gana.json', 'sueldo-minimo-2026-dos-aumentos-rmv-s1300-pymes')

# 3) papa leon xiv batch 1 (duplicado tematico del batch 4)
print("\n3) DUPLICADO TEMATICO: papa-leon-xiv-peru-agenda-visita-actividades")
carpeta = os.path.join(BASE, 'posts', 'papa-leon-xiv-peru-agenda-visita-actividades')
if os.path.isdir(carpeta):
    shutil.rmtree(carpeta)
    print(f"  carpeta borrada: {carpeta}")
quitar_de_json('posts/home.json', 'papa-leon-xiv-peru-agenda-visita-actividades')

print("\nDONE")
