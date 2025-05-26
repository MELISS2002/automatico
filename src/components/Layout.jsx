// src/components/Layout.jsx
import { Outlet } from 'react-router-dom';
import Header from './Header';
import Footer from './Footer'; // Importa el Footer

const Layout = () => {
  return (
    <div className="app-container">
      <Header />
      <Outlet />
      <Footer /> {/* Renderiza el Footer */}
    </div>
  );
};

export default Layout;