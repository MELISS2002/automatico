import React, { useState, useEffect } from 'react';
import { NavLink } from 'react-router-dom';
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

  const navItems = [
    { to: '/', label: 'Inicio', end: true },
    { to: '/gana', label: 'Gana' },
    { to: '/salud', label: 'Salud' },
    { to: '/canales', label: 'Canales' }
  ];

  return (
    <header className={`app-header ${isScrolled ? 'scrolled' : ''}`}>
      <div className="header-container">
        <NavLink to="/" className="logo" onClick={closeMenu}>
          <span className="logo-dot"></span>
          <span>Ultimo<span className="logo-bold">Live</span></span>
        </NavLink>

        <nav className={`desktop-nav`}>
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.end}
              onClick={closeMenu}
              className={({ isActive }) => (isActive ? 'active' : '')}
            >
              {item.label}
            </NavLink>
          ))}
        </nav>

        {/* Drawer móvil: panel completo con su propio header (logo + X) */}
        <nav className={`mobile-nav ${isOpen ? 'open' : ''}`}>
          <div className="mobile-nav-header">
            <NavLink to="/" className="logo" onClick={closeMenu}>
              <span className="logo-dot"></span>
              <span>Ultimo<span className="logo-bold">Live</span></span>
            </NavLink>
            <button className="drawer-close" onClick={closeMenu} aria-label="Cerrar menú">
              &#10005;
            </button>
          </div>
          <div className="mobile-nav-links">
            {navItems.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                end={item.end}
                onClick={closeMenu}
                className={({ isActive }) => (isActive ? 'active' : '')}
              >
                {item.label}
              </NavLink>
            ))}
          </div>
        </nav>

        <button
          className={`hamburger ${isOpen ? 'open' : ''}`}
          onClick={toggleMenu}
          aria-label="Menú"
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
