# -*- coding: utf-8 -*-
r"""crear_lote_v2.py - Generador de lote de articulos MODERNO (sin Selenium, sin pollinations).

Lee C:\Users\dza\Desktop\automatico-main\public\lote_diario.json con la estructura:
  [
    {
      "tema": "titulo periodistico del dia",
      "cat": "home|salud|gana",
      "slug": "slug-limpio",
      "nota": "datos reales de la noticia (hechos, cifras, fuentes) para que el LLM no invente",
      "imgs": ["imagen1.jpg","imagen2.jpg","imagen3.jpg"]   # archivos locales ya descargados
    }, ...
  ]

Genera cada articulo via API local DeepSeek (http://127.0.0.1:8765) pidiendo:
  - HTML periodistico serio, estilo noticia del dia (NO pollinations, NO emojis, NO backticks)
  - 3 imagenes LOCALES (imagen1.jpg/imagen2.jpg/imagen3.jpg) referenciadas en el HTML
  - thumbnail local /posts/<slug>/imagen1.jpg
Guarda el post en public/posts/<slug>/ y actualiza el JSON de su categoria.
NO hace git (el commit lo hace el orquestador publicar_diario.ps1, quirurgico).

Uso:
  python crear_lote_v2.py [--slug abc]   (opcional: solo ese slug)
  exporta/comprueba PYTHONIOENCODING=utf-8 antes de correr (ver orquestador).
"""
import sys, os, io, json, time, re, subprocess, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
os.environ.setdefault("PYTHONIOENCODING", "utf-8")

from auto1 import (extract_val, extract_between, extraer_bloques,
                   actualizar_json, JSON_FILES, POSTS_DIR, limpiar_texto,
                   tema_a_slug)

API_URL = os.environ.get("DEEPSEEK_URL", "http://127.0.0.1:8765/v1/chat/completions")
MODEL = "deepseek-web"
LOTE = os.path.join(HERE, "lote_diario.json")

def cargar_lote():
    with open(LOTE, encoding="utf-8") as f:
        return json.load(f)

def build_prompt(tema, nota):
    return f"""Eres un redactor y disenador web experto de un portal de noticias peruano. Crea un articulo periodistico completo en HTML sobre esta noticia real de actualidad (minimo 1000 palabras):

TEMA: {tema}

DATOS REALES DE LA NOTICIA (usa estos datos, NO inventes cifras, fechas ni nombres):
{nota}

REGLAS OBLIGATORIAS:
- Estilo periodistico serio, en espanol neutro y tono informativo. NO uses clickbait. NO inventes datos; apoyate solo en los DATOS REALES provistos.
- Incluye EXACTAMENTE 3 imagenes usando rutas LOCALES: imagen1.jpg, imagen2.jpg e imagen3.jpg (src="imagen1.jpg", src="imagen2.jpg", src="imagen3.jpg"). Coloca imagen1.jpg en el header destacado y las otras dos en puntos relevantes del cuerpo.
- El HTML debe tener estilos CSS atractivos y responsive, con header de noticia, parrafos, subtitulos, bloques de datos destacados y footer con autor y fecha.
- NO uses backticks (```). NO uses emojis. NO uses markdown. NO uses https://image.pollinations.ai ni URLs externas para imagenes.

Responde EXACTAMENTE con esta estructura (respeta los marcadores):

TITLE: (titulo periodistico)
EXCERPT: (extracto 2-3 frases)
===HTML_START===
(ESCRIBE AQUI TODO EL CODIGO HTML: <!DOCTYPE html>, <head>, <style>, <body>, con las IMAGENES LOCALES imagen1.jpg imagen2.jpg imagen3.jpg, y <footer> con autor y fecha)
===HTML_END===
THUMBNAIL: imagen1.jpg"""

def call_api(prompt):
    body = json.dumps({"model": MODEL,
                       "messages": [{"role": "user", "content": prompt}],
                       "temperature": 0.7})
    p = os.path.join(HERE, "_lote_body.json")
    with open(p, "w", encoding="utf-8") as f:
        f.write(body)
    r = subprocess.run(["curl.exe", "-s", "-m", "570", "-X", "POST", API_URL,
                        "-H", "Content-Type: application/json", "--data", "@" + p],
                       capture_output=True, timeout=590)
    if r.returncode != 0:
        raise RuntimeError(f"curl rc={r.returncode}")
    try:
        data = json.loads(r.stdout.decode("utf-8", errors="replace"))
    except Exception as e:
        raise RuntimeError(f"JSON invalido del LLM: {e} | stdout={r.stdout[:300]}")
    return (data.get("content")
            or data.get("choices", [{}])[0].get("message", {}).get("content")
            or "")

def guardar(respuesta, art):
    slug = art["slug"]
    tema = art["tema"]
    title = extract_val(respuesta, "TITLE:") or tema[:60]
    excerpt = extract_val(respuesta, "EXCERPT:")
    html = extract_between(respuesta, "===HTML_START===", "===HTML_END===")
    if not html:
        for tipo, contenido in extraer_bloques(respuesta):
            if tipo == "html" or (tipo == "code" and ("<html" in contenido.lower() or "<!doctype" in contenido.lower())):
                html = contenido
                break
    if not html:
        m = re.search(r"(<!DOCTYPE html>.*)", respuesta, re.DOTALL | re.IGNORECASE)
        html = m.group(1).strip() if m else None
    if not html:
        return None, "sin HTML"

    html = re.sub(r"^```(?:html)?\s*\n?", "", html.strip())
    html = re.sub(r"\n?```$", "", html.strip())
    # eliminar cualquier referencia a pollinations / URLs externas de imagen
    html = re.sub(r"https?://image\.pollinations\.ai/[^\"')\s]+", "imagen1.jpg", html)
    html = re.sub(r"https?://[^\"')\s]+\.(?:jpg|jpeg|png|webp)[^\"')\s]*", "imagen1.jpg", html)

    if not html.strip().startswith("<!DOCTYPE html>") and not html.strip().startswith("<html"):
        html = f"<!DOCTYPE html>\n<html lang=\"es\">\n<head><meta charset=\"UTF-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"><title>{title}</title></head>\n<body>\n{html}\n</body>\n</html>"

    # sincronizar title con el <title> del HTML si este es mejor
    t = re.search(r"<title>(.*?)</title>", html, re.S)
    if t:
        tn = t.group(1).strip()
        if tn and (len(tn) > len(title) or not title):
            title = tn
    if not excerpt:
        excerpt = "Noticia: " + tema[:120]
    if "<footer>" not in html and "</body>" in html:
        html = html.replace("</body>",
            f"<footer style=\"text-align:center;padding:20px 10px;font-size:0.85em;color:#777;border-top:1px solid #ddd;margin-top:30px\"><p>Autor: ROSA EMILY | Fecha: {time.strftime('%Y-%m-%d')}</p></footer>\n</body>")

    carpeta = os.path.join(POSTS_DIR, slug)
    os.makedirs(carpeta, exist_ok=True)
    # copiar imagenes locales de art['imgs'] a imagen1/2/3.jpg
    imgs = art.get("imgs") or ["imagen1.jpg", "imagen2.jpg", "imagen3.jpg"]
    img_dir = art.get("img_dir") or os.path.join(HERE, "imgs_lote")
    n_copy = 0
    for j, imgname in enumerate(imgs[:3], 1):
        src = os.path.join(img_dir, imgname)
        dst = os.path.join(carpeta, f"imagen{j}.jpg")
        if os.path.isfile(src):
            shutil.copy2(src, dst)
            n_copy += 1
    p = os.path.join(carpeta, "index.html")
    with open(p, "w", encoding="utf-8") as f:
        f.write(html)

    nueva = {"slug": slug, "title": title, "author": "ROSA EMILY",
             "date": time.strftime("%Y-%m-%d"), "excerpt": excerpt,
             "thumbnail": f"/posts/{slug}/imagen1.jpg",
             "htmlPath": f"/posts/{slug}/index.html"}
    if not actualizar_json(JSON_FILES[art["cat"]], nueva):
        return None, "JSON duplicado (slug ya existe)"
    return {"title": title, "html_path": p, "imgs_copiadas": n_copy}, None

def main():
    solo = None
    if "--slug" in sys.argv:
        solo = sys.argv[sys.argv.index("--slug") + 1]
    lote = cargar_lote()
    resultados = []
    for i, art in enumerate(lote, 1):
        if solo and solo not in art.get("slug", ""):
            continue
        print(f"\n=== [{i}/{len(lote)}] {art.get('slug')}", flush=True)
        if art.get("cat") not in JSON_FILES:
            print(f"[{i}] FAIL: categoria invalida '{art.get('cat')}'", flush=True)
            resultados.append((art.get("slug"), False))
            continue
        ok_final = False
        for intento in (1, 2):
            try:
                print(f"[intento {intento}] preguntando a DeepSeek...", flush=True)
                resp = call_api(build_prompt(art["tema"], art.get("nota", "")))
                print(f"[intento {intento}] respuesta {len(resp)} chars", flush=True)
                guardado, err = guardar(resp, art)
                if err:
                    print(f"[intento {intento}] error guardado: {err}", flush=True)
                else:
                    p = guardado["html_path"]
                    sz = os.path.getsize(p)
                    txt = open(p, encoding="utf-8", errors="replace").read().lower()
                    n_img = sum(txt.count(f"imagen{j}.jpg") for j in (1, 2, 3))
                    print(f"[intento {intento}] OK: {guardado['title'][:70]} | size={sz} imgs_copiadas={guardado['imgs_copiadas']} refs_imagenes={n_img}", flush=True)
                    # validacion: HTML grande + al menos 2 refs a imagenes locales + imgs copiadas
                    if sz > 8000 and n_img >= 2 and guardado["imgs_copiadas"] >= 1:
                        ok_final = True
                        break
                    else:
                        shutil.rmtree(os.path.dirname(p), ignore_errors=True)
                        gp = JSON_FILES.get(art["cat"])
                        if gp and os.path.isfile(gp):
                            data = json.load(open(gp, encoding="utf-8"))
                            data = [e for e in data if e.get("slug") != art.get("slug")]
                            json.dump(data, open(gp, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
                        print(f"[intento {intento}] contenido no valido (size={sz} imgs={n_img} copiadas={guardado['imgs_copiadas']}), reintentando...", flush=True)
            except Exception as e:
                print(f"[intento {intento}] ERROR: {repr(e)}", flush=True)
            time.sleep(5)
        resultados.append((art.get("slug"), ok_final))
    print("\n=== RESUMEN ===", flush=True)
    for s, ok in resultados:
        print(("OK  " if ok else "FAIL ") + s, flush=True)
    print("FIN_BATCH", flush=True)

if __name__ == "__main__":
    main()