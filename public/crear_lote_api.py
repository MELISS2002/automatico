# -*- coding: utf-8 -*-
"""Genera articulos en lote via API local DeepSeek (sin Selenium).
Usa el mismo template de auto1.py y parsea marcadores con sus funciones.
NO hace git: el commit/push se hace manualmente despues (quirurgico).
"""
import sys, os, io, json, time, re, urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from auto1 import (extract_val, extract_between, extraer_bloques,
                   actualizar_json, JSON_FILES, POSTS_DIR, limpiar_texto,
                   tema_a_slug)

API_URL = "http://127.0.0.1:8765/v1/chat/completions"
MODEL = "deepseek-web"

ARTICULOS = [
    # (tema, categoria, slug_limpio)
    ("Ministro de Salud Luis Dyer: 'No hay dinero, se lo gastaron todo' y las medidas urgentes que anuncia para rescatar el Minsa", "salud", "minsa-luis-dyer-no-hay-dinero"),
    ("Minsa instalara una torre de control para vigilar equipos medicos en hospitales y revisara los contratos de alquiler tras el caso de la resonancia que no funciona", "salud", "minsa-torre-control-equipos-medicos"),
    ("Dengue en Tumbes: llegan 26 mil dosis de vacuna para reforzar la prevencion ante el Fenomeno El Nino", "salud", "dengue-tumbes-26-mil-dosis-vacuna"),
    ("Sarampion en Arequipa: 100 mil vacunas disponibles y campanas de vacunacion en colegios", "salud", "sarampion-arequipa-100-mil-vacunas"),
    ("La piel como reflejo de la salud intestinal: que habitos influyen y cuales son las senales de alerta", "salud", "piel-reflejo-salud-intestinal"),
    ("Tomar suplementos a ciegas es jugar a los dados con tu cuerpo, advierten medicos: que debes saber antes de comprar", "salud", "suplementos-a-ciegas-riesgos"),
]

def build_prompt(tema):
    return f"""
Eres un redactor y diseñador web experto. Crea un artículo completo en HTML sobre "{tema}" (mínimo 1000 palabras).
Incluye al menos 3 imágenes usando https://image.pollinations.ai/prompt/DESCRIPCION_EN_INGLES.
El HTML debe tener estilos CSS atractivos y responsive.
NO uses backticks (```) en tu respuesta. El HTML debe entregarse directamente.

Responde EXACTAMENTE con esta estructura (respeta los marcadores):

TITLE: (título sugerido)
EXCERPT: (extracto 2-3 frases)
===HTML_START===
(ESCRIBE AQUÍ TODO EL CÓDIGO HTML, INCLUYENDO <!DOCTYPE html>, <head>, <style>, <body>, IMÁGENES, ETC.)
===HTML_END===
THUMBNAIL: (URL de miniatura usando https://image.pollinations.ai/prompt/descripcion-en-ingles)
"""

def call_api(prompt):
    body = json.dumps({
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }).encode("utf-8")
    req = urllib.request.Request(API_URL, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=590) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["choices"][0]["message"]["content"]

def guardar_articulo(tema, categoria, slug, respuesta):
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
        else:
            m = re.search(r'(<html.*?</html>)', respuesta, re.DOTALL | re.IGNORECASE)
            if m:
                html = m.group(1).strip()

    if not html:
        return False, "No HTML en respuesta"

    html = re.sub(r'^```(?:html)?\s*\n?', '', html.strip())
    html = re.sub(r'\n?```$', '', html.strip())

    if not title:
        title = tema[:50]
    if not excerpt:
        excerpt = "Articulo sobre " + tema[:50]
    if not thumbnail or not thumbnail.startswith("http"):
        thumbnail = f"https://image.pollinations.ai/prompt/{slug}-thumbnail"

    if not html.strip().startswith("<!DOCTYPE html>"):
        html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f9f9f9;
            color: #333;
        }}
        h1 {{ color: #2c3e50; }}
        h2 {{ color: #16a085; }}
        img {{ max-width: 100%; height: auto; border-radius: 8px; margin: 20px 0; }}
        footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 0.9em; color: #777; }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    {html}
    <footer>
        <p>Autor: ROSA EMILY | Fecha: {time.strftime("%Y-%m-%d")}</p>
    </footer>
</body>
</html>"""
    else:
        if "<footer>" not in html and "</body>" in html:
            html = html.replace("</body>", f"""
    <footer>
        <p>Autor: ROSA EMILY | Fecha: {time.strftime("%Y-%m-%d")}</p>
    </footer>
</body>""")

    carpeta_post = os.path.join(POSTS_DIR, slug)
    os.makedirs(carpeta_post, exist_ok=True)
    html_path = os.path.join(carpeta_post, "index.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"OK HTML guardado: {html_path}")

    json_path = JSON_FILES.get(categoria)
    if not json_path:
        return False, f"Categoria desconocida: {categoria}"

    nueva_entrada = {
        "slug": slug,
        "title": title,
        "author": "ROSA EMILY",
        "date": time.strftime("%Y-%m-%d"),
        "excerpt": excerpt,
        "thumbnail": thumbnail,
        "htmlPath": f"/posts/{slug}/index.html"
    }
    if not actualizar_json(json_path, nueva_entrada):
        return False, "Error al actualizar JSON (slug duplicado?)"
    return True, title

def main():
    ok = 0
    for i, (tema, categoria, slug) in enumerate(ARTICULOS, 1):
        print(f"\n=== [{i}/{len(ARTICULOS)}] {slug} ===")
        prompt = build_prompt(tema)
        try:
            respuesta = call_api(prompt)
            print(f"Respuesta: {len(respuesta)} chars")
            exito, detalle = guardar_articulo(tema, categoria, slug, respuesta)
            if exito:
                ok += 1
                print(f"OK articulo {i}: {detalle}")
            else:
                print(f"FAIL articulo {i}: {detalle}")
        except Exception as e:
            print(f"ERROR articulo {i}: {e}")
        if i < len(ARTICULOS):
            time.sleep(3)
    print(f"\nRESUMEN: {ok}/{len(ARTICULOS)} OK")

if __name__ == "__main__":
    main()
