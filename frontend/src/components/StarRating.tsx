import { Star, StarHalf } from 'lucide-react';

interface StarRatingProps {
  rating: 'Excellent' | 'Good' | 'Average' | 'Poor' | 'Terrible';
}

export default function StarRating({ rating }: StarRatingProps) {
  const getRatingValue = (rating: string): number => {
    switch (rating) {
      case 'Excellent':
        return 5;
      case 'Good':
        return 4;
      case 'Average':
        return 3;
      case 'Poor':
        return 2;
      case 'Terrible':
        return 1;
      default:
        return 0;
    }
  };

  const ratingValue = getRatingValue(rating);
  const stars = [];

  for (let i = 1; i <= 5; i++) {
    if (i <= ratingValue) {
      stars.push(
        <Star key={i} className="w-5 h-5 fill-yellow-400 text-yellow-400" />
      );
    } else {
      stars.push(
        <Star key={i} className="w-5 h-5 text-gray-300" />
      );
    }
  }

  return (
    <div className="flex gap-1" title={`${rating} - ${ratingValue} stars`}>
      {stars}
    </div>
  );
}