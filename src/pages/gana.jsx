import { useState, useEffect } from 'react';
import NewsGrid from './NewsGridjana';
import './gana.css';

function Gana() {
  const [news, setNews] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  // Cargar noticias desde el JSON
  useEffect(() => {
    const loadNews = async () => {
      try {
        const response = await fetch('/posts/gana.json');
        const data = await response.json();
        setNews(data);
      } catch (err) {
        console.error("Error al cargar noticias:", err);
      } finally {
        setIsLoading(false);
      }
    };
    loadNews();
  }, []);

  return (
    <div className="app">
      <main className="main-content">
        {/* Sección principal: Trucos para ganar dinero */}
        <section className="tips-section">
          <h1 className="main-heading">💸 Cómo Ganar Dinero en Internet en 2025</h1>
          <p className="intro-text">
            ¿Estás buscando nuevas formas de generar ingresos desde casa o aprovechar el poder de internet para ganar dinero extra?
            Has llegado al lugar indicado. En esta guía te revelamos los métodos más efectivos y modernos para ganar dinero online este año.
            ¡Toma nota y comienza tu camino hacia la libertad financiera digital!
          </p>

          <div className="tip-block">
            <h3>🛒 1. Vende Productos o Servicios Online</h3>
            <p>
              Utiliza plataformas como MercadoLibre, Etsy o Facebook Marketplace para ofrecer productos físicos. También puedes vender servicios como edición de video, diseño gráfico o mentorías personalizadas a través de tu sitio web o redes sociales.
            </p>
          </div>

          <div className="tip-block">
            <h3>🤝 2. Marketing de Afiliados</h3>
            <p>
              Promociona productos de terceros en tus redes sociales, blog o canal de YouTube y recibe comisiones por cada venta. Sitios como Hotmart, Amazon Afiliados y ClickBank son ideales para comenzar.
            </p>
          </div>

          <div className="tip-block">
            <h3>🎓 3. Crea Cursos Online</h3>
            <p>
              Si dominas algún tema como fotografía, programación o idiomas, puedes armar un curso en plataformas como Udemy o Teachable y venderlo una y otra vez sin esfuerzo adicional.
            </p>
          </div>

          <div className="tip-block">
            <h3>💼 4. Trabaja como Freelancer</h3>
            <p>
              Ofrece tus habilidades como redactor, traductor, diseñador web o programador en plataformas como Fiverr, Freelancer o Workana. ¡Hay demanda para todo tipo de talento!
            </p>
          </div>

          <div className="tip-block">
            <h3>📊 5. Realiza Encuestas Remuneradas</h3>
            <p>
              Plataformas como Toluna, Swagbucks y LifePoints te pagan por dar tu opinión en encuestas de mercado. No es mucho dinero, pero es fácil y rápido.
            </p>
          </div>

          <div className="call-to-action">
            <p>🔎 Explora más trucos en nuestros artículos a continuación y conviértete en tu propio jefe desde casa. ¡Tu éxito online comienza hoy!</p>
          </div>
        </section>

        {/* Sección de artículos dinámicos */}
        <section className="news-section">
          <h2 className="section-title">📰 Últimos Artículos sobre Ganancias Online</h2>
          {isLoading ? (
            <p className="loading-text">Cargando artículos...</p>
          ) : (
            <NewsGrid articles={news} />
          )}
        </section>
      </main>
    </div>
  );
}

export default Gana;
