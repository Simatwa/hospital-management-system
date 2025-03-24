import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { setPageTitle } from '../lib/utils';
import { api } from '../lib/axios';
import { Calendar, FileText, Star, User, Plus, Clock, CheckCircle, XCircle, ArrowRight } from 'lucide-react';
import type { Treatment, Appointment, Profile } from '../types';
import toast from 'react-hot-toast';
import { formatMoney } from '../lib/utils';

export default function Dashboard() {
  const [profile, setProfile] = useState<Profile | null>(null);
  const [treatments, setTreatments] = useState<Treatment[]>([]);
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    setPageTitle('Patient Portal');
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [profileRes, treatmentsRes, appointmentsRes] = await Promise.all([
        api.get('/profile'),
        api.get('/treatments?limit=5'),
        api.get('/appointments?limit=5')
      ]);
      setProfile(profileRes.data);
      setTreatments(treatmentsRes.data);
      setAppointments(appointmentsRes.data);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      toast.error('Failed to load dashboard data');
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Welcome Section */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-8 dashboard-welcome">
        <div className="flex flex-col sm:flex-row items-center gap-4">
          {profile?.profile ? (
            <img 
              src={profile.profile}
              alt={profile.first_name}
              className="w-16 h-16 rounded-full object-cover"
            />
          ) : (
            <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0">
              <User className="w-8 h-8 text-primary" />
            </div>
          )}
          <div className="text-center sm:text-left">
            <h1 className="text-2xl font-bold text-gray-900">
              Welcome back, {profile?.first_name}!
            </h1>
            <p className="text-gray-600">
              Here's an overview of your health records and upcoming appointments.
            </p>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="grid sm:grid-cols-2 gap-4 mb-8">
        <Link
          to="/appointments"
          className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow dashboard-card"
        >
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-lg font-semibold mb-2">Schedule Appointment</h2>
              <p className="text-gray-600">Book a new appointment with our doctors</p>
            </div>
            <Calendar className="w-12 h-12 text-primary" />
          </div>
        </Link>
        <Link
          to="/treatments"
          className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow dashboard-card"
        >
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-lg font-semibold mb-2">View Treatments</h2>
              <p className="text-gray-600">Check your treatment history and progress</p>
            </div>
            <FileText className="w-12 h-12 text-primary" />
          </div>
        </Link>
      </div>

      {/* Recent Activity */}
      <div className="grid lg:grid-cols-2 gap-8">
        {/* Recent Appointments */}
        <div className="bg-white rounded-lg shadow-md p-6 dashboard-card">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-semibold">Recent Appointments</h2>
            <Link to="/appointments" className="text-primary hover:text-primary-600 text-sm font-medium">
              View All
            </Link>
          </div>
          <div className="space-y-4">
            {appointments.map((appointment) => (
              <div key={appointment.id} className="flex flex-col sm:flex-row sm:items-center justify-between p-4 bg-gray-50 rounded-lg gap-4">
                <div>
                  <p className="font-medium">{appointment.reason}</p>
                  <p className="text-sm text-gray-500">
                    {new Date(appointment.appointment_datetime).toLocaleDateString()}
                  </p>
                </div>
                <span className={`px-2 py-1 rounded-full text-xs font-medium w-fit ${
                  appointment.status === 'Completed' ? 'bg-green-100 text-green-800' :
                  appointment.status === 'Scheduled' ? 'bg-blue-100 text-blue-800' :
                  'bg-red-100 text-red-800'
                }`}>
                  {appointment.status}
                </span>
              </div>
            ))}
            {appointments.length === 0 && (
              <p className="text-gray-500 text-center py-4">No recent appointments</p>
            )}
          </div>
        </div>

        {/* Recent Treatments */}
        <div className="bg-white rounded-lg shadow-md p-6 dashboard-card">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-semibold">Recent Treatments</h2>
            <Link to="/treatments" className="text-primary hover:text-primary-600 text-sm font-medium">
              View All
            </Link>
          </div>
          <div className="space-y-4">
            {treatments.map((treatment) => (
              <div key={treatment.id} className="flex flex-col sm:flex-row sm:items-center justify-between p-4 bg-gray-50 rounded-lg gap-4">
                <div>
                  <p className="font-medium">{treatment.diagnosis}</p>
                  <p className="text-sm text-gray-500">
                    {new Date(treatment.created_at).toLocaleDateString()}
                  </p>
                </div>
                <span className={`px-2 py-1 rounded-full text-xs font-medium w-fit ${
                  treatment.treatment_status === 'Completed' ? 'bg-green-100 text-green-800' :
                  treatment.treatment_status === 'Inprogress' ? 'bg-blue-100 text-blue-800' :
                  'bg-red-100 text-red-800'
                }`}>
                  {treatment.treatment_status}
                </span>
              </div>
            ))}
            {treatments.length === 0 && (
              <p className="text-gray-500 text-center py-4">No recent treatments</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}