import { useState, useEffect, useRef } from 'react';
import NewsGrid from './components/NewsGrid';
import ShareButtons from './components/ShareButtons';
import './App.css';

const SITE_TITLE = 'UltimoLive - Noticias deportivas, resultados y transmisiones en vivo';

function App() {
  const [currentStream, setCurrentStream] = useState(null);
  const [news, setNews] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedArticle, setSelectedArticle] = useState(null);
  const [articleContent, setArticleContent] = useState('');
  const streamPlayerRef = useRef(null);

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

  const loadHTMLContent = async (path) => {
    try {
      const response = await fetch(path);
      if (!response.ok) throw new Error('HTTP error ' + response.status);
      return await response.text();
    } catch (error) {
      console.error('Error cargando contenido:', error);
      return '<p>Error al cargar el artículo</p>';
    }
  };

  const handleReadArticle = async (article) => {
    const content = await loadHTMLContent(article.htmlPath);
    setArticleContent(content);
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

  return (
    <div className="app">
      <main className="main-content">
        {selectedArticle ? (
          <div className="article-viewer">
            <button className="back-button" onClick={handleCloseArticle}>
              &larr; Volver al inicio
            </button>
            <div className="article-header">
              <h1>{selectedArticle.title}</h1>
              <div className="article-meta">
                <span className="author">Por {selectedArticle.author}</span>
                <time className="date">{formatDate(selectedArticle.date)}</time>
              </div>
            </div>
            <ShareButtons
              slug={selectedArticle.slug}
              title={selectedArticle.title}
            />
            <div
              className="html-content"
              dangerouslySetInnerHTML={{ __html: articleContent }}
            />
            <ShareButtons
              slug={selectedArticle.slug}
              title={selectedArticle.title}
            />
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
    </div>
  );
}

export default App;
