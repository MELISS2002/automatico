# -*- coding: utf-8 -*-
import os, re, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
base = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(base, 'posts', 'bochorno-lima-distritos-38-grados-fenomeno-nino')
files = os.listdir(p)
print('FILES:', files)
h = open(os.path.join(p, 'index.html'), encoding='utf-8', errors='replace').read()
print('LEN:', len(h))
imgs = re.findall(r'src="([^"]+)"', h)
print('IMGS:', imgs[:8])
print('POLLINATIONS:', 'pollinations' in h)
print('HAS_DOCTYPE:', h.lstrip().startswith('<!DOCTYPE'))
print('BODY_END:', h.rstrip()[-120:])
