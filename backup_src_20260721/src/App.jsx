import { useState, useEffect, useRef } from 'react';
import Header from './components/Header';
import NewsGrid from './components/NewsGrid';
import './App.css';
import About from './pages/About';
import Contact from './pages/Contact';
import Terms from './pages/Terms';

function App() {
  // Estados para los streams y noticias
  const [currentStream, setCurrentStream] = useState(null);
  const [news, setNews] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  // Referencia para el scroll automático
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

        // Scroll automático al reproductor
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

  return (
    <div className="app">
      <main className="main-content">
        {/* Banner atractivo para descargar la app */}
        <div className="download-banner">
          <div className="banner-content">
            <div className="banner-text">
              <span className="banner-icon">📱</span>
              <div>
                <h3>Descarga nuestra App</h3>
                <p>Disfruta de todos los partidos en HD, sin cortes y con la mejor calidad.</p>
              </div>
            </div>
            <a 
              href="https://raw.githubusercontent.com/belkaperu/json/main/app.apk" // Reemplaza con tu enlace real
              className="download-button"
              target="_blank"
              rel="noopener noreferrer"
            >
              Descargar ahora
              <span className="button-icon">⬇️</span>
            </a>
          </div>
        </div>

        {/* Sección de agenda siempre visible */}
        <section className="live-section">
          <div className="agenda-container">
            <iframe
              src="/agenda.html"
              title="Agenda Deportiva"
            />
          </div>
        </section>

        {/* Sección de noticias */}
        <section className="news-section">
          <h2 className="section-title">Ultimo Articulo 📰</h2>
          {isLoading ? <p>Cargando noticias...</p> : <NewsGrid articles={news} />}
        </section>

        {/* Sección del reproductor con ref para scroll */}
        <section className="stream-section dark-mode" ref={streamPlayerRef}>
          <h2 className="section-title">🎥 Transmisiones en Vivo</h2>
          <div className="stream-player">
            {currentStream ? (
              <iframe
                src={currentStream}
                title="Stream en vivo"
                allowFullScreen
                frameBorder="0"
                className="stream-iframe"
              />
            ) : (
              <center>
                <div className="placeholder">
                  <img
                    src="https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif"
                    alt="Esperando transmisión"
                    className="placeholder-gif"
                  />
                  <p>Selecciona un partido de la agenda para comenzar a disfrutar del juego ⚽</p>
                </div>
              </center>
            )}
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;