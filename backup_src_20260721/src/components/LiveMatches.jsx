import React from 'react';

const LiveMatches = ({ matches }) => (
  <div className="live-matches-container">
    {matches.map(match => (
      <div key={match.id} className="match-card">
        <div className="teams">
          <span className="home-team">{match.homeTeam}</span>
          <span className="score">{match.score}</span>
          <span className="away-team">{match.awayTeam}</span>
        </div>
        <div className="match-info">
          <span className="minute">⏱️ {match.minute}'</span>
          <span className="competition">{match.competition}</span>
        </div>
      </div>
    ))}
  </div>
);

export default LiveMatches;