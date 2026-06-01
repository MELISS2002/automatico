import React, { useState, useEffect, useRef } from 'react';
import './Channels.css';

const Channels = () => {
  const [channels, setChannels] = useState([]);
  const [filteredChannels, setFilteredChannels] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [activeCategory, setActiveCategory] = useState('all');
  const [openDropdownId, setOpenDropdownId] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [streamUrl, setStreamUrl] = useState('');
  const [showPlayer, setShowPlayer] = useState(false);

  const wrapperRef = useRef(null);
  const iframeRef = useRef(null); // Referencia para el iframe

  // Función para extraer la URL directa del stream (elimina /p/espnrepro1.html?r=)
  const extractDirectUrl = (url) => {
    if (!url) return '';
    const match = url.match(/[?&]r=([^&]*)/);
    if (match && match[1]) {
      return decodeURIComponent(match[1]);
    }
    return url;
  };

  // Función para alternar pantalla completa
  const toggleFullscreen = () => {
    const iframe = iframeRef.current;
    if (!iframe) return;

    if (!document.fullscreenElement) {
      iframe.requestFullscreen().catch(err => {
        console.error(`Error al entrar en pantalla completa: ${err.message}`);
      });
    } else {
      document.exitFullscreen();
    }
  };

  useEffect(() => {
    const fetchChannels = async () => {
      try {
        const response = await fetch('https://belkaperu.github.io/belkafut/data1.json');
        if (!response.ok) throw new Error(`Error ${response.status}`);
        const data = await response.json();
        setChannels(data.canales);
        setFilteredChannels(data.canales);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchChannels();
  }, []);

  useEffect(() => {
    let result = channels;
    if (searchTerm) {
      result = result.filter(channel =>
        channel.title.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }
    if (activeCategory !== 'all') {
      result = result.filter(channel => channel.category === activeCategory);
    }
    setFilteredChannels(result);
  }, [searchTerm, activeCategory, channels]);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (wrapperRef.current && !wrapperRef.current.contains(event.target)) {
        setOpenDropdownId(null);
      }
    };
    document.addEventListener('click', handleClickOutside);
    return () => document.removeEventListener('click', handleClickOutside);
  }, []);

  const handleCardClick = (channelId) => {
    setOpenDropdownId(openDropdownId === channelId ? null : channelId);
  };

  if (loading) return <div className="channels-loading">Cargando canales...</div>;
  if (error) return <div className="channels-error">Error: {error}</div>;

  return (
    <div className="channels-container">
      <div className="channels-header">
        <h1>Canales Deportivos</h1>
      </div>

      <div className="search-container">
        <input
          type="text"
          id="search"
          placeholder="Buscar canales..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>

      <div className="category-filter">
        {['all', 'general', 'deportes'].map(cat => (
          <button
            key={cat}
            className={`category-btn ${activeCategory === cat ? 'active' : ''}`}
            onClick={() => setActiveCategory(cat)}
          >
            {cat === 'all' ? 'Todos' : cat.charAt(0).toUpperCase() + cat.slice(1)}
          </button>
        ))}
      </div>

      <div className="canales-grid" ref={wrapperRef}>
        {filteredChannels.length === 0 ? (
          <div className="no-results">No se encontraron canales.</div>
        ) : (
          filteredChannels.map((channel, idx) => (
            <div
              key={idx}
              className={`card-wrapper ${openDropdownId === idx ? 'show' : ''}`}
            >
              <div className="card" onClick={() => handleCardClick(idx)}>
                <img src={channel.image} alt={channel.title} className="card-img" />
                <div className="card-title">{channel.title}</div>
              </div>
              <div className="dropdown-content">
                {channel.options && channel.options.length > 0 ? (
                  channel.options.map((opt, optIdx) => (
                    <div
                      key={optIdx}
                      className="dropdown-option"
                      onClick={() => {
                        const directUrl = extractDirectUrl(opt.url);
                        if (directUrl) {
                          setStreamUrl(directUrl);
                          setShowPlayer(true);
                          setOpenDropdownId(null);
                        }
                      }}
                    >
                      {opt.label}
                    </div>
                  ))
                ) : (
                  <div className="dropdown-option disabled">No hay opciones disponibles</div>
                )}
              </div>
            </div>
          ))
        )}
      </div>

      {/* Modal del reproductor con stream directo y botón fullscreen */}
      {showPlayer && (
        <div className="player-modal" onClick={() => setShowPlayer(false)}>
          <div className="player-modal-content" onClick={(e) => e.stopPropagation()}>
            <button className="close-player" onClick={() => setShowPlayer(false)}>✕</button>
            <button className="fullscreen-btn" onClick={toggleFullscreen}>
              ⛶
            </button>
            <iframe
              ref={iframeRef}
              src={streamUrl}
              title="Stream directo"
              className="direct-stream-iframe"
              allowFullScreen
              frameBorder="0"
            />
          </div>
        </div>
      )}
    </div>
  );
};

export default Channels;