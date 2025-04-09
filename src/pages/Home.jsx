import React from 'react';
import { Link } from 'react-router-dom';

const Home = ({ posts }) => {
  return (
    <div>
      <h1>Últimas Noticias</h1>
      {posts.map(post => (
        <article key={post.slug}>
          <h2><Link to={`/post/${post.slug}`}>{post.title}</Link></h2>
          <p>{post.date}</p>
        </article>
      ))}
    </div>
  );
};