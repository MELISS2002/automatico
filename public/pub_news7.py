# pub_news7.py — batch 7: 5 articulos reales (3 salud + 2 gana) con fotos reales
import sys, os, re, json, time, shutil, subprocess

sys.path.insert(0, r'C:\Users\dza\Desktop\automatico-main\public')
import auto1

API = 'http://127.0.0.1:8765/v1/chat/completions'
IMG_SRC = r'C:\Users\dza\Desktop\neo\tools\news-imgs-final'
POSTS = r'C:\Users\dza\Desktop\automatico-main\public\posts'
HERE = os.path.dirname(os.path.abspath(__file__))

ARTICULOS = [
    {
        "tema": "Resultados SERUMS 2026-II: cuando y donde se publicara la lista de aprobados de la evaluacion del Minsa",
        "cat": "salud",
        "slug": "resultados-serums-2026-ii-lista-aprobados-minsa",
        "imgs": ["serums-1.jpg", "serums-2.jpg", "serums-3.jpg"],
        "nota": "Noticia real de Infobae Peru (publicada 9-10 de agosto de 2026): mas de 23 mil profesionales de ciencias de la salud participaron el domingo 9 de agosto en la evaluacion correspondiente al SERUMS 2026-II (Servicio Rural y Urbano Marginal de Salud), un proceso que forma parte de la adjudicacion de plazas para dicho servicio. La prueba convoco a profesionales de 12 carreras de ciencias de la salud inscritos para esta etapa. La jornada se realizo de forma presencial en 29 sedes distribuidas a nivel nacional. Segun el cronograma oficial del Ministerio de Salud (Minsa), la lista con los resultados finales de la Evaluacion para el SERUMS 2026-II sera publicada el viernes 14 de agosto de 2026 en la pagina web del Minsa. El calendario fue elaborado por el Equipo Tecnico Nacional del SERUMS, la Direccion de Planificacion (DIPLAN) y la Direccion General de Personal de la Salud (DIGEP), con fecha 14 de julio de 2026. La publicacion de resultados corresponde a la septima etapa del proceso, despues de la convocatoria, las inscripciones, la publicacion de participantes inscritos y la aplicacion de la evaluacion."
    },
    {
        "tema": "Tumbes reforzara prevencion contra el dengue con arribo de lote con 26,000 dosis de vacuna",
        "cat": "salud",
        "slug": "tumbes-dengue-26000-dosis-vacuna-prevencion",
        "imgs": ["dengue-1.jpg", "dengue-2.jpg", "dengue-3.jpg"],
        "nota": "Noticia real de la Agencia Andina (10 de agosto de 2026): un importante lote con 26,160 dosis de la vacuna tetravalente contra el dengue recibio la Direccion Regional de Salud (Diresa) de Tumbes. El arribo de estos medicamentos permitira fortalecer las acciones de prevencion contra esta enfermedad antes del inicio de la temporada de lluvias prevista para los ultimos meses de este ano. La llegada de estas vacunas responde a la priorizacion establecida por el Ministerio de Salud (Minsa) para las zonas con mayor riesgo epidemiologico de dengue, entre ellas Tumbes. La directora regional de Salud, Eslhy Yacila Preciado, destaco que la vacunacion constituye una herramienta adicional para reducir el riesgo de complicaciones y hospitalizaciones asociadas al dengue. Segun las disposiciones del Minsa, la estrategia de vacunacion contempla a la poblacion objetivo de 10 a 20 anos y personal de salud, Fuerzas Armadas y PNP menores de 59 anos. El esquema contempla dos dosis, con un intervalo de tres meses entre ambas. La Diresa Tumbes recordo que la vacunacion no reemplaza las medidas de prevencion y control del mosquito Aedes aegypti, transmisor de la enfermedad."
    },
    {
        "tema": "Lima Provincias: Minsa Movil supera las 5700 atenciones en salud en despliegue medico en las provincias de Huaura y Oyon",
        "cat": "salud",
        "slug": "minsa-movil-5700-atenciones-huaura-oyon",
        "imgs": ["minsa-1.jpg", "minsa-2.jpg", "minsa-3.jpg"],
        "nota": "Noticia real de gob.pe - Ministerio de Salud (10 de agosto de 2026): el Minsa, a traves de la estrategia Salud en Accion de Minsa Movil, culmino con exito una importante jornada de atencion medica especializada en las provincias de Huaura y Oyon, en la region Lima. Durante los cuatro dias de intervencion, se alcanzaron un total de 5718 atenciones, lo que beneficio a cientos de personas con servicios de salud gratuitos. La campana se desarrollo del 4 al 7 de agosto y permitio que ninos, jovenes, adultos y adultos mayores accedieran a consultas con medicos especialistas. El despliegue inicio en el centro poblado de Chiuchin, en la provincia de Huaura, donde se realizaron 3576 atenciones, y continuo en el centro poblado Colcapampa de Mani, en la provincia de Oyon, con 2142 atenciones. La poblacion accedio a consultas en ginecologia, neumologia, oftalmologia, endocrinologia, cardiologia, otorrinolaringologia y dermatologia, ademas de medicina general, nutricion, psicologia, optometria, inmunizaciones y tamizajes de VIH y sifilis. Tambien se hizo entrega gratuita de lentes de lectura y medicamentos."
    },
    {
        "tema": "Peru es el tercer pais mas informal de America Latina: las medidas del Gobierno de Keiko Fujimori para reducir la informalidad",
        "cat": "gana",
        "slug": "peru-tercer-pais-informal-america-latina-oit",
        "imgs": ["informal-1.jpg", "informal-2.jpg", "informal-3.jpg"],
        "nota": "Noticia real de Gestion (10 de agosto de 2026): un reciente informe de la Organizacion Internacional del Trabajo (OIT) ubica a Peru como el tercer pais mas informal de America Latina. Especialistas analizan si los recientes anuncios del Gobierno podran reducir la tasa de informalidad en el Peru y ubicar mejor al pais a nivel regional. Dos dias despues de Fiestas Patrias, la presidenta Keiko Fujimori dio anuncios en materia laboral en su Mensaje a la Nacion, y la OIT publico un informe que pone en cifras el reto enorme que enfrentara su Gobierno en este rubro. Ya con Juan Sheput como titular del MTPE, se han tomado decisiones que especialistas consideran que pueden abrir un espacio para seguir los consejos de la OIT. El contexto es complejo: la agricultura enfrenta un 94% de informalidad, y mientras la IA avanza, los jovenes quedan atrapados en la informalidad. El Gobierno tambien anuncio el alza del salario minimo en dos tramos."
    },
    {
        "tema": "Rentabilidad de cajas se duplica: en cual ahorra usted",
        "cat": "gana",
        "slug": "rentabilidad-cajas-municipales-se-duplica",
        "imgs": ["cajas-1.jpg", "cajas-2.jpg", "cajas-3.jpg"],
        "nota": "Noticia real de Gestion (10 de agosto de 2026): la utilidad neta de las cajas municipales se elevo en los ultimos doce meses, mientras que la morosidad descendio de 6.1% a 5.1%. Las cajas municipales, cajas rurales y las empresas de credito cerraron un buen primer semestre, impulsadas por la recuperacion de la actividad economica, una mejora en la calidad de la cartera de creditos y mayor dinamismo en el financiamiento. Ademas, las cajas podran comercializar fondos de AFP que rinden hasta 20%, con Integra y Habitat en la mira. El contexto regulatorio tambien avanza: la SBS agilizara la licencia a empresas de credito, y se preve la llegada de mas entidades financieras 100% digitales. (Foto: Andina)"
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
    html = re.sub(r'https://image\.pollinations\.ai/[^"\']+', 'imagen1.jpg', html)
    if not html.strip().startswith('<!DOCTYPE html>') and not html.strip().startswith('<html'):
        html = f"<!DOCTYPE html>\n<html lang=\"es\">\n<head><meta charset=\"UTF-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"><title>{title}</title></head>\n<body>\n{html}\n</body>\n</html>"
    t_html = re.search(r"<title>(.*?)</title>", html, re.S)
    if t_html:
        t_html = t_html.group(1).strip()
    if t_html and (len(title) > len(t_html) + 20 or not title):
        title = t_html
    if not title:
        title = art['tema'][:60]
    if not excerpt:
        excerpt = "Noticia: " + art['tema'][:120]
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
