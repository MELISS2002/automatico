import { useState, useEffect } from 'react';
import NewsGrid from './NewsGridsalud';
import './salud.css';

function Salud() {
  const [news, setNews] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  // Cargar noticias desde el JSON
  useEffect(() => {
    const loadNews = async () => {
      try {
        const response = await fetch('/posts/salud.json');
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

        {/* Sección principal: Consejos de Salud Natural */}
        <section className="tips-section">
          <h1 className="main-heading">Consejos de Salud Natural</h1>
          <p className="intro-text">
            En un mundo donde el estrés y las enfermedades modernas son cada vez más comunes,
            adoptar un estilo de vida saludable basado en remedios naturales se ha vuelto esencial.
            Descubre aquí las mejores prácticas para mejorar tu bienestar físico y mental de forma natural.
          </p>




          <div className="call-to-action">
            <p>Descubre más consejos saludables en nuestros artículos a continuación y transforma tu estilo de vida con bienestar natural. Tu salud es tu mayor riqueza.</p>
          </div>
        </section>

        {/* Sección de artículos dinámicos */}
        <section className="news-section">
          <h2 className="section-title">Últimos Artículos sobre Salud y Bienestar</h2>
          {isLoading ? (
            <p className="loading-text">Cargando artículos...</p>
          ) : (
            <NewsGrid articles={news} />
          )}
        </section>
          <div className="tip-block">
  <h3>1. Infusiones y Tés Medicinales</h3>
  <p>
    Las infusiones naturales son un regalo milenario para nuestro cuerpo y mente.
    Hierbas como <strong>manzanilla, jengibre, menta o diente de león</strong> ofrecen múltiples beneficios:
    desde aliviar dolores estomacales, hasta calmar la ansiedad o mejorar la digestión.
    Incorpora estas bebidas en tu rutina diaria, ya sea al despertar o antes de dormir,
    y sentirás una diferencia notable en tu bienestar general.
    Acompáñalas con momentos de silencio o lectura para potenciar sus efectos relajantes.
  </p>
</div>

<div className="tip-block">
  <h3>2. Alimentación Consciente y Natural</h3>
  <p>
    Una alimentación saludable no se trata solo de lo que comes, sino de <strong>cómo lo haces</strong>.
    Prioriza alimentos frescos, orgánicos y de temporada: frutas jugosas, verduras verdes, legumbres,
    granos enteros y semillas ricas en omega-3. Evita el consumo de productos ultraprocesados,
    azúcares refinados y grasas trans. Comer con atención plena, masticando lentamente
    y disfrutando cada bocado, te ayudará no solo a nutrir tu cuerpo, sino también
    a equilibrar tu mente y emociones.
  </p>
</div>

<div className="tip-block">
  <h3>3. Relajación Profunda y Meditación Diaria</h3>
  <p>
    La salud no está completa sin <strong>bienestar emocional</strong>.
    Practicar yoga suave, ejercicios de respiración o meditaciones guiadas diariamente reduce
    significativamente el estrés, mejora el enfoque y fortalece la resiliencia mental.
    Dedicar al menos <strong>10 minutos al día</strong> a estar contigo mismo, en silencio y sin distracciones,
    es una inversión poderosa para tu paz interior.
    Puedes comenzar con técnicas sencillas como el <em>escaneo corporal</em> o la <em>respiración 4-7-8</em>.
  </p>
</div>

<div className="tip-block">
  <h3>4. Hidratación Constante y Detox Natural</h3>
  <p>
    El agua es vida, y mantenerse hidratado es esencial para que cada célula funcione correctamente.
    Beber entre <strong>2 y 3 litros de agua</strong> al día ayuda a depurar toxinas, mantener la piel radiante
    y favorecer el metabolismo. Para intensificar el efecto desintoxicante,
    puedes empezar el día con un vaso de agua tibia con limón o preparar <em>jugos verdes</em>
    con apio, pepino y manzana verde. ¡Tu sistema digestivo y tu piel te lo agradecerán!
  </p>
</div>

<div className="tip-block">
  <h3>5. Conexión con la Naturaleza y el Sol</h3>
  <p>
    Pasar tiempo al aire libre es una <strong>medicina natural</strong> muchas veces subestimada.
    Caminar descalzo sobre el césped, respirar aire puro o simplemente sentarte bajo el sol
    te ayuda a recargar energías, fortalecer tus defensas y mejorar tu estado de ánimo.
    La exposición responsable al sol también estimula la producción de <strong>vitamina D</strong>,
    esencial para la salud ósea y la regulación hormonal.
    Intenta desconectarte de la tecnología al menos una vez al día y reconecta con lo esencial.
  </p>
</div>
      </main>
    </div>
  );
}

export default Salud;
