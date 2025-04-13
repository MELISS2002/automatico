import { Link } from 'react-router-dom';
import './Footer.css';

const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer-content">
        <p>© {new Date().getFullYear()} SportsLive. Todos los derechos reservados.</p>
        <nav>
          <ul className="legal-links">
            <li>
              <Link to="/privacy-policy">Política de Privacidad</Link>
            </li>
            <li>
              <Link to="/terms">Términos de Servicio</Link>
            </li>
            <li>
              <Link to="/contact">Contacto</Link>
            </li>
          </ul>
        </nav>
      </div>
    </footer>
  );
};

export default Footer;