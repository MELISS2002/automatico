# -*- coding: utf-8 -*-
"""Test rapido: generar 1 articulo via DeepSeek API."""
import sys, os, io, json, time, re, urllib.request, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from auto1 import (extract_val, extract_between, extraer_bloques,
                   actualizar_json, JSON_FILES, POSTS_DIR, limpiar_texto)

API_URL = "http://127.0.0.1:8765/v1/chat/completions"
MODEL = "deepseek-web"
IMGS_DIR = r"C:\Users\dza\Desktop\neo\tools\news-imgs-final"

SLUG = "subsidio-diesel-transporte-peru"
CATEGORIA = "home"
TITULO = "Elmer Cuba anuncia subsidio de S/4 por galon de diesel para transporte de carga y pasajeros en todo el Peru"
DESC = "Ministro de Economia Elmer Cuba anuncia subsidio de S/4 por galon de diesel. Cubre hasta 20% del precio. Transportistas ahorran S/6 por galon. MEF construyendo padron de beneficiarios. Tras paro de transportistas en Ucayali y otras regiones."
IMGS = ["subsidio-diesel-1.jpg", "subsidio-diesel-2.jpg", "subsidio-diesel-3.jpg"]

prompt = f"""Redacta un articulo de noticia de Peru sobre: {TITULO}

Contexto: {DESC}

Crea el HTML completo con DOCTYPE, head, style CSS bonito y responsive, body.
Usa estas imagenes locales: <img src="{IMGS[0]}"> <img src="{IMGS[1]}"> <img src="{IMGS[2]}">
Minimo 600 palabras. Estilo periodistico. Footer con Autor: ROSA EMILY, fecha {time.strftime('%Y-%m-%d')}.
No uses backticks ni markdown.

Responde con:
TITLE: titulo
EXCERPT: resumen 2 frases
===HTML_START===
<html>...codigo completo...</html>
===HTML_END===
THUMBNAIL: {IMGS[0]}
"""

print(f"Enviando prompt a DeepSeek ({len(prompt)} chars)...")
body = json.dumps({"model": MODEL, "messages": [{"role": "user", "content": prompt}], "temperature": 0.7}).encode("utf-8")
req = urllib.request.Request(API_URL, data=body, headers={"Content-Type": "application/json"})
t0 = time.time()
with urllib.request.urlopen(req, timeout=590) as resp:
    data = json.loads(resp.read().decode("utf-8"))
respuesta = data["choices"][0]["message"]["content"]
print(f"Respuesta en {time.time()-t0:.1f}s: {len(respuesta)} chars")

# Guardar
respuesta = limpiar_texto(respuesta)
title = extract_val(respuesta, "TITLE:")
excerpt = extract_val(respuesta, "EXCERPT:")
html = extract_between(respuesta, "===HTML_START===", "===HTML_END===")
thumbnail = extract_val(respuesta, "THUMBNAIL:")

if not html:
    bloques = extraer_bloques(respuesta)
    for tipo, contenido in bloques:
        if tipo == 'html' or (tipo == 'code' and ('<html' in contenido.lower() or '<!doctype' in contenido.lower())):
            html = contenido
            break
if not html:
    m = re.search(r'(<!DOCTYPE html>.*)', respuesta, re.DOTALL | re.IGNORECASE)
    if m:
        html = m.group(1).strip()

html = re.sub(r'^```(?:html)?\s*\n?', '', html.strip())
html = re.sub(r'\n?```$', '', html.strip())

if not title:
    title = TITULO[:80]
if not excerpt:
    excerpt = "Noticia de Peru"
if not thumbnail:
    thumbnail = IMGS[0]

carpeta_post = os.path.join(POSTS_DIR, SLUG)
os.makedirs(carpeta_post, exist_ok=True)

for img_name in IMGS:
    src = os.path.join(IMGS_DIR, img_name)
    dst = os.path.join(carpeta_post, img_name)
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print(f"IMG copiada: {img_name}")

html_path = os.path.join(carpeta_post, "index.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)
print(f"HTML guardado: {html_path}")

json_path = JSON_FILES.get(CATEGORIA)
nueva_entrada = {
    "slug": SLUG, "title": title, "author": "ROSA EMILY",
    "date": time.strftime("%Y-%m-%d"), "excerpt": excerpt,
    "thumbnail": f"/posts/{SLUG}/{IMGS[0]}",
    "htmlPath": f"/posts/{SLUG}/index.html"
}
if actualizar_json(json_path, nueva_entrada):
    print(f"JSON actualizado OK")
else:
    print("ERROR actualizando JSON")
print(f"TITLE: {title}")
print("DONE!")
