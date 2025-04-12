// src/components/Footer.jsx
import { Link } from 'react-router-dom';
import './Footer.css'; // Añade esta línea
const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer-content">
        <p>© {new Date().getFullYear()} SportsLive</p>
        <nav className="legal-links">
          <Link to="/privacy-policy">Política de Privacidad</Link>
          <Link to="/terms">Términos de Servicio</Link>
          <Link to="/contact">Contacto</Link>
        </nav>
      </div>
    </footer>
  );
};

export default Footer;