# pub_noticias.py — publica artículos de las noticias más destacadas del día vía API local deepseek-server (8765).
import sys, os, re, time, json, subprocess, unicodedata, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import auto1

API = "http://127.0.0.1:8765/v1/chat/completions"
NEO = r"C:\Users\dza\Desktop\neo\tools\neo.cjs"
NEO_OPEN = ["node", NEO, "open", "https://chat.deepseek.com/"]

PLANTILLA = """Eres un redactor y diseñador web experto. Crea un artículo completo en HTML sobre "{tema}" (mínimo 1000 palabras). 
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

def nuevo_chat():
    subprocess.run(NEO_OPEN, capture_output=True, timeout=60)
    time.sleep(4)

def preguntar(tema):
    prompt = auto1.limpiar_texto(PLANTILLA.format(tema=tema))
    body = json.dumps({"model": "deepseek-web", "messages": [{"role": "user", "content": prompt}]})
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_body.json")
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
        raise RuntimeError(f"JSON inválido: {e} | stdout={r.stdout[:200]}")
    return data.get("content") or data.get("choices", [{}])[0].get("message", {}).get("content") or ""

def guardar(respuesta, tema, cat, slug):
    title = auto1.extract_val(respuesta, "TITLE:")
    excerpt = auto1.extract_val(respuesta, "EXCERPT:")
    html = auto1.extract_between(respuesta, "===HTML_START===", "===HTML_END===")
    thumbnail = auto1.extract_val(respuesta, "THUMBNAIL:")
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
    if not excerpt:
        excerpt = "Artículo sobre " + tema[:50]
    if not thumbnail or not thumbnail.startswith("http"):
        thumbnail = f"https://image.pollinations.ai/prompt/{slug}-thumbnail"
    carpeta = os.path.join(auto1.POSTS_DIR, slug)
    os.makedirs(carpeta, exist_ok=True)
    p = os.path.join(carpeta, "index.html")
    t_html = re.search(r"<title>(.*?)</title>", html, re.S)
    if t_html:
        t_html = t_html.group(1).strip()
    if (not title) or (t_html and len(title) > len(t_html) + 20):
        if t_html:
            title = t_html
    if not title:
        title = tema[:60]
    with open(p, "w", encoding="utf-8") as f:
        f.write(html)
    nueva = {"slug": slug, "title": title, "author": "ROSA EMILY", "date": time.strftime("%Y-%m-%d"),
             "excerpt": excerpt, "thumbnail": thumbnail, "htmlPath": f"/posts/{slug}/index.html"}
    if not auto1.actualizar_json(auto1.JSON_FILES[cat], nueva):
        return None, "JSON duplicado"
    return {"title": title, "html_path": p}, None

ARTICULOS = [
    (
        """Junín sigue temblando: esta madrugada se registró un sismo de magnitud 4.3 en Chupaca a las 11:05 de la noche y horas después otro de magnitud 4.7; el IGP explica que las réplicas continúan porque la zona sigue liberando energía. Escribe un artículo periodístico informativo sobre los sismos en Junín de agosto de 2026: qué pasó exactamente (fechas, horas, magnitudes, epicentros), qué dice el IGP sobre por qué continúan las réplicas, cómo reaccionó la población y las autoridades, la ayuda humanitaria (Indeci enviará 111 toneladas a Junín para atender a los damnificados), la promesa del gobierno de construir viviendas y las quejas de los damnificados por la lentitud, y consejos prácticos de qué hacer durante un sismo (mochila de emergencia, puntos de reunión, zonas seguras). Párrafos cortos, tono cercano y humano de periodista peruano, con datos concretos, sin relleno. Debe leerse como si lo hubiera escrito una persona, no una máquina.""",
        "home",
        "sismos-junin-replicas-chupaca-ayuda-humanitaria",
    ),
    (
        """La encuesta nacional de Datum reveló que Keiko Fujimori inicia su gobierno con 60% de aprobación ciudadana, una cifra histórica para un presidente peruano en sus primeros días. Escribe un artículo periodístico informativo sobre la encuesta Datum de agosto de 2026: los resultados (60% de aprobación, ¿cuánta desaprobación tiene?), dónde tiene mayor respaldo (regiones, zonas urbanas vs rurales, niveles socioeconómicos), qué factores explican esta popularidad inicial (el discurso del 28 de julio, la lucha contra la delincuencia, las promesas de orden y paz), cómo se compara con aprobaciones iniciales de presidentes anteriores, qué retos enfrenta el nuevo gobierno para mantener ese respaldo (seguridad ciudadana, economía, reconstrucción tras el sismo en Junín) y qué dice la encuesta sobre las expectativas de la población. Párrafos cortos, tono cercano y humano de periodista peruano, con datos concretos, sin relleno. Debe leerse como si lo hubiera escrito una persona, no una máquina.""",
        "home",
        "keiko-fujimori-60-aprobacion-encuesta-datum",
    ),
    (
        """Netanyahu anunció que Israel rechaza el plan de 15 puntos para Gaza propuesto por Trump, y el gabinete israelí también rechazó una tregua de 14 días pese a la presión de Estados Unidos; Israel dice que no se retirará hasta que Hamás se desarme. Escribe un artículo periodístico informativo sobre esta noticia internacional: qué propone exactamente el plan de 15 puntos de Trump para Gaza, por qué Netanyahu lo rechaza, qué dijo el gabinete israelí sobre la tregua de 14 días, la postura de Hamás (que dice que sigue dispuesto a avanzar con el plan de paz), el papel de Estados Unidos y la presión internacional, y qué podría pasar ahora en la región. Párrafos cortos, tono cercano y humano de periodista, con datos concretos, sin relleno. Debe leerse como si lo hubiera escrito una persona, no una máquina.""",
        "home",
        "israel-rechaza-plan-gaza-netanyahu-treusa",
    ),
    (
        """Un Fenómeno El Niño furioso amenaza Sudamérica: los científicos pronostican que el Pacífico alcanzará una anomalía récord superior a los 3 °C, la OMM alerta por más calor, sequías y lluvias extremas en todo el planeta, y los países vecinos ya se preparan. Escribe un artículo periodístico informativo sobre el super El Niño de 2026: qué es el Fenómeno El Niño y por qué este sería un 'súper El Niño', qué dicen los científicos y la OMM sobre la intensidad (anomalía récord de más de 3°C en el Pacífico según el ECMWF), cómo afectará a Sudamérica y especialmente al Perú (lluvias extremas en el norte, sequías, impacto en agricultura y pesca), cómo se están preparando los países vecinos, y qué puede hacer la población para prepararse. Párrafos cortos, tono cercano y humano de periodista peruano, con datos concretos, sin relleno. Debe leerse como si lo hubiera escrito una persona, no una máquina.""",
        "home",
        "fenomeno-el-nino-furioso-2026-sudamerica",
    ),
    (
        """El eclipse solar total de agosto 2026 será uno de los espectáculos astronómicos más esperados del año: se anuncia que podría ser visible junto a auroras boreales, y la NASA ya adelantó cuándo llegará el próximo eclipse visible desde Perú. Escribe un artículo periodístico informativo sobre el eclipse solar total de agosto de 2026: qué es un eclipse solar total y por qué este es especial, cuándo y dónde será visible (qué países lo verán mejor), si se podrá ver desde Perú y cómo (con qué protección, a qué hora), la curiosidad de que pueda coincidir con auroras boreales, qué dice la NASA sobre los próximos eclipses visibles desde Perú, y consejos prácticos para observarlo con seguridad (nunca mirar directamente al sol, usar lentes certificados, filtros solares). Párrafos cortos, tono cercano y humano de periodista peruano, con datos concretos, sin relleno. Debe leerse como si lo hubiera escrito una persona, no una máquina.""",
        "home",
        "eclipse-solar-total-agosto-2026-visible-desde-peru",
    ),
]

if __name__ == "__main__":
    resultados = []
    for i, (tema, cat, slug) in enumerate(ARTICULOS, 1):
        print(f"\n=== Articulo {i}/{len(ARTICULOS)} [{cat}] {slug} ===", flush=True)
        nuevo_chat()
        ok_final = False
        for intento in (1, 2):
            try:
                print(f"[intento {intento}] preguntando a DeepSeek...", flush=True)
                resp = preguntar(tema)
                print(f"[intento {intento}] respuesta {len(resp)} chars", flush=True)
                guardado, err = guardar(resp, tema, cat, slug)
                if err:
                    print(f"[intento {intento}] error guardado: {err}", flush=True)
                else:
                    p = guardado["html_path"]
                    sz = os.path.getsize(p)
                    txt = open(p, encoding="utf-8", errors="replace").read().lower()
                    txt = ''.join(c for c in unicodedata.normalize('NFD', txt) if unicodedata.category(c) != 'Mn')
                    kws = slug.split('-')[:3]
                    hits = [k in txt for k in kws]
                    hit = any(hits)
                    print(f"[intento {intento}] OK: {guardado['title'][:70]} | size={sz} kw={kws} hits={hits}", flush=True)
                    if sz > 8000 and hit:
                        ok_final = True
                        break
                    else:
                        shutil.rmtree(os.path.dirname(p), ignore_errors=True)
                        gp = auto1.JSON_FILES.get(cat)
                        data = json.load(open(gp, encoding="utf-8"))
                        data = [e for e in data if e["slug"] != slug]
                        json.dump(data, open(gp, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
                        print(f"[intento {intento}] contenido no válido, reintentando...", flush=True)
            except Exception as e:
                print(f"[intento {intento}] ERROR: {repr(e)}", flush=True)
            time.sleep(5)
        resultados.append((slug, ok_final))
    print("\n=== RESUMEN ===", flush=True)
    for s, ok in resultados:
        print(("OK " if ok else "FAIL ") + s, flush=True)
    print("FIN_BATCH", flush=True)
