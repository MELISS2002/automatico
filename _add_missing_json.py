# -*- coding: utf-8 -*-
# Agrega a salud.json los 2 posts que faltan (new-hope-for-breast-cancer-patients, genetic-risk-for-ptsd-may-vary)
import json, io, re, os, sys, unicodedata

out = []
SALUD = 'public/posts/salud.json'
data = json.load(io.open(SALUD, encoding='utf-8'))
slugs = set(x.get('slug') for x in data)

PAIRS = [
    ('new-hope-for-breast-cancer-patients', 'Enhertu llega al NHS de Inglaterra: nueva esperanza para pacientes con cáncer de mama', 'salud'),
    ('genetic-risk-for-ptsd-may-vary', 'El riesgo genético de TEPT varía según el tipo de trauma, según un estudio', 'salud'),
]

for slug, title, cat in PAIRS:
    d = 'public/posts/' + slug
    p = d + '/index.html'
    if not os.path.exists(p):
        out.append('FALTA HTML: ' + slug)
        continue
    h = io.open(p, encoding='utf-8', errors='replace').read()
    m = re.search(r'name="description" content="([^"]*)"', h)
    exc = m.group(1).strip() if m else title
    if slug in slugs:
        out.append('YA EN salud.json: ' + slug)
        continue
    item = {
        'slug': slug,
        'title': title,
        'excerpt': exc[:280],
        'category': cat,
        'image': '/posts/' + slug + '/imagen1.jpg',
        'date': '2026-09-19',
    }
    data.insert(0, item)
    out.append('AGREGADO: ' + slug)

io.open(SALUD, 'w', encoding='utf-8').write(json.dumps(data, ensure_ascii=False, indent=2))
out.append('total salud.json: ' + str(len(data)))
sys.stdout.write('\n'.join(out) + '\n')
