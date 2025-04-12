import { Link } from 'react-router-dom';

const PrivacyPolicy = () => {
  return (
    <div className="legal-page">
      <h1>Política de Privacidad</h1>
      <p>Última actualización: [Fecha]</p>
      
      <section>
        <h2>Información que recopilamos</h2>
        <p>No almacenamos información personal de los usuarios...</p>
      </section>

      <Link to="/" className="back-link">Volver al inicio</Link>
    </div>
  );
};

export default PrivacyPolicy;