# -*- coding: utf-8 -*-
"""Genera articulos en lote via API local DeepSeek (sin Selenium).
Tema: noticias reales de Peru 15-Ago-2026 con imagenes REALES descargadas.
NO hace git: el commit/push se hace manualmente despues (quirurgico).
"""
import sys, os, io, json, time, re, urllib.request, shutil

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from auto1 import (extract_val, extract_between, extraer_bloques,
                   actualizar_json, JSON_FILES, POSTS_DIR, limpiar_texto)

API_URL = "http://127.0.0.1:8765/v1/chat/completions"
MODEL = "deepseek-web"

IMGS_DIR = r"C:\Users\dza\Desktop\neo\tools\news-imgs-final"

ARTICULOS = [
    ("subsidio-diesel-transporte-peru",
     "home",
     "Elmer Cuba anuncia subsidio de S/4 por galon de diesel para transporte de carga y pasajeros en todo el Peru",
     "El ministro de Economia y Finanzas, Elmer Cuba, announces a subsidy of S/4 per gallon of diesel for cargo and passenger transport across Peru. The measure seeks to ease the impact of fuel price hikes on transporters. The subsidy will cover up to 20% of the fuel price and transportistas could save up to S/6 per gallon. The MEF is building a registry of beneficiaries. This comes after strikes by transportistas in Ucayali and other regions paralyzed by fuel costs.",
     ["subsidio-diesel-1.jpg", "subsidio-diesel-2.jpg", "subsidio-diesel-3.jpg"]),

    ("ucayali-paro-transportistas-policias-heridos",
     "home",
     "Ucayali cinco policias heridos y 11 detenidos tras enfrentamiento durante paro de transportistas",
     "Five police officers were injured and 11 people detained in Ucayali after clashes during the transport strike. The transportistas were protesting fuel prices and blocked the Federico Basadre highway. The Minem declared emergency in fuel supply for Ucayali. After the government announced subsidies, the regional government announced the strike was being lifted.",
     ["ucayali-paro-1.jpg", "ucayali-paro-2.jpg", "ucayali-paro-3.jpg", "ucayali-paro-4.jpg"]),

    ("gobierno-designa-nuevos-viceministros-zea-leon-lezameta-bayona",
     "home",
     "Gobierno designa a Elizabeth Zea, Wiliam Leon, Carlos Lezameta y Diana Bayona como nuevos viceministros",
     "The Peruvian government has designated new vice ministers across various sectors: Elizabeth Zea in Interculturality, Wiliam Leon, Carlos Lezameta, and Diana Bayona as vice minister of Foreign Commerce (Mincetur). The redesignation is part of a broader government restructuring. Elizabeth Zea's appointment was controversial due to her background. The changes affect Minam, Mincetur and other ministries.",
     ["viceministros-1.jpg", "viceministros-2.jpg", "viceministros-3.jpg"]),


]


def build_prompt(tema_titulo, descripcion, img_names):
    img1 = img_names[0] if len(img_names) > 0 else "imagen1.jpg"
    img2 = img_names[1] if len(img_names) > 1 else "imagen2.jpg"
    img3 = img_names[2] if len(img_names) > 2 else "imagen3.jpg"
    return f"""Redacta un articulo de noticia de Peru sobre: {tema_titulo}

Contexto: {descripcion}

Crea el HTML completo con DOCTYPE, head, style CSS bonito y responsive, body.
Usa estas imagenes locales: <img src="{img1}"> <img src="{img2}"> <img src="{img3}">
Minimo 600 palabras. Estilo periodistico. Footer con Autor: ROSA EMILY, fecha {time.strftime('%Y-%m-%d')}.
No uses backticks ni markdown.

Responde con:
TITLE: titulo
EXCERPT: resumen 2 frases
===HTML_START===
<html>...codigo completo...</html>
===HTML_END===
THUMBNAIL: {img1}
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


def guardar_articulo(slug, categoria, tema, respuesta, img_names):
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
        title = tema[:80]
    if not excerpt:
        excerpt = "Noticia de Peru: " + tema[:60]
    if not thumbnail or not thumbnail.startswith("http"):
        thumbnail = img_names[0] if img_names else f"imagen1.jpg"

    if not html.strip().startswith("<!DOCTYPE html>"):
        html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            line-height: 1.7;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
            color: #333;
        }}
        h1 {{ color: #1a237e; font-size: 1.8em; }}
        h2 {{ color: #0277bd; }}
        img {{ max-width: 100%; height: auto; border-radius: 10px; margin: 16px 0; }}
        .excerpt {{ font-size: 1.1em; color: #555; font-style: italic; margin-bottom: 20px; padding-left: 15px; border-left: 4px solid #1a237e; }}
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
        # asegurar footer
        if "<footer>" not in html and "</body>" in html:
            html = html.replace("</body>", f"""
    <footer>
        <p>Autor: ROSA EMILY | Fecha: {time.strftime("%Y-%m-%d")}</p>
    </footer>
</body>""")

    # crear carpeta del post
    carpeta_post = os.path.join(POSTS_DIR, slug)
    os.makedirs(carpeta_post, exist_ok=True)

    # copiar imagenes a la carpeta del post
    for img_name in img_names:
        src = os.path.join(IMGS_DIR, img_name)
        dst = os.path.join(carpeta_post, img_name)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"  IMG copiada: {img_name}")
        else:
            print(f"  IMG NO encontrada: {img_name}")

    # guardar HTML
    html_path = os.path.join(carpeta_post, "index.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  OK HTML guardado: {html_path}")

    # actualizar JSON
    json_path = JSON_FILES.get(categoria)
    if not json_path:
        return False, f"Categoria desconocida: {categoria}"

    nueva_entrada = {
        "slug": slug,
        "title": title,
        "author": "ROSA EMILY",
        "date": time.strftime("%Y-%m-%d"),
        "excerpt": excerpt,
        "thumbnail": f"/posts/{slug}/{img_names[0]}" if img_names else "",
        "htmlPath": f"/posts/{slug}/index.html"
    }
    if not actualizar_json(json_path, nueva_entrada):
        return False, "Error al actualizar JSON (slug duplicado?)"
    return True, title


def main():
    ok = 0
    for i, (slug, categoria, titulo, descripcion, img_names) in enumerate(ARTICULOS, 1):
        print(f"\n=== [{i}/{len(ARTICULOS)}] {slug} ===")
        prompt = build_prompt(titulo, descripcion, img_names)
        try:
            respuesta = call_api(prompt)
            print(f"  Respuesta: {len(respuesta)} chars")
            exito, detalle = guardar_articulo(slug, categoria, titulo, respuesta, img_names)
            if exito:
                ok += 1
                print(f"  OK articulo {i}: {detalle}")
            else:
                print(f"  FAIL articulo {i}: {detalle}")
        except Exception as e:
            print(f"  ERROR articulo {i}: {e}")
        # abrir chat nuevo en DeepSeek antes de cada articulo
        try:
            import subprocess
            subprocess.run(['node', 'neo.cjs', 'open', 'https://chat.deepseek.com/'],
                         cwd=r'C:\Users\dza\Desktop\neo\tools',
                         capture_output=True, timeout=15)
            time.sleep(3)
        except:
            time.sleep(5)
    print(f"\nRESUMEN: {ok}/{len(ARTICULOS)} OK")


if __name__ == "__main__":
    main()
