# -*- coding: utf-8 -*-
import sys, os, time, traceback
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import crear_lote_api as L

L.ARTICULOS = [
    ("Bochorno en Lima: los distritos que podrian llegar a 38 grados por el Fenomeno El Nino", "home", "bochorno-lima-distritos-38-grados-fenomeno-nino"),
    ("Tipo de cambio del dolar en Peru repunta ante expectativa de mayor tasa de interes en Estados Unidos", "home", "tipo-cambio-dolar-peru-repunta-tasa-interes-estados-unidos"),
    ("Debate para la Alcaldia de Lima 2026: temas, fechas, duplas y la situacion de Rafael Lopez Aliaga", "home", "debate-alcaldia-lima-2026-fechas-duplas-lopez-aliaga"),
    ("Que es el RSI: la tecnica de inteligencia artificial que podria salirse de control", "gana", "que-es-rsi-tecnica-inteligencia-artificial-salirse-control"),
    ("Trucos para proteger tu celular Android y grabar mejores videos para redes sociales", "gana", "trucos-proteger-celular-android-grabar-mejores-videos-redes"),
]

def build_prompt_local(tema):
    return (
        "Eres un redactor y disenador web experto. Crea un articulo completo en HTML sobre "
        + chr(34) + tema + chr(34)
        + " (minimo 900 palabras), en espanol, con datos reales y verificables de la noticia.\n"
        + "Incluye exactamente 3 imagenes locales usando src=\"imagen1.jpg\", src=\"imagen2.jpg\" y src=\"imagen3.jpg\" "
        + "(rutas relativas, NO uses URLs externas, NO uses pollinations).\n"
        + "El HTML debe tener estilos CSS atractivos, responsive y un diseno de revista. NO uses backticks.\n\n"
        + "Responde EXACTAMENTE con esta estructura (respeta los marcadores):\n\n"
        + "TITLE: (titulo periodistico real)\n"
        + "EXCERPT: (extracto 2-3 frases)\n"
        + "===HTML_START===\n"
        + "(ESCRIBE AQUI TODO EL CODIGO HTML, INCLUYENDO <!DOCTYPE html>, <head>, <style>, <body>, IMAGENES, ETC.)\n"
        + "===HTML_END===\n"
        + "THUMBNAIL: imagen1.jpg\n"
    )

L.build_prompt = build_prompt_local

import auto1
auto1.GIT_ACTIVO = False

ok = 0
total = len(L.ARTICULOS)
for i, (tema, categoria, slug) in enumerate(L.ARTICULOS, 1):
    sys.stderr.write("=== [%d/%d] %s ===\n" % (i, total, slug))
    sys.stderr.flush()
    try:
        prompt = L.build_prompt(tema)
        respuesta = L.call_api(prompt)
        sys.stderr.write("respuesta: %d chars\n" % len(respuesta))
        sys.stderr.flush()
        exito, detalle = L.guardar_articulo(tema, categoria, slug, respuesta)
        if exito:
            ok += 1
            sys.stderr.write("OK %s\n" % detalle)
        else:
            sys.stderr.write("FAIL %s\n" % detalle)
    except Exception as e:
        sys.stderr.write("ERROR %s: %r\n" % (slug, e))
        traceback.print_exc(file=sys.stderr)
    sys.stderr.flush()
    if i < total:
        time.sleep(3)

sys.stderr.write("RESUMEN: %d/%d OK\n" % (ok, total))
sys.stderr.flush()
os._exit(0)
