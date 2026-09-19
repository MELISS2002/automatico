# -*- coding: utf-8 -*-
import sys, os, time, traceback
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import crear_lote_api as L

L.ARTICULOS = [
    ("Senamhi alerta temperaturas de hasta 40 grados y sensacion de 42 grados por Fenomeno El Nino: region afectada y recomendaciones para la salud", "salud", "senamhi-alerta-temperaturas-40-grados-sensacion-42-nino-recomendaciones"),
    ("Dengue en Peru: detectan el zancudo vector en mas de 300 casas en Casma y el control larvario solo llega al 41 por ciento", "salud", "dengue-peru-zancudo-vector-casma-control-larvario-41-por-ciento"),
    ("SUNAT: como consultar con tu DNI si tienes saldo a favor y como cobrar la devolucion de impuestos", "home", "sunat-consultar-dni-saldo-favor-cobrar-devolucion-impuestos"),
    ("Essalud refuerza la vacunacion diaria en Lima sur: que vacunas estan disponibles y como acceder gratis", "salud", "essalud-refuerza-vacunacion-diaria-lima-sur-vacunas-gratis"),
    ("Cienciano vs Montevideo City Torque: fecha, hora y canal del partido de vuelta por los cuartos de final de la Copa Sudamericana", "home", "cienciano-vs-montevideo-city-torque-fecha-hora-canal-copa-sudamericana"),
]

def build_prompt_local(tema):
    return (
        "Eres un redactor y disenador web experto. Crea un articulo completo en HTML sobre "
        + chr(34) + tema + chr(34)
        + " (minimo 900 palabras), en espanol, con datos reales y verificables de la noticia de hoy en Peru.\n"
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
