# -*- coding: utf-8 -*-
# Batch 4 — temas trending 2026-08-08 (ola de calor, corte de agua, eclipse solar, papa Leon XIV, Soda Sinfonico)
import sys, os, time, json, shutil, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pub_api
import auto1

ARTICULOS = [
    (
        """El SENAMHI anunció que la ola de calor se extiende hasta el lunes 10 de agosto en Lima y otras 16 regiones del Perú, y miles de personas buscan cómo protegerse. Escribe un artículo periodístico informativo y práctico sobre la ola de calor en Perú de agosto de 2026: qué anunció el SENAMHI (la ola de calor se extiende hasta el lunes 10 de agosto en Lima y otras 16 regiones del país), por qué se produce este fenómeno (el aumento de temperaturas diurnas que superan los valores normales durante varios días consecutivos), qué temperaturas se esperan en Lima (los distritos de Lima Metropolitana con mayor sensación de calor, como La Molina, Jesús María, Ate, entre otros, y los registros que se han alcanzado), las regiones más afectadas (costa norte como Piura y Lambayeque, costa central, sierra y selva), los efectos en la salud (golpe de calor, deshidratación, insolación, agotamiento; grupos más vulnerables como niños, adultos mayores y mascotas), y las recomendaciones prácticas de los especialistas: hidratarse constantemente sin esperar a tener sed, evitar la exposición al sol entre 10 de la mañana y 4 de la tarde, usar ropa ligera de colores claros, protección solar, no dejar a niños ni mascotas dentro de autos estacionados, mantener la casa ventilada y usar ventiladores o paños húmedos. Incluye las señales de alerta del golpe de calor (piel seca y caliente, confusión, mareos, pulso acelerado) y qué hacer ante una emergencia. Párrafos cortos, tono cercano y humano de periodista peruano, datos concretos, sin relleno ni repeticiones. Debe leerse como si lo hubiera escrito una persona, no una máquina.""",
        "salud",
        "ola-de-calor-lima-senamhi-10-agosto-regiones",
    ),
    (
        """Sedapal anunció un corte de agua programado para el lunes 10 de agosto en Lima, y los vecinos de los distritos afectados quieren saber horarios exactos y cómo prepararse. Escribe un artículo periodístico informativo y práctico sobre el corte de agua de Sedapal del 10 de agosto de 2026: qué anunció Sedapal (el corte de agua programado en varios distritos de Lima por trabajos de mantenimiento y mejora de la red), los distritos afectados y los horarios exactos según la información pública disponible (el corte aplica para el lunes 10 de agosto y las zonas comprendidas en el comunicado de la empresa), por qué se realizan estos cortes programados (mantenimiento de redes, empalmes, renovación de tuberías, limpieza de reservorios), qué deben hacer los vecinos antes del corte (almacenar agua en recipientes limpios y tapados, llenar baldes y botellas, evitar almacenar en recipientes que hayan contenido productos químicos, usar el agua almacenada solo para consumo humano si es potable), durante el corte (uso responsable del agua almacenada, cerrar bien los caños para evitar accidentes cuando regrese el servicio) y después (dejar correr el agua unos minutos hasta que salga limpia, revisar que no haya fugas). Explica también cómo consultar el cronograma oficial de cortes de Sedapal (la página web oficial, el número de atención al cliente y las redes sociales de la empresa), y da consejos para hogares con adultos mayores, bebés y mascotas. Párrafos cortos, tono cercano y humano de periodista peruano, datos concretos, sin relleno ni repeticiones. Debe leerse como si lo hubiera escrito una persona, no una máquina.""",
        "home",
        "corte-agua-sedapal-10-agosto-distritos-horarios",
    ),
    (
        """El eclipse solar total de agosto de 2026 es el fenómeno astronómico más esperado del año: pasará por España y el Reino Unido, y millones de personas lo verán en vivo. Escribe un artículo periodístico informativo sobre el eclipse solar total de agosto de 2026: qué es un eclipse solar total (cuando la Luna se interpone entre el Sol y la Tierra y oculta completamente el disco solar), cuándo ocurrirá exactamente (el 12 de agosto de 2026, según los cálculos astronómicos), en qué países y ciudades será visible en su fase total (España: la costa norte, Galicia, Asturias, Cantabria, País Vasco, Aragón, Castilla y León, y también Baleares e Islas Canarias; en el Reino Unido se verá parcial pero muy significativo), por qué este eclipse es especial (será el primer eclipse solar total visible en la España peninsular desde 1905, más de 120 años), a qué hora comenzará en cada zona, cómo observarlo de forma SEGURA (nunca mirar directamente al sol sin protección certificada: usar gafas especiales con filtro ISO 12312-2, no usar lentes de sol comunes, radiografías, vidrios ahumados ni CDs; métodos indirectos como la proyección con una caja o los filtros de soldador número 14), por qué hay tanta expectativa (los pueblos de España se preparan para recibir a miles de turistas astronómicos y se han agotado alojamientos, según reportes de la prensa británica y española), y si será visible desde Perú y América Latina (en Perú no se verá la totalidad, pero se podrá seguir en vivo por internet). Párrafos cortos, tono cercano y humano, datos concretos, sin relleno ni repeticiones. Debe leerse como si lo hubiera escrito una persona, no una máquina.""",
        "home",
        "eclipse-solar-total-agosto-2026-espana-fecha",
    ),
    (
        """El Vaticano confirmó que el papa León XIV visitará el Perú del 11 al 17 de noviembre de 2026, una noticia que emociona a millones de peruanos. Escribe un artículo periodístico cálido e informativo sobre la visita del papa León XIV al Perú en noviembre de 2026: qué anunció el Vaticano (la visita oficial del papa León XIV al Perú del 11 al 17 de noviembre de 2026, según la información difundida por la agencia oficial), quién es el papa León XIV (un pontífice conocido por su cercanía con los fieles y su mensaje de esperanza y unidad, elegido en el cónclave), qué ciudades del Perú visitará según lo informado (Lima, Chiclayo, Cusco y Pucallpa según los reportes que se han difundido, con actividades religiosas, misas multitudinarias y encuentros con jóvenes y comunidades), por qué esta visita es histórica (será la segunda visita de un papa al Perú en el siglo XXI y la primera de León XIV a Latinoamérica), qué se sabe del programa de actividades (encuentros con autoridades, misas masivas, visitas a santuarios y comunidades, mensajes de esperanza), qué preparativos se están realizando (logística, seguridad, alojamiento de peregrinos, transporte), y cómo los fieles pueden seguir los eventos (transmisión en vivo por TV y redes sociales). Explica también por qué el Perú es un país con fuerte tradición católica y qué significa para los peruanos recibir a un papa. Párrafos cortos, tono cercano y humano de periodista peruano, datos concretos, sin relleno ni repeticiones. Debe leerse como si lo hubiera escrito una persona, no una máquina.""",
        "home",
        "papa-leon-xiv-visita-peru-noviembre-2026",
    ),
    (
        """Soda Sinfónico, el espectáculo que une los clásicos de Soda Stereo con una orquesta sinfónica, llega por primera vez al Perú y los fans ya hacen cola por las entradas. Escribe un artículo periodístico de entretenimiento sobre Soda Sinfónico en Perú 2026: qué es Soda Sinfónico (un espectáculo tributo que versiona los grandes clásicos de Soda Stereo con arreglos sinfónicos, con músicos en vivo y una orquesta, que ya recorrió varios países con gran éxito), por qué es tan especial (Soda Stereo es la banda más influyente del rock latinoamericano y sus canciones como De música ligera, Persiana americana, Cuando pase el temblor, En la ciudad de la furia y Trátame suavemente marcaron a generaciones enteras), cuándo y dónde será el concierto en Perú según la información disponible (fecha y lugar anunciados para este año), cómo comprar entradas y cuánto cuestan (canales oficiales de venta, rangos de precios según zona), qué esperar del show (orquesta sinfónica en vivo, coros, pantallas, el setlist con los himnos de la banda), y por qué este tipo de tributos sinfónicos son tendencia en Latinoamérica (reviven la música de las bandas clásicas en formato sinfónico y reúnen a fans de todas las edades, de padres que crecieron con la banda a hijos que la descubren ahora). Incluye un repaso breve de la historia de Soda Stereo y de Gustavo Cerati. Párrafos cortos, tono cercano y humano, datos concretos, sin relleno ni repeticiones. Debe leerse como si lo hubiera escrito una persona, no una máquina.""",
        "home",
        "soda-sinfonico-peru-concierto-soda-stereo",
    ),
]

if __name__ == "__main__":
    pub_api.ARTICULOS = ARTICULOS
    resultados = []
    for i, (tema, cat, slug) in enumerate(ARTICULOS, 1):
        print(f"\n=== Articulo {i}/{len(ARTICULOS)} [{cat}] {slug} ===", flush=True)
        pub_api.nuevo_chat()
        ok_final = False
        for intento in (1, 2):
            try:
                print(f"[intento {intento}] preguntando a DeepSeek...", flush=True)
                resp = pub_api.preguntar(tema)
                print(f"[intento {intento}] respuesta {len(resp)} chars", flush=True)
                guardado, err = pub_api.guardar(resp, tema, cat, slug)
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
