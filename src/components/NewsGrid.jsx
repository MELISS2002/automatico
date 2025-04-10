import React, { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';

const NewsGrid = () => {
  const [articles, setArticles] = useState([]);

  useEffect(() => {
    const loadArticles = async () => {
      try {
        const response = await fetch('/posts/manifest.json');
        const data = await response.json();
        setArticles(data);
      } catch (error) {
        console.error('Failed to load articles:', error);
      }
    };

    loadArticles();
  }, []);

  // Estilos en línea
  const gridStyles = {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
    gap: '20px',
    padding: '20px',
  };

  const cardStyles = {
    background: '#fff',
    border: '1px solid #ddd',
    borderRadius: '8px',
    padding: '20px',
    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
  };

  const imageStyles = {
    maxWidth: '100%',
    borderRadius: '8px',
    marginBottom: '15px',
  };

  const contentStyles = {
    padding: '10px 0',
  };

  const metaInfoStyles = {
    fontSize: '14px',
    color: '#777',
    marginBottom: '10px',
  };

  const readMoreStyles = {
    color: '#1a73e8',
    textDecoration: 'none',
  };

  const readMoreHoverStyles = {
    textDecoration: 'underline',
  };

  const handleImageError = (e) => {
    e.target.style.display = 'none';
  };

  const formatDate = (date) => {
    const formattedDate = new Date(date);
    return formattedDate.toLocaleDateString();
  };

  return (
    <div style={gridStyles}>
      {articles.length === 0 ? (
        <p>No hay artículos disponibles.</p>
      ) : (
        articles.map((article) => (
          <article key={article.id} style={cardStyles}>
            {article.image && (
              <img
                src={article.image}
                alt={article.title}
                style={imageStyles}
                onError={handleImageError}
              />
            )}
            <div style={contentStyles}>
              <div style={metaInfoStyles}>
                <span>{article.author}</span>
                <time>{formatDate(article.date)}</time>
              </div>
              <h3>{article.title}</h3>
              <ReactMarkdown>{article.content}</ReactMarkdown>
              <a
                href={article.link}
                target="_blank"
                rel="noopener noreferrer"
                style={readMoreStyles}
                onMouseEnter={(e) => (e.target.style.textDecoration = readMoreHoverStyles.textDecoration)}
                onMouseLeave={(e) => (e.target.style.textDecoration = 'none')}
              >
                Leer más →
              </a>
            </div>
          </article>
        ))
      )}
    </div>
  );
};

export default NewsGrid;
