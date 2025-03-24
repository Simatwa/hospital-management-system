import { useEffect, useState } from 'react';
import { setPageTitle } from '../lib/utils';
import { getTreatments, getTreatment } from '../lib/treatments';
import { Calendar, AlertCircle, MessageSquare, User, Pill, DollarSign } from 'lucide-react';
import { format } from 'date-fns';
import toast from 'react-hot-toast';
import type { Treatment } from '../types';
import { formatMoney } from '../lib/utils';
import TreatmentDetailsModal from '../components/TreatmentDetailsModal';

export default function Treatments() {
  const [treatments, setTreatments] = useState<Treatment[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedTreatment, setSelectedTreatment] = useState<Treatment | null>(null);
  const [loadingTreatment, setLoadingTreatment] = useState(false);

  useEffect(() => {
    setPageTitle('Treatments');
    fetchTreatments();
  }, []);

  const fetchTreatments = async () => {
    try {
      const data = await getTreatments();
      setTreatments(data);
    } catch (error) {
      console.error('Error fetching treatments:', error);
      toast.error('Failed to load treatments');
    } finally {
      setLoading(false);
    }
  };

  const handleViewTreatment = async (treatmentId: number) => {
    setLoadingTreatment(true);
    try {
      const treatment = await getTreatment(treatmentId);
      setSelectedTreatment(treatment);
    } catch (error) {
      console.error('Error fetching treatment details:', error);
      toast.error('Failed to load treatment details');
    } finally {
      setLoadingTreatment(false);
    }
  };

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

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Treatment History</h1>

      <div className="bg-white rounded-lg shadow-md overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Date
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Diagnosis
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Type
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Total Bill
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {treatments.map((treatment) => (
                <tr 
                  key={treatment.id}
                  className="hover:bg-gray-50 cursor-pointer transition-colors"
                  onClick={() => handleViewTreatment(treatment.id)}
                >
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <Calendar className="h-5 w-5 text-gray-400 mr-2" />
                      <span className="text-sm text-gray-900">
                        {format(new Date(treatment.created_at), 'MMM d, yyyy')}
                      </span>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <div className="text-sm text-gray-900">{treatment.diagnosis}</div>
                    <div className="text-sm text-gray-500">{treatment.details}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="text-sm text-gray-900">{treatment.patient_type}</span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${getStatusColor(treatment.treatment_status)}`}>
                      {treatment.treatment_status}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    Ksh {formatMoney(treatment.total_bill)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        handleViewTreatment(treatment.id);
                      }}
                      className="text-primary hover:text-primary-600 transition-colors"
                      title="View Details"
                    >
                      <MessageSquare className="h-5 w-5" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {treatments.length === 0 && (
          <div className="text-center py-8">
            <AlertCircle className="mx-auto h-12 w-12 text-gray-400" />
            <h3 className="mt-2 text-sm font-medium text-gray-900">No treatments</h3>
            <p className="mt-1 text-sm text-gray-500">No treatment history found.</p>
          </div>
        )}
      </div>

      {/* Treatment Details Modal */}
      {loadingTreatment && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
        </div>
      )}

      {selectedTreatment && !loadingTreatment && (
        <TreatmentDetailsModal
          treatment={selectedTreatment}
          onClose={() => setSelectedTreatment(null)}
          onSuccess={fetchTreatments}
        />
      )}
    </div>
  );
}