#!/usr/bin/env python3
"""Elimina artículos de riesgo alto y renombra títulos de riesgo medio."""
import json
import os
import re
import shutil

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS_DIR = os.path.join(BASE, "public", "posts")

DELETE_SLUGS = [
    "cura-milagrosa-aceite-queso",
    "frutas-anticancer",
    "cancer",
    "la-cura-esta-prohibida",
    "el-mejor-remidio-para-el-ser-humano",
]

RENAME = {
    "higado-adelgazar": "El Hígado y la Pérdida de Peso: Datos y Recomendaciones",
    "el-ingrediente-que-usas-todos-los-das-y-est-destruyendo-tu-memoria-sin-que-lo-se": "El Azúcar y la Salud Cognitiva: Lo que Dice la Ciencia",
    "por-que-debes-comer-mucha-cantidad-de-miel-para-mejorar-y-salcar-tu-colon": "La Miel y la Salud Digestiva: Beneficios y Precauciones",
    "articulo-sobre-que-causa-las-hemoriedes-y-como-evitarlos-y-se-salen-como-curarlo": "Hemorroides: Causas, Prevención y Tratamientos Recomendados",
    "qu-dice-tu-cuerpo-sobre-tu-salud-haz-este-test-interactivo-de-2-minutos-y-descbrelo": "Señales del Cuerpo y Bienestar General: Guía Informativa",
}


def quitar_de_json(slug, nombre_archivo):
    path = os.path.join(POSTS_DIR, nombre_archivo)
    if not os.path.exists(path):
        return False
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    filtrado = [item for item in data if item.get("slug") != slug]
    if len(filtrado) == len(data):
        return False
    with open(path, "w", encoding="utf-8") as f:
        json.dump(filtrado, f, indent=2, ensure_ascii=False)
    print(f"  -> quitado de {nombre_archivo}")
    return True


def renombrar_en_json(slug, titulo, nombre_archivo):
    path = os.path.join(POSTS_DIR, nombre_archivo)
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    for item in data:
        if item.get("slug") == slug:
            item["title"] = titulo
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"  -> renombrado en {nombre_archivo}")


def renombrar_en_html(slug, titulo):
    html_path = os.path.join(POSTS_DIR, slug, "index.html")
    if not os.path.exists(html_path):
        return
    with open(html_path, "r", encoding="utf-8", errors="replace") as f:
        contenido = f.read()
    contenido = re.sub(r"<title>.*?</title>", f"<title>{titulo}</title>", contenido, flags=re.DOTALL | re.IGNORECASE)
    contenido = re.sub(r'<h1[^>]*>.*?</h1>', f"<h1>{titulo}</h1>", contenido, flags=re.DOTALL | re.IGNORECASE)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(contenido)
    print(f"  -> <title>/<h1> actualizados en {slug}")


print("== ELIMINACIÓN DE RIESGO ALTO ==")
for slug in DELETE_SLUGS:
    carpeta = os.path.join(POSTS_DIR, slug)
    print(f"* {slug}")
    if os.path.isdir(carpeta):
        shutil.rmtree(carpeta)
        print("  -> carpeta eliminada")
    quitar_de_json(slug, "home.json")
    quitar_de_json(slug, "salud.json")
    quitar_de_json(slug, "gana.json")

print("\n== RENOMBRADO DE RIESGO MEDIO ==")
for slug, titulo in RENAME.items():
    print(f"* {slug}")
    renombrar_en_json(slug, titulo, "home.json")
    renombrar_en_json(slug, titulo, "salud.json")
    renombrar_en_html(slug, titulo)

print("\nLimpieza completada.")
