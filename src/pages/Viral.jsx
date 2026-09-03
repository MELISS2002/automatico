import React, { useState, useEffect, useRef, useCallback } from 'react';
import { Helmet } from 'react-helmet-async';
import './Viral.css';

// Vista de recuento: intenta sumar/leer via el Worker de Cloudflare.
const VIEWS_API = '/api/viral-views';

function Viral() {
  const [items, setItems] = useState([]);
  const [visible, setVisible] = useState(4);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [views, setViews] = useState({}); // id -> count
  const loadMoreRef = useRef(null);
  const pageLoadedRef = useRef({});

  useEffect(() => {
    fetch('/viral.json')
      .then((r) => {
        if (!r.ok) throw new Error('HTTP ' + r.status);
        return r.json();
      })
      .then((data) => {
        const list = data.items || [];
        setItems(list);
        const seed = {};
        list.forEach((it) => (seed[it.id] = it.views || 0));
        setViews(seed);
      })
      .catch((e) => setError('No se pudo cargar el feed viral'))
      .finally(() => setLoading(false));
  }, []);

  // incremento una vez por item visible (evita doble conteo)
  useEffect(() => {
    items.slice(0, visible).forEach((it) => {
      if (pageLoadedRef.current[it.id]) return;
      pageLoadedRef.current[it.id] = true;
      incView(it.id);
    });
  }, [items, visible]);

  const incView = useCallback((id) => {
    setViews((v) => ({ ...v, [id]: (v[id] || 0) + 1 }));
    try {
      fetch(`${VIEWS_API}/${id}`, { method: 'POST', keepalive: true }).catch(() => {});
    } catch (e) {}
  }, []);

  // infinite scroll
  useEffect(() => {
    const obs = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting) setVisible((n) => Math.min(n + 3, items.length));
      },
      { rootMargin: '200px' }
    );
    if (loadMoreRef.current) obs.observe(loadMoreRef.current);
    return () => obs.disconnect();
  }, [items, visible]);

  const fmtViews = (n) => (n > 999 ? (n / 1000).toFixed(1).replace('.0', '') + 'k' : String(n));
  const srcDomain = (url) => {
    try { return new URL(url).hostname.replace(/^www\./, ''); } catch (e) { return ''; }
  };
  const fmtDate = (d) => {
    try { return new Date(d).toLocaleDateString('es-ES', { day: 'numeric', month: 'short' }); } catch (e) { return ''; }
  };

  return (
    <div className="viral-app">
      <Helmet>
        <title>Lo viral del día | UltimoLive</title>
        <meta name="description" content="Feed viral de noticias de Perú y el mundo: desplázate y toca para leer la noticia completa." />
        <meta property="og:type" content="website" />
      </Helmet>
      <header className="viral-top">
        <h1>Lo Viral</h1>
        <span className="viral-sub">Desplázate. Toca. Entérate.</span>
      </header>

      {loading && <div className="viral-loading">Cargando…</div>}
      {error && <div className="viral-error">{error}</div>}

      <div className="viral-feed">
        {items.slice(0, visible).map((it, i) => (
          <article key={it.id} className={`viral-card ${i === 0 ? 'first' : ''}`}>
            <a
              className="viral-link"
              href={it.url}
              target="_blank"
              rel="noopener noreferrer"
              aria-label={it.title}
            >
              <div
                className="viral-img"
                style={it.image ? { backgroundImage: `url(${it.image})` } : undefined}
              ></div>
            </a>
            <div className="viral-shade" />
            <div className="viral-body">
              <div className="viral-meta">
                <span className="viral-num">{i + 1}</span>
                <span className="viral-src">
                  {it.source} · {srcDomain(it.url)}
                </span>
                {fmtDate(it.published) && <time className="viral-date">{fmtDate(it.published)}</time>}
              </div>
              <a className="viral-title" href={it.url} target="_blank" rel="noopener noreferrer">
                {it.title}
              </a>
              <p className="viral-summary">{it.summary}</p>
              <div className="viral-foot">
                <span className="viral-views">
                  <svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true">
                    <path fill="currentColor" d="M12 5c5 0 9.3 3.1 11 7-1.7 3.9-6 7-11 7s-9.3-3.1-11-7c1.7-3.9 6-7 11-7zm0 9a2.5 2.5 0 100-5 2.5 2.5 0 000 5z"/>
                  </svg>
                  {fmtViews(views[it.id] || it.views || 0)}
                </span>
                <span className="viral-cta">Ver noticia completa →</span>
              </div>
            </div>
          </article>
        ))}
      </div>

      {visible < items.length && (
        <div ref={loadMoreRef} className="viral-more">
          Cargando más…
        </div>
      )}
      {visible >= items.length && items.length > 0 && (
        <div className="viral-end">Fin del feed · UltimoLive</div>
      )}
    </div>
  );
}

export default Viral;