import { useState } from 'react';
import { Calendar, User, Pill, DollarSign, MessageSquare, Building2, Clock } from 'lucide-react';
import { format } from 'date-fns';
import type { Treatment } from '../types';
import { cn } from '../lib/utils';
import { formatMoney } from '../lib/utils';
import FeedbackModal from './FeedbackModal';
import Modal from './ui/Modal';

interface TreatmentDetailsModalProps {
  treatment: Treatment;
  onClose: () => void;
  onSuccess: () => void;
}

export default function TreatmentDetailsModal({ treatment, onClose, onSuccess }: TreatmentDetailsModalProps) {
  const [showFeedbackModal, setShowFeedbackModal] = useState(false);

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'completed':
        return 'text-green-600 bg-green-100';
      case 'inprogress':
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
        title="Treatment Details"
        onClose={onClose}
        className="max-w-4xl"
        titleExtra={
          <span className={cn(
            "px-2 py-1 text-xs font-semibold rounded-full mt-1",
            getStatusColor(treatment.treatment_status)
          )}>
            {treatment.treatment_status}
          </span>
        }
      >
        <div className="space-y-6">
          {/* Basic Info */}
          <div className="grid sm:grid-cols-2 gap-4">
            <div className="flex items-center gap-3 p-4 bg-gray-50 rounded-lg">
              <div className="p-2 bg-primary-100 text-primary rounded-lg">
                <Calendar className="h-5 w-5" />
              </div>
              <div>
                <p className="text-sm text-gray-500">Date</p>
                <p className="font-medium">
                  {format(new Date(treatment.created_at), 'MMMM d, yyyy')}
                </p>
              </div>
            </div>

            <div className="flex items-center gap-3 p-4 bg-gray-50 rounded-lg">
              <div className="p-2 bg-primary-100 text-primary rounded-lg">
                <Clock className="h-5 w-5" />
              </div>
              <div>
                <p className="text-sm text-gray-500">Patient Type</p>
                <p className="font-medium">{treatment.patient_type}</p>
              </div>
            </div>
          </div>

          {/* Diagnosis */}
          <div className="p-4 bg-gray-50 rounded-lg">
            <h3 className="font-medium mb-2">Diagnosis</h3>
            <p className="text-gray-600">{treatment.diagnosis}</p>
            <p className="text-gray-500 mt-2">{treatment.details}</p>
          </div>

          {/* Doctors */}
          {treatment.doctors_involved && treatment.doctors_involved.length > 0 && (
            <div>
              <h3 className="text-lg font-medium mb-4">Doctors Involved</h3>
              <div className="grid md:grid-cols-2 gap-4">
                {treatment.doctors_involved.map((doctor, index) => (
                  <div key={index} className="flex items-start gap-3 p-4 bg-gray-50 rounded-lg">
                    <div className="p-3 bg-primary-100 text-primary rounded-full">
                      <User className="h-6 w-6" />
                    </div>
                    <div>
                      <p className="font-medium">{doctor.name || 'Doctor'}</p>
                      <p className="text-sm text-gray-600">{doctor.speciality}</p>
                      <p className="text-sm text-gray-500 flex items-center gap-1">
                        <Building2 className="h-4 w-4" />
                        {doctor.speciality_department_name}
                      </p>
                      <p className="text-sm text-gray-500 mt-1">
                        Charges: Ksh {formatMoney(doctor.speciality_treatment_charges)}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Medicines */}
          {treatment.medicines_given && treatment.medicines_given.length > 0 && (
            <div>
              <h3 className="text-lg font-medium mb-4">Medicines</h3>
              <div className="grid md:grid-cols-2 gap-4">
                {treatment.medicines_given.map((medicine, index) => (
                  <div key={index} className="p-4 bg-gray-50 rounded-lg">
                    <div className="flex items-center gap-2 mb-2">
                      <Pill className="h-5 w-5 text-primary" />
                      <h4 className="font-medium">{medicine.medicine_name}</h4>
                    </div>
                    <p className="text-sm text-gray-600">Quantity: {medicine.quantity}</p>
                    <p className="text-sm text-gray-600">{medicine.prescription}</p>
                    <div className="mt-2 text-sm text-gray-500 flex items-center justify-between">
                      <span>Price per unit: Ksh {formatMoney(medicine.price_per_medicine)}</span>
                      <span className="font-medium">Total: Ksh {formatMoney(medicine.medicine_bill)}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Extra Fees */}
          {treatment.extra_fees && treatment.extra_fees.length > 0 && (
            <div>
              <h3 className="text-lg font-medium mb-4">Extra Fees</h3>
              <div className="space-y-3">
                {treatment.extra_fees.map((fee, index) => (
                  <div key={index} className="flex justify-between p-4 bg-gray-50 rounded-lg">
                    <div>
                      <p className="font-medium">{fee.name}</p>
                      <p className="text-sm text-gray-600">{fee.details}</p>
                    </div>
                    <p className="font-medium">Ksh {formatMoney(fee.amount)}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Bill Summary */}
          <div className="p-4 bg-gray-50 rounded-lg">
            <h3 className="text-lg font-medium mb-4">Bill Summary</h3>
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Treatment Charges</span>
                <span>Ksh {formatMoney(treatment.total_treatment_bill)}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Medicine Charges</span>
                <span>Ksh {formatMoney(treatment.total_medicine_bill)}</span>
              </div>
              <div className="flex justify-between font-medium text-lg pt-2 border-t">
                <span>Total Bill</span>
                <span>Ksh {formatMoney(treatment.total_bill)}</span>
              </div>
            </div>
          </div>

          {/* Feedback Section */}
          {treatment.treatment_status === 'Completed' && (
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
                  {treatment.feedbacks?.length > 0 ? 'Edit Feedback' : 'Add Feedback'}
                </button>
              </div>

              {treatment.feedbacks && treatment.feedbacks.length > 0 ? (
                <div className="p-4 bg-gray-50 rounded-lg">
                  <div className="flex items-start gap-3">
                    <img
                      src={treatment.feedbacks[0].user?.profile || "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&q=80"}
                      alt={treatment.feedbacks[0].user?.username}
                      className="w-10 h-10 rounded-full object-cover"
                    />
                    <div>
                      <p className="font-medium">
                        {treatment.feedbacks[0].user?.first_name} {treatment.feedbacks[0].user?.last_name}
                      </p>
                      <p className="text-sm text-gray-500">
                        {format(new Date(treatment.feedbacks[0].created_at), 'MMM d, yyyy')}
                      </p>
                      <div className="mt-2">
                        <span className={cn(
                          "px-2 py-1 text-xs font-medium rounded-full",
                          treatment.feedbacks[0].rate === 'Excellent' && "bg-green-100 text-green-700",
                          treatment.feedbacks[0].rate === 'Good' && "bg-blue-100 text-blue-700",
                          treatment.feedbacks[0].rate === 'Average' && "bg-yellow-100 text-yellow-700",
                          treatment.feedbacks[0].rate === 'Poor' && "bg-orange-100 text-orange-700",
                          treatment.feedbacks[0].rate === 'Terrible' && "bg-red-100 text-red-700"
                        )}>
                          {treatment.feedbacks[0].rate}
                        </span>
                      </div>
                      <p className="mt-2 text-gray-600">{treatment.feedbacks[0].message}</p>
                    </div>
                  </div>
                </div>
              ) : (
                <p className="text-gray-500 text-center py-4">No feedback provided yet.</p>
              )}
            </div>
          )}
        </div>
      </Modal>

      {/* Feedback Modal */}
      {showFeedbackModal && (
        <FeedbackModal
          type="treatment"
          id={treatment.id}
          existingFeedback={treatment.feedbacks?.[0]}
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