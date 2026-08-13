# pub_api.py — publica artículos vía API local deepseek-server (8765). Chat limpio por artículo.
import sys, os, re, time, json, subprocess, unicodedata
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
    # Si el TITLE del modelo es feo (muy largo o arranca con el tema), usar el <title> del HTML generado
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
        """Las APIs de inteligencia artificial gratuitas son una de las búsquedas más populares de 2026 entre desarrolladores, estudiantes y emprendedores que quieren crear aplicaciones sin pagar por tokens. Escribe un artículo periodístico práctico y natural sobre las mejores API de IA gratis de 2026: Google AI Studio (Gemini, con generoso límite gratuito diario de solicitudes), OpenRouter (acceso a muchos modelos con opciones 100% gratuitas y límites claros), Groq (chips ultrarrápidos con nivel gratuito), la API de DeepSeek (precios muy bajos y a veces promociones gratis), Mistral (nivel free para experimentar) y Cloudflare Workers AI (créditos gratuitos diarios para correr modelos). Explica en lenguaje sencillo qué es una API, cómo empezar con cada una (dónde sacar la clave, qué límites tiene el plan gratis), para qué tipo de proyectos conviene cada una y consejos para no pasarse de los límites gratuitos. Párrafos cortos, tono cercano y humano de periodista de tecnología peruano, con datos concretos, sin relleno ni repeticiones. Debe leerse como si lo hubiera escrito una persona, no una máquina.""",
        "home",
        "apis-ia-gratis-2026-mejores-api-modelos-sin-pagar",
    ),
    (
        """Crear imágenes con inteligencia artificial gratis es una de las búsquedas más populares de 2026: millones de personas quieren generar ilustraciones, logos y fotos sin pagar suscripciones. Escribe un artículo periodístico práctico y natural sobre las mejores páginas para crear imágenes con IA gratis en 2026: Bing Image Creator (de Microsoft, con tecnología DALL-E, gratis con cuenta de Microsoft y límite diario de generaciones), Ideogram (ideal para imágenes con texto, con créditos gratuitos diarios), Leonardo AI (nivel gratuito con tokens diarios renovables), Canva (Magic Media, con créditos gratis al crear cuenta), Grok de X (genera imágenes gratis con límites para usuarios gratuitos) y Flux (el modelo abierto que puedes usar gratis en webs como fal.ai o incluso instalar en tu PC). Incluye consejos prácticos: cómo escribir buenos prompts (estilo, luz, detalle), cómo hacer que una imagen salga más realista, y cómo descargar sin marca de agua. Párrafos cortos, tono cercano y humano, datos concretos, sin relleno ni repeticiones. Debe leerse como si lo hubiera escrito una persona, no una máquina.""",
        "home",
        "crear-imagenes-con-ia-gratis-2026-paginas",
    ),
    (
        """Automatizar videos con inteligencia artificial gratis es el sueño de miles de creadores en 2026: canales de YouTube y TikTok que se alimentan solos con videos generados automáticamente. Escribe un artículo periodístico práctico y natural sobre cómo automatizar videos con IA gratis y cómo se puede ganar dinero: qué es un canal faceless o 'sin rostro', herramientas gratuitas de edición con IA (CapCut con sus funciones automáticas, Canva, InVideo con plan gratis), cómo generar guiones con chatbots gratuitos (DeepSeek, Gemini), voces de narración gratuitas (texto a voz con Edge TTS o herramientas libres), imágenes y clips gratis (bancos de imágenes libres, generadores de imágenes con IA), subtítulos automáticos y montaje con plantillas. Explica los primeros pasos de un flujo completo de automatización (idea -> guion -> voz -> video -> subtítulos -> publicación), cuánto puede costar empezar desde cero, y cómo se monetiza (publicidad de YouTube, programa de creatividad de TikTok, afiliados). Incluye una nota breve de que no constituye asesoría financiera y que la calidad y constancia importan. Párrafos cortos, tono cercano y humano, datos concretos, sin relleno ni promesas exageradas. Debe leerse como si lo hubiera escrito una persona, no una máquina.""",
        "gana",
        "automatizar-videos-con-ia-gratis-y-ganar-dinero",
    ),
    (
        """Usar inteligencia artificial gratis en tu propia computadora es posible gracias a proyectos de código abierto en GitHub, y en agosto de 2026 hay novedades muy comentadas. Escribe un artículo periodístico natural y útil sobre proyectos de GitHub para usar IA gratis en tu PC: Ollama (la forma más fácil de ejecutar modelos de lenguaje localmente), AirLLM (proyecto viral con más de 30 mil estrellas que permite ejecutar modelos de 70 mil millones de parámetros en una GPU de solo 4GB), el nuevo motor ds4 del famoso programador antirez (ejecuta DeepSeek 4 Flash y PRO en tu propia computadora con Metal, CUDA o ROCm), DeepSeek-Reasonix (agente de programación con IA que corre en la terminal, más de 30 mil estrellas), ComfyUI (la interfaz más potente para generar imágenes con modelos de difusión, con API incluida), Whisper (transcripción de audio a texto gratis) y Invidious (ver YouTube sin anuncios ni rastreo). Explica en lenguaje sencillo qué necesita tu computadora para cada uno, cuál es el más fácil para empezar y para qué sirve cada proyecto. Párrafos cortos, tono cercano y humano, datos concretos y actuales, sin relleno. Debe leerse como si lo hubiera escrito una persona, no una máquina.""",
        "gana",
        "proyectos-github-ia-gratis-correr-en-tu-pc",
    ),
    (
        """Los cursos gratuitos de inteligencia artificial están en auge en el Perú y el mundo. La Universidad Nacional de Ingeniería (UNI) lanzó más de 80 cursos virtuales gratuitos de inteligencia artificial, programación y ciberseguridad, una noticia muy comentada en el país. Además, la empresa Anthropic (creadora de Claude) publicó 12 cursos gratuitos de IA con certificado incluido, y la Presidencia del Consejo de Ministros (PCM) del Perú ofrece cursos gratis de IA y seguridad. Escribe un artículo periodístico informativo y práctico sobre los cursos gratis de IA disponibles para peruanos en 2026: qué anunció la UNI (más de 80 cursos virtuales gratuitos, de qué temas, cómo inscribirse según la información pública disponible), los 12 cursos gratuitos de Claude/Anthropic con certificado (de qué tratan, para qué niveles), los cursos de la PCM, y consejos generales para aprovechar cursos gratis de IA (dónde buscar más opciones confiables, cómo organizarse para terminarlos, qué habilidades priorizar para el mercado laboral peruano). Párrafos cortos, tono cercano y humano de periodista peruano, con datos concretos, sin relleno. Debe leerse como si lo hubiera escrito una persona, no una máquina.""",
        "home",
        "cursos-gratis-ia-peru-uni-claude-2026",
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
                        import shutil
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
