import feedparser
from transformers import pipeline
from datetime import datetime
import json
import os

# Configurar modelo
summarizer = pipeline("summarization", model="t5-small")

# Fuente RSS
RSS_FEED = "https://www.espn.com/espn/rss/soccer/news"

def process_article(entry):
    """Procesa un artículo del RSS feed"""
    try:
        summary = summarizer(entry.description, max_length=150, min_length=30)[0]['summary_text']
        
        return {
            'title': entry.title,
            'date': datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %Z').strftime('%Y-%m-%d'),
            'content': summary,
            'author': entry.author if hasattr(entry, 'author') else 'ESPN',
            'image': entry.media_content[0]['url'] if hasattr(entry, 'media_content') else '',
            'link': entry.link
        }
    except Exception as e:
        print(f"Error procesando artículo: {str(e)}")
        return None

def main():
    # Obtener feed
    feed = feedparser.parse(RSS_FEED)
    
    # Procesar artículos
    articles = [process_article(entry) for entry in feed.entries[:5]]  # Últimos 5 artículos
    articles = [a for a in articles if a is not None]
    
    # Guardar en Markdown y generar manifest
    manifest = []
    os.makedirs('../posts', exist_ok=True)
    
    for idx, article in enumerate(articles):
        filename = f"../posts/{datetime.now().strftime('%Y%m%d')}_{idx}.md"
        with open(filename, 'w') as f:
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
        
        # Combine dictionaries using the correct syntax
        manifest.append({
            'id': idx,
            'slug': filename.split('/')[-1].replace('.md', ''),
            **article  # Use the unpacking operator to merge dictionaries
        })
    
    # Guardar manifest
    with open('../posts/manifest.json', 'w') as f:
        json.dump(manifest, f, indent=4)

if __name__ == "__main__":
    main()