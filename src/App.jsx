import { useState, useEffect, useRef } from 'react';
import { Helmet } from 'react-helmet-async';
import DOMPurify from 'dompurify';
import NewsGrid from './components/NewsGrid';
import ShareButtons from './components/ShareButtons';
import './App.css';

const SITE_TITLE = 'UltimoLive - Noticias deportivas, resultados y transmisiones en vivo';

// Limpia el HTML de los posts: quita head/style/script/footer y el bloque hero
// (duplica el titulo y meta que ya muestra el viewer) para que el articulo
// use el design system del sitio en lugar del CSS propio del post.
// Sanitiza y limpia el HTML de los posts usando DOMPurify
const cleanArticleHTML = (raw) => {
  try {
    return DOMPurify.sanitize(raw, {
      ALLOWED_TAGS: ['p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li', 'a', 'img', 'blockquote', 'pre', 'code', 'hr', 'table', 'thead', 'tbody', 'tr', 'th', 'td', 'div', 'span', 'section', 'article', 'header', 'footer', 'nav', 'main', 'aside', 'figure', 'figcaption', 'mark', 'small', 'sub', 'sup', 'time'],
      ALLOWED_ATTR: ['href', 'src', 'alt', 'title', 'class', 'id', 'style', 'target', 'rel', 'width', 'height', 'loading', 'role', 'aria-label']
    });
  } catch (e) {
    return raw;
  }
};

// Estimacion de lectura: ~200 palabras/minuto
const estimateReadTime = (html) => {
  const text = html.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();
  const words = text ? text.split(' ').length : 0;
  return Math.max(1, Math.round(words / 200));
};

function App() {
  const [currentStream, setCurrentStream] = useState(null);
  const [news, setNews] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedArticle, setSelectedArticle] = useState(null);
  const [articleContent, setArticleContent] = useState('');
  const [readTime, setReadTime] = useState(0);
  const [readingProgress, setReadingProgress] = useState(0);
  const [showTopBtn, setShowTopBtn] = useState(false);
  const streamPlayerRef = useRef(null);

  // Metadatos SEO dinámicos
  const pageTitle = selectedArticle ? `${selectedArticle.title} | UltimoLive` : 'UltimoLive - Noticias deportivas, resultados y transmisiones en vivo';
  const pageDescription = selectedArticle?.excerpt || 'Últimas noticias deportivas, resultados en vivo y transmisiones en directo.';
  const pageImage = selectedArticle?.image || '/logo-og.png';
  const pageUrl = typeof window !== 'undefined' ? window.location.href : 'https://ultimolive.com';

  // Metadatos SEO dinámicos
  const pageTitle = selectedArticle ? `${selectedArticle.title} | UltimoLive` : 'UltimoLive - Noticias deportivas, resultados y transmisiones en vivo';
  const pageDescription = selectedArticle?.excerpt || 'Últimas noticias deportivas, resultados en vivo y transmisiones en directo.';

  // Cargar noticias
  useEffect(() => {
    const loadNews = async () => {
      try {
        const response = await fetch('/posts/home.json');
        const data = await response.json();
        setNews(data);
      } catch (err) {
        console.error("Error loading news:", err);
      } finally {
        setIsLoading(false);
      }
    };
    loadNews();
  }, []);

  // Manejar mensajes del iframe de la agenda
  useEffect(() => {
    const handleMessage = (event) => {
      if (event.data.type === 'LOAD_STREAM') {
        setCurrentStream(event.data.url);
        setTimeout(() => {
          streamPlayerRef.current?.scrollIntoView({
            behavior: 'smooth',
            block: 'center'
          });
        }, 300);
      }
    };

    window.addEventListener('message', handleMessage);
    return () => window.removeEventListener('message', handleMessage);
  }, []);

  // Progreso de lectura + boton volver arriba
  useEffect(() => {
    const handleScroll = () => {
      const doc = document.documentElement;
      const total = doc.scrollHeight - window.innerHeight;
      setReadingProgress(total > 0 ? (window.scrollY / total) * 100 : 0);
      setShowTopBtn(window.scrollY > 600);
    };
    window.addEventListener('scroll', handleScroll, { passive: true });
    handleScroll();
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const loadHTMLContent = async (path) => {
    try {
      const response = await fetch(path);
      if (!response.ok) throw new Error('HTTP error ' + response.status);
      return cleanArticleHTML(await response.text());
    } catch (error) {
      console.error('Error cargando contenido:', error);
      return '<p>Error al cargar el artículo</p>';
    }
  };

  const handleReadArticle = async (article) => {
    const content = await loadHTMLContent(article.htmlPath);
    setArticleContent(content);
    setReadTime(estimateReadTime(content));
    setSelectedArticle(article);
    document.title = article.title;
    window.scrollTo(0, 0);
  };

  const handleCloseArticle = () => {
    setSelectedArticle(null);
    setArticleContent('');
    document.title = SITE_TITLE;
    window.scrollTo(0, 0);
  };

  const formatDate = (dateString) => {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('es-ES', options);
  };

  const featured = news[0];
  const secondary = news.slice(1, 5);
  const rest = news.slice(5);

  // Articulos relacionados: misma categoria, excluye el actual, max 3
  const related = selectedArticle
    ? news
        .filter((a) => a.slug !== selectedArticle.slug)
        .sort((a, b) => {
          const sameA = a.category === selectedArticle.category ? 0 : 1;
          const sameB = b.category === selectedArticle.category ? 0 : 1;
          return sameA - sameB;
        })
        .slice(0, 3)
    : [];

  const categoryName = (cat) => {
    const map = { home: 'Inicio', gana: 'Gana', salud: 'Salud' };
    return map[cat] || cat || 'Noticias';
  };

  return (
    <div className="app">
      <Helmet>
        <title>{pageTitle}</title>
        <meta name="description" content={pageDescription} />
        <meta property="og:title" content={pageTitle} />
        <meta property="og:description" content={pageDescription} />
        <meta property="og:image" content={pageImage} />
        <meta property="og:url" content={pageUrl} />
        <meta property="og:type" content="website" />
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:title" content={pageTitle} />
        <meta name="twitter:description" content={pageDescription} />
        <meta name="twitter:image" content={pageImage} />
        <link rel="canonical" href={pageUrl} />
      </Helmet>
      {/* Barra de progreso de lectura (patron editorial profesional) */}
      <div
        className="reading-progress"
        style={{ width: `${readingProgress}%` }}
        aria-hidden="true"
      ></div>

      <main className="main-content">
        {selectedArticle ? (
          <div className="article-viewer">
            <nav className="breadcrumbs" aria-label="Ruta de navegación">
              <button className="crumb-link" onClick={handleCloseArticle}>Inicio</button>
              <span className="crumb-sep">/</span>
              <span className="crumb-current">{categoryName(selectedArticle.category)}</span>
            </nav>
            <button className="back-button" onClick={handleCloseArticle}>
              &larr; Volver al inicio
            </button>
            <div className="article-header">
              <h1>{selectedArticle.title}</h1>
              <div className="article-meta">
                <span className="author">Por {selectedArticle.author}</span>
                <time className="date">{formatDate(selectedArticle.date)}</time>
                {readTime > 0 && (
                  <span className="read-time">{readTime} min de lectura</span>
                )}
              </div>
            </div>
            <div
              className="html-content"
              dangerouslySetInnerHTML={{ __html: articleContent }}
            />
            <ShareButtons
              slug={selectedArticle.slug}
              title={selectedArticle.title}
            />
            {related.length > 0 && (
              <section className="related-section">
                <h2 className="section-title">Sigue leyendo</h2>
                <NewsGrid articles={related} onRead={handleReadArticle} />
              </section>
            )}
          </div>
        ) : (
          <>
            {/* Banner de descarga */}
            <div className="download-banner">
              <div className="banner-content">
                <div className="banner-text">
                  <div>
                    <h3>Descarga nuestra App</h3>
                    <p>Disfruta de todos los partidos en HD, sin cortes y con la mejor calidad.</p>
                  </div>
                </div>
                <a
                  href="https://raw.githubusercontent.com/belkaperu/json/main/app.apk"
                  className="download-button"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Descargar ahora
                </a>
              </div>
            </div>

            {/* Hero: artículo destacado */}
            {isLoading ? (
              <div className="skeleton skeleton-hero"></div>
            ) : featured ? (
              <article className="hero-card" onClick={() => handleReadArticle(featured)}>
                <div className="hero-image">
                  <img src={featured.thumbnail} alt={featured.title} loading="lazy" />
                </div>
                <div className="hero-overlay">
                  <span className="kicker">Destacado</span>
                  <h1 className="hero-title">{featured.title}</h1>
                  <p className="hero-excerpt">{featured.excerpt}</p>
                  <div className="hero-meta">
                    <span>{featured.author}</span>
                    <time>{formatDate(featured.date)}</time>
                  </div>
                </div>
              </article>
            ) : null}

            {/* Agenda + Streams — arriba, justo después del hero */}
            <section className="live-section">
              <div className="live-panel">
                <h3>Agenda deportiva</h3>
                <div className="agenda-container">
                  <iframe
                    src="/agenda.html"
                    title="Agenda Deportiva"
                    loading="lazy"
                  />
                </div>
              </div>
              <div className="live-panel" ref={streamPlayerRef}>
                <h3>Transmisiones en vivo</h3>
                <div className="stream-player">
                  {currentStream ? (
                    <iframe
                      src={currentStream}
                      title="Stream en vivo"
                      allowFullScreen
                      frameBorder="0"
                      className="stream-iframe"
                      loading="lazy"
                    />
                  ) : (
                    <div className="placeholder">
                      <p>Selecciona un partido de la agenda para comenzar a disfrutar del juego</p>
                    </div>
                  )}
                </div>
              </div>
            </section>

            {/* Secundarias */}
            {secondary.length > 0 && (
              <section className="news-section">
                <h2 className="section-title">Más noticias</h2>
                <NewsGrid articles={secondary} onRead={handleReadArticle} />
              </section>
            )}

            {/* Resto de artículos */}
            {rest.length > 0 && (
              <section className="news-section">
                <h2 className="section-title">Últimos artículos</h2>
                <NewsGrid articles={rest} onRead={handleReadArticle} />
              </section>
            )}

            {/* Banners internos */}
            <section className="banners">
              <a className="banner-card" href="/gana">
                <h3>Trucos para Ganar</h3>
                <p>Métodos prácticos para generar ingresos desde casa y aprovechar internet.</p>
                <span className="read-more">Explorar la sección</span>
              </a>
              <a className="banner-card" href="/salud">
                <h3>Salud Natural</h3>
                <p>Guías de bienestar y remedios naturales respaldados por información clara.</p>
                <span className="read-more">Explorar la sección</span>
              </a>
            </section>
          </>
        )}
      </main>

      {/* Volver arriba */}
      {showTopBtn && (
        <button
          className="back-to-top"
          onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
          aria-label="Volver arriba"
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
            <path d="M12 19V5M5 12l7-7 7 7" />
          </svg>
        </button>
      )}
    </div>
  );
}

export default App;
