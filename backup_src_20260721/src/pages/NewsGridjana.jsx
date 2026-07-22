import React, { useState, useEffect } from 'react';
import './NewsGridjana.css';

const NewsGrid = () => {
  const [articles, setArticles] = useState([]);
  const [selectedArticle, setSelectedArticle] = useState(null);
  const [articleContent, setArticleContent] = useState('');

  useEffect(() => {
    const loadArticles = async () => {
      try {
        // Asegurar que la ruta del manifiesto es correcta
        const response = await fetch('/posts/gana.json');
        if (!response.ok) throw new Error('HTTP error ' + response.status);
        const data = await response.json();
        setArticles(data);
      } catch (error) {
        console.error('Error cargando artículos:', error);
      }
    };
    
    loadArticles();
  }, []);

  const loadHTMLContent = async (path) => {
    try {
      const response = await fetch(path);
      if (!response.ok) throw new Error('HTTP error ' + response.status);
      return await response.text();
    } catch (error) {
      console.error('Error cargando contenido:', error);
      return '<p>Error al cargar el artículo</p>';
    }
  };

  const handleReadArticle = async (article) => {
    const content = await loadHTMLContent(article.htmlPath);
    setArticleContent(content);
    setSelectedArticle(article);
  };

  const handleCloseArticle = () => {
    setSelectedArticle(null);
    setArticleContent('');
  };

  const formatDate = (dateString) => {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('es-ES', options);
  };

  return (
    <div className="news-container">
      {!selectedArticle ? (
        <div className="news-grid">
          {articles.map((article) => (
            <article key={article.slug} className="news-card">
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
                <h2 className="card-title">{article.title}</h2>
                <p className="excerpt">{article.excerpt}</p>
                <button
                  className="read-more"
                  onClick={() => handleReadArticle(article)}
                >
                  Leer artículo completo
                </button>
              </div>
            </article>
          ))}
        </div>
      ) : (
        <div className="article-viewer">
          <button className="back-button" onClick={handleCloseArticle}>
            &larr; Volver al listado
          </button>
          <div className="article-header">
            <h1>{selectedArticle.title}</h1>
            <div className="article-meta">
              <span className="author">Por {selectedArticle.author}</span>
              <time className="date">{formatDate(selectedArticle.date)}</time>
            </div>
          </div>
          <div 
            className="html-content"
            dangerouslySetInnerHTML={{ __html: articleContent }}
          />
        </div>
      )}
    </div>
  );
};

export default NewsGrid;