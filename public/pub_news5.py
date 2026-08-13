# pub_news5.py — genera 5 articulos de noticias destacadas con imagenes REALES locales
# usa API local DeepSeek (8765) + template auto1, luego inyecta las imagenes locales
import sys, os, re, json, time, shutil, urllib.request

sys.path.insert(0, r'C:\Users\dza\Desktop\automatico-main\public')
import auto1

API = 'http://127.0.0.1:8765/v1/chat/completions'
IMG_SRC = r'C:\Users\dza\Desktop\neo\tools\news-imgs-final'
POSTS = r'C:\Users\dza\Desktop\automatico-main\public\posts'

ARTICULOS = [
    {
        "tema": "Temblor en Venezuela hoy, lunes 10 de agosto: epicentro, profundidad y magnitud de los últimos sismos según FUNVISIS",
        "cat": "home",
        "slug": "temblor-venezuela-10-agosto-funvisis",
        "imgs": ["temblor-venezuela.jpg", "temblor-venezuela-1.jpg", "temblor-venezuela-2.jpg"],
        "nota": "Noticia real: el 10 de agosto de 2026 FUNVISIS reporto sismos en Venezuela, incluyendo uno a 9 km al oeste de Naiguata (10-08-2026 01:01, profundidad 5.0 km, magnitud 2.6) y otro a 6 km al noroeste de Naiguata (09-08-2026 22:56, profundidad 5.0 km, magnitud 2.4). Tambien hubo sismos cerca de Valledupar, Punta Arenas, Bucaramanga y Pedernales. Incluye contexto del Cinturon de Fuego del Pacifico, enjambres sismicos, diferencias entre temblor y terremoto, y recomendaciones de seguridad durante sismos."
    },
    {
        "tema": "Un meteorito de Marte de 1.270 millones de años ayuda a reconstruir la historia del planeta rojo",
        "cat": "home",
        "slug": "meteorito-marte-1270-millones-anos-historia",
        "imgs": ["meteorito-marte.jpg", "meteorito-marte-1.jpg", "meteorito-marte-2.jpg"],
        "nota": "Noticia real: investigadores del Boston College descubrieron que el meteorito marciano NWA 13441, hallado en Argelia en 2019, tiene 1.270 millones de anos y proviene de una zona de Marte nunca antes estudiada. Ayuda a cubrir casi 2.000 millones de anos sin muestras de shergottitas (tipo de roca mas comun de Marte). Estudio publicado en Geochimica et Cosmochimica Acta. Lider: Ethan Baxter. Participaron la Instituci Scripps de Oceanografia y la Universidad Abierta de Gran Bretana. Solo hay unas 400 piezas de meteoritos marcianos."
    },
    {
        "tema": "Motorola lanza Global Connect y ofrece roaming gratis para millones de usuarios durante el torneo de fútbol más importante",
        "cat": "home",
        "slug": "motorola-global-connect-roaming-gratis-torneo",
        "imgs": ["motorola-roaming.jpg", "motorola-v2.jpg", "motorola-v3.jpg"],
        "nota": "Noticia real de Business Empresarial (Peru): Motorola lanzo Global Connect, un servicio que ofrece roaming gratis para mantener conectados a millones de usuarios durante el torneo de futbol mas importante del mundo. Pensado para viajeros que no quieren perder conexion. Incluye SIM de viaje para datos en el extranjero."
    },
    {
        "tema": "Keiko Fujimori anuncia que aplicará el modelo de Bukele: 'mucha firmeza para recuperar el orden'",
        "cat": "home",
        "slug": "keiko-fujimori-modelo-bukele-firmeza-orden",
        "imgs": ["keiko-bukele.jpg", "keiko-bukele-1.jpg", "keiko-bukele-2.jpg"],
        "nota": "Noticia real de Infobae: la presidenta Keiko Fujimori anuncio este domingo que su Gobierno empezara a aplicar una politica de mucha firmeza contra la delincuencia, tomando como referencia a Nayib Bukele, durante una transmision en vivo. Gladys me dice que siga los pasos del presidente Bukele. Si, mucha firmeza para recuperar el orden, dijo. Ratifico respaldo a policias que participaron en operativos, incluido el caso de un cambista en el Centro de Lima. Ya se gestiono mejorar condiciones de comisarias. A inicios de julio Bukele le envio carta de felicitaciones."
    },
    {
        "tema": "Once peruanos murieron combatiendo por Rusia y otros 114 están desaparecidos, según autoridades de Perú",
        "cat": "home",
        "slug": "peruanos-muertos-combatiendo-rusia-114-desaparecidos",
        "imgs": ["peruanos-rusia.jpg", "peruanos-rusia-1.jpg", "peruanos-rusia-2.jpg"],
        "nota": "Noticia real de CNN en espanol: autoridades de Peru reportaron que once peruanos murieron combatiendo por Rusia en la guerra contra Ucrania y otros 114 estan desaparecidos. Familiares protestan exigiendo el regreso de sus familiares, denunciando enganos en el reclutamiento (carteles: 'Basta de injusticia', 'No es nuestra guerra')."
    }
]

def generar(tema, nota, slug):
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
    body = json.dumps({
        "model": "deepseek-web",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 12000
    }).encode('utf-8')
    req = urllib.request.Request(API, data=body, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=580) as r:
        resp = json.loads(r.read().decode('utf-8'))
    return resp['choices'][0]['message']['content']

def main():
    solo = sys.argv[1] if len(sys.argv) > 1 else None
    for i, art in enumerate(ARTICULOS):
        if solo and solo not in art['slug']:
            continue
        print(f"\n=== [{i+1}/{len(ARTICULOS)}] {art['tema'][:70]}")
        try:
            respuesta = generar(art['tema'], art['nota'], art['slug'])
        except Exception as e:
            print(f"  ERROR API: {e}")
            continue
        # extraer marcadores
        title = auto1.extract_val(respuesta, "TITLE:") or art['tema'][:60]
        excerpt = auto1.extract_val(respuesta, "EXCERPT:")
        html = auto1.extract_between(respuesta, "===HTML_START===", "===HTML_END===")
        if not html:
            bloques = auto1.extraer_bloques(respuesta)
            for tipo, contenido in bloques:
                if tipo == 'html' or (tipo == 'code' and '<html' in contenido.lower()):
                    html = contenido
                    break
        if not html:
            print("  ERROR: no se extrajo HTML")
            continue
        html = re.sub(r'^```(?:html)?\s*\n?', '', html.strip())
        html = re.sub(r'\n?```$', '', html.strip())
        if not html.strip().startswith('<!DOCTYPE html>') and not html.strip().startswith('<html'):
            html = f"<!DOCTYPE html>\n<html lang=\"es\">\n<head><meta charset=\"UTF-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"><title>{title}</title>\n<style>body{{font-family:Arial,sans-serif;line-height:1.6;max-width:800px;margin:0 auto;padding:20px;background:#f9f9f9;color:#333}}h1{{color:#2c3e50}}h2{{color:#c0392b}}img{{max-width:100%;height:auto;border-radius:8px;margin:20px 0}}footer{{margin-top:40px;padding-top:20px;border-top:1px solid #ddd;font-size:.9em;color:#777}}</style></head>\n<body>\n{html}\n</body>\n</html>"
        # carpeta del post
        carpeta = os.path.join(POSTS, art['slug'])
        os.makedirs(carpeta, exist_ok=True)
        # copiar imagenes locales
        for j, img in enumerate(art['imgs']):
            src = os.path.join(IMG_SRC, img)
            dst = os.path.join(carpeta, f"imagen{j+1}.jpg")
            if os.path.isfile(src):
                shutil.copy2(src, dst)
                print(f"  img imagen{j+1}.jpg <- {img}")
            else:
                print(f"  ! falta {src}")
        # limpiar posibles rutas absolutas
        html = html.replace('src="https://image.pollinations.ai', 'src="imagen1.jpg"')
        html_path = os.path.join(carpeta, 'index.html')
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"  HTML guardado: {html_path} ({len(html)} chars)")
        # JSON
        entry = {
            "slug": art['slug'],
            "title": title,
            "author": "ROSA EMILY",
            "date": time.strftime("%Y-%m-%d"),
            "excerpt": excerpt or ("Noticia: " + art['tema'][:120]),
            "thumbnail": f"/posts/{art['slug']}/imagen1.jpg",
            "htmlPath": f"/posts/{art['slug']}/index.html"
        }
        ok = auto1.actualizar_json(os.path.join(POSTS, art['cat'] + '.json'), entry)
        print(f"  JSON {'OK' if ok else 'DUPLICADO/ERROR'}")
        time.sleep(3)

if __name__ == '__main__':
    main()
