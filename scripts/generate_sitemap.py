#!/usr/bin/env python3
"""Genera sitemap.xml y robots.txt con todas las URLs del sitio."""
import os
from datetime import datetime, timezone

BASE = "https://automatico.pages.dev"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS_DIR = os.path.join(ROOT, "public", "posts")

MAIN_ROUTES = [
    ("/", 1.0),
    ("/gana", 0.8),
    ("/salud", 0.8),
    ("/canales", 0.7),
    ("/about", 0.4),
    ("/contact", 0.4),
    ("/terms", 0.3),
    ("/privacy-policy", 0.3),
]


def post_slugs():
    if not os.path.isdir(POSTS_DIR):
        return []
    return sorted(
        name for name in os.listdir(POSTS_DIR)
        if os.path.isfile(os.path.join(POSTS_DIR, name, "index.html"))
    )


def build_sitemap():
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    urls = []
    for path, prio in MAIN_ROUTES:
        urls.append((BASE + path, prio, today))
    for slug in post_slugs():
        urls.append((f"{BASE}/posts/{slug}/index.html", 0.8, today))
    return urls


def write_sitemap(urls):
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for loc, prio, lastmod in urls:
        lines.append("  <url>")
        lines.append(f"    <loc>{loc}</loc>")
        lines.append(f"    <lastmod>{lastmod}</lastmod>")
        lines.append(f"    <priority>{prio}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    path = os.path.join(ROOT, "public", "sitemap.xml")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"sitemap.xml actualizado: {len(urls)} URLs")


def write_robots():
    path = os.path.join(ROOT, "public", "robots.txt")
    content = "\n".join([
        "User-agent: *",
        "Allow: /",
        "",
        "Sitemap: https://automatico.pages.dev/sitemap.xml",
        "",
    ])
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("robots.txt actualizado")


if __name__ == "__main__":
    urls = build_sitemap()
    write_sitemap(urls)
    write_robots()
