# -*- coding: utf-8 -*-
# pub_soda.py — regenera SOLO el articulo Soda Sinfonico
import sys, os, time, json, shutil, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pub_api
import auto1

TEMA = """Soda Sinfónico, el espectáculo que une los clásicos de Soda Stereo con una orquesta sinfónica, llega por primera vez al Perú y los fans ya hacen cola por las entradas. Escribe un artículo periodístico de entretenimiento sobre Soda Sinfónico en Perú 2026: qué es Soda Sinfónico (un espectáculo tributo que versiona los grandes clásicos de Soda Stereo con arreglos sinfónicos, con músicos en vivo y una orquesta, que ya recorrió varios países con gran éxito), por qué es tan especial (Soda Stereo es la banda más influyente del rock latinoamericano y sus canciones como De música ligera, Persiana americana, Cuando pase el temblor, En la ciudad de la furia y Trátame suavemente marcaron a generaciones enteras), cuándo y dónde será el concierto en Perú según la información disponible (fecha y lugar anunciados para este año), cómo comprar entradas y cuánto cuestan (canales oficiales de venta, rangos de precios según zona), qué esperar del show (orquesta sinfónica en vivo, coros, pantallas, el setlist con los himnos de la banda), y por qué este tipo de tributos sinfónicos son tendencia en Latinoamérica (reviven la música de las bandas clásicas en formato sinfónico y reúnen a fans de todas las edades, de padres que crecieron con la banda a hijos que la descubren ahora). Incluye un repaso breve de la historia de Soda Stereo y de Gustavo Cerati. Párrafos cortos, tono cercano y humano, datos concretos, sin relleno ni repeticiones. Debe leerse como si lo hubiera escrito una persona, no una máquina."""
CAT = "home"
SLUG = "soda-sinfonico-peru-concierto-soda-stereo"

if __name__ == "__main__":
    ok_final = False
    for intento in (1, 2, 3):
        try:
            print(f"[intento {intento}] chat limpio + preguntando...", flush=True)
            pub_api.nuevo_chat()
            resp = pub_api.preguntar(TEMA)
            print(f"[intento {intento}] respuesta {len(resp)} chars", flush=True)
            if len(resp) < 5000:
                print(f"[intento {intento}] respuesta vacia, reintento...", flush=True)
                continue
            guardado, err = pub_api.guardar(resp, TEMA, CAT, SLUG)
            if err:
                print(f"[intento {intento}] error: {err}", flush=True)
                continue
            p = guardado["html_path"]
            sz = os.path.getsize(p)
            txt = open(p, encoding="utf-8", errors="replace").read().lower()
            txt = ''.join(c for c in unicodedata.normalize('NFD', txt) if unicodedata.category(c) != 'Mn')
            kws = SLUG.split('-')[:3]
            hits = [k in txt for k in kws]
            print(f"[intento {intento}] OK: {guardado['title'][:80]} | size={sz} kw={kws} hits={hits}", flush=True)
            if sz > 8000 and any(hits):
                ok_final = True
                break
            shutil.rmtree(os.path.dirname(p), ignore_errors=True)
            gp = auto1.JSON_FILES.get(CAT)
            data = json.load(open(gp, encoding="utf-8"))
            data = [e for e in data if e["slug"] != SLUG]
            json.dump(data, open(gp, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[intento {intento}] ERROR: {repr(e)}", flush=True)
        time.sleep(5)
    print("OK" if ok_final else "FAIL", flush=True)
