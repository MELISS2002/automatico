import { Link } from 'react-router-dom';
import './PrivacyPolicy.css';  // Asegúrate de tener los estilos en un archivo CSS

const PrivacyPolicy = () => {
  return (
    <div className="legal-page">
      <center><h1 className="title">Política de Privacidad</h1></center>

      <p>
        Cuando navegas por nuestro sitio web y nos envías tus datos personales, como al comunicarte con nosotros a través de tu correo electrónico, confías en nosotros con tu información. Somos conscientes de esta gran responsabilidad y trabajamos seriamente para proteger tus datos y brindarte control sobre ellos.
        <br /><br />
        Esta política de privacidad tiene como objetivo ayudarte a comprender qué información recopilamos, por qué la recopilamos, así como la forma de actualizarla, exportarla y eliminarla.
        <br /><br />
        Esta política de privacidad se aplica a todos los datos personales que nos proporcionas a través de la aplicación móvil Goal4Kora o del sitio web Yalla Shoot Exclusive.
        <br /><br />
        Hemos establecido esta política de privacidad para fortalecer tu confianza en cuanto a la privacidad y seguridad de tus datos personales.
      </p>

      <div className="section-title"><h2>Información Recopilada</h2></div>
      <p>
        Es posible que se recopilen automáticamente información y datos mediante el uso de cookies, pequeños archivos de texto que permiten identificar tus preferencias y mejorar tu experiencia de navegación. Si prefieres no permitir la recopilación de información a través de cookies, puedes desactivarlas en tu navegador.
      </p>

      <div className="section-title"><h2>Datos Introducidos por Ti</h2></div>
      <p>
        Al completar formularios en nuestro sitio, como los de contacto o comentarios, nos proporcionas datos personales como nombre y correo electrónico. Esta información nos ayuda a responder a tus consultas. Bajo ninguna circunstancia se venderán ni compartirán estos datos con terceros, excepto por orden judicial.
      </p>

      <div className="section-title"><h2>¿Qué Hacemos con Tu Información?</h2></div>
      <p>
        Utilizamos tu información personal para:
        <ul>
          <li>Realizar análisis estadísticos del comportamiento de los visitantes.</li>
          <li>Cumplir con requisitos legales.</li>
          <li>Enviar comunicaciones periódicas, como boletines informativos.</li>
        </ul>
      </p>

      <div className="section-title"><h2>Actualizaciones</h2></div>
      <p>
        Nos reservamos el derecho de actualizar esta política de privacidad. Te recomendamos revisarla periódicamente para estar al tanto de cualquier cambio.
      </p>

      <div className="section-title"><h2>Correos Electrónicos</h2></div>
      <p>
        Al registrarte en nuestra lista de correos, aceptas recibir mensajes de nuestra parte. Si prefieres dejar de recibirlos, puedes cancelar la suscripción en cualquier momento desde el enlace en la parte inferior de cada correo.
      </p>

      <div className="section-title"><h2>Enlaces Externos</h2></div>
      <p>
        Nuestro sitio contiene enlaces a sitios externos. No somos responsables de las políticas de privacidad de esos sitios ni de su contenido. También usamos Google AdSense, que genera cookies para mejorar los anuncios.
      </p>

      <div className="section-title"><h2>Protección de Tu Información Personal</h2></div>
      <p>
        Aunque tomamos medidas de seguridad para proteger tu información, no podemos garantizar la seguridad absoluta de la transmisión de datos. Sin embargo, nos comprometemos a seguir estándares del sector para minimizar los riesgos.
      </p>

      <div className="section-title"><h2>Contacto</h2></div>
      <p>
        Si tienes alguna pregunta sobre esta política de privacidad, no dudes en contactarnos a: <a href="mailto:ameurus293@gmail.com">ameurus293@gmail.com</a>
      </p>

      <center><h1>¡Gracias por tu confianza!</h1></center>

      <Link to="/" className="back-link">Volver al inicio</Link>
    </div>
  );
};

export default PrivacyPolicy;
