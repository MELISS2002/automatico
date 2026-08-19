# -*- coding: utf-8 -*-
"""Batch de articulos para UltimoLive - 14 ago 2026
Genera via API local DeepSeek. Sin git (commit quirurgico manual despues).
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

# 5 noticias reales de hoy 14 ago 2026 (de Google News RSS + noticias-pe.cjs)
# (tema, categoria, slug)
ARTICULOS = [
    ("Simulacro Nacional Multipeligro INDECI: Peru ensaya respuesta ante sismo de magnitud 8.8 este viernes 14 de agosto", "home", "simulacro-nacional-multipeligro-indeci-sismo-88"),
    ("Gobierno de Keiko Fujimori anuncia subsidio de hasta 20% para transportistas ante alza de combustible", "home", "keiko-fujimori-subsidio-transportistas-combustible"),
    ("Encuesta Datum: Keiko Fujimori inicia con 60% de aprobacion, donde tiene mayor respaldo", "home", "encuesta-datum-keiko-fujimori-60-aprobacion"),
    ("Keiko Fujimori anuncia que empezara a aplicar el modelo de Bukele: firmeza para recuperar el orden", "home", "keiko-fujimori-modelo-bukele-firmeza-orden"),
    ("Once peruanos murieron combatiendo por Rusia y otros 114 estan desaparecidos, dicen autoridades de Peru", "home", "peruanos-murieron-combatiendo-rusia-114-desaparecidos"),
]

def build_prompt(tema):
    return f"""Eres un redactor periodistico y diseñador web experto. Crea un articulo completo en HTML sobre: "{tema}".
El articulo debe ser de noticias reales de Peru de hoy 14 de agosto 2026, minimo 1000 palabras, estilo periodistico profesional.

IMAGENES: Incluye exactamente 3 imagenes con src="imagen1.jpg", src="imagen2.jpg", src="imagen3.jpg" (rutas locales, las imagenes se descargan aparte).

ESTILO: CSS atractivo y responsive dentro de <style>. NO uses backticks (```) en tu respuesta.

Responde EXACTAMENTE con esta estructura (respeta los marcadores):

TITLE: (titulo de la noticia)
EXCERPT: (extracto de 2-3 frases)
===HTML_START===
(ESCRIBE AQUI TODO EL CODIGO HTML completo, incluyendo <!DOCTYPE html>, <head>, <style>, <body>, articulo, imagenes con src="imagen1.jpg" etc.)
===HTML_END===
THUMBNAIL: (descripcion de la miniatura en ingles para generarla, ej: "peru earthquake simulation disaster preparedness")
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
        title = tema[:80]
    if not excerpt:
        excerpt = "Articulo sobre " + tema[:60]
    if not thumbnail:
        thumbnail = f"peru news august 2026 {slug}"

    # Template base si no tiene DOCTYPE
    if not html.strip().startswith("<!DOCTYPE html>"):
        html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.7; max-width: 820px; margin: 0 auto; padding: 20px; background: #f5f5f5; color: #222; }}
        h1 {{ color: #1a1a2e; font-size: 1.8em; border-bottom: 3px solid #e94560; padding-bottom: 10px; }}
        h2 {{ color: #16213e; }}
        img {{ max-width: 100%; height: auto; border-radius: 10px; margin: 18px 0; box-shadow: 0 4px 8px rgba(0,0,0,0.15); }}
        p {{ text-align: justify; }}
        .fecha {{ color: #888; font-size: 0.85em; margin-bottom: 20px; }}
        footer {{ margin-top: 40px; padding-top: 15px; border-top: 1px solid #ddd; font-size: 0.85em; color: #777; }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <div class="fecha">14 de agosto, 2026 - UltimoLive</div>
    {html}
    <footer><p>Autor: ROSA EMILY | Fecha: 2026-08-14 | UltimoLive</p></footer>
</body>
</html>"""
    else:
        # Asegurar footer
        if "<footer>" not in html and "</body>" in html:
            html = html.replace("</body>", """
    <footer><p>Autor: ROSA EMILY | Fecha: 2026-08-14 | UltimoLive</p></footer>
</body>""")

    carpeta_post = os.path.join(POSTS_DIR, slug)
    os.makedirs(carpeta_post, exist_ok=True)
    html_path = os.path.join(carpeta_post, "index.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  OK HTML guardado: {html_path}")

    # Actualizar JSON
    json_path = JSON_FILES.get(categoria)
    if not json_path:
        return False, f"Categoria desconocida: {categoria}"

    nueva_entrada = {
        "slug": slug,
        "title": title,
        "author": "ROSA EMILY",
        "date": "2026-08-14",
        "excerpt": excerpt,
        "thumbnail": thumbnail,
        "htmlPath": f"/posts/{slug}/index.html"
    }
    if not actualizar_json(json_path, nueva_entrada):
        return False, "Error al actualizar JSON (slug duplicado?)"
    return True, title

def main():
    print(f"=== BATCH ULTIMOLIVE 14 ago 2026 ===")
    print(f"Articulos a generar: {len(ARTICULOS)}")
    ok = 0
    for i, (tema, categoria, slug) in enumerate(ARTICULOS, 1):
        print(f"\n--- [{i}/{len(ARTICULOS)}] {slug} ---")
        prompt = build_prompt(tema)
        try:
            print(f"  Llamando a DeepSeek...")
            respuesta = call_api(prompt)
            print(f"  Respuesta: {len(respuesta)} chars")
            exito, detalle = guardar_articulo(tema, categoria, slug, respuesta)
            if exito:
                ok += 1
                print(f"  ✅ Articulo {i}: {detalle}")
            else:
                print(f"  ❌ Articulo {i}: {detalle}")
        except Exception as e:
            print(f"  ❌ ERROR articulo {i}: {e}")
        if i < len(ARTICULOS):
            time.sleep(5)
    print(f"\n=== RESUMEN: {ok}/{len(ARTICULOS)} OK ===")

if __name__ == "__main__":
    main()
