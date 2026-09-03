# viralapp/ — App viral (feed de noticias) de UltimoLive

Carpeta dedicada a la **app viral** (estilo notiviral.com) desplegada en
`automatico.pages.dev/viral`. Agrupa el motor y las herramientas de esta app;
el frontend React y las Pages Functions **no se mueven** porque Vite/Pages los
requieren en `src/` y `functions/`.

## Estructura
| Archivo / ruta | Qué es |
|---|---|
| `viralapp/build-viral.cjs` | Scraper: lee RSS de `fuentes_rss_confiables.json`, descarga imágenes REALES (header `Referer`), genera feed + páginas SEO. |
| `viralapp/publicar_viral.ps1` | Motor 1-clic: scrape → build → commit quirúrgico → push (auto-deploy). |
| `viralapp/README.md` | Este documento. |
| `public/viral.json` | Feed generado (se sirve en `automatico.pages.dev/viral.json`). |
| `public/viral/<id>.html` + `public/viral/img/` | Páginas SEO + imágenes reales por noticia. |
| `src/pages/Viral.jsx` + `Viral.css` | Frontend React (ruta `/viral`). |
| `src/main.jsx` / `src/components/Header.jsx` | Registro de la ruta y enlace en el menú. |
| `functions/api/viral-views/[id].js` | Pages Function: contador de vistas (KV `VIEWS_KV` con fallback en memoria). |

## Publicar (un solo bat)
El lanzador del proyecto es **`_correr_diario.bat`** (raíz): hace el feed viral y
luego el blog diario. Para correr SOLO el viral:

```powershell
powershell -ExecutionPolicy Bypass -File viralapp\publicar_viral.ps1
# opciones: -Top 20 (mas items) | -NoGit (solo scrape+build) | -Pe (peruano)
```

## Flujo del motor
1. Scrapea portales reales (RSS) + descarga imágenes reales → `public/viral.json` + `public/viral/`.
2. `npm run build` → actualiza `dist/` con el feed + la página `/viral`.
3. Commit QUIRÚRGICO (solo `viral.json`, `viral/`, `functions/`, `src/pages/Viral.*`, `src/main.jsx`, `Header.jsx`) + push con rebase → auto-deploy.

### Notas del motor
- **No usa `$ErrorActionPreference = "Stop"`**: git escribe su progreso normal a
  stderr y con `Stop` lanzaría `NativeCommandError` abortando en `From https://...`.
  Se verifica el éxito con `$LASTEXITCODE`.
- Si hay archivos sueltos sin commitear, los resguarda en stash antes del push y
  los devuelve al final.
- El scraper original también existe en `C:\Users\dza\Desktop\neo\tools\build-viral.cjs`
  (fuente histórica). La copia canónica para este repo es `viralapp/build-viral.cjs`.