import { useState } from 'react';
import { format } from 'date-fns';
import { Calendar, Clock, DollarSign, MessageSquare, User, Building2 } from 'lucide-react';
import type { Appointment } from '../types';
import FeedbackModal from './FeedbackModal';
import { cn } from '../lib/utils';
import Modal from './ui/Modal';
import StarRating from './StarRating';

interface AppointmentDetailsModalProps {
  appointment: Appointment;
  onClose: () => void;
  onSuccess: () => void;
}

export default function AppointmentDetailsModal({ appointment, onClose, onSuccess }: AppointmentDetailsModalProps) {
  const [showFeedbackModal, setShowFeedbackModal] = useState(false);

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'completed':
        return 'text-green-600 bg-green-100';
      case 'scheduled':
        return 'text-blue-600 bg-blue-100';
      case 'cancelled':
        return 'text-red-600 bg-red-100';
      default:
        return 'text-gray-600 bg-gray-100';
    }
  };

  return (
    <>
      <Modal
        title="Appointment Details"
        onClose={onClose}
        className="max-w-2xl"
        titleExtra={
          <span className={cn(
            "px-2 py-1 text-xs font-semibold rounded-full mt-1",
            getStatusColor(appointment.status)
          )}>
            {appointment.status}
          </span>
        }
      >
        <div className="overflow-y-auto p-6 space-y-6">
          {/* Date and Time */}
          <div className="grid sm:grid-cols-2 gap-4">
            <div className="flex items-center gap-3 p-4 bg-gray-50 rounded-lg">
              <div className="p-2 bg-primary-100 text-primary rounded-lg">
                <Calendar className="h-5 w-5" />
              </div>
              <div>
                <p className="text-sm text-gray-500">Date</p>
                <p className="font-medium">
                  {format(new Date(appointment.appointment_datetime), 'MMMM d, yyyy')}
                </p>
              </div>
            </div>

            <div className="flex items-center gap-3 p-4 bg-gray-50 rounded-lg">
              <div className="p-2 bg-primary-100 text-primary rounded-lg">
                <Clock className="h-5 w-5" />
              </div>
              <div>
                <p className="text-sm text-gray-500">Time</p>
                <p className="font-medium">
                  {format(new Date(appointment.appointment_datetime), 'h:mm a')}
                </p>
              </div>
            </div>
          </div>

          {/* Reason */}
          <div className="p-4 bg-gray-50 rounded-lg">
            <h3 className="font-medium mb-2">Reason for Visit</h3>
            <p className="text-gray-600">{appointment.reason}</p>
          </div>

          {/* Doctor Information */}
          <div className="p-4 bg-gray-50 rounded-lg">
            <h3 className="font-medium mb-4">Doctor Information</h3>
            <div className="flex items-center gap-4">
              <div className="p-3 bg-primary-100 text-primary rounded-full">
                <User className="h-6 w-6" />
              </div>
              <div>
                <p className="font-medium">Dr. John Doe</p>
                <p className="text-sm text-gray-600">Cardiologist</p>
                <p className="text-sm text-gray-500 flex items-center gap-1">
                  <Building2 className="h-4 w-4" />
                  Cardiology Department
                </p>
              </div>
            </div>
          </div>

          {/* Charges */}
          <div className="p-4 bg-gray-50 rounded-lg">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <DollarSign className="h-5 w-5 text-primary" />
                <span className="font-medium">Appointment Charges</span>
              </div>
              <span className="text-lg font-semibold">
                Ksh {appointment.status === 'Cancelled' ? '0' : appointment.appointment_charges}
              </span>
            </div>
          </div>

          {/* Feedback Section */}
          {appointment.status === 'Completed' && (
            <div className="border-t pt-6">
              <div className="flex justify-between items-center mb-4">
                <h3 className="font-medium flex items-center gap-2">
                  <MessageSquare className="h-5 w-5 text-primary" />
                  Feedback
                </h3>
                <button
                  onClick={() => setShowFeedbackModal(true)}
                  className="text-primary hover:text-primary-600 text-sm font-medium"
                >
                  {appointment.feedbacks.length > 0 ? 'Edit Feedback' : 'Add Feedback'}
                </button>
              </div>

              {appointment.feedbacks.map((feedback, index) => (
                <div key={index} className="p-4 bg-gray-50 rounded-lg mb-4">
                  <div className="flex items-start gap-3">
                    <img
                      src={feedback.user.profile || "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&q=80"}
                      alt={feedback.user.username}
                      className="w-10 h-10 rounded-full object-cover"
                    />
                    <div className="flex-1">
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="font-medium">
                            {feedback.user.first_name} {feedback.user.last_name}
                          </p>
                          <p className="text-sm text-gray-500">
                            {format(new Date(feedback.created_at), 'MMM d, yyyy')}
                          </p>
                        </div>
                        <StarRating rating={feedback.rate} />
                      </div>
                      <p className="mt-2 text-gray-600">{feedback.message}</p>
                    </div>
                  </div>
                </div>
              ))}

              {appointment.feedbacks.length === 0 && (
                <p className="text-gray-500 text-center py-4">No feedback provided yet.</p>
              )}
            </div>
          )}
        </div>
      </Modal>

      {/* Feedback Modal */}
      {showFeedbackModal && (
        <FeedbackModal
          type="appointment"
          id={appointment.id}
          existingFeedback={appointment.feedbacks[0]}
          onClose={() => setShowFeedbackModal(false)}
          onSuccess={() => {
            setShowFeedbackModal(false);
            onSuccess();
          }}
        />
      )}
    </>
  );
}