import os
import json
import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil import parser
from dateutil.tz import tzlocal
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
load_dotenv()

HF_API_KEY= os.getenv('HUGGINGFACE_TOKEN')
# Configuración de la API de Hugging Face

MODEL_NAME = "google/flan-t5-large"  # Modelo gratuito para reescritura en inglés

# URL del feed RSS
RSS_FEED = "https://www.espn.com/espn/rss/soccer/news"

# Encabezados para simular una solicitud desde un navegador
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://www.espn.com/",
}

# Configurar el cliente de inferencia de Hugging Face
client = InferenceClient(api_key=HF_API_KEY)

def download_image(image_url, output_dir):
    """Descarga una imagen desde su URL y la guarda en la carpeta especificada"""
    try:
        response = requests.get(image_url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        image_name = os.path.basename(image_url)
        image_path = os.path.join(output_dir, image_name)
        with open(image_path, 'wb') as f:
            f.write(response.content)
        return image_name
    except Exception as e:
        print(f"⚠️ Error downloading image: {str(e)}")
        return None

def fetch_article_content(url):
    """Descarga el contenido completo del artículo desde su URL"""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extraer el contenido principal del artículo
        content_div = soup.find('div', class_='article-body')  # Clase específica del sitio web
        if content_div:
            paragraphs = content_div.find_all('p')
            full_content = "\n".join([p.get_text() for p in paragraphs])
            return full_content.strip()
        else:
            print(f"⚠️ No se encontró el contenido del artículo en: {url}")
            return None
    except Exception as e:
        print(f"⚠️ Error descargando el contenido del artículo: {str(e)}")
        return None

def rewrite_article(text):
    """Reescribe un artículo utilizando un modelo de Hugging Face"""
    try:
        prompt = f"Rewrite the following article in a more engaging and professional style: {text}"
        response = client.text_generation(
            model=MODEL_NAME,
            prompt=prompt,
            max_new_tokens=300,
            temperature=0.7,
            do_sample=True
        )
        return response.strip() if response else text
    except Exception as e:
        print(f"⚠️ Error rewriting article: {str(e)}")
        return text

def process_article(entry):
    """Procesa un artículo individual"""
    try:
        # Descargar el contenido completo del artículo
        full_content = fetch_article_content(entry.link)
        if not full_content:
            print(f"⚠️ No se pudo obtener el contenido completo del artículo: {entry.title}")
            return None

        # Reescribir el contenido completo del artículo
        rewritten_content = rewrite_article(full_content)

        # Descargar la imagen asociada al artículo
        image_url = entry.media_content[0]['url'] if hasattr(entry, 'media_content') else ''
        image_name = download_image(image_url, 'public/images') if image_url else ''

        # Usar dateutil.parser para parsear la fecha
        date = parser.parse(entry.published, tzinfos={'EST': tzlocal()}).strftime('%Y-%m-%d')

        return {
            'title': entry.title,
            'date': date,
            'content': rewritten_content,
            'author': getattr(entry, 'author', 'ESPN'),
            'image': f"images/{image_name}" if image_name else '',
            'link': entry.link
        }
    except Exception as e:
        print(f"⚠️ Error processing article: {str(e)}")
        return None

def main():
    # Parsear el feed RSS
    feed = feedparser.parse(RSS_FEED)

    # Procesar los artículos (últimos 5)
    articles = [process_article(entry) for entry in feed.entries[:10]]
    articles = [a for a in articles if a is not None]

    # Directorio donde se guardarán los archivos generados
    output_dir = 'public/posts'
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs('public/images', exist_ok=True)  # Carpeta para imágenes

    # Crear el archivo de manifiesto
    manifest = []

    # Guardar cada artículo como archivo .md
    for idx, article in enumerate(articles):
        filename = f"{output_dir}/{datetime.now().strftime('%Y%m%d')}_{idx}.md"
        with open(filename, 'w', encoding='utf-8') as f:
            content = f"""---
title: "{article['title']}"
date: "{article['date']}"
author: "{article['author']}"
image: "{article['image']}"
---

{article['content']}

[Read more]({article['link']})
"""
            f.write(content)

        # Agregar información del artículo al manifiesto
        manifest.append({
            'id': idx,
            'slug': os.path.splitext(os.path.basename(filename))[0],
            **article
        })

    # Guardar el manifiesto como manifest.json
    with open(f'{output_dir}/manifest.json', 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    main()