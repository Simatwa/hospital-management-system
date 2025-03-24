import { useEffect } from 'react';
import { setPageTitle } from '../../lib/utils';

export default function Profile() {
  useEffect(() => {
    setPageTitle('Profile');
  }, []);

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Profile</h1>
      <div className="bg-white rounded-lg shadow-md p-6">
        <p className="text-gray-600">Profile settings coming soon</p>
      </div>
    </div>
  );
}