import React, { useState } from 'react';
import './ShareButtons.css';

const SITE = 'https://automatico.pages.dev';
// TODO: reemplazar con el App ID de la app de Facebook de UltimoLive
// (developers.facebook.com -> Crear aplicacion -> tipo Consumidor -> ID de aplicacion)
// Con un app_id ajeno el dialogo abre sin destinos ("no hay feed") y no deja publicar.
const FB_APP_ID = '2290800501460325';

const ShareButtons = ({ slug, title }) => {
  const [copied, setCopied] = useState(false);
  const url = `${SITE}/posts/${slug}/`;
  const enc = encodeURIComponent;
  const t = enc(title);
  const u = enc(url);
  const links = [
    { name: 'WhatsApp', cls: 'share-wa', href: `https://wa.me/?text=${t}%20${u}` },
    { name: 'Facebook', cls: 'share-fb', href: `https://www.facebook.com/dialog/share?app_id=${FB_APP_ID}&display=popup&href=${u}&redirect_uri=${enc('https://www.facebook.com/')}` },
    { name: 'X', cls: 'share-tw', href: `https://twitter.com/intent/tweet?text=${t}&url=${u}` },
    { name: 'Telegram', cls: 'share-tg', href: `https://t.me/share/url?url=${u}&text=${t}` },
  ];

  const copyLink = () => {
    const done = () => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2500);
    };
    const fallback = () => {
      try {
        const ta = document.createElement('textarea');
        ta.value = url;
        ta.style.position = 'fixed';
        ta.style.opacity = '0';
        document.body.appendChild(ta);
        ta.select();
        document.execCommand('copy');
        ta.remove();
      } catch (e) {
        // sin clipboard disponible
      }
      done();
    };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      const t = setTimeout(fallback, 800);
      navigator.clipboard.writeText(url).then(() => {
        clearTimeout(t);
        done();
      }).catch(() => {
        clearTimeout(t);
        fallback();
      });
    } else {
      fallback();
    }
  };

  return (
    <div className="share-buttons">
      <span className="share-label">Compartir</span>
      <div className="share-row">
        {links.map((l) => (
          <a
            key={l.name}
            className={`share-btn ${l.cls}`}
            href={l.href}
            target="_blank"
            rel="noopener noreferrer"
            title={`Compartir en ${l.name}`}
          >
            {l.name}
          </a>
        ))}
        <button
          type="button"
          className={`share-btn share-copy ${copied ? 'copied' : ''}`}
          onClick={copyLink}
        >
          {copied ? 'Enlace copiado' : 'Copiar enlace'}
        </button>
      </div>
    </div>
  );
};

export default ShareButtons;
