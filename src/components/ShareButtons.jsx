import React, { useState } from 'react';
import './ShareButtons.css';

const SITE = 'https://automatico.pages.dev';

const ShareButtons = ({ slug, title }) => {
  const [copied, setCopied] = useState(false);
  const url = `${SITE}/posts/${slug}/`;
  const enc = encodeURIComponent;
  const t = enc(title);
  const u = enc(url);
  const links = [
    { name: 'WhatsApp', cls: 'share-wa', href: `https://wa.me/?text=${t}%20${u}` },
    { name: 'Facebook', cls: 'share-fb', href: `https://www.facebook.com/sharer/sharer.php?u=${u}` },
    { name: 'X', cls: 'share-tw', href: `https://twitter.com/intent/tweet?text=${t}&url=${u}` },
    { name: 'Telegram', cls: 'share-tg', href: `https://t.me/share/url?url=${u}&text=${t}` },
  ];

  const copyLink = async () => {
    try {
      await navigator.clipboard.writeText(url);
    } catch (e) {
      const ta = document.createElement('textarea');
      ta.value = url;
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.select();
      document.execCommand('copy');
      ta.remove();
    }
    setCopied(true);
    setTimeout(() => setCopied(false), 2500);
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
