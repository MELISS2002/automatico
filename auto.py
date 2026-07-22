import json
import os

# Ruta al archivo home.json
data_path = "C:/Users/dza/Desktop/automatico-main/public/posts/home.json"

# Nuevo artículo
nuevo_articulo = {
    "title": "5 Beneficios de la Salud Natural en el Deporte",
    "excerpt": "Descubre cómo integrar elementos naturales en tu rutina deportiva para mejorar tu recuperación y rendimiento físico.",
    "date": "2026-07-22",
    "category": "Salud Natural"
}

def crear_articulo():
    # Asegurar que el directorio existe
    os.makedirs(os.path.dirname(data_path), exist_ok=True)
    
    # Leer existentes
    if os.path.exists(data_path):
        with open(data_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    # Agregar nuevo
    data.insert(0, nuevo_articulo)

    # Escribir
    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Artículo creado exitosamente en {data_path}")

if __name__ == "__main__":
    crear_articulo()
