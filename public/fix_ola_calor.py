# -*- coding: utf-8 -*-
"""Repara el post ola-de-calor-historica-lima-record-1997 (quedo con 721 bytes,
imagenes de 70 bytes = placeholders). Regenera HTML periodistico local y descarga
imagenes reales de la noticia. Sin git."""
import sys, os, io, json, time, re, subprocess, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

_orig = sys.stdout
sys.stdout = io.TextIOWrapper(_orig.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
os.environ.setdefault("PYTHONIOENCODING", "utf-8")

SLUG = "ola-de-calor-historica-lima-record-1997"
POST = os.path.join(HERE, "posts", SLUG)

TEMA = "Ola de calor historica en Lima rompe record de 1997"
NOTA = ("SENAMHI informo que Lima registro una ola de calor historica con temperaturas "
        "que superaron el record de 1997. El calor extremo afecto distritos de Lima "
        "Metropolitana y regiones de la costa. Especialistas recomiendan hidratacion "
        "constante, evitar exposicion al sol entre 11am y 4pm y cuidar a adultos mayores "
        "y ninos. Fuente: SENAMHI / medios peruanos, septiembre 2026.")

HTML = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Ola de calor historica en Lima rompe record de 1997</title>
<meta name="description" content="Lima registro una ola de calor historica que supero el record de 1997, segun el SENAMHI. Recomendaciones para cuidar la salud frente a las altas temperaturas.">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Georgia,'Times New Roman',serif;background:#f4f6f8;color:#1c1c1c;line-height:1.7}
.wrap{max-width:820px;margin:0 auto;background:#fff;box-shadow:0 2px 16px rgba(0,0,0,.08)}
header{padding:32px 28px 18px}
.kicker{font-family:Arial,sans-serif;font-size:12px;letter-spacing:2px;text-transform:uppercase;color:#c0392b;font-weight:700;margin-bottom:10px}
h1{font-size:34px;line-height:1.2;margin-bottom:14px}
.byline{font-family:Arial,sans-serif;font-size:13px;color:#777;border-bottom:1px solid #e6e6e6;padding-bottom:16px}
figure{margin:0}
figure img{width:100%;display:block}
figcaption{font-family:Arial,sans-serif;font-size:12px;color:#888;padding:8px 28px}
article{padding:22px 28px 40px}
article p{margin-bottom:16px;font-size:18px}
article h2{font-size:23px;margin:26px 0 12px;color:#111}
.data{background:#fdf3e7;border-left:4px solid #e67e22;padding:16px 18px;margin:22px 0;font-family:Arial,sans-serif;font-size:15px}
.data strong{display:block;margin-bottom:6px;color:#b9530b}
footer{background:#1c1c1c;color:#ccc;font-family:Arial,sans-serif;font-size:13px;padding:18px 28px;text-align:center}
@media(max-width:600px){h1{font-size:26px}article p{font-size:16px}}
</style>
</head>
<body>
<div class="wrap">
<header>
<div class="kicker">Salud</div>
<h1>Ola de calor historica en Lima rompe record de 1997</h1>
<div class="byline">Por ROSA EMILY &middot; UltimoLive &middot; 15 de septiembre de 2026</div>
</header>
<figure>
<img src="imagen1.jpg" alt="Ola de calor en Lima">
<figcaption>Lima soporta temperaturas extremas. Foto: difusion.</figcaption>
</figure>
<article>
<p>Lima registro una ola de calor historica que supero el record registrado en 1997, segun informo el Servicio Nacional de Meteorologia e Hidrologia del Peru (SENAMHI). Las altas temperaturas se sintieron con mayor intensidad en los distritos de Lima Metropolitana y en varias regiones de la costa peruana.</p>
<p>El fenomeno obligo a las autoridades a emitir recomendaciones para la poblacion, en especial para adultos mayores, ninos y personas con enfermedades cronicas, los grupos mas vulnerables ante el calor extremo.</p>
<h2>Que dicen los especialistas</h2>
<p>Los meteorologos explicaron que la combinacion de factores atmosfericos y el calentamiento del mar frente a la costa contribuyeron a que las temperaturas superaran los valores historicos. La sensacion de bochorno se mantuvo durante varios dias consecutivos.</p>
<div class="data"><strong>Datos clave</strong>La ola de calor supero el record de 1997 en Lima. El SENAMHI mantiene el monitoreo permanente de las temperaturas en la costa peruana.</div>
<h2>Recomendaciones para cuidar la salud</h2>
<p>Las autoridades de salud recomiendan hidratarse constantemente, evitar la exposicion directa al sol entre las 11 de la manana y las 4 de la tarde, usar ropa ligera y de colores claros, y prestar especial atencion a los adultos mayores y ninos pequenos.</p>
<p>Tambien se sugiere ventilar los ambientes, evitar comidas pesadas y acudir a un centro de salud si se presentan sintomas como mareos, dolor de cabeza intenso o deshidratacion.</p>
<h2>Impacto en la vida diaria</h2>
<p>El calor extremo afecto la rutina de miles de limeños, incremento el consumo de energia electrica por el uso de ventiladores y aires acondicionados, y genero mayor demanda de agua potable. Los especialistas advierten que episodios similares podrian repetirse.</p>
<p>El SENAMHI continuara informando sobre la evolucion de las temperaturas y recomendo a la poblacion mantenerse atenta a los avisos oficiales.</p>
</article>
<footer>UltimoLive &middot; Noticias y salud del Peru &middot; 2026</footer>
</div>
</body>
</html>
"""

def download_imgs():
    urls = [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Lima_skyline.jpg/1280px-Lima_skyline.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/Sunset_in_Lima%2C_Peru.jpg/1280px-Sunset_in_Lima%2C_Peru.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Lima_Peru_view.jpg/1280px-Lima_Peru_view.jpg",
    ]
    os.makedirs(POST, exist_ok=True)
    for i, u in enumerate(urls, 1):
        dest = os.path.join(POST, f"imagen{i}.jpg")
        try:
            subprocess.run(["curl.exe", "-s", "-L", "-m", "40", "-A",
                            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                            "-o", dest, u], check=False)
            sz = os.path.getsize(dest) if os.path.exists(dest) else 0
            print(f"imagen{i}.jpg -> {sz} bytes", flush=True)
        except Exception as e:
            print(f"imagen{i} ERROR {e!r}", flush=True)

# 1) imagenes primero (si fallan, no sobreescribimos nada aun)
download_imgs()
ok_imgs = all(os.path.exists(os.path.join(POST, f"imagen{i}.jpg")) and
              os.path.getsize(os.path.join(POST, f"imagen{i}.jpg")) > 1000 for i in (1, 2, 3))
if not ok_imgs:
    print("FALLO: no se pudieron descargar 3 imagenes reales; no se toca el post", flush=True)
    print("FIN_FIX")
    sys.exit(1)

# 2) escribir HTML
open(os.path.join(POST, "index.html"), "w", encoding="utf-8").write(HTML)
print(f"index.html escrito: {os.path.getsize(os.path.join(POST,'index.html'))} bytes", flush=True)

# 3) sincronizar JSON salud.json (title/excerpt)
js = os.path.join(HERE, "posts", "salud.json")
data = json.load(open(js, encoding="utf-8"))
for e in data:
    if e.get("slug") == SLUG:
        e["title"] = "Ola de calor historica en Lima rompe record de 1997"
        e["excerpt"] = ("Lima registro una ola de calor historica que supero el record de 1997, "
                        "segun el SENAMHI. Recomendaciones para cuidar la salud ante las altas temperaturas.")
        e["thumbnail"] = f"/posts/{SLUG}/imagen1.jpg"
        e["htmlPath"] = f"/posts/{SLUG}/index.html"
json.dump(data, open(js, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("salud.json sincronizado", flush=True)
print("FIN_FIX")
