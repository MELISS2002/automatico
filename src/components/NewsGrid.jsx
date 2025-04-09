import React from 'react';

const NewsGrid = ({ articles }) => (
  <div className="news-grid">
    {articles.map(article => (
      <article key={article.id} className="news-card">
        <img src={article.image} alt={article.title} className="news-image" />
        <div className="news-content">
          <span className="news-category">{article.category}</span>
          <h3 className="news-title">{article.title}</h3>
          <p className="news-excerpt">{article.excerpt}</p>
          <time className="news-date">{article.date}</time>
        </div>
      </article>
    ))}
  </div>
);

export default NewsGrid;