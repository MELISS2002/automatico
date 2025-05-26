import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import App from './App'; // Tu App original ahora es Home
import About from './pages/About';
import Contact from './pages/Contact';
import Terms from './pages/Terms';
import Gana from './pages/gana';
import Salud from './pages/salud';
import PrivacyPolicy from './pages/PrivacyPolicy';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <Router>
      <Routes>
        {/* Todas las rutas usan el Layout */}
        <Route path="/" element={<Layout />}>
          <Route index element={<App />} />
          <Route path="gana" element={<Gana />} />
          <Route path="salud" element={<Salud />} />
          <Route path="about" element={<About />} />
          <Route path="contact" element={<Contact />} />
          <Route path="terms" element={<Terms />} />
          <Route path="privacy-policy" element={<PrivacyPolicy />} />
        </Route>
      </Routes>
    </Router>
  </React.StrictMode>
);