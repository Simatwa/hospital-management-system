import { useState } from 'react';
import { Star } from 'lucide-react';
import { createFeedback, updateFeedback, deleteFeedback } from '../lib/feedback';
import toast from 'react-hot-toast';
import type { FeedbackFormData, UserFeedback } from '../types';
import { cn } from '../lib/utils';
import Modal from './ui/Modal';

interface FeedbackModalProps {
  type: 'appointment' | 'treatment';
  id: number;
  existingFeedback?: UserFeedback;
  onClose: () => void;
  onSuccess: () => void;
}

export default function FeedbackModal({ type, id, existingFeedback, onClose, onSuccess }: FeedbackModalProps) {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [formData, setFormData] = useState<FeedbackFormData>({
    message: existingFeedback?.message || '',
    rate: existingFeedback?.rate || 'Good',
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);

    try {
      if (existingFeedback) {
        await updateFeedback(type, id, existingFeedback.id, formData);
        toast.success('Feedback updated successfully');
      } else {
        await createFeedback(type, id, formData);
        toast.success('Feedback submitted successfully');
      }
      onSuccess();
      onClose();
    } catch (error) {
      console.error('Error submitting feedback:', error);
      toast.error('Failed to submit feedback');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDelete = async () => {
    if (!existingFeedback) return;
    
    if (!confirm('Are you sure you want to delete this feedback?')) return;

    setIsSubmitting(true);
    try {
      await deleteFeedback(type, id, existingFeedback.id);
      toast.success('Feedback deleted successfully');
      onSuccess();
      onClose();
    } catch (error) {
      console.error('Error deleting feedback:', error);
      toast.error('Failed to delete feedback');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Modal
      title={existingFeedback ? 'Edit Feedback' : 'Add Feedback'}
      onClose={onClose}
      className="max-w-md"
    >
      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Rating
          </label>
          <div className="grid grid-cols-5 gap-2">
            {['Terrible', 'Poor', 'Average', 'Good', 'Excellent'].map((rating) => (
              <button
                key={rating}
                type="button"
                onClick={() => setFormData(prev => ({ ...prev, rate: rating as FeedbackFormData['rate'] }))}
                className={cn(
                  "p-2 rounded-lg border text-sm font-medium transition-colors",
                  formData.rate === rating
                    ? "bg-primary text-white border-primary"
                    : "bg-white text-gray-700 border-gray-300 hover:bg-gray-50"
                )}
              >
                {rating}
              </button>
            ))}
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Message
          </label>
          <textarea
            value={formData.message}
            onChange={(e) => setFormData(prev => ({ ...prev, message: e.target.value }))}
            rows={4}
            className="w-full border-gray-300 rounded-lg shadow-sm focus:ring-primary focus:border-primary resize-none"
            placeholder="Share your experience..."
            required
          />
        </div>

        <div className="flex justify-end gap-3 pt-4">
          {existingFeedback && (
            <button
              type="button"
              onClick={handleDelete}
              disabled={isSubmitting}
              className="px-4 py-2 text-white bg-red-600 hover:bg-red-700 rounded-lg disabled:opacity-50 transition-colors"
            >
              Delete
            </button>
          )}
          <button
            type="submit"
            disabled={isSubmitting}
            className="px-4 py-2 text-white bg-primary hover:bg-primary-600 rounded-lg disabled:opacity-50 transition-colors"
          >
            {isSubmitting ? 'Submitting...' : existingFeedback ? 'Update' : 'Submit'}
          </button>
        </div>
      </form>
    </Modal>
  );
}