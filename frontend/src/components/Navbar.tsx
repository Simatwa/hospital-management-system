import { Link, useNavigate, useLocation } from 'react-router-dom';
import { Menu, X, User, Calendar, FileText, LogOut, Phone, MapPin, Newspaper, Info, Home, Stethoscope, Building2, Image, LogIn, LayoutDashboard, Settings } from 'lucide-react';
import { useState, useEffect } from 'react';
import { useAuthStore } from '../store/auth';
import { cn } from '../lib/utils';

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false);
  const [isScrolled, setIsScrolled] = useState(false);
  const { isAuthenticated, user, logout } = useAuthStore();
  const navigate = useNavigate();
  const location = useLocation();
  const isHome = location.pathname === '/';

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 0);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const handleLogout = () => {
    logout();
    navigate('/');
    setIsOpen(false);
  };

  const scrollToSection = (sectionId: string) => {
    setIsOpen(false);
    if (isHome) {
      const element = document.getElementById(sectionId);
      if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
      }
    } else {
      navigate(`/?section=${sectionId}`);
    }
  };

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const section = params.get('section');
    if (section && isHome) {
      const element = document.getElementById(section);
      if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
        navigate('/', { replace: true });
      }
    }
  }, [location, isHome, navigate]);

  return (
    <nav className={cn(
      "fixed top-0 left-0 right-0 z-50 bg-primary shadow-lg transition-all duration-300",
      isScrolled && "bg-opacity-95 backdrop-blur-sm"
    )}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex">
            <Link to="/" className="flex items-center" onClick={() => setIsOpen(false)}>
              <Stethoscope className="h-8 w-8 text-white" />
              <span className="text-white font-bold text-xl ml-2">HMS</span>
            </Link>
          </div>

          {/* Desktop Menu */}
          <div className="hidden lg:flex items-center space-x-2">
            <button onClick={() => scrollToSection('home')} className="nav-link">
              <Home size={18} />
              <span>Home</span>
            </button>
            <button onClick={() => scrollToSection('about')} className="nav-link">
              <Info size={18} />
              <span>About</span>
            </button>
            <button onClick={() => scrollToSection('departments')} className="nav-link">
              <Building2 size={18} />
              <span>Departments</span>
            </button>
            <button onClick={() => scrollToSection('doctors')} className="nav-link">
              <User size={18} />
              <span>Doctors</span>
            </button>
            <button onClick={() => scrollToSection('gallery')} className="nav-link">
              <Image size={18} />
              <span>Gallery</span>
            </button>
            <button onClick={() => scrollToSection('news')} className="nav-link">
              <Newspaper size={18} />
              <span>News</span>
            </button>
            <button onClick={() => scrollToSection('contact')} className="nav-link">
              <Phone size={18} />
              <span>Contact</span>
            </button>
            <button onClick={() => scrollToSection('location')} className="nav-link">
              <MapPin size={18} />
              <span>Location</span>
            </button>
            
            {isAuthenticated ? (
              <div className="flex items-center space-x-2">
                <Link
                  to="/dashboard"
                  onClick={() => setIsOpen(false)}
                  className="bg-accent hover:bg-accent-600 text-white px-4 py-2 rounded-lg font-medium flex items-center space-x-2 transition-colors"
                >
                  <LayoutDashboard size={18} />
                  <span>Dashboard</span>
                </Link>
                {user?.is_staff && (
                  <Link
                    to="/d/admin"
                    target="_blank"
                    className="text-white hover:text-gray-200 px-3 py-2 rounded-md text-sm font-medium flex items-center space-x-1"
                  >
                    <Settings size={18} />
                    <span>Admin</span>
                  </Link>
                )}
                <button
                  onClick={handleLogout}
                  className="text-white hover:text-gray-200 flex items-center space-x-1 px-3 py-2 rounded-md text-sm font-medium"
                >
                  <LogOut size={18} />
                  <span>Logout</span>
                </button>
              </div>
            ) : (
              <div className="flex items-center space-x-2">
                <Link
                  to="/login"
                  onClick={() => setIsOpen(false)}
                  className="text-white hover:text-gray-200 px-3 py-2 rounded-md text-sm font-medium flex items-center space-x-1"
                >
                  <LogIn size={18} />
                  <span>Login</span>
                </Link>
                <Link
                  to="/register"
                  onClick={() => setIsOpen(false)}
                  className="bg-accent hover:bg-accent-600 text-white px-4 py-2 rounded-lg font-medium flex items-center space-x-2 transition-colors"
                >
                  <User size={18} />
                  <span>Register</span>
                </Link>
              </div>
            )}
          </div>

          {/* Mobile menu button */}
          <div className="lg:hidden flex items-center">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="text-white hover:text-gray-200"
            >
              {isOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      <div className={cn('lg:hidden', isOpen ? 'block' : 'hidden')}>
        <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
          <MobileButton onClick={() => scrollToSection('home')} icon={<Home size={18} />}>Home</MobileButton>
          <MobileButton onClick={() => scrollToSection('about')} icon={<Info size={18} />}>About</MobileButton>
          <MobileButton onClick={() => scrollToSection('departments')} icon={<Building2 size={18} />}>Departments</MobileButton>
          <MobileButton onClick={() => scrollToSection('doctors')} icon={<User size={18} />}>Doctors</MobileButton>
          <MobileButton onClick={() => scrollToSection('gallery')} icon={<Image size={18} />}>Gallery</MobileButton>
          <MobileButton onClick={() => scrollToSection('news')} icon={<Newspaper size={18} />}>News</MobileButton>
          <MobileButton onClick={() => scrollToSection('contact')} icon={<Phone size={18} />}>Contact</MobileButton>
          <MobileButton onClick={() => scrollToSection('location')} icon={<MapPin size={18} />}>Location</MobileButton>
          
          {isAuthenticated ? (
            <>
              <MobileNavLink to="/dashboard" icon={<LayoutDashboard size={18} />}>
                Dashboard
              </MobileNavLink>
              {user?.is_staff && (
                <MobileNavLink to="/d/admin" icon={<Settings size={18} />}>
                  Admin
                </MobileNavLink>
              )}
              <button
                onClick={handleLogout}
                className="w-full text-left text-gray-100 hover:bg-primary-700 block px-3 py-2 rounded-md text-base font-medium flex items-center space-x-2"
              >
                <LogOut size={18} />
                <span>Logout</span>
              </button>
            </>
          ) : (
            <>
              <MobileNavLink to="/login" icon={<LogIn size={18} />}>Login</MobileNavLink>
              <MobileNavLink to="/register" icon={<User size={18} />}>Register</MobileNavLink>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}

function NavLink({ to, children, icon }: { to: string; children: React.ReactNode; icon?: React.ReactNode }) {
  const location = useLocation();
  const isActive = location.pathname === to;

  return (
    <Link
      to={to}
      className={cn(
        "text-white hover:text-gray-200 px-3 py-2 rounded-md text-sm font-medium flex items-center space-x-1 transition-colors",
        isActive && "bg-primary-700"
      )}
    >
      {icon}
      <span>{children}</span>
    </Link>
  );
}

function MobileNavLink({
  to,
  children,
  icon,
}: {
  to: string;
  children: React.ReactNode;
  icon?: React.ReactNode;
}) {
  const location = useLocation();
  const isActive = location.pathname === to;
  const navigate = useNavigate();

  return (
    <Link
      to={to}
      onClick={() => {
        const mobileMenu = document.querySelector('[role="dialog"]');
        if (mobileMenu) {
          mobileMenu.setAttribute('aria-hidden', 'true');
        }
      }}
      className={cn(
        "text-gray-100 hover:bg-primary-700 block px-3 py-2 rounded-md text-base font-medium flex items-center space-x-2 transition-colors",
        isActive && "bg-primary-700"
      )}
    >
      {icon}
      <span>{children}</span>
    </Link>
  );
}

function MobileButton({
  onClick,
  children,
  icon,
}: {
  onClick: () => void;
  children: React.ReactNode;
  icon?: React.ReactNode;
}) {
  return (
    <button
      onClick={onClick}
      className="text-gray-100 hover:bg-primary-700 w-full text-left block px-3 py-2 rounded-md text-base font-medium flex items-center space-x-2 transition-colors"
    >
      {icon}
      <span>{children}</span>
    </button>
  );
}