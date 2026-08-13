# sync-dist.py — copia posts nuevos de public a dist y sincroniza home.json
import os, json, shutil

PUBLIC = r'C:\Users\dza\Desktop\automatico-main\public\posts'
DIST = r'C:\Users\dza\Desktop\automatico-main\dist\posts'

slugs = ['temblor-venezuela-10-agosto-funvisis',
         'meteorito-marte-1270-millones-anos-historia',
         'motorola-global-connect-roaming-gratis-torneo',
         'keiko-fujimori-modelo-bukele-firmeza-orden',
         'peruanos-muertos-combatiendo-rusia-114-desaparecidos']

for slug in slugs:
    src = os.path.join(PUBLIC, slug)
    dst = os.path.join(DIST, slug)
    if os.path.isdir(src):
        if os.path.isdir(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        print(f'copiado: {slug}')
    else:
        print(f'NO existe en public: {slug}')

# sincronizar home.json (insertar los nuevos al inicio, sin duplicar)
pub_json = json.load(open(os.path.join(PUBLIC, 'home.json'), encoding='utf-8'))
dist_json = json.load(open(os.path.join(DIST, 'home.json'), encoding='utf-8'))
dist_slugs = {x['slug'] for x in dist_json}
nuevos = [x for x in pub_json if x['slug'] not in dist_slugs and x['slug'] in slugs]
# orden: los nuevos al inicio como en public
result = [x for x in pub_json if x['slug'] in slugs] + [x for x in dist_json if x['slug'] not in slugs]
json.dump(result, open(os.path.join(DIST, 'home.json'), 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
print(f'home.json dist: {len(dist_json)} -> {len(result)} (agregados {len(nuevos)})')
