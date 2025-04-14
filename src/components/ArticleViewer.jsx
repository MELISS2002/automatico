import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import './ArticleViewer.css';

const ArticleViewer = ({ article }) => {
  const [imageLoaded, setImageLoaded] = useState(false);

  if (!article) {
    return <div className="loading">Cargando artículo...</div>;
  }

  const { title, date, author, image, content } = article;

  return (
    <div className="article-container">
      <header className="article-header">
        <h1 className="article-title">{title}</h1>
        <div className="article-meta">
          <span className="article-author">{author}</span>
          <span className="article-date">{date}</span>
        </div>
      </header>

      {image && (
        <figure className="article-image-container">
          <img
            src={image}
            alt={title}
            className={`article-image ${imageLoaded ? 'loaded' : ''}`}
            loading="lazy"
            decoding="async"
            onLoad={() => setImageLoaded(true)}
          />
          <figcaption className="image-caption">{title}</figcaption>
        </figure>
      )}

      <article className="article-content">
        <ReactMarkdown
          components={{
            p: ({ node, ...props }) => <p className="article-paragraph" {...props} />,
            strong: ({ node, ...props }) => <strong className="article-bold" {...props} />
          }}
        >
          {content}
        </ReactMarkdown>
      </article>
    </div>
  );
};

export default ArticleViewer;