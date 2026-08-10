// src/components/Layout.jsx
import { useEffect } from 'react';
import { Outlet, useLocation } from 'react-router-dom';
import Header from './Header';
import Footer from './Footer'; // Importa el Footer

const Layout = () => {
  const { pathname } = useLocation();

  // Al cambiar de ruta, volver arriba para que el header sticky no tape el inicio
  useEffect(() => {
    window.scrollTo(0, 0);
  }, [pathname]);

  return (
    <div className="app-container">
      <Header />
      <Outlet />
      <Footer /> {/* Renderiza el Footer */}
    </div>
  );
};

export default Layout;