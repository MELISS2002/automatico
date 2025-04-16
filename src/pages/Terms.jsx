import React from 'react';
import { Link } from 'react-router-dom';  // Importa el Link para navegar entre páginas
import './Terms.css';  // Asegúrate de tener un archivo CSS para los estilos

const Terms = () => (
  <div className="terms-page-container">
    <center><h1 className="page-title">Términos de Servicio</h1></center>

    <p>
      Al acceder y utilizar nuestra plataforma, aceptas cumplir con los siguientes términos y condiciones. Te recomendamos leer detenidamente todos los términos antes de continuar con el uso del sitio web y nuestros servicios.
    </p>

    <div className="section-title"><h2>Condiciones de Uso</h2></div>
    <p>
      Nuestro sitio web ofrece una plataforma para [describir brevemente el servicio ofrecido]. El acceso y uso de nuestros servicios están sujetos a las siguientes condiciones:
      <ul>
        <li>El uso del sitio es únicamente para fines personales y no comerciales.</li>
        <li>El contenido del sitio web es propiedad de [nombre de la empresa] y está protegido por derechos de autor.</li>
        <li>No está permitido modificar, copiar, distribuir o reproducir los materiales sin el permiso explícito de [nombre de la empresa].</li>
      </ul>
    </p>

    <div className="section-title"><h2>Responsabilidades del Usuario</h2></div>
    <p>
      Como usuario, eres responsable de:
      <ul>
        <li>Proveer información veraz y completa al registrarte en el sitio.</li>
        <li>Cumplir con todas las leyes aplicables al usar la plataforma.</li>
        <li>No utilizar el sitio de forma que pueda dañar, deshabilitar, sobrecargar o interferir con el uso de otros usuarios.</li>
      </ul>
    </p>

    <div className="section-title"><h2>Modificaciones y Actualizaciones</h2></div>
    <p>
      [Nombre de la empresa] se reserva el derecho de modificar, actualizar o cambiar estos términos en cualquier momento. Te recomendamos revisar esta página periódicamente para estar informado sobre cualquier cambio.
    </p>

    <div className="section-title"><h2>Política de Privacidad</h2></div>
    <p>
      Para conocer cómo recopilamos, usamos y protegemos tu información personal, consulta nuestra <a href="/privacy-policy">Política de Privacidad</a>.
    </p>

    <div className="section-title"><h2>Limitación de Responsabilidad</h2></div>
    <p>
      En ningún caso, [nombre de la empresa] será responsable por daños indirectos, incidentales o consecuentes derivados del uso de la plataforma.
    </p>

    <center><h1>Gracias por leer nuestros Términos de Servicio</h1></center>

    <Link to="/" className="back-link">Volver al inicio</Link>
  </div>
);

export default Terms;
