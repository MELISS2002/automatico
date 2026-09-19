# -*- coding: utf-8 -*-
import json, io, os, re

for slug in ['new-hope-for-breast-cancer-patients', 'genetic-risk-for-ptsd-may-vary']:
    p = 'public/posts/' + slug + '/index.html'
    if not os.path.exists(p):
        print(slug, '| NO EXISTE')
        continue
    h = io.open(p, encoding='utf-8', errors='replace').read()
    t = re.search(r'<title>(.*?)</title>', h, re.S)
    title = t.group(1).strip() if t else slug
    m = re.search(r'name="description" content="([^"]*)"', h)
    exc = m.group(1)[:200] if m else title
    print(slug, '|', os.path.getsize(p), '|', title[:80])
    print('   desc:', exc[:150])
