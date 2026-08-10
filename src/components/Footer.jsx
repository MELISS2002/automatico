import { Link } from 'react-router-dom';
import './Footer.css';

const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer-content">
        <div className="footer-section">
          <div className="footer-logo">
            <span className="logo-text"><span className="logo-highlight">Ultimo</span>Live</span>
          </div>
          <p>Tu fuente confiable para deportes en vivo, consejos para ganar y bienestar natural.</p>
        </div>

        <div className="footer-section">
          <h4>Secciones</h4>
          <ul className="footer-links">
            <li><Link to="/">Inicio</Link></li>
            <li><Link to="/gana">Trucos para Ganar</Link></li>
            <li><Link to="/salud">Salud Natural</Link></li>
            <li><Link to="/canales">Canales</Link></li>
          </ul>
        </div>

        <div className="footer-section">
          <h4>Legal</h4>
          <ul className="footer-links">
            <li><Link to="/privacy-policy">Política de Privacidad</Link></li>
            <li><Link to="/terms">Términos de Servicio</Link></li>
            <li><Link to="/contact">Contacto</Link></li>
          </ul>
        </div>
      </div>

      <div className="footer-bottom">
        <p>© {new Date().getFullYear()} UltimoLive. Todos los derechos reservados.</p>
      </div>
    </footer>
  );
};

export default Footer;
