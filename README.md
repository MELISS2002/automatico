# UltimoLive

Sitio web de noticias deportivas, resultados y transmisiones en vivo, desplegado en **Cloudflare Pages** en [automatico.pages.dev](https://automatico.pages.dev/).

## 🚀 Tecnologías

- **Frontend**: React 19 + Vite 6 (SPA)
- **Enrutado**: React Router
- **Estilos**: CSS + Tailwind
- **Deploy**: Cloudflare Pages (GitHub integrado, auto-build en cada `push` a `main`)

## 📁 Estructura del proyecto

```
├── public/
│   ├── posts/              # Artículos en HTML estático (SEO-friendly)
│   │   ├── home.json       # Noticias del inicio
│   │   ├── gana.json       # Artículos de "Gana"
│   │   ├── salud.json      # Artículos de "Salud"
│   │   └── <slug>/index.html
│   ├── auto.py             # Publicador automático (Selenium + DeepSeek)
│   ├── auto1.py            # Versión batch del publicador
│   ├── agenda.html         # Calendario deportivo (iframe en el home)
│   ├── sitemap.xml         # Generado por scripts/generate_sitemap.py
│   └── robots.txt
├── src/
│   ├── App.jsx             # Página de inicio
│   ├── components/         # Header, Footer, NewsGrid, etc.
│   └── pages/              # About, Contact, Gana, Salud, Canales, Terms, PrivacyPolicy
├── scripts/
│   ├── generate_sitemap.py # Regenera sitemap.xml + robots.txt
│   └── cleanup_content.py  # Elimina/renombra artículos (uso puntual)
└── .github/workflows/
    └── sitemap.yml         # Regenera el sitemap en cada push a main
```

## ✍️ Publicar un artículo

El flujo de publicación usa `public/auto.py` (requiere **Chrome abierto en el puerto 9222** con la sesión de DeepSeek iniciada):

```bash
# Artículo individual
python public/auto.py

# Varios artículos por lotes (categorías: home, salud, gana)
python public/auto1.py "Título 1::home" "Título 2::salud"
python public/auto1.py --file titulos.txt
```

El script genera el HTML del artículo con DeepSeek, lo guarda en `public/posts/<slug>/`, actualiza el JSON correspondiente, **regenera el sitemap** y hace `git push`. Cloudflare Pages despliega automáticamente.

## 🔧 Desarrollo local

```bash
npm install
npm run dev        # servidor de desarrollo
npm run build      # build de producción en dist/
npm run lint       # ESLint
```

## 🔍 SEO y mantenimiento

- `scripts/generate_sitemap.py` genera `public/sitemap.xml` (todas las URLs) y `public/robots.txt`. Se ejecuta automáticamente en cada push vía GitHub Actions.
- El `index.html` raíz incluye metadatos Open Graph, Twitter Card y JSON-LD en español.
- Al crear artículos nuevos, `auto.py` regenera el sitemap antes del commit para que Google pueda indexarlos.

## ⚠️ Notas

- `config_geniptv.json` y las listas `.m3u` son archivos de trabajo locales del scraper de canales; no se usan en la app.
- Antes de publicar contenido de salud, evita titulares tipo "cura milagrosa" para no incumplir las políticas de Google AdSense.
