import { useState, useEffect } from 'react';
import Header from './components/Header';
import LiveMatches from './components/LiveMatches';
import NewsGrid from './components/NewsGrid';
import './App.css';

function App() {
  const [liveMatches, setLiveMatches] = useState([
    {
      id: 1,
      homeTeam: 'Manchester United',
      awayTeam: 'Liverpool',
      score: '2-1',
      minute: '78',
      competition: 'Premier League'
    },
    {
      id: 2,
      homeTeam: 'Real Madrid',
      awayTeam: 'Barcelona',
      score: '1-0',
      minute: '45+3',
      competition: 'La Liga'
    }
  ]);

  const [news, setNews] = useState([]);

  useEffect(() => {
    const loadArticles = async () => {
      try {
        const response = await fetch('/posts/manifest.json');
        const articles = await response.json();
        setNews(articles);
      } catch (error) {
        console.error('Failed to load articles:', error);
      }
    };
    loadArticles();
  }, []);

  return (
    <div className="app">
      <Header />
      
      <main className="main-content">
        <section className="live-section">
          <h2 className="section-title">Live Matches ⚽</h2>
          <LiveMatches matches={liveMatches} />
        </section>

        <section className="news-section">
          <h2 className="section-title">Latest News 📰</h2>
          <NewsGrid articles={news} />
        </section>

        <section className="streaming-section">
          <h2 className="section-title">Live Streams 📺</h2>
          <div className="stream-container">
            <div className="stream-card">
              <h3>Real Madrid vs Barcelona</h3>
              <div className="stream-embed">
                {/* Aquí iría el embed de streaming */}
                <div className="placeholder-stream">
                  LIVE STREAM EMBED
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>

      <footer className="site-footer">
        <p>© 2024 SportsLive - All rights reserved</p>
        <nav className="footer-nav">
          <a href="/about">About</a>
          <a href="/contact">Contact</a>
          <a href="/terms">Terms of Service</a>
        </nav>
      </footer>
    </div>
  );
}

export default App;
