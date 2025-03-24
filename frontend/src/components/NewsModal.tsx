import React, { useEffect } from 'react';
import { X, Calendar, Tag, FileText, Youtube } from 'lucide-react';
import { format, parseISO, isValid } from 'date-fns';
import type { NewsDetail } from '../types';

interface NewsModalProps {
  news: NewsDetail;
  onClose: () => void;
}

// Helper function to safely format dates
const formatDate = (dateString: string) => {
  const date = parseISO(dateString);
  return isValid(date) ? format(date, 'MMMM d, yyyy') : 'Date not available';
};

export default function NewsModal({ news, onClose }: NewsModalProps) {
  // Close modal when clicking outside
  const handleBackdropClick = (e: React.MouseEvent<HTMLDivElement>) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  // Close on escape key
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };

    window.addEventListener('keydown', handleEscape);
    return () => window.removeEventListener('keydown', handleEscape);
  }, [onClose]);

  return (
    <div 
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm"
      onClick={handleBackdropClick}
    >
      <div className="bg-white rounded-lg shadow-xl w-full max-w-4xl max-h-[90vh] overflow-y-auto">
        <div className="sticky top-0 z-10 bg-white p-4 border-b flex justify-between items-center">
          <div>
            <span className="text-sm text-primary font-medium">{news.category}</span>
            <h2 className="text-2xl font-bold">{news.title}</h2>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 rounded-full transition-colors"
            aria-label="Close modal"
          >
            <X className="h-6 w-6" />
          </button>
        </div>
        
        <div className="p-6">
          {news.cover_photo && (
            <img
              src={news.cover_photo}
              alt={news.title}
              className="w-full h-[300px] object-cover rounded-lg mb-6"
            />
          )}
          
          <div className="flex items-center gap-4 mb-6">
            <div className="flex items-center gap-2 text-sm text-gray-600">
              <Calendar size={14} />
              <span>{formatDate(news.created_at)}</span>
            </div>
            <div className="text-sm text-gray-600">
              {news.views} views
            </div>
          </div>

          <div 
            className="prose max-w-none mb-6"
            dangerouslySetInnerHTML={{ __html: news.content }}
          />
          
          <div className="flex flex-wrap gap-4 mt-6">
            {news.document && (
              <a
                href={news.document}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg text-gray-700 transition-colors"
              >
                <FileText size={18} />
                <span>View Document</span>
              </a>
            )}
            
            {news.video_link && (
              <a
                href={news.video_link}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg text-gray-700 transition-colors"
              >
                <Youtube size={18} />
                <span>Watch Video</span>
              </a>
            )}
          </div>

          {news.tags && news.tags.length > 0 && (
            <div className="mt-6 flex flex-wrap gap-2 items-center">
              <Tag size={16} className="text-gray-600" />
              {news.tags.map((tag, index) => (
                <span
                  key={index}
                  className="px-3 py-1 bg-gray-100 rounded-full text-sm text-gray-700 hover:bg-gray-200 transition-colors"
                >
                  {tag}
                </span>
              ))}
            </div>
          )}

          {news.related_news && news.related_news.length > 0 && (
            <div className="mt-8 pt-6 border-t">
              <h3 className="text-xl font-semibold mb-4">Related News</h3>
              <div className="grid md:grid-cols-2 gap-4">
                {news.related_news.map((related) => (
                  <div
                    key={related.id}
                    className="flex gap-4 p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors cursor-pointer"
                    onClick={(e) => {
                      e.stopPropagation();
                      window.location.href = `/news/${related.id}`;
                    }}
                  >
                    {related.cover_photo && (
                      <img
                        src={related.cover_photo}
                        alt={related.title}
                        className="w-24 h-24 object-cover rounded"
                      />
                    )}
                    <div>
                      <span className="text-sm text-primary">{related.category}</span>
                      <h4 className="font-semibold line-clamp-2">{related.title}</h4>
                      <p className="text-sm text-gray-600 line-clamp-2">{related.summary}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}