from transformers import pipeline
from datetime import datetime
import json
import os
import feedparser
from dateutil import parser
from dateutil.tz import tzlocal
import shutil
# Configurar el modelo para la summarización de noticias
summarizer = pipeline("summarization", model="t5-small")

# URL del feed RSS
RSS_FEED = "https://www.espn.com/espn/rss/soccer/news"

def process_article(entry):
    """Procesa un artículo individual"""
    try:
        # Resumen del artículo
        summary = summarizer(entry.description, max_length=150, min_length=30, do_sample=False)[0]['summary_text']

        # Usar dateutil.parser para parsear la fecha, con tzinfos para manejar zonas horarias
        date = parser.parse(entry.published, tzinfos={'EST': tzlocal()}).strftime('%Y-%m-%d')

        return {
            'title': entry.title,
            'date': date,  # Usamos la fecha procesada aquí
            'content': summary,
            'author': getattr(entry, 'author', 'ESPN'),
            'image': entry.media_content[0]['url'] if hasattr(entry, 'media_content') else '',
            'link': entry.link
        }
    except Exception as e:
        print(f"⚠️ Error procesando artículo: {str(e)}")
        return None

def main():
    # Parsear el feed RSS
    feed = feedparser.parse(RSS_FEED)

    # Procesar los artículos (últimos 5)
    articles = [process_article(entry) for entry in feed.entries[:5]]
    articles = [a for a in articles if a is not None]

    # Directorio donde se guardarán los archivos generados
    output_dir = 'public/posts'
    os.makedirs(output_dir, exist_ok=True)

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

[Leer más]({article['link']})
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
