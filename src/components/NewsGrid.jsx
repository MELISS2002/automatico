import React from 'react';
import './NewsGrid.css';

const NewsGrid = ({ articles = [], onRead }) => {
  const formatDate = (dateString) => {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('es-ES', options);
  };

  return (
    <div className="news-grid">
      {articles.map((article) => (
        <article
          key={article.slug}
          className="news-card"
          onClick={() => onRead && onRead(article)}
        >
          <div className="card-image">
            <img
              src={article.thumbnail}
              alt={article.title}
              className="article-thumbnail"
              loading="lazy"
            />
          </div>
          <div className="card-content">
            <div className="meta-info">
              <span className="author">{article.author}</span>
              <time className="date">{formatDate(article.date)}</time>
            </div>
            <h3 className="card-title">{article.title}</h3>
            <p className="excerpt">{article.excerpt}</p>
            <span className="read-more">Leer artículo completo</span>
          </div>
        </article>
      ))}
    </div>
  );
};

export default NewsGrid;
