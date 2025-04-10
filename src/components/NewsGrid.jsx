// components/NewsGrid.jsx
import React from 'react';
import ReactMarkdown from 'react-markdown';

const NewsGrid = ({ articles }) => (
  <div className="news-grid">
    {articles.map(article => (
      <article key={article.id} className="news-card">
        {article.image && (
          <img 
            src={article.image} 
            alt={article.title} 
            className="news-image"
            onError={(e) => e.target.style.display = 'none'}
          />
        )}
        <div className="news-content">
          <div className="meta-info">
            <span className="author">{article.author}</span>
            <time className="date">{article.date}</time>
          </div>
          <h3>{article.title}</h3>
          <ReactMarkdown className="news-excerpt">
            {article.content}
          </ReactMarkdown>
          <a 
            href={article.link} 
            target="_blank" 
            rel="noopener noreferrer"
            className="read-more"
          >
            Leer más →
          </a>
        </div>
      </article>
    ))}
  </div>
);

export default NewsGrid;