import React, { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';

const NewsGrid = () => {
  const [articles, setArticles] = useState([]);
  const [selectedArticle, setSelectedArticle] = useState(null);

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

  const handleReadMore = (article) => {
    setSelectedArticle(article);
  };

  const handleCloseArticle = () => {
    setSelectedArticle(null);
  };

  const formatDate = (date) => {
    const formattedDate = new Date(date);
    return formattedDate.toLocaleDateString();
  };

  return (
    <div>
      {!selectedArticle && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '20px', padding: '20px' }}>
          {articles.length === 0 ? (
            <p>No hay artículos disponibles.</p>
          ) : (
            articles.map((article) => (
              <article key={article.id} style={{ background: '#fff', border: '1px solid #ddd', borderRadius: '8px', padding: '20px', boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)' }}>
                {article.image && <img src={article.image} alt={article.title} style={{ maxWidth: '100%', borderRadius: '8px', marginBottom: '15px' }} />}
                <div style={{ padding: '10px 0' }}>
                  <div style={{ fontSize: '14px', color: '#777', marginBottom: '10px' }}>
                    <span>{article.author}</span>
                    <time>{formatDate(article.date)}</time>
                  </div>
                  <h3>{article.title}</h3>
                  <ReactMarkdown>{String(article.content || "").slice(0, 100) + "..."}</ReactMarkdown>
                  <button
                    style={{ color: '#1a73e8', textDecoration: 'none', cursor: 'pointer' }}
                    onClick={() => handleReadMore(article)}
                  >
                    Leer más →
                  </button>
                </div>
              </article>
            ))
          )}
        </div>
      )}

      {selectedArticle && (
        <div style={{ padding: '20px' }}>
          <button
            style={{ marginBottom: '20px', color: '#1a73e8', cursor: 'pointer' }}
            onClick={handleCloseArticle}
          >
            ← Volver
          </button>
          <h1>{selectedArticle.title}</h1>
          <div style={{ fontSize: '14px', color: '#777', marginBottom: '10px' }}>
            <span>{selectedArticle.author}</span>
            <time>{formatDate(selectedArticle.date)}</time>
          </div>
          {selectedArticle.image && (
            <img
              src={selectedArticle.image}
              alt={selectedArticle.title}
              style={{ maxWidth: '100%', borderRadius: '8px', marginBottom: '15px' }}
            />
          )}
          <ReactMarkdown>{String(selectedArticle.content || "")}</ReactMarkdown>
        </div>
      )}
    </div>
  );
};

export default NewsGrid;