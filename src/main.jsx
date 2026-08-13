import React, { lazy, Suspense } from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { HelmetProvider } from 'react-helmet-async';
import Layout from './components/Layout';
import App from './App'; // Tu App original ahora es Home

// Lazy load páginas para mejorar rendimiento
const About = lazy(() => import('./pages/About'));
const Contact = lazy(() => import('./pages/Contact'));
const Terms = lazy(() => import('./pages/Terms'));
const Gana = lazy(() => import('./pages/gana'));
const Salud = lazy(() => import('./pages/salud'));
const PrivacyPolicy = lazy(() => import('./pages/PrivacyPolicy'));
const Channels = lazy(() => import('./pages/Channels'));

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <HelmetProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<App />} />
            <Route path="gana" element={
              <Suspense fallback={<div className="text-center p-10">Cargando...</div>}>
                <Gana />
              </Suspense>
            } />
            <Route path="salud" element={
              <Suspense fallback={<div className="text-center p-10">Cargando...</div>}>
                <Salud />
              </Suspense>
            } />
            <Route path="about" element={
              <Suspense fallback={<div className="text-center p-10">Cargando...</div>}>
                <About />
              </Suspense>
            } />
            <Route path="contact" element={
              <Suspense fallback={<div className="text-center p-10">Cargando...</div>}>
                <Contact />
              </Suspense>
            } />
            <Route path="terms" element={
              <Suspense fallback={<div className="text-center p-10">Cargando...</div>}>
                <Terms />
              </Suspense>
            } />
            <Route path="privacy-policy" element={
              <Suspense fallback={<div className="text-center p-10">Cargando...</div>}>
                <PrivacyPolicy />
              </Suspense>
            } />
            <Route path="canales" element={
              <Suspense fallback={<div className="text-center p-10">Cargando...</div>}>
                <Channels />
              </Suspense>
            } />
          </Route>
        </Routes>
      </Router>
    </HelmetProvider>
  </React.StrictMode>
);