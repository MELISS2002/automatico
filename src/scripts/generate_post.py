from transformers import pipeline
from datetime import datetime
import json
import os
import feedparser

# Configurar modelo de resumen
summarizer = pipeline("summarization", model="t5-small")

# RSS de ESPN
RSS_FEED = "https://www.espn.com/espn/rss/soccer/news"

def process_article(entry):
    try:
        summary = summarizer(entry.description, max_length=150, min_length=30, do_sample=False)[0]['summary_text']
        return {
            'title': entry.title,
            'date': datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %Z').strftime('%Y-%m-%d'),
            'content': summary,
            'author': getattr(entry, 'author', 'ESPN'),
            'image': entry.media_content[0]['url'] if hasattr(entry, 'media_content') else '',
            'link': entry.link
        }
    except Exception as e:
        print(f"Error procesando artículo: {str(e)}")
        return None

def main():
    feed = feedparser.parse(RSS_FEED)
    articles = [process_article(entry) for entry in feed.entries[:5]]
    articles = [a for a in articles if a is not None]

    output_dir = 'src/posts'
    os.makedirs(output_dir, exist_ok=True)

    manifest = []

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

        manifest.append({
            'id': idx,
            'slug': os.path.splitext(os.path.basename(filename))[0],
            **article
        })

    # Guardar manifest
    with open(f'{output_dir}/manifest.json', 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    main()
