import { X } from 'lucide-react';
import type { DepartmentInfo } from '../types';
import Modal from './ui/Modal';

interface DepartmentModalProps {
  department: DepartmentInfo;
  onClose: () => void;
}

export default function DepartmentModal({ department, onClose }: DepartmentModalProps) {
  return (
    <Modal
      title={department.name}
      onClose={onClose}
      className="max-w-2xl"
    >
      <div className="space-y-6">
        {department.profile && (
          <img 
            src={department.profile} 
            alt={department.name}
            className="w-full h-64 object-cover rounded-lg"
          />
        )}

        <div>
          <h3 className="text-lg font-medium mb-2">About</h3>
          <p className="text-gray-600">{department.details}</p>
        </div>

        <div>
          <h3 className="text-lg font-medium mb-4">Specialities</h3>
          <div className="grid md:grid-cols-2 gap-4">
            {department.specialities.map((speciality, index) => (
              <div key={index} className="bg-gray-50 p-4 rounded-lg">
                <h4 className="font-medium mb-2">{speciality.name}</h4>
                {speciality.details && (
                  <p className="text-sm text-gray-600 mb-2">{speciality.details}</p>
                )}
                <div className="text-sm text-primary">
                  {speciality.total_doctors} {speciality.total_doctors === 1 ? 'Doctor' : 'Doctors'}
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="text-sm text-gray-500">
          Department established: {new Date(department.created_at).toLocaleDateString()}
        </div>
      </div>
    </Modal>
  );
}