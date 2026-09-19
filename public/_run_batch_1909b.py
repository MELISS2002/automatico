# -*- coding: utf-8 -*-
import sys, os, io, time, traceback
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import crear_lote_api as L

L.ARTICULOS = [
    ("Keiko Fujimori: primera medicion de su gestion presidencial da 37% de aprobacion y 49% de desaprobacion", "home", "keiko-fujimori-aprobacion-37-desaprobacion-49"),
    ("Destituyen al juez que envio a prision a Keiko Fujimori y a los expresidentes Toledo y Humala", "home", "destituyen-juez-keiko-toledo-humala"),
    ("Caso Liceo Naval: jueza ordena cuatro meses de internamiento para seis adolescentes por presunta violacion sexual", "home", "liceo-naval-internamiento-seis-adolescentes"),
    ("Dengue en Nuevo Chimbote: reportan el cuarto caso confirmado en Via Central", "salud", "dengue-nuevo-chimbote-cuarto-caso-via-central"),
    ("Banco Pichincha comprara Diners Club Peru por S/ 23.4 millones tras autorizacion de la SBS", "gana", "banco-pichincha-compra-diners-club-peru"),
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

logf = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '_lote_out1909b.txt'), 'w', encoding='utf-8')
ok = 0
total = len(L.ARTICULOS)
for i, (tema, categoria, slug) in enumerate(L.ARTICULOS, 1):
    logf.write("=== [%d/%d] %s ===\n" % (i, total, slug))
    logf.flush()
    try:
        prompt = L.build_prompt(tema)
        respuesta = L.call_api(prompt)
        logf.write("respuesta: %d chars\n" % len(respuesta))
        logf.flush()
        exito, detalle = L.guardar_articulo(tema, categoria, slug, respuesta)
        if exito:
            ok += 1
            logf.write("OK %s\n" % detalle)
        else:
            logf.write("FAIL %s\n" % detalle)
    except Exception as e:
        logf.write("ERROR %s: %r\n" % (slug, e))
        logf.write(traceback.format_exc())
    logf.flush()
    if i < total:
        time.sleep(3)

logf.write("RESUMEN: %d/%d OK\n" % (ok, total))
logf.close()
