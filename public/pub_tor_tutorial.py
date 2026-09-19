# pub_tor_tutorial.py - articulo tutorial: Tor como VPN/proxy global en Windows
import sys, os, re, json, time, shutil, subprocess

sys.path.insert(0, r'C:\Users\dza\Desktop\automatico-main\public')
import auto1

API = os.environ.get('TOR_API', 'http://127.0.0.1:8765/v1/chat/completions')
MODEL = os.environ.get('TOR_MODEL', 'deepseek-web')
IMG_SRC = r'C:\Users\dza\Desktop\tor-proxy\article-imgs'
POSTS = r'C:\Users\dza\Desktop\automatico-main\public\posts'
HERE = os.path.dirname(os.path.abspath(__file__))

ARTICULO = {
    "tema": "Guia completa: como usar Tor como VPN y proxy global en Windows 10/11",
    "cat": "home",
    "slug": "tor-vpn-proxy-global-windows",
    "imgs": ["imagen1.jpg", "imagen2.jpg", "imagen3.jpg"],
    "nota": """Tutorial tecnico real basado en un montaje verificado: convertir Windows en un proxy global / VPN completo que sale a internet por la red Tor.
Datos reales del montaje (usa estas cifras y pasos, no inventes):
1) Se instala el daemon de Tor para Windows (0.4.9.x). Se crea un archivo torrc en C:\\Users\\dza\\Desktop\\tor-proxy\\ que define SocksPort 9050, ControlPort 9051 y ControlPortWriteToFile para automatizacion. Con eso ya se tiene un proxy SOCKS5 local en 127.0.0.1:9050.
2) Con un proxy SOCKS disponible, el sistema operativo puede enviar por el todo el trafico TCP. Para que TODO el trafico de la maquina salga por Tor (mal llamado VPN), se usa tun2socks (herramienta opensource que redirige trafico de un adaptador de red virtual al proxy SOCKS). Aun con firewall del sistema, el adaptador virtual (interfaz 'wintun' de tun2socks) recibe todo el trafico; una ruta por defecto con metrica 1 hace que todo salga por el adaptador TUN (10.0.90.1), dejando la red local excluida con metrica mayor para que el enrutador no se rompa.
3) El adaptador virtual usa la interfaz 'wintun' instalada con Wintun 0.14. El comando usado: tun2socks --proxy socks5://127.0.0.1:9050 --interface wintun.
4) Soy socio de la configuracion de DNS para evitar fugas: un servicio local (dns-tor) escucha en 127.0.0.1:53 y reenvia las consultas DNS por HTTPS (DoH, a 1.1.1.1 con fallback a 8.8.8.8) atravesando el tunel de Tor, de modo que ni las consultas DNS salen por la IP real.
5) Se crean scripts de un toque: TorPOR_INICIO = "tor-vpn-on.ps1" activa todo (daemon, adaptador, DNS, ruta), "tor-vpn-off.ps1" apaga y restaura la ruta normal, y "tor-vpn-watcher.ps1" vigila que Tor siga vivo: si Tor cae, revierte automaticamente a internet directo (quita la ruta y el DNS) y si vuelve, re-arma todo solo. Tambien hay versiones .bat para el usuario final.
6) Verificacion real: check.torproject.org devuelve IsTor=true y la IP de salida pertenece a nodos de salida de Tor (por ejemplo 104.223.84.121 desde Toronto, Canada, o 185.220.101.38 en Brandemburgo, Alemania - ForPrivacyNET). La IP cambio sola al rotar de circuito. ipinfo.io devuelve 403 porque bloquea las IPs de Tor.
7) Riesgos reales: Tor no es VPN comercial, no protege del DNS leak si no se configura, hay que bloquear WebRTC en navegadores (revela IP real), la velocidad es menor (saltos por 3 nodos), algunos sitios bloquean por deteccion de la red Tor, y las descargas P2P estan prohibidas y degradan la red. Tor sirve para privacidad y eludir censura, no para esconder al 100% el trafico de aplicaciones con datos propios.
8) El articulo debe explicar la diferencia entre: usar Tor solo en el navegador (Tor Browser), proxy SOCKS global a nivel de aplicacion, y VPN total de todo el sistema con tun2socks. Contar para que sirve cada modo y que scripts se usan en cada paso.
Las 3 imagenes locales reales son: imagen1.jpg (imagen del logo oficial de Tor), imagen2.jpg (captura real de pantalla de check.torproject.org confirmando "This browser is configured to use Tor"), imagen3.jpg (captura real del sitio web del portal donde se publica el articulo). Coloca imagen1 en el encabezado destacado, imagen2 en la seccion de verificacion y imagen3 en la seccion final de resultados/en pruebas.""",
}

def preguntar(art):
    tema = art['tema']
    nota = art['nota']
    prompt = f"""Eres un redactor y disenador web experto de un portal de tecnologia peruano. Crea un articulo TUTORIAL completo en HTML sobre este tema (minimo 1200 palabras):

TEMA: {tema}

DATOS REALES DEL TUTORIAL (usa estos datos tecnicos verificados, no inventes cifras):
{nota}

REGlas OBLIGATORIAS:
- Estilo periodistico-tecnico serio, en espanol neutro, tono informativo y didactico. NO uses clickbait.
- Incluye EXACTAMENTE 3 imagenes usando rutas locales: imagen1.jpg, imagen2.jpg e imagen3.jpg (src="imagen1.jpg", src="imagen2.jpg", src="imagen3.jpg"). Colocalas en el featured header y en puntos relevantes del cuerpo segun lo descrito.
- El HTML debe tener estilos CSS atractivos, responsive, con header de tutorial, parrafos, subtitulos (h2), bloques de pasos numerados, bloques de datos destacados (code-boxes o cards con comandos), tablas comparativas si aplica, y footer.
- El titulo y el contenido deben incluir las palabras clave Tor, VPN y proxy (juntas o cercanas) para SEO.
- NO uses backticks (```) en tu respuesta. NO uses emojis. NO uses markdown.
- Responde EXACTAMENTE con esta estructura (respeta los marcadores):

TITLE: (titulo periodistico-tutorial)
EXCERPT: (extracto 2-3 frases)
===HTML_START===
(ESCRIBE AQUI TODO EL CODIGO HTML: <!DOCTYPE html>, <head>, <style>, <body>, IMAGENES LOCALES imagen1.jpg imagen2.jpg imagen3.jpg, ETC.)
===HTML_END===
THUMBNAIL: imagen1.jpg"""
    prompt = auto1.limpiar_texto(prompt)
    body = json.dumps({"model": MODEL, "messages": [{"role": "user", "content": prompt}]})
    p = os.path.join(HERE, "_body_tor.json")
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
        excerpt = "Tutorial: " + art['tema'][:120]
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
    art = ARTICULO
    ok_final = False
    for intento in (1, 2, 3):
        try:
            print(f"[intento {intento}] preguntando a DeepSeek...", flush=True)
            resp = preguntar(art)
            print(f"[intento {intento}] respuesta {len(resp)} chars", flush=True)
            guardado, err = guardar(resp, art)
            if err:
                print(f"[intento {intento}] error guardado: {err}", flush=True)
            else:
                p = guardado["html_path"]
                sz = os.path.getsize(p)
                txt = open(p, encoding="utf-8", errors="replace").read().lower()
                n_img = txt.count('imagen1.jpg') + txt.count('imagen2.jpg') + txt.count('imagen3.jpg')
                kw = all(w in txt for w in ('tor', 'vpn', 'proxy'))
                print(f"[intento {intento}] OK: {guardado['title'][:70]} | size={sz} refs_imagenes={n_img} keyword_tor_vpn_proxy={kw}", flush=True)
                if sz > 9000 and n_img >= 2 and kw:
                    ok_final = True
                    break
                else:
                    shutil.rmtree(os.path.dirname(p), ignore_errors=True)
                    gp = auto1.JSON_FILES.get(art['cat'])
                    data = json.load(open(gp, encoding="utf-8"))
                    data = [e for e in data if e["slug"] != art['slug']]
                    json.dump(data, open(gp, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
                    print(f"[intento {intento}] contenido no valido (size={sz} imgs={n_img} kw={kw}), reintentando...", flush=True)
        except Exception as e:
            print(f"[intento {intento}] ERROR: {repr(e)}", flush=True)
        time.sleep(5)
    print(("OK " if ok_final else "FAIL ") + art['slug'], flush=True)
    print("FIN_BATCH", flush=True)