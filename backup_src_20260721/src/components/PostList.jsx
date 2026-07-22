import React, { useEffect, useState } from 'react';

const PostList = () => {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    // Leer lista de archivos Markdown
    fetch("/posts/manifest.json")
      .then(res => res.json())
      .then(data => setPosts(data));
  }, []);

  return (
    <div>
      {posts.map(post => (
        <article key={post.slug}>
          <h2>{post.title}</h2>
          <p>{post.date}</p>
          <a href={`/post/${post.slug}`}>Leer más</a>
        </article>
      ))}
    </div>
  );
};

export default PostList;