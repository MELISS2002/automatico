import { useState, useEffect, useRef } from 'react';
import Header from './components/Header';
import NewsGrid from './components/NewsGrid';
import './App.css';
import About from './pages/About';
import Contact from './pages/Contact';
import Terms from './pages/Terms';
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
    const operation = Math.floor(Math.random() * 4); // 0: suma, 1: resta, 2: multiplicación, 3: división
    let problemText;
    let correctAnswer;
    let firstNumber = num1;
    let secondNumber = num2;
    let generatedDividend;
    let generatedDivisor;
  
    switch (operation) {
     case 0:
      problemText = `${firstNumber} + ${secondNumber} = ?`;
      correctAnswer = firstNumber + secondNumber;
      break;
     case 1:
      // Asegurar que el resultado no sea negativo para un nivel básico
      firstNumber = Math.max(num1, num2);
      secondNumber = Math.min(num1, num2);
      problemText = `${firstNumber} - ${secondNumber} = ?`;
      correctAnswer = firstNumber - secondNumber;
      break;
     case 2:
      problemText = `${firstNumber} * ${secondNumber} = ?`;
      correctAnswer = firstNumber * secondNumber;
      break;
     case 3:
      // Generar números que den una división entera dentro de un rango razonable
      correctAnswer = Math.floor(Math.random() * 10) + 1;
      generatedDivisor = Math.floor(Math.random() * 5) + 1;
      generatedDividend = correctAnswer * generatedDivisor;
      firstNumber = generatedDividend;
      secondNumber = generatedDivisor;
      problemText = `${generatedDividend} / ${generatedDivisor} = ?`;
      break;
     default:
      problemText = "";
      correctAnswer = 0;
    }
  
    return {
     num1: firstNumber,
     num2: secondNumber,
     answer: correctAnswer,
     text: problemText,
     operation: ["suma", "resta", "multiplicación", "división"][operation],
     checkAnswer: (userAnswer) => {
      if (parseInt(userAnswer) === correctAnswer) {
       return true;
      } else {
       const operationName = ["sumando", "restando", "multiplicando", "dividiendo"][operation];
       const funnyMessages = [
        `¡Uy! Casi le atinas, pero ${firstNumber} ${operationName} ${secondNumber} no da eso. ¡Inténtalo otra vez antes de que los números se escapen!`,
        `Hmm, parece que los números están un poco rebeldes hoy. ¡Dale otra oportunidad a este acertijo matemático!`,
        `¡No te rindas! Incluso los genios tienen un mal día con las cuentas. ¿Será este tu día de gloria numérica?`,
        `Esa respuesta está... interesante. ¡Pero no es la que estamos buscando! Prueba otra vez, ¡quizás los números te tengan más cariño ahora!`,
        `¡Cuidado! Parece que tus cálculos se fueron de paseo. ¡Tráelos de vuelta e inténtalo de nuevo!`,
       ];
       const randomIndex = Math.floor(Math.random() * funnyMessages.length);
       return funnyMessages[randomIndex];
      }
     },
    };
   }

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
   
      <main className="main-content">
        {/* Sección de verificación y agenda */}
        <section className="live-section">
          <h2 className="section-title">Problema resuelto</h2>
          
          {!showAgenda ? (
            <div className="verification-box">
<h3>¡Desafío Exclusivo!</h3>
<p>¡Desafío en Marcha! Pon a prueba tu ingenio con este reto ágil y descubre una recompensa aún más gratificante. ¡Acepta el desafío ahora y eleva tu experiencia al máximo!</p>

              
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
      <center>    <div className="placeholder">
        <img
          src="https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif"
          alt="Esperando transmisión"
          className="placeholder-gif"
        />
        <p>Selecciona un partido de la agenda para comenzar a disfrutar del juego ⚽</p>
      </div></center>
    )}
  </div>
</section>

      </main>


    </div>
  );
}

export default App;