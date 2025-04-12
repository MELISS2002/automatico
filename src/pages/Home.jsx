import React, { useState } from 'react';
import ArticleViewer from './components/ArticleViewer';

const Home = ({ posts }) => {
  const [selectedArticle, setSelectedArticle] = useState(null);

  const handleReadMore = (article) => {
    setSelectedArticle(article);
  };

  return (
    <div>
      {selectedArticle ? (
        <ArticleViewer article={selectedArticle} />
      ) : (
        <div>
          <h1>Últimas Noticias</h1>
          {posts.map((post) => (
            <article key={post.slug}>
              <h2>{post.title}</h2>
              <p>{post.date}</p>
              <button onClick={() => handleReadMore(post)}>Leer más →</button>
            </article>
          ))}
        </div>
      )}
    </div>
  );
};

export default Home;