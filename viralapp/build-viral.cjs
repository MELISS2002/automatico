// build-viral.cjs : scrapea portales reales (RSS + sitemap notiviral) + descarga imagenes REALES,
// extrae el CUERPO completo de cada noticia (para "leer dentro"), lo alarga con DeepSeek local
// si es corto, y genera la app tipo notiviral: public/viral.json + public/viral/<id>.html
//
// uso: node build-viral.cjs [--top 14] [--pe] [--og] [--feed N] [--no-expand]
//   --top N     : cuantos items generar (default 14)
//   --pe        : solo fuentes peruanas
//   --og        : rellenar imagenes faltantes via CDP (news-og)
//   --feed N    : solo la fuente en el indice N de la lista
//   --no-expand : no alargar con DeepSeek (usa el cuerpo tal cual)
//   --no-notiviral : excluir la fuente notiviral.com
const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');
const { execSync } = require('child_process');

const ARGS = process.argv.slice(2);
function arg(s, d) { const i = ARGS.indexOf(s); return i >= 0 && ARGS[i + 1] !== undefined ? ARGS[i + 1] : d; }
function has(s) { return ARGS.includes(s); }

const TOP = parseInt(arg('--top', '14'), 10);
const ONLY_PE = has('--pe');
const WITH_OG = has('--og');
const FEED_IDX = has('--feed') ? parseInt(arg('--feed', '0'), 10) : null;
const EXPAND = !has('--no-expand');
const WITH_NOTIVIRAL = !has('--no-notiviral');

const BASE = path.join(__dirname, '..', '..', 'automatico-main');
const PUBLIC = path.join(BASE, 'public');
const SRC = path.join(PUBLIC, 'fuentes_rss_confiables.json');
const OUT_JSON = path.join(PUBLIC, 'viral.json');
const VIRAL_DIR = path.join(PUBLIC, 'viral');
const IMG_DIR = path.join(VIRAL_DIR, 'img');

const HEADE = 'UltimoLive Viral';
const UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0 Safari/537.36';
const DEEPSEEK = process.env.DEEPSEEK_URL || 'http://127.0.0.1:8765/v1/chat/completions';
const DS_MODEL = process.env.MODEL_OVERRIDE || 'deepseek-web';

function clean(s) {
  return (s || '').replace(/<!\[CDATA\[|\]\]>/g, '')
    .replace(/<[^>]+>/g, '')
    .replace(/&amp;/g, '&').replace(/&quot;/g, '"')
    .replace(/&#39;|&apos;/g, "'").replace(/&nbsp;/g, ' ')
    .replace(/&lt;/g, '<').replace(/&gt;/g, '>').trim();
}
function slugify(t, n) {
  let s = t.toLowerCase().replace(/[^a-z0-9\s-]/g, '').replace(/\s+/g, '-').replace(/-+/g, '-').trim('-');
  if (s.length > 60) s = s.slice(0, 60).replace(/-$/g, '');
  return (s || 'viral-' + n) + '-' + (n + 1);
}
function summaryOfTitle(t) { return t.slice(0, 170) + (t.length > 170 ? '…' : ''); }
function stripHtml(html) {
  let t = clean((html || '').replace(/<[^>]+>/g, ' '));
  return t.replace(/\s+/g, ' ').trim();
}

// ---- extraer items de un RSS/atom XML ----
function extraerItems(xml) {
  const atom = xml.match(/<entry[\s>][\s\S]*?<\/entry>/gi) || [];
  const items = [];
  const grab = (e) => {
    const title = clean((e.match(/<title[^>]*>([\s\S]*?)<\/title>/i) || [])[1]);
    let link = (e.match(/<link[^>]*>([\s\S]*?)<\/link>/i) || [])[1] || '';
    if (!link) link = (e.match(/<link[^>]*href="([^"]+)/i) || [])[1] || '';
    const img = (e.match(/<media:content[^>]*url="([^"]+)/i) || [])[1]
      || (e.match(/<enclosure[^>]*url="([^"]+)/i) || [])[1]
      || (e.match(/<media:thumbnail[^>]*url="([^"]+)/i) || [])[1] || '';
    const desc = stripHtml((e.match(/<(?:summary|description)[^>]*>([\s\S]*?)<\/(?:summary|description)>/i) || [])[1] || '');
    if (title && link) items.push({ title, link, img, desc, pub: (e.match(/<(?:published|updated|pubDate)[^>]*>([\s\S]*?)<\/\1>/i) || [])[1] || '' });
  };
  if (atom.length) atom.forEach(grab);
  else {
    const rss = xml.match(/<item[\s>][\s\S]*?<\/item>/gi) || [];
    rss.forEach(grab);
  }
  return items;
}

async function fetchFeed(f) {
  try {
    const ctrl = new AbortController();
    const t = setTimeout(() => ctrl.abort(), 15000);
    const r = await fetch(f.url, { signal: ctrl.signal, headers: { 'User-Agent': UA, 'Accept': 'application/rss+xml, application/xml, text/xml, */*' }, redirect: 'follow' });
    clearTimeout(t);
    if (r.status !== 200) return { f, items: [] };
    const xml = await r.text();
    return { f, items: extraerItems(xml) };
  } catch (e) { return { f, items: [], err: (e.name === 'AbortError' ? 'timeout' : e.message).slice(0, 50) }; }
}

// ---- descargar HTML de una URL (con timeout + UA) ----
function getHtml(url, timeout = 20000) {
  return new Promise((resolve) => {
    let u;
    try { u = new URL(url); } catch (e) { return resolve(''); }
    const mod = u.protocol === 'https:' ? https : http;
    const req = mod.get(url, { headers: { 'User-Agent': UA, 'Accept': 'text/html,application/xhtml+xml,*/*' }, timeout }, (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        res.resume();
        return getHtml(new URL(res.headers.location, url).href, timeout).then(resolve);
      }
      if (res.statusCode !== 200) { res.resume(); return resolve(''); }
      const chunks = [];
      let len = 0;
      res.on('data', (c) => { chunks.push(c); len += c.length; if (len > 1500000) { req.destroy(); resolve(''); } });
      res.on('end', () => resolve(Buffer.concat(chunks).toString('utf-8')));
    });
    req.on('timeout', () => { req.destroy(); resolve(''); });
    req.on('error', () => resolve(''));
  });
}

// ---- extraer el CUERPO (parrafos) de una pagina de noticia generica ----
// Estrategia: usa <article> si tiene parrafos largos; si no, toma los <p> largos del body
// filtrando navegacion/footer/app. Devuelve [tituloH1, ogImage, parrafosTexto]
function parseArticle(html) {
  let h1 = clean((html.match(/<h1[^>]*>([\s\S]*?)<\/h1>/i) || [])[1] || '');
  if (!h1) h1 = clean((html.match(/<title[^>]*>([\s\S]*?)<\/title>/i) || [])[1] || '').replace(/\s*\|\s*.*$/, '').trim();
  const og = (html.match(/<meta[^>]+property=["']og:image["'][^>]+content=["']([^"']+)/i) || [])[1]
    || (html.match(/<meta[^>]+content=["']([^"']+)["'][^>]+property=["']og:image["']/i) || [])[1] || '';

  // candidatos: parrafos largos (>= 90 chars) evitando footer/nav/app/share
  const MATCH = /<p[^>]*>([\s\S]*?)<\/p>/gi;
  const pars = [];
  let m;
  const bad = /descargue la app|compartir|suscr|siguenos|seguir|footer|newsletter|boletin|publicidad|le puede interesar|copyright|reproduccion|edicion digital|@andina|follow us|like us|comment/i;
  while ((m = MATCH.exec(html)) !== null) {
    let t = stripHtml(m[1]);
    if (t.length < 90 || bad.test(t)) continue;
    t = t.replace(/[']+/g, '');
    pars.push(t);
    if (pars.length >= 12) break;
  }
  return { h1, og, pars };
}

// ---- fuente notiviral.com: sitemap + abrir cada noticia ----
async function fetchNotiviral(max = TOP) {
  try {
    const ctrl = new AbortController();
    const t = setTimeout(() => ctrl.abort(), 15000);
    const r = await fetch('https://notiviral.com/sitemap.xml', { signal: ctrl.signal, headers: { 'User-Agent': UA } });
    clearTimeout(t);
    if (r.status !== 200) return [];
    const xml = await r.text();
    const locs = (xml.match(/<loc>([^<]*\/noticia\/[^<]+)<\/loc>/gi) || [])
      .map((s) => s.replace(/<\/?loc>/gi, '').trim());
    const out = [];
    for (let i = 0; i < locs.length && out.length < max; i++) {
      const url = locs[i];
      const html = await getHtml(url, 20000);
      if (!html) continue;
      const { h1, og, pars } = parseArticle(html);
      const title = h1 || clean((html.match(/<meta[^>]+property=["']og:title["'][^>]+content=["']([^"']+)/i) || [])[1] || '');
      if (!title) continue;
      const desc = clean((html.match(/<meta[^>]+property=["']og:description["'][^>]+content=["']([^"']+)/i) || [])[1] || '');
      const pub = clean((html.match(/<meta[^>]+property=["']article:published_time["'][^>]+content=["']([^"']+)/i) || [])[1] || '');
      out.push({
        title, link: url, img: og, desc,
        pars, pub, source: 'Noti Viral', country: 'AR', notiviral: true,
      });
    }
    return out;
  } catch (e) { console.log('  [notiviral] err:', (e.message || '').slice(0, 60)); return []; }
}

// ---- alargar un texto corto con DeepSeek local ----
async function expandText(title, body, source) {
  if (!body || body.length >= 1200) return body; // ya es largo, no hace falta
  const prompt = `Eres redactor periodistico. Amplia esta noticia real conservando TODOS los datos del original y SIN inventar cifras, fechas ni nombres. Extiende de forma natural, agrega contexto, antecedentes y desarrollo coherente (minimo 500 palabras, en espanol neutro, tono serio, CON parrafos separados por doble salto de linea). Responde SOLO con el texto del articulo ampliado, sin titulo, sin "aqui tienes" ni intro.

TITULO: ${title}
FUENTE: ${source}
TEXTO ORIGINAL:
${body}`;
  try {
    const ctrl = new AbortController();
    const t = setTimeout(() => ctrl.abort(), 120000);
    const resp = await fetch(DEEPSEEK, {
      method: 'POST', signal: ctrl.signal,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ model: DS_MODEL, messages: [{ role: 'user', content: prompt }], stream: false }),
    });
    clearTimeout(t);
    if (!resp.ok) return body;
    const j = await resp.json();
    const txt = ((j.choices && j.choices[0] && j.choices[0].message && j.choices[0].message.content) || '').trim();
    if (txt.length < 200) return body;
    return txt;
  } catch (e) { console.log(`  [expand] ${title.slice(0, 30)}... -> USAR original (${(e.message || '').slice(0, 40)})`); return body; }
}

function getOgImageCDP(url) {
  try { execSync(`node neo.cjs open "${url.replace(/"/g, '\\"')}"`, { cwd: __dirname, encoding: 'utf-8', timeout: 25000 }); } catch (e) {}
  const js = `(()=>{const m=document.querySelector('meta[property="og:image"]');return m?m.content:''})()`;
  try {
    const out = execSync(`node neo.cjs eval "${js}"`, { cwd: __dirname, encoding: 'utf-8', timeout: 25000 }).toString().trim();
    return out && /^https?:/.test(out) ? out : '';
  } catch (e) { return ''; }
}

function download(url, dest, referer) {
  return new Promise((resolve) => {
    const u = new URL(url);
    const mod = u.protocol === 'https:' ? https : http;
    const hdrs = { 'User-Agent': UA, 'Accept': 'image/*,*/*;q=0.8' };
    if (referer) hdrs['Referer'] = referer;
    const req = mod.get(url, { headers: hdrs, timeout: 20000 }, (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        res.resume();
        return download(new URL(res.headers.location, url).href, dest, referer).then(resolve);
      }
      if (res.statusCode !== 200) { res.resume(); return resolve(false); }
      const chunks = [];
      res.on('data', (c) => chunks.push(c));
      res.on('end', () => {
        try {
          const buf = Buffer.concat(chunks);
          if (buf.length < 500) return resolve(false);
          fs.writeFileSync(dest, buf);
          resolve(true);
        } catch (e) { resolve(false); }
      });
    });
    req.on('timeout', () => { req.destroy(); resolve(false); });
    req.on('error', () => resolve(false));
  });
}

async function main() {
  const all = JSON.parse(fs.readFileSync(SRC, 'utf-8'));
  let fuentes = all.fuentes;
  if (ONLY_PE) fuentes = fuentes.filter((f) => f.country === 'PE');
  if (FEED_IDX !== null) { const f = fuentes[FEED_IDX]; fuentes = f ? [f] : []; }
  console.log(`Fuentes rss a scrapear: ${fuentes.length}`);

  const items = [];
  for (const f of fuentes) {
    const { items: its } = await fetchFeed(f);
    console.log(`  ${f.name}: ${its.length} items`);
    its.forEach((it) => items.push({ ...it, source: f.name, country: f.country }));
    if (items.length >= TOP * 3) break;
  }

  // + notiviral (via sitemap + cuerpo) como fuente extra
  if (WITH_NOTIVIRAL) {
    console.log('  Noti Viral (sitemap): scrapeando...');
    const nv = await fetchNotiviral(Math.max(5, Math.ceil(TOP / 2)));
    console.log(`  Noti Viral: ${nv.length} noticias`);
    items.push(...nv);
  }

  // dedupe por link
  const seen = new Set();
  const uniq = items.filter((it) => { const k = it.link; if (seen.has(k)) return false; seen.add(k); return true; });
  console.log(`Items unicos: ${uniq.length}`);

  // Intercalado: garantiza que notiviral tenga presencia visible (no lo ahogue Clarin/Infobae).
  // Reserva hasta ~40% del TOP para notiviral, entrelazandose de a uno con el resto.
  const pendientes = uniq.slice();
  const nv = pendientes.filter((it) => it.notiviral);
  const resto = pendientes.filter((it) => !it.notiviral);
  nv.sort((a, b) => { const d = new Date(b.pub) - new Date(a.pub); return isNaN(d) ? 0 : d; });
  const inter = [];
  const maxNV = Math.max(1, Math.ceil(TOP * 0.4));
  let ni = 0, ri = 0, steps = 0;
  // Entrelaza: 1 notiviral cada 2 del resto hasta cubrir maxNV notiviral.
  while (inter.length < TOP && (ni < nv.length || ri < resto.length)) {
    if (ni < nv.length && ni < maxNV && (steps % 3 === 0 || ri >= resto.length)) { inter.push(nv[ni++]); }
    else if (ri < resto.length) { inter.push(resto[ri++]); }
    else if (ni < nv.length) break;
    steps++;
  }
  const uniqFinal = inter.slice(0, TOP);
  console.log(`Intercalado: ${uniqFinal.length} items (notiviral dentro: ${uniqFinal.filter((x) => x.notiviral).length})`);

  // tomamos los primeros TOP; recogemos imagen y CUERPO.
  const out = [];
  let withImg = 0, withBody = 0, expanded = 0;
  for (let i = 0; i < uniqFinal.length && out.length < TOP; i++) {
    const it = uniqFinal[i];
    let img = it.img || '';
    if (process.env.VIRAL_DEBUG) console.log(`    DBG#${i} img=${(img || '(none)').slice(0, 60)} title=${it.title.slice(0, 40)}`);
    if (img && !/^https?:/.test(img)) img = '';
    if (!img && WITH_OG && out.length < TOP) {
      img = getOgImageCDP(it.link);
      console.log(`    og:image "${it.title.slice(0, 50)}" -> ${img.slice(0, 70) || 'NO'}`);
    }

    // CUERPO: ya viene con notiviral; para rss hay que abrir la noticia
    let body = (it.pars || []).join('\n\n');
    let bodyTitle = it.title, bodyOg = img;
    if (!body && it.link) {
      const html = await getHtml(it.link, 20000);
      const a = parseArticle(html);
      body = a.pars.join('\n\n');
      bodyTitle = a.h1 || it.title;
      bodyOg = a.og || img;
      if (!img && a.og) img = a.og;
      if (process.env.VIRAL_DEBUG) console.log(`    BODY#${i} "${it.title.slice(0, 40)}" -> ${body.length} chars img=${(a.og || '').slice(0, 40)}`);
    }
    if (body) withBody++;

    // ALARGAR con DeepSeek si es corto
    let content = body || it.desc || summaryOfTitle(it.title);
    if (EXPAND && content.length < 1200) {
      const ex = await expandText(bodyTitle, content, it.source);
      if (ex && ex.length > content.length + 100) { content = ex; expanded++; }
    }

    const id = slugify(it.title, i);
    let ext = 'jpg';
    try { const mm = (new URL(img).pathname.match(/\.(jpg|jpeg|png|webp|gif)$/i) || [])[1]; if (mm) ext = mm.toLowerCase(); } catch (e) {}
    const dest = path.join(IMG_DIR, id + '.' + ext);
    let dl = false;
    if (img) {
      let ref = '';
      try { ref = new URL(it.link).origin; } catch (e) {}
      dl = await download(img, dest, ref);
    }
    const rel = `${id}.${ext}`;
    if (process.env.VIRAL_DEBUG) console.log(`    DL#${i} img=${(img || '(none)').slice(0, 55)} -> dl=${dl}`);
    if (dl) withImg++;
    const views = 1 + Math.floor(Math.random() * 45);
    out.push({
      id, title: (bodyTitle || it.title).slice(0, 140),
      summary: (it.desc || summaryOfTitle(bodyTitle || it.title)).slice(0, 220),
      source: it.source, country: it.country || '',
      url: it.link, image: dl ? `/viral/img/${rel}` : '',
      views, published: it.pub || new Date().toISOString().slice(0, 10),
      content,
    });
  }

  fs.mkdirSync(IMG_DIR, { recursive: true });
  fs.writeFileSync(OUT_JSON, JSON.stringify({ generated: new Date().toISOString(), items: out }, null, 2), 'utf-8');
  console.log(`\nviral.json: ${out.length} items (imagenes: ${withImg}, cuerpos: ${withBody}, alargados: ${expanded})`);
  generatePages(out);
  console.log('FIN');
}

function generatePages(out) {
  if (!fs.existsSync(VIRAL_DIR)) fs.mkdirSync(VIRAL_DIR, { recursive: true });
  for (const it of out) {
    const imgTag = it.image ? `<meta property="og:image" content="https://automatico.pages.dev${it.image}"/>\n  <meta name="twitter:image" content="https://automatico.pages.dev${it.image}"/>` : '';
    const content = `<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>${escapeHtml(it.title)} | ${HEADE}</title>
  <meta name="description" content="${escapeHtml(it.summary)}"/>
  <meta property="og:title" content="${escapeHtml(it.title)}"/>
  <meta property="og:description" content="${escapeHtml(it.summary)}"/>
  <meta property="og:type" content="article"/>
  <meta property="og:url" content="https://automatico.pages.dev/viral/${it.id}.html"/>
  ${imgTag}
  <link rel="canonical" href="${it.url}"/>
  <script>
    fetch('/api/viral-views/' + ${JSON.stringify(it.id)}, {method:'POST'}).catch(function(){});
  </script>
</head>
<body style="background:#000;color:#fff;font-family:sans-serif;text-align:center;padding:80px 20px">
  <p>Cargando noticia <strong>${escapeHtml(it.source)}</strong>…</p>
  <p><a href="/viral" style="color:#4ea1ff">Volver al feed</a></p>
</body>
</html>`;
    fs.writeFileSync(path.join(VIRAL_DIR, `${it.id}.html`), content, 'utf-8');
  }
  console.log(`Paginacion HTML: ${out.length} paginas`);
}
function escapeHtml(s) { return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); }

main().catch((e) => { console.error(e); process.exit(1); });