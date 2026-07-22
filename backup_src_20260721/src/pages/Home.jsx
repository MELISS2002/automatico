import React, { useState } from 'react';
import ArticleViewer from './components/ArticleViewer';
import './Home.css';

const Home = ({ posts }) => {
  const [selectedArticle, setSelectedArticle] = useState(null);

  const handleReadMore = (article) => {
    setSelectedArticle(article);
  };

  return (
    <div className="home-container">
      {selectedArticle ? (
        <ArticleViewer article={selectedArticle} />
      ) : (
        <div className="articles-list">
          <h1 className="main-title">Últimas Noticias</h1>
          {posts.map((post) => (
            <article key={post.slug} className="article-preview">
              {post.featuredImage && (
                <img 
                  src={post.featuredImage} 
                  alt={post.title}
                  className="preview-image"
                  loading="lazy"
                />
              )}
              <div className="preview-content">
                <h2 className="preview-title">{post.title}</h2>
                <p className="preview-date">
                  {new Date(post.date).toLocaleDateString('es-ES', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric'
                  })}
                </p>
                <button 
                  onClick={() => handleReadMore(post)}
                  className="read-more-btn"
                >
                  Leer más
                  <span aria-hidden="true">→</span>
                </button>
              </div>
            </article>
          ))}
        </div>
      )}
    </div>
  );
};

export default Home;