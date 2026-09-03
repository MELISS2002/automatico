// src/components/AdSlot.jsx
import React, { useEffect, useRef } from 'react';
import './AdSlot.css';

const AD_CLIENT = 'ca-pub-5634091835281348';

const AdSlot = ({ slot, format = 'auto', className, fullWidth = true }) => {
  const insRef = useRef(null);
  const pushedRef = useRef(false);

  useEffect(() => {
    // Evita doble push en StrictMode (el efecto corre 2 veces en dev)
    if (pushedRef.current) return;
    pushedRef.current = true;

    const t = setTimeout(() => {
      try {
        (window.adsbygoogle = window.adsbygoogle || []).push({});
      } catch {
        // adsbygoogle aún no cargado; no bloquear el render
      }
    }, 0);

    return () => clearTimeout(t);
  }, []);

  return (
    <div className={`ad-slot ${className || ''}`} data-format={format}>
      <ins
        ref={insRef}
        className="adsbygoogle"
        style={{ display: 'block', width: fullWidth ? '100%' : undefined }}
        data-ad-client={AD_CLIENT}
        data-ad-slot={slot}
        data-ad-format={format}
        data-full-width-responsive={fullWidth ? 'true' : 'false'}
      />
    </div>
  );
};

export default AdSlot;