import { Outlet, useLocation } from 'react-router-dom';
import { useAuthStore } from '../store/auth';
import Navbar from './Navbar';
import PatientPortalNav from './PatientPortalNav';
import Footer from './Footer';

const PORTAL_ROUTES = ['/dashboard', '/appointments', '/treatments', '/profile'];

export default function Layout() {
  const { isAuthenticated } = useAuthStore();
  const location = useLocation();
  const isPortalRoute = PORTAL_ROUTES.some(route => location.pathname.startsWith(route));

  return (
    <div className="min-h-screen flex flex-col">
      {isAuthenticated && isPortalRoute ? (
        <>
          <PatientPortalNav />
          <main className="flex-1 bg-gray-50">
            <Outlet />
          </main>
        </>
      ) : (
        <>
          <Navbar />
          <main className="flex-1">
            <Outlet />
          </main>
          <Footer />
        </>
      )}
    </div>
  );
}