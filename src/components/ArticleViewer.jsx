import React from 'react';
import ReactMarkdown from 'react-markdown';
import './ArticleViewer.css'; // Archivo CSS para estilos

const ArticleViewer = ({ article }) => {
  if (!article) {
    return <div className="loading">Cargando artículo...</div>;
  }

  const { title, date, author, image, content } = article;

  return (
    <div className="article-container">
      {/* Encabezado */}
      <div className="article-header">
        <h1 className="article-title">{title}</h1>
        <div className="article-meta">
          <span className="article-author">{author}</span>
          <span className="article-date">{date}</span>
        </div>
      </div>

      {/* Imagen destacada */}
      {image && (
        <div className="article-image-container">
          <img src={image} alt={title} className="article-image" />
        </div>
      )}

      {/* Contenido del artículo */}
      <div className="article-content">
        <ReactMarkdown>{content}</ReactMarkdown>
      </div>
    </div>
  );
};

export default ArticleViewer;