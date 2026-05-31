import React, { useState, useEffect, useRef } from 'react';

const Channels = () => {
  const [channels, setChannels] = useState([]);
  const [filteredChannels, setFilteredChannels] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [activeCategory, setActiveCategory] = useState('all');
  const [openDropdownId, setOpenDropdownId] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Referencia para cerrar dropdowns al hacer clic fuera
  const wrapperRef = useRef(null);

  // Cargar datos del JSON externo
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

  // Filtrar por búsqueda y categoría
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

  // Cerrar dropdown si se hace clic fuera
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
                    <a
                      key={optIdx}
                      href={opt.url}
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      {opt.label}
                    </a>
                  ))
                ) : (
                  <a href="#" style={{ cursor: 'default', color: '#999' }}>
                    No hay opciones disponibles
                  </a>
                )}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default Channels;