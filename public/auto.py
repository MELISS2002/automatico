import time
import re
import os
import sys
import json
import pyperclip
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# ============================================
# CONFIGURACIÓN
# ============================================
CHROME_DEBUG_PORT = 9222
DEEPSEEK_URL = "https://chat.deepseek.com/"
REPO_PATH = r"C:\Users\dza\Desktop\automatico-main"
POSTS_DIR = os.path.join(REPO_PATH, "public", "posts")
JSON_FILES = {
    "salud": os.path.join(POSTS_DIR, "salud.json"),
    "home": os.path.join(POSTS_DIR, "home.json"),
    "gana": os.path.join(POSTS_DIR, "gana.json")
}
GIT_ACTIVO = True
TIMEOUT_RESPUESTA = 600

def limpiar_texto(texto):
    return re.sub(r'[^\u0000-\uFFFF]', '', texto)

# ============================================
# FUNCIONES SELENIUM
# ============================================
def conectar_chrome():
    options = Options()
    options.add_experimental_option("debuggerAddress", f"127.0.0.1:{CHROME_DEBUG_PORT}")
    return webdriver.Chrome(options=options)

def esperar_respuesta_completa(driver, timeout=TIMEOUT_RESPUESTA):
    print(f"⏳ Esperando respuesta (timeout {timeout}s)...")
    start = time.time()
    copy_detected = False
    while time.time() - start < timeout:
        try:
            copy_btn = driver.find_element(By.XPATH, "//button[@aria-label='Copy']")
            if copy_btn.is_displayed():
                if not copy_detected:
                    print("✅ Botón Copy detectado, esperando estabilización...")
                    copy_detected = True
                    time_after_copy = time.time()
                if copy_detected and (time.time() - time_after_copy > 5):
                    print("✅ Respuesta estable.")
                    return True
        except:
            pass
        time.sleep(1)
    print("⚠️ Tiempo de espera agotado.")
    return False

def obtener_ultimo_mensaje_asistente(driver):
    try:
        asistentes = driver.find_elements(By.XPATH, "//div[@data-role='assistant']")
        if asistentes:
            for elem in reversed(asistentes):
                texto = elem.text.strip()
                if len(texto) > 50:
                    print(f"✅ Extraído del asistente: {len(texto)} caracteres")
                    return texto
    except:
        pass
    try:
        mds = driver.find_elements(By.XPATH, "//div[contains(@class, 'markdown')]")
        for md in reversed(mds):
            texto = md.text.strip()
            if len(texto) > 100:
                print(f"✅ Extraído de markdown: {len(texto)} caracteres")
                return texto
    except:
        pass
    try:
        body = driver.find_element(By.TAG_NAME, "body")
        texto_body = body.text
        lineas = texto_body.splitlines()
        filtradas = [l.strip() for l in lineas if l.strip() and not re.match(r'^(New Chat|Instant|DeepThink|Search|Expert|Vision)$', l.strip(), re.IGNORECASE)]
        respuesta = '\n'.join(filtradas)[-2000:]
        if len(respuesta) > 100:
            print(f"✅ Extraído del body: {len(respuesta)} caracteres")
            return respuesta
    except:
        pass
    return ""

def preguntar_deepseek(prompt, driver):
    input_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//textarea"))
    )
    prompt_limpio = limpiar_texto(prompt)

    pyperclip.copy(prompt_limpio)
    input_box.click()
    time.sleep(0.2)
    actions = ActionChains(driver)
    actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
    time.sleep(0.5)
    if len(prompt_limpio) > 4000:
        time.sleep(1)

    input_box.send_keys(Keys.RETURN)
    print(f"📤 Prompt enviado ({len(prompt_limpio)} caracteres).")

    if not esperar_respuesta_completa(driver):
        print("⚠️ No se detectó fin de respuesta, extrayendo igual...")
    time.sleep(2)
    respuesta = obtener_ultimo_mensaje_asistente(driver)
    return limpiar_texto(respuesta) if respuesta else ""

# ============================================
# LECTURA DE TEMA (ARCHIVO O TEXTO)
# ============================================
def obtener_tema():
    print("\n📝 ¿Cómo quieres ingresar el tema del artículo?")
    print("  1. Escribir un tema corto (ej: 'Beneficios del té verde')")
    print("  2. Usar un archivo .txt (escribe 'archivo' o arrastra el archivo aquí)")
    opcion = input("   Opción (Enter = tema corto): ").strip().lower()

    if opcion in ['archivo', 'file', '2']:
        ruta = input("   Arrastra el archivo .txt o escribe su ruta: ").strip().strip('"')
        if os.path.isfile(ruta):
            with open(ruta, 'r', encoding='utf-8') as f:
                contenido = f.read()
            print(f"✅ Archivo leído: {len(contenido)} caracteres.")
            return contenido
        else:
            print("❌ No se encontró el archivo. Intenta de nuevo.")
            return obtener_tema()

    # Si no es archivo, consideramos que es el tema en sí (texto normal)
    if opcion == "":
        tema = input("   Escribe el tema: ").strip()
        return tema
    else:
        # El usuario escribió directamente un tema (opción 1 implícita)
        return opcion

# ============================================
# RESTO DE FUNCIONES (slug, json, git, etc.)
# ============================================
def tema_a_slug(tema):
    slug = tema.lower().strip()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'\s+', '-', slug)
    slug = re.sub(r'-+', '-', slug).strip('-')
    if len(slug) > 80:
        slug = slug[:80].rstrip('-')
    return slug

def crear_articulo(tema, categoria, driver):
    tema = limpiar_texto(tema)
    slug = tema_a_slug(tema)
    print(f"📝 Creando artículo (slug: {slug})...")

    prompt = f"""
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
    prompt = limpiar_texto(prompt)
    print("📤 Enviando prompt a DeepSeek...")
    respuesta = preguntar_deepseek(prompt, driver)
    
    if not respuesta:
        print("❌ No se recibió respuesta de DeepSeek.")
        return False

    print("📄 Respuesta recibida (primeros 500 chars):", respuesta[:500])

    title = extract_val(respuesta, "TITLE:")
    excerpt = extract_val(respuesta, "EXCERPT:")
    html = extract_between(respuesta, "===HTML_START===", "===HTML_END===")
    thumbnail = extract_val(respuesta, "THUMBNAIL:")

    if not html:
        print("⚠️ Marcadores no encontrados. Buscando bloques de código...")
        bloques = extraer_bloques(respuesta)
        for tipo, contenido in bloques:
            if tipo == 'html' or (tipo == 'code' and ('<html' in contenido.lower() or '<!doctype' in contenido.lower())):
                html = contenido
                print("✅ HTML extraído desde bloque de código.")
                break

    if not html:
        print("⚠️ Buscando HTML directamente en la respuesta...")
        match = re.search(r'(<!DOCTYPE html>.*)', respuesta, re.DOTALL | re.IGNORECASE)
        if match:
            html = match.group(1).strip()
        else:
            match = re.search(r'(<html.*?</html>)', respuesta, re.DOTALL | re.IGNORECASE)
            if match:
                html = match.group(1).strip()
        if html:
            print("✅ HTML encontrado mediante búsqueda directa.")

    if not html:
        print("❌ No se pudo extraer HTML. Respuesta completa de DeepSeek:")
        print(respuesta)
        return False

    html = re.sub(r'^```(?:html)?\s*\n?', '', html.strip())
    html = re.sub(r'\n?```$', '', html.strip())

    if not title:
        title = tema[:50]
    if not excerpt:
        excerpt = "Artículo sobre " + tema[:50]
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
    print(f"✅ HTML guardado en {html_path}")

    json_path = JSON_FILES.get(categoria)
    if not json_path:
        print(f"❌ Categoría desconocida: {categoria}")
        return False

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
        print("❌ Error al actualizar el JSON")
        return False

    print("✅ JSON actualizado correctamente.")
    return True

def extract_val(text, key):
    pattern = rf"{re.escape(key)}\s*(.*?)(?:\n|$)"
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1).strip() if match else ""

def extract_between(text, start, end):
    pattern = rf"{re.escape(start)}\s*(.*?){re.escape(end)}"
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else ""

def extraer_bloques(texto):
    bloques = []
    for match in re.finditer(r'```(\w*)\s*\n(.*?)```', texto, re.DOTALL):
        lang = match.group(1).strip().lower()
        code = match.group(2).strip()
        if not code:
            continue
        lineas = code.splitlines()
        lineas_filtradas = [l for l in lineas if l.strip().lower() not in ['copy', 'copy code', 'download']]
        contenido = '\n'.join(lineas_filtradas).strip()
        if lang in ('python', 'py'):
            bloques.append(('python', contenido))
        elif lang in ('cmd', 'bash', 'shell', 'powershell'):
            bloques.append(('cmd', contenido))
        elif lang in ('html', 'htm') or contenido.lstrip().startswith('<!DOCTYPE') or contenido.lstrip().startswith('<html'):
            bloques.append(('html', contenido))
        else:
            bloques.append(('code', contenido))
    return bloques

def actualizar_json(json_path, nueva_entrada):
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        slugs = [item.get("slug") for item in data]
        if nueva_entrada["slug"] in slugs:
            print("⚠️ El slug ya existe. Se omite.")
            return False
        data.insert(0, nueva_entrada)
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error al manipular JSON: {e}")
        return False

def regenerar_sitemap():
    """Regenera sitemap.xml y robots.txt para que el artículo nuevo quede indexable."""
    script = os.path.join(REPO_PATH, "scripts", "generate_sitemap.py")
    if not os.path.isfile(script):
        print("⚠️ No se encontró scripts/generate_sitemap.py. Omitiendo sitemap.")
        return
    try:
        subprocess.run([sys.executable, script], cwd=REPO_PATH, check=True)
        print("✅ Sitemap regenerado.")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Error al regenerar sitemap: {e}")

def git_commit_and_push(mensaje="Nuevo artículo automático"):
    if not GIT_ACTIVO:
        print("⏸️  Git desactivado. No se subió a GitHub.")
        return
    try:
        regenerar_sitemap()
        subprocess.run(["git", "add", "."], cwd=REPO_PATH, check=True)
        subprocess.run(["git", "commit", "-m", mensaje], cwd=REPO_PATH, check=True)
        subprocess.run(["git", "push"], cwd=REPO_PATH, check=True)
        print("🚀 Cambios subidos a GitHub correctamente.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en Git: {e}")

# ============================================
# PROGRAMA PRINCIPAL
# ============================================
def main():
    print("🤖 PUBLICADOR AUTOMÁTICO DE ARTÍCULOS (SOPORTE TXT)")
    print("=" * 60)
    print("Asegúrate de tener Chrome abierto en puerto 9222 y DeepSeek iniciado.\n")

    tema = obtener_tema()
    tema = limpiar_texto(tema)
    if not tema.strip():
        print("❌ Tema vacío. Saliendo.")
        return

    print("\nCategorías disponibles: salud, home, gana")
    categoria = input("🏷️ Categoría: ").strip().lower()
    if categoria not in JSON_FILES:
        print("❌ Categoría no válida.")
        return

    try:
        driver = conectar_chrome()
    except Exception as e:
        print(f"❌ No se pudo conectar a Chrome: {e}")
        return

    if "deepseek" not in driver.current_url:
        driver.get(DEEPSEEK_URL)
        time.sleep(5)
    print("✅ Sesión de DeepSeek lista.\n")

    exito = crear_articulo(tema, categoria, driver)
    if exito:
        print("\n🎉 Artículo creado con éxito.")
        git_commit_and_push(f"Nuevo artículo: {tema[:50]}")
    else:
        print("\n❌ No se pudo completar la creación del artículo.")

    driver.quit()

if __name__ == "__main__":
    main()