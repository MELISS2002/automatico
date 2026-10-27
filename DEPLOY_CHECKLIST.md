# Checklist de despliegue - UltimoLive

## Antes de desplegar
- [ ] Verificar que `public/` y `dist/` estén sincronizados (`sync_dist.py` / copias manuales).
- [ ] Ejecutar `python scripts/generate_sitemap.py` y confirmar `public/sitemap.xml` actualizado.
- [ ] Validar JSON: `python -c "import json; json.load(open('public/ai-catalog.json'))"`.
- [ ] Probar localmente: abrir `public/pelis/index.html` y navegar rutas (detalle, género, país).

## Despliegue (Cloudflare Pages)
- [ ] Push a rama `main` (o la configurada).
- [ ] Confirmar que el workflow `Regenerar Sitemap` se ejecuta y commitea cambios.
- [ ] Verificar en Cloudflare Pages que el deploy termina sin errores.

## Post-despliegue
- [ ] Enviar `https://automatico.pages.dev/sitemap.xml` a Google Search Console.
- [ ] Solicitar indexación de URLs clave (home, /peliculas, /series, top géneros).
- [ ] Verificar Core Web Vitals en Search Console (LCP, CLS, INP).
- [ ] Comprobar `https://automatico.pages.dev/llms.txt` y `/ai-catalog.json` devuelven 200 con contenido correcto.
- [ ] Validar rich results con Google Rich Results Test en una ficha de película.
- [ ] Monitorear errores 404 en Search Console y añadir redirecciones si aparecen.

## Backlinks (mensual)
- [ ] Publicar 5-10 enlaces de calidad siguiendo `BACKLINKS_PLAN.md`.
- [ ] Revisar métricas (referring domains, posiciones) mensualmente.
