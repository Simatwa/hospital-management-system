import { Link, useNavigate, useLocation } from 'react-router-dom';
import { Home, Calendar, FileText, User, LogOut, ArrowLeft, Menu, X, Settings } from 'lucide-react';
import { useAuthStore } from '../store/auth';
import { cn } from '../lib/utils';
import { useState } from 'react';

export default function PatientPortalNav() {
  const navigate = useNavigate();
  const location = useLocation();
  const { logout, user } = useAuthStore();
  const [isOpen, setIsOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/');
    setIsOpen(false);
  };

  return (
    <nav className="bg-white border-b shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex">
            <div className="flex-shrink-0 flex items-center">
              <Link 
                to="/" 
                onClick={() => setIsOpen(false)}
                className="text-primary hover:text-primary-600 flex items-center gap-2"
              >
                <ArrowLeft size={20} />
                <span className="hidden sm:inline">Return to Website</span>
                <span className="sm:hidden">Back</span>
              </Link>
            </div>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex md:items-center md:space-x-4">
            <NavLink to="/dashboard" active={location.pathname === '/dashboard'}>
              <Home size={20} />
              <span>Dashboard</span>
            </NavLink>

            <NavLink to="/appointments" active={location.pathname === '/appointments'}>
              <Calendar size={20} />
              <span>Appointments</span>
            </NavLink>

            <NavLink to="/treatments" active={location.pathname === '/treatments'}>
              <FileText size={20} />
              <span>Treatments</span>
            </NavLink>

            <NavLink to="/profile" active={location.pathname === '/profile'}>
              <User size={20} />
              <span>Profile</span>
            </NavLink>

            {user?.is_staff && (
              <a
                href="/d/admin"
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-700 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium flex items-center space-x-2"
              >
                <Settings size={20} />
                <span>Admin</span>
              </a>
            )}

            <button
              onClick={handleLogout}
              className="text-gray-700 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium flex items-center space-x-2"
            >
              <LogOut size={20} />
              <span>Logout</span>
            </button>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden flex items-center">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="text-gray-700 hover:text-gray-900 p-2"
            >
              {isOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Navigation */}
      <div className={cn('md:hidden', isOpen ? 'block' : 'hidden')}>
        <div className="px-2 pt-2 pb-3 space-y-1">
          <MobileNavLink 
            to="/dashboard" 
            active={location.pathname === '/dashboard'}
            onClick={() => setIsOpen(false)}
          >
            <Home size={20} />
            <span>Dashboard</span>
          </MobileNavLink>

          <MobileNavLink 
            to="/appointments" 
            active={location.pathname === '/appointments'}
            onClick={() => setIsOpen(false)}
          >
            <Calendar size={20} />
            <span>Appointments</span>
          </MobileNavLink>

          <MobileNavLink 
            to="/treatments" 
            active={location.pathname === '/treatments'}
            onClick={() => setIsOpen(false)}
          >
            <FileText size={20} />
            <span>Treatments</span>
          </MobileNavLink>

          <MobileNavLink 
            to="/profile" 
            active={location.pathname === '/profile'}
            onClick={() => setIsOpen(false)}
          >
            <User size={20} />
            <span>Profile</span>
          </MobileNavLink>

          {user?.is_staff && (
            <a
              href="/d/admin"
              target="_blank"
              rel="noopener noreferrer"
              className="text-gray-700 hover:text-gray-900 hover:bg-gray-50 block px-3 py-2 rounded-md text-base font-medium flex items-center space-x-2"
              onClick={() => setIsOpen(false)}
            >
              <Settings size={20} />
              <span>Admin</span>
            </a>
          )}

          <button
            onClick={handleLogout}
            className="w-full text-left text-gray-700 hover:text-gray-900 hover:bg-gray-50 px-3 py-2 rounded-md text-base font-medium flex items-center space-x-2"
          >
            <LogOut size={20} />
            <span>Logout</span>
          </button>
        </div>
      </div>
    </nav>
  );
}

function NavLink({ to, children, active }: { to: string; children: React.ReactNode; active: boolean }) {
  return (
    <Link
      to={to}
      className={cn(
        "text-gray-700 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium flex items-center space-x-2",
        active && "bg-gray-100"
      )}
    >
      {children}
    </Link>
  );
}

function MobileNavLink({ 
  to, 
  children, 
  active,
  onClick 
}: { 
  to: string; 
  children: React.ReactNode; 
  active: boolean;
  onClick: () => void;
}) {
  return (
    <Link
      to={to}
      onClick={onClick}
      className={cn(
        "text-gray-700 hover:text-gray-900 hover:bg-gray-50 block px-3 py-2 rounded-md text-base font-medium flex items-center space-x-2",
        active && "bg-gray-100"
      )}
    >
      {children}
    </Link>
  );
}