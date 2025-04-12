import { useState, useEffect, useRef } from 'react';
import Header from './components/Header';
import NewsGrid from './components/NewsGrid';
import './App.css';

function App() {
  // Estados para la verificación
  const [mathProblem, setMathProblem] = useState(generateMathProblem());
  const [userAnswer, setUserAnswer] = useState('');
  const [showAgenda, setShowAgenda] = useState(false);
  const [error, setError] = useState('');
  const [attempts, setAttempts] = useState(0);

  // Estados para los streams y noticias
  const [currentStream, setCurrentStream] = useState(null);
  const [news, setNews] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  // Referencia para el scroll automático
  const streamPlayerRef = useRef(null);

  // Generar problema matemático
  function generateMathProblem() {
    const num1 = Math.floor(Math.random() * 10) + 1;
    const num2 = Math.floor(Math.random() * 10) + 1;
    return {
      num1,
      num2,
      answer: num1 + num2,
      text: `${num1} + ${num2} = ?`
    };
  }

  // Cargar noticias
  useEffect(() => {
    const loadNews = async () => {
      try {
        const response = await fetch('/posts/manifest.json');
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

  // Verificar respuesta matemática
  const verifyAnswer = (e) => {
    e.preventDefault();
    
    if (attempts >= 3) {
      setError('Demasiados intentos. Por favor espera unos minutos.');
      return;
    }

    if (parseInt(userAnswer) === mathProblem.answer) {
      setShowAgenda(true);
      setError('');
    } else {
      setAttempts(attempts + 1);
      setError('Respuesta incorrecta. Intenta nuevamente.');
      setMathProblem(generateMathProblem());
      setUserAnswer('');
    }
  };

  return (
    <div className="app">
      <Header />
      
      <main className="main-content">
        {/* Sección de verificación y agenda */}
        <section className="live-section">
          <h2 className="section-title">Live Matches ⚽</h2>
          
          {!showAgenda ? (
            <div className="verification-box">
              <h3>Verificación Requerida</h3>
              <p>Resuelve para ver los partidos en HD:</p>
              
              <div className="math-problem">{mathProblem.text}</div>
              
              <form onSubmit={verifyAnswer}>
                <input
                  type="number"
                  value={userAnswer}
                  onChange={(e) => setUserAnswer(e.target.value)}
                  placeholder="Tu respuesta"
                  required
                />
                {error && <p className="error">{error}</p>}
                <button type="submit">Verificar</button>
              </form>
            </div>
          ) : (
            <div className="agenda-container">
              <iframe 
                src="/agenda.html" 
                title="Agenda Deportiva"
              
              />
            </div>
          )}
        </section>

        {/* Sección de noticias */}
        <section className="news-section">
          <h2 className="section-title">Latest News 📰</h2>
          {isLoading ? <p>Cargando noticias...</p> : <NewsGrid articles={news} />}
        </section>

        {/* Sección del reproductor con ref para scroll */}
        <section className="stream-section" ref={streamPlayerRef}>
          <h2 className="section-title">Live Streams 📺</h2>
          <div className="stream-player">
            {currentStream ? (
              <iframe
                src={currentStream}
                title="Stream en vivo"
                allowFullScreen
        
              />
            ) : (
              <div className="placeholder">
                <p>Selecciona un partido de la agenda para ver el stream</p>
              </div>
            )}
          </div>
        </section>
      </main>

      <footer className="footer">
        <p>© {new Date().getFullYear()} SportsLive</p>
      </footer>
    </div>
  );
}

export default App;