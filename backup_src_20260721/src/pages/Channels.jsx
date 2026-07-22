import React, { useState, useRef, useMemo } from 'react';
import './Channels.css';

// ===================== CANALES MANTENIDOS =====================
const channelsData = [
    { name: "TUDN", url: "https://embed.saohgdasregions.fun/embed2/tudn.html", category: "Deportes" },
    { name: "Gol Perú", url: "https://embed.saohgdasregions.fun/embed2/golperu.html", category: "Deportes" },
    { name: "TNT Sports", url: "https://embed.saohgdasregions.fun/embed2/tntsports.html", category: "Deportes" },
    { name: "ESPN Premium", url: "https://embed.saohgdasregions.fun/embed2/espnpremium.html", category: "Deportes" },
    { name: "ESPN Premium Argentina", url: "https://embed.saohgdasregions.fun/embed2/espnpremiumargentina.html", category: "Deportes" },
    { name: "TyC Sports", url: "https://embed.saohgdasregions.fun/embed2/tycsports.html", category: "Deportes" },
    { name: "Fox Sports", url: "https://embed.saohgdasregions.fun/embed2/foxsports.html", category: "Deportes" },
    { name: "Fox Sports 2", url: "https://embed.saohgdasregions.fun/embed2/foxsports2.html", category: "Deportes" },
    { name: "Fox Sports 3", url: "https://embed.saohgdasregions.fun/embed2/foxsports3.html", category: "Deportes" },
    { name: "Fox Deportes", url: "https://embed.saohgdasregions.fun/embed2/foxdeportes.html", category: "Deportes" },
    { name: "ESPN", url: "https://embed.saohgdasregions.fun/embed2/espn.html", category: "Deportes" },
    { name: "ESPN Ar", url: "https://embed.saohgdasregions.fun/embed2/espnar.html", category: "Deportes" },
    { name: "ESPN Col", url: "https://embed.saohgdasregions.fun/embed2/espncol.html", category: "Deportes" },
    { name: "ESPN 2", url: "https://embed.saohgdasregions.fun/embed2/espn2.html", category: "Deportes" },
    { name: "ESPN 3", url: "https://embed.saohgdasregions.fun/embed2/espn3.html", category: "Deportes" },
    { name: "ESPN 4", url: "https://embed.saohgdasregions.fun/embed2/espn4.html", category: "Deportes" },
    { name: "ESPN 5", url: "https://embed.saohgdasregions.fun/embed2/espn5.html", category: "Deportes" },
    { name: "ESPN 6", url: "https://embed.saohgdasregions.fun/embed2/espn6.html", category: "Deportes" },
    { name: "ESPN 7", url: "https://embed.saohgdasregions.fun/embed2/espn7.html", category: "Deportes" },
    { name: "DirecTV Sports", url: "https://embed.saohgdasregions.fun/embed2/directvsports.html", category: "Deportes" },
    { name: "DirecTV Sports 2", url: "https://embed.saohgdasregions.fun/embed2/directvsports2.html", category: "Deportes" },
    { name: "DirecTV Sports Plus", url: "https://embed.saohgdasregions.fun/embed2/directvsportsplus.html", category: "Deportes" },
    { name: "Fox Sports México", url: "https://embed.saohgdasregions.fun/embed2/foxsportsmexico.html", category: "Deportes" },
    { name: "Fox Sports 2 México", url: "https://embed.saohgdasregions.fun/embed2/foxsports2mexico.html", category: "Deportes" },
    { name: "Fox Sports 3 México", url: "https://embed.saohgdasregions.fun/embed2/foxsports3mexico.html", category: "Deportes" },
    { name: "ESPN México", url: "https://embed.saohgdasregions.fun/embed2/espnmexico.html", category: "Deportes" },
    { name: "ESPN 2 México", url: "https://embed.saohgdasregions.fun/embed2/espn2mexico.html", category: "Deportes" },
    { name: "ESPN 3 México", url: "https://embed.saohgdasregions.fun/embed2/espn3mexico.html", category: "Deportes" },
    { name: "ESPN 4 México", url: "https://embed.saohgdasregions.fun/embed2/espn4mexico.html", category: "Deportes" },
    { name: "ESPN 5 México", url: "https://embed.saohgdasregions.fun/embed2/espn5mexico.html", category: "Deportes" },
    { name: "Tvc Deportes", url: "https://embed.saohgdasregions.fun/embed2/tvcdeportes.html", category: "Deportes" },
    { name: "Liga 1", url: "https://embed.saohgdasregions.fun/embed2/liga1.html", category: "Deportes" },
    { name: "Liga 1 Max", url: "https://embed.saohgdasregions.fun/embed2/liga1max.html", category: "Deportes" },
    { name: "Fox Sports Premium", url: "https://embed.saohgdasregions.fun/embed2/foxsportspremium.html", category: "Deportes" },
    { name: "Movistar Deportes", url: "https://embed.saohgdasregions.fun/embed2/movistardeportes.html", category: "Deportes" },
    { name: "DAZN F1", url: "https://embed.saohgdasregions.fun/embed2/daznf1.html", category: "Deportes" },
    { name: "DAZN La Liga", url: "https://embed.saohgdasregions.fun/embed2/daznlaliga.html", category: "Deportes" },
    { name: "Movistar Liga de Campeones", url: "https://embed.saohgdasregions.fun/embed2/movistarligadecampeones.html", category: "Deportes" },
    { name: "Win Sports", url: "https://embed.saohgdasregions.fun/embed2/winsports.html", category: "Deportes" },
    { name: "Win Sports Plus", url: "https://embed.saohgdasregions.fun/embed2/winsportsplus.html", category: "Deportes" },
    { name: "BeIN Sports Xtra", url: "https://embed.saohgdasregions.fun/embed2/beinsportsxtra.html", category: "Deportes" },
    { name: "Movistar La Liga", url: "https://embed.saohgdasregions.fun/embed2/movistarlaliga.html", category: "Deportes" },
    { name: "NBA", url: "https://embed.saohgdasregions.fun/embed2/nba.html", category: "Deportes" },
    { name: "Movistar Deportes Es", url: "https://embed.saohgdasregions.fun/embed2/movistardeporteses.html", category: "Deportes" },
    { name: "Azteca Deportes", url: "https://embed.saohgdasregions.fun/embed2/aztecadeportes.html", category: "Deportes" },
    { name: "TNT Sports Chile", url: "https://embed.saohgdasregions.fun/embed2/tntsportschile.html", category: "Deportes" },
    { name: "MLB Network", url: "https://embed.saohgdasregions.fun/embed2/mlbnetwork.html", category: "Deportes" },
    { name: "Sky Sports México", url: "https://embed.saohgdasregions.fun/embed2/skysportsmexico.html", category: "Deportes" },
    { name: "Sky Sports Bundesliga", url: "https://embed.saohgdasregions.fun/embed2/skysportsbundesliga.html", category: "Deportes" },
    { name: "Sky Sports F1", url: "https://embed.saohgdasregions.fun/embed2/skysportsf1.html", category: "Deportes" },
    { name: "Azteca 7", url: "https://embed.saohgdasregions.fun/embed2/azteca7.html", category: "Entretenimiento" },
    { name: "Canal 5", url: "https://embed.saohgdasregions.fun/embed2/canal5.html", category: "Entretenimiento" },
    { name: "Latina", url: "https://embed.saohgdasregions.fun/embed2/latina.html", category: "Entretenimiento" },
    { name: "America TV", url: "https://embed.saohgdasregions.fun/embed2/americatv.html", category: "Entretenimiento" },
    { name: "Space", url: "https://embed.saohgdasregions.fun/embed2/space.html", category: "Entretenimiento" },
    { name: "Warner Channel", url: "https://embed.saohgdasregions.fun/embed2/warnerchannel.html", category: "Entretenimiento" },
    { name: "TNT", url: "https://embed.saohgdasregions.fun/embed2/tnt.html", category: "Entretenimiento" },
    { name: "Star Channel", url: "https://embed.saohgdasregions.fun/embed2/starchannel.html", category: "Entretenimiento" },
    { name: "Cinemax", url: "https://embed.saohgdasregions.fun/embed2/cinemax.html", category: "Películas" },
    { name: "Cinecanal", url: "https://embed.saohgdasregions.fun/embed2/cinecanal.html", category: "Películas" },
    { name: "Telefe", url: "https://embed.saohgdasregions.fun/embed2/telefe.html", category: "Entretenimiento" },
    { name: "El Trece", url: "https://embed.saohgdasregions.fun/embed2/eltrece.html", category: "Entretenimiento" },
    { name: "Distrito Comedia", url: "https://embed.saohgdasregions.fun/embed2/distritocomedia.html", category: "Entretenimiento" },
    { name: "Telemundo 51", url: "https://embed.saohgdasregions.fun/embed2/telemundo51.html", category: "Entretenimiento" },
    { name: "History", url: "https://embed.saohgdasregions.fun/embed2/history.html", category: "Entretenimiento" },
    { name: "History 2", url: "https://embed.saohgdasregions.fun/embed2/history2.html", category: "Entretenimiento" },
    { name: "Pasiones", url: "https://embed.saohgdasregions.fun/embed2/pasiones.html", category: "Entretenimiento" },
    { name: "Azteca Uno", url: "https://embed.saohgdasregions.fun/embed2/aztecauno.html", category: "Entretenimiento" },
    { name: "Galavision", url: "https://embed.saohgdasregions.fun/embed2/galavision.html", category: "Entretenimiento" },
    { name: "Tlnovelas", url: "https://embed.saohgdasregions.fun/embed2/tlnovelas.html", category: "Entretenimiento" },
    { name: "Las Estrellas", url: "https://embed.saohgdasregions.fun/embed2/lasestrellas.html", category: "Entretenimiento" },
    { name: "SyFy", url: "https://embed.saohgdasregions.fun/embed2/syfy.html", category: "Entretenimiento" },
    { name: "Caracol", url: "https://embed.saohgdasregions.fun/embed2/caracol.html", category: "Entretenimiento" },
    { name: "ATV", url: "https://embed.saohgdasregions.fun/embed2/atv.html", category: "Entretenimiento" },
    { name: "Univision", url: "https://embed.saohgdasregions.fun/embed2/univision.html", category: "Entretenimiento" },
    { name: "Unicable", url: "https://embed.saohgdasregions.fun/embed2/unicable.html", category: "Entretenimiento" },
    { name: "FX", url: "https://embed.saohgdasregions.fun/embed2/fx.html", category: "Entretenimiento" },
    { name: "Golden Plus", url: "https://embed.saohgdasregions.fun/embed2/goldenplus.html", category: "Películas" },
    { name: "Golden Edge", url: "https://embed.saohgdasregions.fun/embed2/goldenedge.html", category: "Películas" },
    { name: "Golden Premier", url: "https://embed.saohgdasregions.fun/embed2/goldenpremier.html", category: "Películas" },
    { name: "Golden Premier 2", url: "https://embed.saohgdasregions.fun/embed2/goldenpremier2.html", category: "Películas" },
    { name: "TNT Series", url: "https://embed.saohgdasregions.fun/embed2/tntseries.html", category: "Entretenimiento" },
    { name: "Sony", url: "https://embed.saohgdasregions.fun/embed2/sony.html", category: "Entretenimiento" },
    { name: "AXN", url: "https://embed.saohgdasregions.fun/embed2/axn.html", category: "Entretenimiento" },
    { name: "Universal Channel", url: "https://embed.saohgdasregions.fun/embed2/universalchannel.html", category: "Entretenimiento" },
    { name: "Studio Universal", url: "https://embed.saohgdasregions.fun/embed2/studiouniversal.html", category: "Películas" },
    { name: "Multipremier", url: "https://embed.saohgdasregions.fun/embed2/multipremier.html", category: "Películas" },
    { name: "AMC", url: "https://embed.saohgdasregions.fun/embed2/amc.html", category: "Películas" },
    { name: "Paramount Channel", url: "https://embed.saohgdasregions.fun/embed2/paramountchannel.html", category: "Películas" },
    { name: "DPelicula", url: "https://embed.saohgdasregions.fun/embed2/dpelicula.html", category: "Películas" },
    { name: "MTV", url: "https://embed.saohgdasregions.fun/embed2/mtv.html", category: "Entretenimiento" },
    { name: "Comedy Central", url: "https://embed.saohgdasregions.fun/embed2/comedycentral.html", category: "Entretenimiento" },
    { name: "Nat Geo", url: "https://embed.saohgdasregions.fun/embed2/natgeo.html", category: "Entretenimiento" },
    { name: "Animal Planet", url: "https://embed.saohgdasregions.fun/embed2/animalplanet.html", category: "Entretenimiento" },
    { name: "Discovery Channel", url: "https://embed.saohgdasregions.fun/embed2/discoverychannel.html", category: "Entretenimiento" },
    { name: "Discovery H&H", url: "https://embed.saohgdasregions.fun/embed2/discoveryhyh.html", category: "Entretenimiento" },
    { name: "ID Investigation", url: "https://embed.saohgdasregions.fun/embed2/idinvestigation.html", category: "Entretenimiento" },
    { name: "Discovery A&E", url: "https://embed.saohgdasregions.fun/embed2/discoveryaye.html", category: "Entretenimiento" },
    { name: "Discovery TLC", url: "https://embed.saohgdasregions.fun/embed2/discoverytlc.html", category: "Entretenimiento" },
    { name: "Discovery Theater", url: "https://embed.saohgdasregions.fun/embed2/discoverytheater.html", category: "Entretenimiento" },
    { name: "Discovery World", url: "https://embed.saohgdasregions.fun/embed2/discoveryworld.html", category: "Entretenimiento" },
    { name: "Everything", url: "https://embed.saohgdasregions.fun/embed2/everything.html", category: "Entretenimiento" },
    { name: "El Gourmet", url: "https://embed.saohgdasregions.fun/embed2/elgourmet.html", category: "Entretenimiento" },
    { name: "Disney Jr.", url: "https://embed.saohgdasregions.fun/embed2/disneyjr.html", category: "Infantiles" },
    { name: "Nick", url: "https://embed.saohgdasregions.fun/embed2/nick.html", category: "Infantiles" },
    { name: "Nick Jr.", url: "https://embed.saohgdasregions.fun/embed2/nickjr.html", category: "Infantiles" },
    { name: "Cartoon Network", url: "https://embed.saohgdasregions.fun/embed2/cartoonnetwork.html", category: "Infantiles" },
    { name: "Cartoonito", url: "https://embed.saohgdasregions.fun/embed2/cartoonito.html", category: "Infantiles" },
    { name: "Tooncast", url: "https://embed.saohgdasregions.fun/embed2/tooncast.html", category: "Infantiles" },
    { name: "Discovery Kids", url: "https://embed.saohgdasregions.fun/embed2/discoverykids.html", category: "Infantiles" },
    { name: "Telemundo Puerto Rico", url: "https://embed.saohgdasregions.fun/embed2/telemundopuertorico.html", category: "Entretenimiento" },
    { name: "Willax", url: "https://embed.saohgdasregions.fun/embed2/willax.html", category: "Noticias" },
    { name: "Global TV", url: "https://embed.saohgdasregions.fun/embed2/globaltv.html", category: "Entretenimiento" },
    { name: "RCN", url: "https://embed.saohgdasregions.fun/embed2/rcn.html", category: "Entretenimiento" },
    { name: "Antena 3", url: "https://embed.saohgdasregions.fun/embed2/antena3.html", category: "Internacionales" },
    { name: "TV Pública", url: "https://embed.saohgdasregions.fun/embed2/tvpublica.html", category: "Entretenimiento" },
    { name: "Disney Channel", url: "https://embed.saohgdasregions.fun/embed2/disneychannel.html", category: "Infantiles" },
    { name: "TNT Novelas", url: "https://embed.saohgdasregions.fun/embed2/tntnovelas.html", category: "Entretenimiento" },
    { name: "Universal Cinema", url: "https://embed.saohgdasregions.fun/embed2/universalcinema.html", category: "Películas" },
    { name: "FM Hot Kids", url: "https://embed.saohgdasregions.fun/embed2/fmhotkids.html", category: "Infantiles" }
];

const categories = [
    { id: 'all', label: 'Todos' },
    { id: 'Deportes', label: 'Deportes' },
    { id: 'Entretenimiento', label: 'Entretenimiento' },
    { id: 'Películas', label: 'Películas' },
    { id: 'Infantiles', label: 'Infantiles' },
    { id: 'Noticias', label: 'Noticias' },
    { id: 'Internacionales', label: 'Internacionales' }
];

export default function Channels() {
    // --- ESTADOS ---
    const [searchTerm, setSearchTerm] = useState('');
    const [activeCategory, setActiveCategory] = useState('all');
    const [selectedChannel, setSelectedChannel] = useState(null);

    // --- REFS ---
    const playerModalContentRef = useRef(null);

    // Generador de imágenes (placeholder)
    const getPlaceholderImg = (name) => {
        return `https://placehold.co/100x70/8baf1c/white?text=${encodeURIComponent(name.substring(0, 5))}`;
    };

    // --- FILTRADO DE CANALES ---
    const filteredChannels = useMemo(() => {
        return channelsData.filter(channel => {
            const matchesSearch = channel.name.toLowerCase().includes(searchTerm.toLowerCase());
            const matchesCategory = activeCategory === 'all' || channel.category === activeCategory;
            return matchesSearch && matchesCategory;
        });
    }, [searchTerm, activeCategory]);

    // --- EVENTOS DEL REPRODUCTOR ---
    const openPlayer = (channel) => {
        if (channel.url) {
            setSelectedChannel(channel);
        }
    };

    const closePlayer = () => {
        setSelectedChannel(null);
    };

    const toggleFullscreen = () => {
        if (!document.fullscreenElement) {
            if (playerModalContentRef.current) {
                playerModalContentRef.current.requestFullscreen().catch(err => {
                    console.error(`Error al solicitar pantalla completa: ${err.message}`);
                });
            }
        } else {
            document.exitFullscreen();
        }
    };

    return (
        <div className="channels-container">
            <div className="channels-header">
                <h1>Canales en Vivo</h1>
            </div>

            {/* BÚSQUEDA */}
            <div className="search-container">
                <input
                    type="text"
                    className="search-input"
                    placeholder="Buscar canales..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                />
            </div>

            {/* FILTROS */}
            <div className="category-filter">
                {categories.map((cat) => (
                    <button
                        key={cat.id}
                        className={`category-btn ${activeCategory === cat.id ? 'active' : ''}`}
                        onClick={() => setActiveCategory(cat.id)}
                    >
                        {cat.label}
                    </button>
                ))}
            </div>

            {/* GRID DE RESULTADOS */}
            <div className="canales-grid">
                {filteredChannels.length > 0 ? (
                    filteredChannels.map((channel, index) => (
                        <div 
                            key={index} 
                            className="card" 
                            onClick={() => openPlayer(channel)}
                        >
                            <div className="card-img-container">
                                <img src={getPlaceholderImg(channel.name)} alt={channel.name} />
                            </div>
                            <div className="card-title" title={channel.name}>
                                {channel.name}
                            </div>
                        </div>
                    ))
                ) : (
                    <div className="no-results">No se encontraron canales en esta categoría.</div>
                )}
            </div>

            {/* MODAL (Renderizado condicional) */}
            {selectedChannel && (
                <div className="player-modal" onClick={closePlayer}>
                    <div 
                        className="player-modal-content" 
                        ref={playerModalContentRef} 
                        onClick={(e) => e.stopPropagation()} /* Evita cerrar al clickear el reproductor */
                    >
                        <button className="close-player" onClick={closePlayer}>✕</button>
                        <button className="fullscreen-btn" onClick={toggleFullscreen}>⛶</button>
                        
                        <iframe
                            src={selectedChannel.url}
                            title={`Stream - ${selectedChannel.name}`}
                            className="direct-stream-iframe"
                            allow="autoplay; fullscreen; encrypted-media; picture-in-picture"
                            allowFullScreen
                            frameBorder="0"
                            scrolling="no"
                            referrerPolicy="no-referrer"
                            sandbox="allow-scripts allow-same-origin allow-forms"
                        ></iframe>
                    </div>
                </div>
            )}
        </div>
    );
}