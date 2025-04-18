import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './Header.css';

function Header() {
  const [isOpen, setIsOpen] = useState(false);
  const [isScrolled, setIsScrolled] = useState(false);

  const toggleMenu = () => setIsOpen(!isOpen);
  const closeMenu = () => setIsOpen(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 50);
    };

    const handleResize = () => {
      if (window.innerWidth > 768) closeMenu();
    };

    window.addEventListener('scroll', handleScroll);
    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('scroll', handleScroll);
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  return (
    <header className={`app-header ${isScrolled ? 'scrolled' : ''}`}>
      <div className="header-container">
        <Link to="/" className="logo" onClick={closeMenu}>
          <span className="logo-highlight">Ultimo</span>Live
        </Link>

        <nav className={`desktop-nav ${isOpen ? 'mobile-active' : ''}`}>
          <ul>
            <li><Link to="/" onClick={closeMenu}>Inicio</Link></li>
            <li><Link to="/gana" onClick={closeMenu}>Trucos para Ganar </Link></li>
            <li><Link to="/salud" onClick={closeMenu}>Salud Natural </Link></li>
          </ul>
        </nav>

        <button 
          className={`hamburger ${isOpen ? 'open' : ''}`} 
          onClick={toggleMenu}
          aria-label="Menu"
        >
          <div className="hamburger-line"></div>
          <div className="hamburger-line"></div>
          <div className="hamburger-line"></div>
        </button>

        <div className={`mobile-overlay ${isOpen ? 'active' : ''}`} onClick={closeMenu}></div>
      </div>
    </header>
  );
}

export default Header;