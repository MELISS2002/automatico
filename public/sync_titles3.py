# -*- coding: utf-8 -*-
"""Sincroniza titulos JSON <-> HTML para los posts del batch 3."""
import json, re

slugs = ['sueldo-minimo-2026-aumento-s1300-dos-etapas',
         'como-recuperar-mensajes-borrados-whatsapp-android-iphone',
         'simone-biles-lima-mensaje-salud-mental',
         'pension-onp-bono-edad-avanzada-80-anos',
         'whatsapp-nuevas-funciones-grupos-2026']

changed = 0
for cat_file in ['gana.json', 'home.json', 'salud.json']:
    path = 'posts/' + cat_file
    data = json.load(open(path, encoding='utf-8'))
    for e in data:
        if e['slug'] in slugs:
            html = open('posts/' + e['slug'] + '/index.html', encoding='utf-8', errors='replace').read()
            m = re.search(r'<title>(.*?)</title>', html, re.S)
            html_title = m.group(1).strip() if m else None
            if html_title and e['title'] != html_title:
                print(f'SYNC: {e["slug"][:45]} | JSON="{e["title"][:45]}" -> HTML="{html_title[:45]}"')
                e['title'] = html_title
                changed += 1
    json.dump(data, open(path, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
print(f'Cambios de titulo: {changed}')
