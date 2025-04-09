import React from 'react';

const Header = () => (
  <header className="site-header">
    <div className="header-content">
      <h1 className="logo">SportsLive</h1>
      <nav className="main-nav">
        <a href="/live">Live Matches</a>
        <a href="/news">News</a>
        <a href="/schedule">Schedule</a>
      </nav>
    </div>
  </header>
);

export default Header;