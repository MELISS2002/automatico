import { useState, useEffect } from 'react';
import DOMPurify from 'dompurify';

const cleanArticleHTML = (raw) => {
  try {
    return DOMPurify.sanitize(raw, {
      ALLOWED_TAGS: ['p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li', 'a', 'img', 'blockquote', 'pre', 'code', 'hr', 'table', 'thead', 'tbody', 'tr', 'th', 'td', 'div', 'span', 'section', 'article', 'header', 'footer', 'nav', 'main', 'aside', 'figure', 'figcaption', 'mark', 'small', 'sub', 'sup', 'time'],
      ALLOWED_ATTR: ['href', 'src', 'alt', 'title', 'class', 'id', 'style', 'target', 'rel', 'width', 'height', 'loading', 'role', 'aria-label']
    });
  } catch (e) {
    return raw;
  }
};

const estimateReadTime = (html) => {
  const text = html.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();
  const words = text ? text.split(' ').length : 0;
  return Math.max(1, Math.round(words / 200));
};

export const useArticle = (selectedArticle) => {
  const [articleContent, setArticleContent] = useState('');
  const [readTime, setReadTime] = useState(0);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!selectedArticle) {
      setArticleContent('');
      setReadTime(0);
      return;
    }

    const fetchArticle = async () => {
      setLoading(true);
      try {
        const response = await fetch(/posts/.html);
        if (!response.ok) throw new Error('Failed to fetch article');
        const rawHtml = await response.text();
        const cleaned = cleanArticleHTML(rawHtml);
        setArticleContent(cleaned);
        setReadTime(estimateReadTime(cleaned));
      } catch (err) {
        console.error('Error loading article:', err);
        setArticleContent('<p>Error al cargar el artículo.</p>');
        setReadTime(0);
      } finally {
        setLoading(false);
      }
    };

    fetchArticle();
  }, [selectedArticle]);

  return { articleContent, readTime, loading };
};
