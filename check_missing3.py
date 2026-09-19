# -*- coding: utf-8 -*-
import json, io, os, re, sys

out = []
for slug in ['new-hope-for-breast-cancer-patients', 'genetic-risk-for-ptsd-may-vary']:
    d = 'public/posts/' + slug
    p = d + '/index.html'
    out.append('=== ' + slug)
    out.append('files: ' + repr(sorted(os.listdir(d))))
    h = io.open(p, encoding='utf-8', errors='replace').read()
    imgs = re.findall(r'src="([^"]+)"', h)
    out.append('imgs: ' + repr(imgs[:12]))
    for pat in ['pollinations', 'unsplash', 'picsum', 'placehold', 'data:image', 'loremflickr']:
        if pat in h:
            out.append('FAKE PATTERN: ' + pat)
    txt = re.sub(r'<[^>]+>', ' ', h)
    txt = re.sub(r'\s+', ' ', txt)
    out.append('LEN: ' + str(len(txt)))
    out.append('TXT: ' + txt[:400])
    jsonp = None
    for jn in ['home.json', 'salud.json', 'gana.json']:
        jp = 'public/posts/' + jn
        if os.path.exists(jp):
            data = json.load(io.open(jp, encoding='utf-8'))
            for it in data:
                if it.get('slug') == slug:
                    jsonp = jn
    out.append('EN JSON: ' + repr(jsonp))

sys.stdout.write('\n'.join(out) + '\n')
