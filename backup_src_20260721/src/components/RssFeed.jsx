import React, { useEffect, useState } from 'react';

const RssFeed = () => {
  const [feed, setFeed] = useState([]);
  
  useEffect(() => {
    // Usar un proxy RSS gratuito para evitar CORS
    fetch("https://api.rss2json.com/v1/api.json?rss_url=https://www.espn.com/espn/rss/soccer/news")
      .then(res => res.json())
      .then(data => setFeed(data.items));
  }, []);

  return (
    <div className="rss-feed">
      <h2>Últimas Noticias</h2>
      {feed.map((item, index) => (
        <article key={index}>
          <h3><a href={item.link}>{item.title}</a></h3>
          <div dangerouslySetInnerHTML={{ __html: item.description }} />
        </article>
      ))}
    </div>
  );
};

export default RssFeed;