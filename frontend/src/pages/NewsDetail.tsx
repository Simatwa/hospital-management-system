import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { setPageTitle } from '../lib/utils';
import { ArrowLeft, Calendar, User, Tag } from 'lucide-react';
import { format } from 'date-fns';
import toast from 'react-hot-toast';

interface NewsDetail {
  id: number;
  title: string;
  content: string;
  cover_photo: string;
  category: string;
  author: {
    first_name: string;
    last_name: string;
    profile: string;
  };
  created_at: string;
  updated_at: string;
  tags: string[];
  related_news: Array<{
    id: number;
    title: string;
    cover_photo: string;
    category: string;
  }>;
}

export default function NewsDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [news, setNews] = useState<NewsDetail | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchNewsDetail = async () => {
      try {
        const response = await fetch(`/api/v1/news/${id}`);
        if (!response.ok) throw new Error('News not found');
        const data = await response.json();
        setNews(data);
        setPageTitle(data.title);
      } catch (error) {
        console.error('Error fetching news:', error);
        toast.error('Failed to load news details');
        navigate('/');
      } finally {
        setLoading(false);
      }
    };

    fetchNewsDetail();
  }, [id, navigate]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
      </div>
    );
  }

  if (!news) return null;

  return (
    <div className="min-h-screen bg-gray-50 pt-20">
      <article className="max-w-4xl mx-auto px-4 py-8">
        <button
          onClick={() => navigate(-1)}
          className="flex items-center text-primary hover:text-primary-600 mb-6 transition-colors"
        >
          <ArrowLeft className="mr-2" />
          Back to News
        </button>

        <img
          src={news.cover_photo}
          alt={news.title}
          className="w-full h-[400px] object-cover rounded-xl shadow-lg mb-8"
        />

        <div className="bg-white rounded-lg shadow-md p-8">
          <div className="flex items-center gap-4 mb-6">
            <img
              src={news.author.profile}
              alt={`${news.author.first_name} ${news.author.last_name}`}
              className="w-12 h-12 rounded-full object-cover"
            />
            <div>
              <h3 className="font-semibold">{news.author.first_name} {news.author.last_name}</h3>
              <div className="flex items-center gap-4 text-sm text-gray-600">
                <span className="flex items-center">
                  <Calendar size={16} className="mr-1" />
                  {format(new Date(news.created_at), 'MMM d, yyyy')}
                </span>
                <span className="flex items-center">
                  <Tag size={16} className="mr-1" />
                  {news.category}
                </span>
              </div>
            </div>
          </div>

          <h1 className="text-3xl font-bold mb-6">{news.title}</h1>
          <div className="prose max-w-none mb-8" dangerouslySetInnerHTML={{ __html: news.content }} />

          {news.tags.length > 0 && (
            <div className="flex flex-wrap gap-2 mb-8">
              {news.tags.map((tag, index) => (
                <span
                  key={index}
                  className="bg-gray-100 text-gray-700 px-3 py-1 rounded-full text-sm"
                >
                  {tag}
                </span>
              ))}
            </div>
          )}
        </div>

        {news.related_news.length > 0 && (
          <div className="mt-12">
            <h2 className="text-2xl font-bold mb-6">Related News</h2>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {news.related_news.map((relatedNews) => (
                <div
                  key={relatedNews.id}
                  className="bg-white rounded-lg shadow-md overflow-hidden cursor-pointer transform hover:scale-105 transition-transform duration-300"
                  onClick={() => navigate(`/news/${relatedNews.id}`)}
                >
                  <img
                    src={relatedNews.cover_photo}
                    alt={relatedNews.title}
                    className="w-full h-48 object-cover"
                  />
                  <div className="p-4">
                    <span className="text-sm text-primary mb-2 block">{relatedNews.category}</span>
                    <h3 className="font-semibold line-clamp-2">{relatedNews.title}</h3>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </article>
    </div>
  );
}