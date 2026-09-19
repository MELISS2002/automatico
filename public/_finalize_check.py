# -*- coding: utf-8 -*-
import os, io, sys, json, re, unicodedata
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
base = os.path.dirname(os.path.abspath(__file__))
posts = os.path.join(base, 'posts')

def norm(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s.lower()) if unicodedata.category(c) != 'Mn')

CATS = ['home', 'salud', 'gana']
for cat in CATS:
    jf = os.path.join(posts, cat + '.json')
    if not os.path.exists(jf):
        print('MISSING JSON:', cat)
        continue
    data = json.load(open(jf, encoding='utf-8'))
    print('=== %s.json: %d entries ===' % (cat, len(data)))
    for item in data:
        slug = item.get('slug', '')
        pdir = os.path.join(posts, slug)
        idx = os.path.join(pdir, 'index.html')
        if not os.path.exists(idx):
            print('  MISSING HTML for', slug)
            continue
        h = open(idx, encoding='utf-8', errors='replace').read()
        imgs = re.findall(r'src="([^"]+)"', h)
        local = [i for i in imgs if i.startswith('imagen')]
        poll = 'pollinations' in h.lower()
        words = norm(slug).replace('-', ' ').split()[:3]
        body = norm(h)
        kw = all(w in body for w in words)
        files = sorted(os.listdir(pdir))
        print('  %s | imgs=%s | poll=%s | kw3=%s | files=%s' % (slug, local, poll, kw, files))
