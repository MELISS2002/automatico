#!/usr/bin/env python3
"""
Driver batch: genera articulos via API local DeepSeek y los publica.
Pipeline robusto: API local (no Selenium directo), commit quirurgico, push.
"""
import time, re, os, sys, json, subprocess, unicodedata, urllib.request

REPO_PATH = r"C:\Users\dza\Desktop\automatico-main"
POSTS_DIR = os.path.join(REPO_PATH, "public", "posts")
JSON_FILES = {
    "salud": os.path.join(POSTS_DIR, "salud.json"),
    "home": os.path.join(POSTS_DIR, "home.json"),
    "gana": os.path.join(POSTS_DIR, "gana.json"),
}
API_URL = "http://127.0.0.1:8765/v1/chat/completions"
MODEL = "deepseek-web"

# Importar funciones de auto1
sys.path.insert(0, os.path.join(REPO_PATH, "public"))
import auto1

ARTICULOS = [
    ("Fujimorismo preside la Comisión de Constitución del Senado: clave en la reforma judicial", "home",
     "fujimorismo-preside-comision-constitucion-senado"),
    ("Rafael Rey desmiente a López Aliaga: tren Lima-Chosica fue una compra a Caltrain no una donación", "home",
     "rafael-rey-tren-lima-chosica-caltrain-compra"),
    ("Crisis CAL-JNJ: miembros de la Junta Nacional de Justicia renuncian al Colegio de Abogados de Lima", "home",
     "cal-jnj-miembros-renuncian-colegio-abogados-lima"),
    ("Eclipse solar total 12 agosto 2026: el evento astronómico del siglo que hoy oscurece España", "home",
     "eclipse-solar-total-12-agosto-2026-evento-astronomico-siglo"),
    ("Beneficios del ayuno intermitente según la ciencia 2026: lo que sí funciona y lo que es mito", "salud",
     "beneficios-ayuno-intermitente-ciencia-2026"),
]

PROMPT_TEMPLATE = """Eres un redactor y diseñador web experto. Crea un articulo completo en HTML sobre "{tema}" (minimo 1000 palabras).
Incluye al menos 3 imagenes usando https://image.pollinations.ai/prompt/DESCRIPCION_EN_INGLES.
El HTML debe tener estilos CSS atractivos y responsive.
NO uses backticks en tu respuesta. El HTML debe entregarse directamente.

Responde EXACTAMENTE con esta estructura (respete los marcadores):

TITLE: (titulo sugerido)
EXCERPT: (extracto 2-3 frases)
===HTML_START===
(ESCRIBE AQUI TODO EL CODIGO HTML, INCLUYENDO <!DOCTYPE html>, <head>, <style>, <body>, IMAGENES, ETC.)
===HTML_END===
THUMBNAIL: (URL de miniatura usando https://image.pollinations.ai/prompt/descripcion-en-ingles)
"""


def call_deepseek_api(prompt):
    """Llama a la API local de DeepSeek y devuelve la respuesta de texto."""
    body = json.dumps({
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 8000,
    }).encode("utf-8")

    req = urllib.request.Request(
        API_URL,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    print(f"  Enviando prompt a API ({len(prompt)} chars)...")
    try:
        with urllib.request.urlopen(req, timeout=600) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"  ERROR API: {e}")
        # Intentar recuperar del DOM si la API falla
        return None


def regenerar_sitemap():
    script = os.path.join(REPO_PATH, "scripts", "generate_sitemap.py")
    if os.path.isfile(script):
        subprocess.run([sys.executable, script], cwd=REPO_PATH, check=False)
        print("  Sitemap regenerado.")
    else:
        print("  No se encontro generate_sitemap.py, omitiendo sitemap.")


def git_quirurgico(archivos, mensaje):
    """Commit quirurgico: solo los archivos pasados."""
    try:
        for f in archivos:
            subprocess.run(["git", "add", f], cwd=REPO_PATH, check=False)
        subprocess.run(["git", "commit", "-m", mensaje], cwd=REPO_PATH, check=False)
        subprocess.run(["git", "push"], cwd=REPO_PATH, check=False)
        print(f"  Push OK: {mensaje[:60]}")
    except Exception as e:
        print(f"  Error git: {e}")


def main():
    print("=" * 60)
    print("PUBLICADOR BATCH 4 - API local DeepSeek")
    print(f"Articulos a generar: {len(ARTICULOS)}")
    print("=" * 60)

    exitosos = 0
    fallidos = 0

    for i, (tema, categoria, slug) in enumerate(ARTICULOS, 1):
        print(f"\n{'='*60}")
        print(f"Articulo {i}/{len(ARTICULOS)}: {tema}")
        print(f"Categoria: {categoria} | Slug: {slug}")
        print(f"{'='*60}")

        # Verificar que no exista ya
        post_dir = os.path.join(POSTS_DIR, slug)
        if os.path.isdir(post_dir):
            print(f"  SKIP: ya existe {slug}")
            fallidos += 1
            continue

        # Preparar prompt
        prompt = PROMPT_TEMPLATE.format(tema=tema)

        # Llamar API
        respuesta = call_deepseek_api(prompt)
        if not respuesta:
            print("  No se obtuvo respuesta.")
            fallidos += 1
            continue

        print(f"  Respuesta recibida: {len(respuesta)} chars")

        # Extraer campos
        title = auto1.extract_val(respuesta, "TITLE:")
        excerpt = auto1.extract_val(respuesta, "EXCERPT:")
        html = auto1.extract_between(respuesta, "===HTML_START===", "===HTML_END===")
        thumbnail = auto1.extract_val(respuesta, "THUMBNAIL:")

        # Fallbacks
        if not html:
            print("  Marcadores no encontrados, buscando bloques...")
            bloques = auto1.extraer_bloques(respuesta)
            for tipo, contenido in bloques:
                if tipo == "html" or (tipo == "code" and ("<html" in contenido.lower() or "<!doctype" in contenido.lower())):
                    html = contenido
                    print("  HTML extraido desde bloque de codigo.")
                    break

        if not html:
            match = re.search(r'(<!DOCTYPE html>.*)', respuesta, re.DOTALL | re.IGNORECASE)
            if match:
                html = match.group(1).strip()
                print("  HTML encontrado por busqueda directa.")
            else:
                match = re.search(r'(<html.*?</html>)', respuesta, re.DOTALL | re.IGNORECASE)
                if match:
                    html = match.group(1).strip()
                    print("  HTML encontrado (tag html).")

        if not html:
            print("  No se pudo extraer HTML. Falla.")
            fallidos += 1
            continue

        # Limpiar html
        html = re.sub(r'^```(?:html)?\s*\n?', '', html.strip())
        html = re.sub(r'\n?```$', '', html.strip())

        if not title:
            title = tema[:60]
        if not excerpt:
            excerpt = "Articulo sobre " + tema[:50]
        if not thumbnail or not thumbnail.startswith("http"):
            thumbnail = f"https://image.pollinations.ai/prompt/{slug}-thumbnail"

        # Asegurar footer
        if "<footer>" not in html and "</body>" in html:
            html = html.replace("</body>", f'\n<footer>\n    <p>Autor: ROSA EMILY | Fecha: {time.strftime("%Y-%m-%d")}</p>\n</footer>\n</body>')

        # Crear carpeta y guardar HTML
        os.makedirs(post_dir, exist_ok=True)
        html_path = os.path.join(post_dir, "index.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  HTML guardado: {html_path} ({len(html)} chars)")

        # Actualizar JSON
        json_path = JSON_FILES.get(categoria)
        if not json_path:
            print(f"  Categoria invalida: {categoria}")
            fallidos += 1
            continue

        nueva_entrada = {
            "slug": slug,
            "title": title,
            "author": "ROSA EMILY",
            "date": time.strftime("%Y-%m-%d"),
            "excerpt": excerpt,
            "thumbnail": thumbnail,
            "htmlPath": f"/posts/{slug}/index.html",
        }

        if not auto1.actualizar_json(json_path, nueva_entrada):
            print("  Error al actualizar JSON (ya existe?)")
            fallidos += 1
            continue
        print(f"  JSON actualizado: {categoria}.json")

        # Commit quirurgico de este articulo
        archivos = [
            f"public/posts/{slug}/index.html",
            f"public/posts/{categoria}.json",
        ]
        # Sitemap si existe
        sitemap = os.path.join(REPO_PATH, "public", "sitemap.xml")
        robots = os.path.join(REPO_PATH, "public", "robots.txt")
        if os.path.isfile(sitemap):
            archivos.append("public/sitemap.xml")
        if os.path.isfile(robots):
            archivos.append("public/robots.txt")

        # Regenerar sitemap antes del commit
        regenerar_sitemap()

        git_quirurgico(archivos, f"batch agost12: {title[:50]}")
        exitosos += 1
        print(f"  Articulo {i} OK.")

        # Pausa entre articulos
        if i < len(ARTICULOS):
            print("  Pausa 3s...")
            time.sleep(3)

    print(f"\n{'='*60}")
    print(f"RESUMEN: {exitosos} exitosos, {fallidos} fallidos, {len(ARTICULOS)} total")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
