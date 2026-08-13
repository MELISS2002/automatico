# check-news-posts.py — verifica los 5 posts de noticias: imagenes locales, 0 pollinations, titulos, thumbnails
import os, re, json, sys

POSTS = r'C:\Users\dza\Desktop\automatico-main\public\posts'
slugs = ['temblor-venezuela-10-agosto-funvisis',
         'meteorito-marte-1270-millones-anos-historia',
         'motorola-global-connect-roaming-gratis-torneo',
         'keiko-fujimori-modelo-bukele-firmeza-orden',
         'peruanos-muertos-combatiendo-rusia-114-desaparecidos']

all_ok = True
for slug in slugs:
    carpeta = os.path.join(POSTS, slug)
    if not os.path.isdir(carpeta):
        print(f"FAIL {slug}: no existe carpeta")
        all_ok = False
        continue
    html_path = os.path.join(carpeta, 'index.html')
    html = open(html_path, encoding='utf-8', errors='replace').read()
    # 1. pollinations
    n_poll = len(re.findall(r'pollinations', html))
    # 2. refs a imagenes locales
    n_refs = len(re.findall(r'imagen[123]\.jpg', html))
    # 3. archivos de imagen presentes
    imgs = [f for f in os.listdir(carpeta) if f.endswith('.jpg')]
    # 4. emojis
    n_emoji = len(re.findall(r'[\U0001F000-\U0001FAFF\u2600-\u27BF]', html))
    # 5. titulo
    t = re.search(r'<title>(.*?)</title>', html, re.S)
    title = t.group(1).strip() if t else 'SIN TITLE'
    # 6. img srcs
    srcs = re.findall(r'<img[^>]+src="([^"]+)"', html)
    print(f"\n{slug}")
    print(f"  title: {title[:80]}")
    print(f"  size: {len(html)} chars | pollinations: {n_poll} | refs imagen*.jpg: {n_refs} | emojis: {n_emoji}")
    print(f"  imgs en carpeta: {sorted(imgs)}")
    print(f"  srcs en HTML: {srcs}")
    if n_poll > 0 or n_emoji > 0 or n_refs < 2 or len(imgs) < 3:
        all_ok = False

# JSON home
home = json.load(open(os.path.join(POSTS, 'home.json'), encoding='utf-8'))
print("\n=== home.json (primeros 7) ===")
for x in home[:7]:
    print(f"  {x['slug'][:45]} | thumb={x['thumbnail'][:60]}")

print("\n" + ("TODO OK" if all_ok else "HAY PROBLEMAS"))
