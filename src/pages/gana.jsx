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
    El comercio digital ha democratizado la posibilidad de emprender desde casa.
    Puedes comenzar vendiendo productos físicos como ropa, artesanías, accesorios personalizados
    o incluso productos de segunda mano en plataformas como <strong>MercadoLibre, Etsy</strong> o <strong>Facebook Marketplace</strong>.
    Además, si tienes conocimientos especializados, también puedes <strong>ofrecer servicios digitales</strong> como
    edición de video, diseño gráfico, asesorías en redes sociales, mentorías personalizadas, clases particulares
    o creación de contenido. Crea tu propia tienda en línea, utiliza redes sociales para llegar a tu audiencia
    y brinda una experiencia de usuario única.
  </p>
</div>

<div className="tip-block">
  <h3>🤝 2. Marketing de Afiliados</h3>
  <p>
    El marketing de afiliados te permite ganar dinero recomendando productos o servicios
    de otras marcas. Recibes una comisión cada vez que alguien compra a través de tu enlace.
    Puedes usar tus <strong>redes sociales, blog, canal de YouTube o newsletter</strong> para promocionar productos que uses
    o en los que creas. Plataformas como <strong>Hotmart, Amazon Afiliados</strong> y <strong>ClickBank</strong> son perfectas para comenzar,
    y puedes elegir nichos que te apasionen: tecnología, bienestar, cursos, gadgets, etc.
    Es un modelo escalable y sin necesidad de inventario propio.
  </p>
</div>

<div className="tip-block">
  <h3>🎓 3. Crea y Vende Cursos Online</h3>
  <p>
    Compartir tus conocimientos puede convertirse en una fuente constante de ingresos pasivos.
    Si eres experto en un tema como <strong>fotografía, cocina, idiomas, finanzas, programación o desarrollo personal</strong>,
    puedes estructurar ese conocimiento en módulos y crear un curso online. Utiliza plataformas como <strong>Udemy,
    Domestika, Coursera</strong> o <strong>Teachable</strong> para publicarlo. Lo mejor es que puedes venderlo miles de veces sin tener
    que grabarlo nuevamente. Solo necesitas un buen guion, contenido claro, práctica, y constancia para promocionarlo.
  </p>
</div>

<div className="tip-block">
  <h3>💼 4. Trabaja como Freelancer</h3>
  <p>
    Si tienes habilidades profesionales, puedes convertirte en tu propio jefe ofreciendo tus servicios
    como freelancer. Algunas de las áreas más solicitadas incluyen: <strong>redacción, traducción, diseño gráfico, programación,
    marketing digital, gestión de redes sociales, soporte técnico, y más</strong>.
    Existen plataformas como <strong>Fiverr, Freelancer, Upwork</strong> y <strong>Workana</strong> donde puedes crear tu perfil,
    mostrar tu portafolio y comenzar a recibir encargos desde cualquier parte del mundo.
    Es una excelente opción para trabajar por proyectos, ganar en dólares y escalar poco a poco.
  </p>
</div>

<div className="tip-block">
  <h3>📊 5. Realiza Encuestas Remuneradas y Microtareas</h3>
  <p>
    Aunque no es una fuente de ingresos elevada, participar en encuestas pagadas o completar
    microtareas online puede brindarte un ingreso extra sin complicaciones.
    Plataformas como <strong>Toluna, Swagbucks, LifePoints</strong> o <strong>ySense</strong> te pagan por compartir tu opinión
    sobre productos, hábitos de consumo, y tendencias del mercado. También puedes probar tareas pequeñas como
    clasificar imágenes, probar apps o responder trivias. Es ideal para estudiantes o personas que quieren
    aprovechar tiempos muertos de forma productiva.
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
