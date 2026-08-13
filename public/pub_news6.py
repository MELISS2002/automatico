# pub_news6.py — genera 5 articulos de noticias con imagenes REALES locales
# patron exacto de pub_api.py: curl --data @_body.json (sin max_tokens)
import sys, os, re, json, time, shutil, subprocess, unicodedata

sys.path.insert(0, r'C:\Users\dza\Desktop\automatico-main\public')
import auto1

API = 'http://127.0.0.1:8765/v1/chat/completions'
IMG_SRC = r'C:\Users\dza\Desktop\neo\tools\news-imgs-final'
POSTS = r'C:\Users\dza\Desktop\automatico-main\public\posts'
HERE = os.path.dirname(os.path.abspath(__file__))

ARTICULOS = [
    {
        "tema": "Terremoto en Colombia de magnitud 7,4: al menos 111 muertos y 87 heridos, segun el presidente Abelardo de la Espriella",
        "cat": "home",
        "slug": "terremoto-colombia-111-muertos-87-heridos-espriella",
        "imgs": ["terremoto-colombia.jpg", "terremoto-colombia-1.jpg", "terremoto-colombia-2.jpg"],
        "nota": "Noticia real del 10 de agosto de 2026 (EFE/RPP): un terremoto de magnitud 7,4 sacudio la mayor parte de Colombia este lunes. Epicentro en San Jose del Palmar, departamento de Choco, con profundidad cercana a los 100 kilometros. El presidente Abelardo de la Espriella, en su primera declaracion publica en Bogota, reporto una cifra parcial de 111 fallecidos, 87 heridos, 1.575 viviendas averiadas, 37 completamente destruidas, 61 edificios colapsados, 18 centros de salud y 52 centros educativos averiados, con destruccion en al menos cinco departamentos. El balance fue dado a las 12:30 (17:30 GMT). La presidenta de Peru, Keiko Fujimori, se solidarizo con Colombia y ofrecio apoyo; la Cancilleria peruana informo que hasta el momento no hay peruanos afectados y activo lineas de emergencia para connacionales."
    },
    {
        "tema": "Colombia y otros siete paises del Cinturon de Fuego ya sufrieron terremotos en 2026: 'En algun momento ocurrira en Peru', senala el IGP",
        "cat": "home",
        "slug": "igp-cinturon-de-fuego-terremotos-2026-peru",
        "imgs": ["igp-cinturon.jpg", "igp-cinturon-1.jpg", "igp-cinturon-2.jpg"],
        "nota": "Noticia real de Infobae (10 de agosto de 2026): tras el terremoto de magnitud 7,4 en Colombia, Fernando Tavera, presidente del Instituto Geofisico del Peru (IGP), analizo el riesgo para el Peru. El Cinturon de Fuego del Pacifico libera mas del 80% de la energia sismica anual del planeta y en el se ubican paises como Peru, Ecuador, Chile y Colombia. Ademas de Colombia, en 2026 ya registraron fuertes terremotos Mexico, Filipinas, Japon, Indonesia, Vanuatu, Tonga y Chile (ocho paises en total). Tavera advirtio que la sucesion de terremotos no significa que exista una cadena que permita anticipar un gran sismo en Peru, pero que 'en algun momento ocurrira en Peru', por lo que pidio prevencion, simulacros y planificacion familiar ante sismos."
    },
    {
        "tema": "Harvey Colchado puso su cargo a disposicion en la Comision de Etica tras pedido de prision efectiva en su contra",
        "cat": "home",
        "slug": "harvey-colchado-cargo-disposicion-comision-etica",
        "imgs": ["colchado.jpg", "colchado-1.jpg", "colchado-2.jpg"],
        "nota": "Noticia real de RPP (10 de agosto de 2026): la Comision de Etica de la Camara de Diputados quedo instalada este lunes en la Sala Fabiola Salazar Leguia. Durante la sesion, Harvey Colchado (Ahora Nacion) puso su cargo a disposicion del pleno, luego de que la Fiscalia solicitara 9 anos y 4 meses de prision efectiva en su contra por los presuntos delitos de negociacion incompatible y falsedad ideologica. Colchado condiciono su permanencia a que sus demas integrantes le ratifiquen la confianza. La mesa directiva de la comision se elegira el martes 11 de agosto. El congresista Javier Cipriani lo acuso de obstaculizar el trabajo de la comision con su renuncia."
    },
    {
        "tema": "MEF plantea ajustes a los regimenes tributarios: el cambio para el pago del Impuesto a la Renta",
        "cat": "gana",
        "slug": "mef-ajustes-regimenes-tributarios-impuesto-renta",
        "imgs": ["mef-renta.jpg", "mef-renta-1.jpg", "mef-renta-2.jpg"],
        "nota": "Noticia real de Gestion (10 de agosto de 2026): el ministro de Economia y Finanzas, Elmer Cuba, adelanto en una entrevista los proximos pasos de las comisiones presidenciales anunciadas el viernes, que abordaran cuatro frentes: informalidad, inversion publica, mercados financieros y evasion tributaria. Entre los ajustes se plantean cambios a los regimenes tributarios, incluida la forma de pago del Impuesto a la Renta. El MEF tambien anuncio el alza del salario minimo en dos tramos, el reajuste de feriados (pasarian a los lunes salvo excepciones) y el cambio de reglas fiscales. El MEF critico ademas el alza de pensiones de militares y policias: 'Nadie se jubila al 100% del ultimo sueldo'."
    },
    {
        "tema": "AFP Integra dara el salto a compania de seguros: ya presento solicitud ante la SBS, revela su CEO Aldo Ferrini",
        "cat": "gana",
        "slug": "afp-integra-compania-seguros-solicitud-sbs",
        "imgs": ["afp-integra.jpg", "afp-integra-1.jpg", "afp-integra-2.jpg"],
        "nota": "Noticia real de El Comercio DIA1 (10 de agosto de 2026): Aldo Ferrini, gerente general de AFP Integra, del grupo Sura, revelo en exclusiva que la administradora de fondos ya presento una solicitud ante la SBS para transformarse en una empresa de seguros y pensiones. 'Estamos entrando a un proceso para pasar de AFP a una compania de seguros', afirmo. Apuntan como fecha tentativa a recibir la autorizacion de empresa de seguros hacia octubre. En una etapa inicial preveen enfocarse en rentas particulares."
    }
]

def preguntar(tema, nota, slug):
    prompt = f"""Eres un redactor y disenador web experto de un portal de noticias peruano. Crea un articulo periodistico completo en HTML sobre esta noticia real de actualidad (minimo 1000 palabras):

TEMA: {tema}

DATOS REALES DE LA NOTICIA (usa estos datos, no inventes cifras):
{nota}

REGLAS OBLIGATORIAS:
- Estilo periodistico serio, en espanol neutro, tono informativo. NO uses clickbait.
- Incluye EXACTAMENTE 3 imagenes usando rutas locales: imagen1.jpg, imagen2.jpg e imagen3.jpg (src="imagen1.jpg", src="imagen2.jpg", src="imagen3.jpg"). Colocalas en el featured header y en puntos relevantes del cuerpo.
- El HTML debe tener estilos CSS atractivos, responsive, con header de noticia, parrafos, subtitulos, bloques de datos destacados y footer.
- NO uses backticks (```) en tu respuesta. NO uses emojis. NO uses markdown.
- Responde EXACTAMENTE con esta estructura (respeta los marcadores):

TITLE: (titulo periodistico)
EXCERPT: (extracto 2-3 frases)
===HTML_START===
(ESCRIBE AQUI TODO EL CODIGO HTML: <!DOCTYPE html>, <head>, <style>, <body>, IMAGENES LOCALES imagen1.jpg imagen2.jpg imagen3.jpg, ETC.)
===HTML_END===
THUMBNAIL: imagen1.jpg"""
    prompt = auto1.limpiar_texto(prompt)
    body = json.dumps({"model": "deepseek-web", "messages": [{"role": "user", "content": prompt}]})
    p = os.path.join(HERE, "_body.json")
    with open(p, "w", encoding="utf-8") as f:
        f.write(body)
    r = subprocess.run(["curl.exe", "-s", "-m", "570", "-X", "POST", API,
                        "-H", "Content-Type: application/json", "--data", "@" + p],
                       capture_output=True, timeout=590)
    if r.returncode != 0:
        raise RuntimeError(f"curl rc={r.returncode}")
    try:
        data = json.loads(r.stdout.decode("utf-8", errors="replace"))
    except Exception as e:
        raise RuntimeError(f"JSON invalido: {e} | stdout={r.stdout[:200]}")
    return data.get("content") or data.get("choices", [{}])[0].get("message", {}).get("content") or ""

def guardar(respuesta, art):
    slug = art['slug']
    title = auto1.extract_val(respuesta, "TITLE:") or art['tema'][:60]
    excerpt = auto1.extract_val(respuesta, "EXCERPT:")
    html = auto1.extract_between(respuesta, "===HTML_START===", "===HTML_END===")
    if not html:
        for tipo, contenido in auto1.extraer_bloques(respuesta):
            if tipo == 'html' or (tipo == 'code' and ('<html' in contenido.lower() or '<!doctype' in contenido.lower())):
                html = contenido
                break
    if not html:
        m = re.search(r'(<!DOCTYPE html>.*)', respuesta, re.DOTALL | re.IGNORECASE)
        html = m.group(1).strip() if m else None
    if not html:
        return None, "sin HTML"
    html = re.sub(r'^```(?:html)?\s*\n?', '', html.strip())
    html = re.sub(r'\n?```$', '', html.strip())
    # reemplazar cualquier pollinations por imagen1.jpg
    html = re.sub(r'https://image\.pollinations\.ai/[^"\']+', 'imagen1.jpg', html)
    # si no hay <!DOCTYPE>, envolver
    if not html.strip().startswith('<!DOCTYPE html>') and not html.strip().startswith('<html'):
        html = f"<!DOCTYPE html>\n<html lang=\"es\">\n<head><meta charset=\"UTF-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"><title>{title}</title></head>\n<body>\n{html}\n</body>\n</html>"
    # sincronizar title con <title> del HTML
    t_html = re.search(r"<title>(.*?)</title>", html, re.S)
    if t_html:
        t_html = t_html.group(1).strip()
    if t_html and (len(title) > len(t_html) + 20 or not title):
        title = t_html
    if not title:
        title = art['tema'][:60]
    if not excerpt:
        excerpt = "Noticia: " + art['tema'][:120]
    # carpeta + imagenes
    carpeta = os.path.join(POSTS, slug)
    os.makedirs(carpeta, exist_ok=True)
    for j, img in enumerate(art['imgs']):
        src = os.path.join(IMG_SRC, img)
        dst = os.path.join(carpeta, f"imagen{j+1}.jpg")
        if os.path.isfile(src):
            shutil.copy2(src, dst)
    p = os.path.join(carpeta, "index.html")
    with open(p, "w", encoding="utf-8") as f:
        f.write(html)
    nueva = {"slug": slug, "title": title, "author": "ROSA EMILY", "date": time.strftime("%Y-%m-%d"),
             "excerpt": excerpt, "thumbnail": f"/posts/{slug}/imagen1.jpg", "htmlPath": f"/posts/{slug}/index.html"}
    if not auto1.actualizar_json(auto1.JSON_FILES[art['cat']], nueva):
        return None, "JSON duplicado"
    return {"title": title, "html_path": p}, None

if __name__ == "__main__":
    solo = sys.argv[1] if len(sys.argv) > 1 else None
    resultados = []
    for i, art in enumerate(ARTICULOS, 1):
        if solo and solo not in art['slug']:
            continue
        print(f"\n=== [{i}/{len(ARTICULOS)}] {art['slug']}", flush=True)
        ok_final = False
        for intento in (1, 2):
            try:
                print(f"[intento {intento}] preguntando a DeepSeek...", flush=True)
                resp = preguntar(art['tema'], art['nota'], art['slug'])
                print(f"[intento {intento}] respuesta {len(resp)} chars", flush=True)
                guardado, err = guardar(resp, art)
                if err:
                    print(f"[intento {intento}] error guardado: {err}", flush=True)
                else:
                    p = guardado["html_path"]
                    sz = os.path.getsize(p)
                    txt = open(p, encoding="utf-8", errors="replace").read().lower()
                    n_img = txt.count('imagen1.jpg') + txt.count('imagen2.jpg') + txt.count('imagen3.jpg')
                    print(f"[intento {intento}] OK: {guardado['title'][:70]} | size={sz} refs_imagenes={n_img}", flush=True)
                    if sz > 8000 and n_img >= 2:
                        ok_final = True
                        break
                    else:
                        shutil.rmtree(os.path.dirname(p), ignore_errors=True)
                        gp = auto1.JSON_FILES.get(art['cat'])
                        data = json.load(open(gp, encoding="utf-8"))
                        data = [e for e in data if e["slug"] != art['slug']]
                        json.dump(data, open(gp, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
                        print(f"[intento {intento}] contenido no valido (size={sz} imgs={n_img}), reintentando...", flush=True)
            except Exception as e:
                print(f"[intento {intento}] ERROR: {repr(e)}", flush=True)
            time.sleep(5)
        resultados.append((art['slug'], ok_final))
    print("\n=== RESUMEN ===", flush=True)
    for s, ok in resultados:
        print(("OK " if ok else "FAIL ") + s, flush=True)
    print("FIN_BATCH", flush=True)
