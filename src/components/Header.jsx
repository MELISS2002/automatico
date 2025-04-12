import React from 'react';
import { Link } from 'react-router-dom';
import './Header.css';

function Header() {
  return (
    <header className="app-header">
      <div className="header-content">
      <h1><Link to="/" className="nav-link ">SportsLive</Link></h1>
        <nav className="main-navigation">
          <ul className="nav-menu">
            <li className="nav-item">
              <Link to="/" className="nav-link ">Live Matches</Link>
            </li>
            <li className="nav-item">
              <Link to="/news" className="nav-link">News</Link>
            </li>
            <li className="nav-item">
              <Link to="/schedule" className="nav-link">Schedule</Link>
            </li>
          </ul>
        </nav>
      </div>
    </header>
  );
}

export default Header;