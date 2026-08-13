# -*- coding: utf-8 -*-
# Batch 3 — temas trending 2026-08-08 (sueldo minimo, WhatsApp, salud mental, ONP, grupos WhatsApp)
import sys, os, time, json, shutil, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pub_api
import auto1

ARTICULOS = [
    (
        """El aumento del sueldo mínimo en Perú es la noticia económica más comentada de agosto de 2026. El MEF anunció que la Remuneración Mínima Vital subirá a S/ 1,300 en dos etapas: primero un aumento de S/ 100 (probablemente en octubre) y luego un segundo tramo de S/ 70 después de la temporada del Fenómeno El Niño. Escribe un artículo periodístico informativo y práctico sobre el aumento del sueldo mínimo 2026: qué anunció exactamente el Ministerio de Economía (la RMV actual es S/ 1,130 y subiría a S/ 1,300), las dos etapas del aumento (primero S/ 100 y luego S/ 70), los plazos que se manejan según lo dicho por el ministro Elmer Cuba, a quiénes beneficia el aumento (trabajadores formales que ganan la mínima, cerca de 1.5 millones de personas), qué dice el gobierno sobre el impacto en las pequeñas empresas (la ayuda económica a pymes que se anunció en paralelo) y las opiniones de los gremios empresariales y sindicatos. Incluye también un apartado práctico: qué deben hacer los trabajadores para verificar que su empleador aplique el aumento, qué hacer si no lo aplican (Superintendencia Nacional de Fiscalización Laboral - Sunafil) y cuánto sería el nuevo sueldo mínimo por día. Párrafos cortos, tono cercano y humano de periodista peruano, datos concretos, sin relleno ni repeticiones. Debe leerse como si lo hubiera escrito una persona, no una máquina.""",
        "gana",
        "sueldo-minimo-2026-aumento-s1300-dos-etapas",
    ),
    (
        """Recuperar mensajes borrados de WhatsApp es una de las búsquedas más populares del momento. Escribe un artículo periodístico práctico y útil sobre cómo recuperar mensajes borrados de WhatsApp en Android y iPhone en 2026: los métodos que realmente funcionan explicados paso a paso (1) restaurar desde la copia de seguridad de Google Drive en Android (requisitos, cómo verificar la fecha de la última copia, cómo desinstalar y reinstalar la app para restaurar), (2) restaurar desde iCloud en iPhone (ajustes de WhatsApp, iCloud Drive, reinstalar la app), (3) usar los chats archivados como alternativa (muchos creen que borraron chats que solo están archivados), (4) revisar la papelera de WhatsApp que ahora existe en la versión nueva de la app (cómo vaciarla, cuánto tiempo guarda los mensajes borrados), y (5) las apps de terceros que prometen recuperar mensajes: por qué NO funcionan y los riesgos de seguridad (apps falsas, malware, robo de datos). Explica también qué NO se puede recuperar nunca (mensajes borrados por el remitente para todos, chats sin copia de seguridad previa) y da consejos para configurar copias de seguridad automáticas diarias. Párrafos cortos, tono cercano y humano, datos concretos, sin relleno ni repeticiones. Debe leerse como si lo hubiera escrito una persona, no una máquina.""",
        "home",
        "como-recuperar-mensajes-borrados-whatsapp-android-iphone",
    ),
    (
        """Simone Biles, la gimnasta más condecorada de la historia, visitó Lima y compartió un mensaje sobre salud mental y bienestar que emocionó a miles de peruanos. Escribe un artículo periodístico cálido y humano sobre la visita de Simone Biles a Lima y su mensaje de salud mental: qué dijo la gimnasta durante su visita al Perú (según la información pública difundida por la agencia Andina), por qué su mensaje sobre salud mental es tan importante (ella misma se retiró de los Juegos Olímpicos de Tokio 2021 por problemas de salud mental, popularizando el concepto de 'twisties' y convirtiéndose en símbolo mundial del cuidado de la salud mental en el deporte de élite), cómo su historia ayudó a millones de personas a hablar abiertamente de la ansiedad y la presión, qué consejos prácticos de bienestar mencionó (priorizar el descanso, buscar ayuda profesional, no normalizar el agotamiento), y por qué su mensaje conecta con el Perú (el creciente interés por la salud mental en el país, la línea gratuita 113 opción 5 del Ministerio de Salud para contención emocional, la importancia de desestigmatizar la terapia). Párrafos cortos, tono cercano y humano, datos concretos, sin relleno. Debe leerse como si lo hubiera escrito una persona, no una máquina.""",
        "salud",
        "simone-biles-lima-mensaje-salud-mental",
    ),
    (
        """La pensión de la ONP aumenta cuando el afiliado cumple 80 años gracias al llamado 'bono por edad avanzada', y muchos jubilados peruanos no saben que les corresponde. Escribe un artículo periodístico informativo y práctico sobre el bono por edad avanzada de la ONP en 2026: qué es exactamente (un beneficio adicional que reciben los pensionistas de la ONP al cumplir 80 años), de cuánto es el monto según la información pública disponible, cómo y cuándo se cobra (si se entrega automáticamente con la pensión o hay que solicitarlo), qué documentos se necesitan, dónde se realiza el trámite (agencias de la ONP, Banco de la Nación), y qué pasa con los pensionistas que ya cumplieron 80 años y nunca lo cobraron (si pueden reclamarlo retroactivamente). Explica también de forma sencilla qué es la ONP, quiénes reciben pensión de jubilación, y la diferencia con la AFP. Incluye datos de contacto oficiales de la ONP y consejos para evitar estafas (la ONP nunca pide depósitos ni claves por teléfono o WhatsApp). Párrafos cortos, tono cercano y humano de periodista peruano, datos concretos, sin relleno ni repeticiones. Debe leerse como si lo hubiera escrito una persona, no una máquina.""",
        "gana",
        "pension-onp-bono-edad-avanzada-80-anos",
    ),
    (
        """WhatsApp lanzó nuevas funciones para los grupos que lo convierten en una herramienta mucho más potente, y la mayoría de usuarios aún no las conoce. Escribe un artículo periodístico práctico y natural sobre las nuevas funciones de WhatsApp para grupos en 2026: las novedades que anunció la app (nuevas herramientas de administración de grupos que permiten configurarlos como un profesional: mejores controles para administradores, opciones para fijar mensajes, encuestas más avanzadas, respuestas rápidas, eventos y recordatorios dentro del grupo, entre otras funciones recientes de WhatsApp que se fueron lanzando durante 2025 y 2026 como los canales, la transcripción de notas de voz, los temas de chat y los mensajes temporales). Explica paso a paso cómo usar cada función nueva en Android y iPhone: cómo crear un evento, cómo hacer una encuesta, cómo fijar varios mensajes, cómo silenciar a miembros específicos, cómo proteger un grupo con aprobación de nuevos miembros y cómo sacar a miembros problemáticos. Da consejos para administradores de grupos de trabajo, familia y colegio (cómo mantener el orden, evitar cadenas y spam). Párrafos cortos, tono cercano y humano, datos concretos, sin relleno. Debe leerse como si lo hubiera escrito una persona, no una máquina.""",
        "home",
        "whatsapp-nuevas-funciones-grupos-2026",
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
