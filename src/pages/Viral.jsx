import React, { useState, useEffect, useRef, useCallback } from 'react';
import { Helmet } from 'react-helmet-async';
import './Viral.css';

const VIEWS_API = '/api/viral-views';

function Viral() {
  const [items, setItems] = useState([]);
  const [visible, setVisible] = useState(4);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [views, setViews] = useState({});
  const [reader, setReader] = useState(null); // item abierto en vista de lectura
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
    try { return new Date(d).toLocaleDateString('es-ES', { day: 'numeric', month: 'short', year: 'numeric' }); } catch (e) { return ''; }
  };

  const openReader = (it) => {
    incView(it.id);
    setReader(it);
    try { window.scrollTo({ top: 0, behavior: 'smooth' }); } catch (e) {}
  };

  const closeReader = () => setReader(null);

  const renderContent = (content) => {
    if (!content) return <p>No hay texto disponible para esta noticia.</p>;
    return content.split(/\n{2,}/).map((par, i) => (
      <p key={i} className="reader-p">{par}</p>
    ));
  };

  return (
    <div className="viral-app">
      <Helmet>
        <title>{reader ? reader.title + ' | UltimoLive' : 'Lo viral del día | UltimoLive'}</title>
        <meta name="description" content="Feed viral de noticias de Perú y el mundo: desplázate y toca para leer la noticia completa." />
        <meta property="og:type" content="website" />
      </Helmet>

      {!reader && (
        <>
          <header className="viral-top">
            <h1>Lo Viral</h1>
            <span className="viral-sub">Desplázate. Toca. Entérate.</span>
          </header>

          {loading && <div className="viral-loading">Cargando…</div>}
          {error && <div className="viral-error">{error}</div>}

          <div className="viral-feed">
            {items.slice(0, visible).map((it, i) => (
              <article key={it.id} className={`viral-card ${i === 0 ? 'first' : ''}`}>
                <button
                  className="viral-link"
                  onClick={() => openReader(it)}
                  aria-label={it.title}
                >
                  <div
                    className="viral-img"
                    style={it.image ? { backgroundImage: `url(${it.image})` } : undefined}
                  ></div>
                </button>
                <div className="viral-shade" />
                <div className="viral-body">
                  <div className="viral-meta">
                    <span className="viral-num">{i + 1}</span>
                    <span className="viral-src">
                      {it.source} · {srcDomain(it.url)}
                    </span>
                    {fmtDate(it.published) && <time className="viral-date">{fmtDate(it.published)}</time>}
                  </div>
                  <button className="viral-title" onClick={() => openReader(it)}>
                    {it.title}
                  </button>
                  <p className="viral-summary">{it.summary}</p>
                  <div className="viral-foot">
                    <span className="viral-views">
                      <svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true">
                        <path fill="currentColor" d="M12 5c5 0 9.3 3.1 11 7-1.7 3.9-6 7-11 7s-9.3-3.1-11-7c1.7-3.9 6-7 11-7zm0 9a2.5 2.5 0 100-5 2.5 2.5 0 000 5z"/>
                      </svg>
                      {fmtViews(views[it.id] || it.views || 0)}
                    </span>
                    <span className="viral-cta">Leer noticia →</span>
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
        </>
      )}

      {reader && (
        <div className="reader">
          <header className="reader-top">
            <button className="reader-back" onClick={closeReader}>← Volver al feed</button>
            <span className="reader-source">{reader.source} · {srcDomain(reader.url)}</span>
          </header>
          <div className="reader-hero" style={reader.image ? { backgroundImage: `url(${reader.image})` } : undefined}>
            <div className="reader-shade" />
          </div>
          <article className="reader-article">
            <h1 className="reader-title">{reader.title}</h1>
            <div className="reader-byline">
              <span className="viral-views">
                <svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true">
                  <path fill="currentColor" d="M12 5c5 0 9.3 3.1 11 7-1.7 3.9-6 7-11 7s-9.3-3.1-11-7c1.7-3.9 6-7 11-7zm0 9a2.5 2.5 0 100-5 2.5 2.5 0 000 5z"/>
                </svg>
                {fmtViews(views[reader.id] || reader.views || 0)} vistas
              </span>
              {fmtDate(reader.published) && <time className="reader-date">{fmtDate(reader.published)}</time>}
            </div>
            <div className="reader-content">
              {renderContent(reader.content)}
            </div>
            <p className="reader-note">
              Fuente: <a href={reader.url} target="_blank" rel="noopener noreferrer">{reader.source}</a>
            </p>
          </article>
        </div>
      )}
    </div>
  );
}

export default Viral;