import React from 'react';
import ReactMarkdown from 'react-markdown';
import { useParams } from 'react-router-dom';

const Post = () => {
  const { slug } = useParams();
  const [content, setContent] = React.useState('');

  React.useEffect(() => {
    fetch(`/posts/${slug}.md`)
      .then(res => res.text())
      .then(text => setContent(text));
  }, [slug]);

  return (
    <div className="post-container">
      <ReactMarkdown>{content}</ReactMarkdown>
    </div>
  );
};

export default Post;