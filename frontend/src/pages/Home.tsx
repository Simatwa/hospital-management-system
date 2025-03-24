import { useEffect, useState, lazy, Suspense } from 'react';
import { setPageTitle } from '../lib/utils';
import { MapPin, Mail, Phone, Calendar, ArrowRight, Search, Send, Clock, AlertCircle } from 'lucide-react';
import type { HospitalAbout, DepartmentInfo, AvailableDoctor, HospitalGallery, ShallowHospitalNews, UserFeedback, NewsDetail } from '../types';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import { format, isValid, parseISO } from 'date-fns';
import 'leaflet/dist/leaflet.css';
import StarRating from '../components/StarRating';
import toast from 'react-hot-toast';
import { useNavigate } from 'react-router-dom';

// Lazy load the NewsModal component
const NewsModal = lazy(() => import('../components/NewsModal'));

// Helper function to safely format dates
const formatDate = (dateString: string) => {
  const date = parseISO(dateString);
  return isValid(date) ? format(date, 'MMM d, yyyy') : 'Date not available';
};

export default function Home() {
  const [about, setAbout] = useState<HospitalAbout | null>(null);
  const [departments, setDepartments] = useState<DepartmentInfo[]>([]);
  const [doctors, setDoctors] = useState<AvailableDoctor[]>([]);
  const [galleries, setGalleries] = useState<HospitalGallery[]>([]);
  const [news, setNews] = useState<ShallowHospitalNews[]>([]);
  const [testimonials, setTestimonials] = useState<UserFeedback[]>([]);
  const [email, setEmail] = useState('');
  const [isSubscribing, setIsSubscribing] = useState(false);
  const [selectedNews, setSelectedNews] = useState<NewsDetail | null>(null);
  const [visibleGalleries, setVisibleGalleries] = useState(6);
  const navigate = useNavigate();

  useEffect(() => {
    setPageTitle('Home');
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [aboutRes, departmentsRes, doctorsRes, galleriesRes, newsRes, testimonialsRes] = await Promise.all([
        fetch('/api/v1/about'),
        fetch('/api/v1/departments'),
        fetch('/api/v1/doctors?limit=6'),
        fetch('/api/v1/galleries'),
        fetch('/api/v1/news'),
        fetch('/api/v1/feedbacks')
      ]);

      const [aboutData, departmentsData, doctorsData, galleriesData, newsData, testimonialsData] = await Promise.all([
        aboutRes.json(),
        departmentsRes.json(),
        doctorsRes.json(),
        galleriesRes.json(),
        newsRes.json(),
        testimonialsRes.json()
      ]);

      setAbout(aboutData);
      setDepartments(departmentsData);
      setDoctors(doctorsData);
      setGalleries(galleriesData);
      setNews(newsData);
      setTestimonials(testimonialsData);
    } catch (error) {
      console.error('Error fetching data:', error);
      toast.error('Failed to load content. Please try again later.', {
        icon: <AlertCircle className="text-red-500" />
      });
    }
  };

  const handleSubscribe = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email) return;

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      toast.error('Please enter a valid email address');
      return;
    }

    setIsSubscribing(true);
    try {
      const response = await fetch('/api/v1/subscribe', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `email=${encodeURIComponent(email)}`,
      });
      const data = await response.json();
      
      if (response.ok) {
        toast.success(data.detail);
        setEmail('');
      } else {
        toast.error(data.detail);
      }
    } catch (error) {
      console.error('Error subscribing:', error);
      toast.error('Failed to subscribe. Please try again later.');
    } finally {
      setIsSubscribing(false);
    }
  };

  const handleNewsClick = async (newsId: number) => {
    try {
      const response = await fetch(`/api/v1/news/${newsId}`);
      if (!response.ok) throw new Error('News not found');
      const newsDetail = await response.json();
      setSelectedNews(newsDetail);
    } catch (error) {
      console.error('Error fetching news details:', error);
      toast.error('Failed to load news details');
    }
  };

  const loadMoreGalleries = () => {
    setVisibleGalleries(prev => prev + 6);
  };

  return (
    <div className="min-h-screen pt-16">
      {/* Hero Section */}
      <section id="home" className="relative h-[600px] bg-gradient-to-r from-primary-900 to-primary-700 text-white">
        <div className="absolute inset-0">
          <img 
            src={about?.wallpaper || "https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?auto=format&fit=crop&q=80"} 
            alt="Hospital" 
            className="w-full h-full object-cover opacity-20"
          />
        </div>
        <div className="relative container mx-auto px-4 h-full flex flex-col justify-center">
          <h1 className="text-5xl md:text-6xl font-bold mb-6 hero-content hero-title">{about?.name || 'Smart Hospital'}</h1>
          <p className="text-xl md:text-2xl mb-8 text-gray-200 hero-content hero-subtitle">{about?.slogan || 'We treat but God heals.'}</p>
          <div className="flex flex-wrap gap-4 hero-content hero-buttons">
            <a href="/register" className="bg-accent hover:bg-accent-600 text-white px-8 py-3 rounded-lg font-semibold transition-colors">
              Register Now
            </a>
            <a href="#departments" className="bg-white hover:bg-gray-100 text-primary px-8 py-3 rounded-lg font-semibold transition-colors">
              Our Departments
            </a>
          </div>
        </div>
      </section>

      {/* About Section */}
      <section id="about" className="py-16 bg-gray-50">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12">About Us</h2>
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div>
              <p className="text-gray-600 mb-6">{about?.details}</p>
              <div className="space-y-4">
                <div className="flex items-start gap-4">
                  <div className="p-3 bg-primary-100 text-primary rounded-lg">
                    <MapPin />
                  </div>
                  <div>
                    <h3 className="font-semibold">Location</h3>
                    <p className="text-gray-600">{about?.location_name}</p>
                  </div>
                </div>
                <div className="flex items-start gap-4">
                  <div className="p-3 bg-primary-100 text-primary rounded-lg">
                    <Mail />
                  </div>
                  <div>
                    <h3 className="font-semibold">Email</h3>
                    <p className="text-gray-600">{about?.email}</p>
                  </div>
                </div>
                <div className="flex items-start gap-4">
                  <div className="p-3 bg-primary-100 text-primary rounded-lg">
                    <Calendar />
                  </div>
                  <div>
                    <h3 className="font-semibold">Founded</h3>
                    <p className="text-gray-600">Est. {about?.founded_in}</p>
                  </div>
                </div>
                <div className="flex items-start gap-4">
                  <div className="p-3 bg-primary-100 text-primary rounded-lg">
                    <Clock />
                  </div>
                  <div>
                    <h3 className="font-semibold">Working Hours</h3>
                    <p className="text-gray-600">24/7 Emergency Services</p>
                  </div>
                </div>
              </div>
            </div>
            <div className="space-y-6">
              <div className="bg-white p-6 rounded-lg shadow-md">
                <h3 className="text-xl font-semibold mb-4">Our Mission</h3>
                <p className="text-gray-600">{about?.mission}</p>
              </div>
              <div className="bg-white p-6 rounded-lg shadow-md">
                <h3 className="text-xl font-semibold mb-4">Our Vision</h3>
                <p className="text-gray-600">{about?.vision}</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Departments Section */}
      <section id="departments" className="py-16">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12">Our Departments</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {departments.map((dept, index) => (
              <div 
                key={index} 
                className="card-hover fade-in-up stagger-1"
              >
                {dept.profile && (
                  <img src={dept.profile} alt={dept.name} className="w-full h-48 object-cover" />
                )}
                <div className="p-6">
                  <h3 className="text-xl font-semibold mb-3">{dept.name}</h3>
                  <p className="text-gray-600 mb-4">{dept.details}</p>
                  <div className="space-y-2">
                    {dept.specialities.map((spec, idx) => (
                      <div key={idx} className="flex items-center text-gray-700">
                        <ArrowRight size={16} className="mr-2 text-primary" />
                        <span>{spec.name}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Doctors Section */}
      <section id="doctors" className="py-16 bg-gray-50">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12">Our Doctors</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {doctors.map((doctor, index) => (
              <div 
                key={index} 
                className="card-hover fade-in-up stagger-2"
              >
                <img 
                  src={doctor.profile || "https://images.unsplash.com/photo-1537368910025-700350fe46c7?auto=format&fit=crop&q=80"} 
                  alt={doctor.fullname} 
                  className="w-full h-64 object-cover"
                />
                <div className="p-6">
                  <h3 className="text-xl font-semibold mb-2">{doctor.fullname}</h3>
                  <p className="text-primary mb-4">{doctor.speciality}</p>
                  <p className="text-gray-600">{doctor.department_name}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Gallery Section */}
      <section id="gallery" className="py-16">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12">Gallery</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {galleries.slice(0, visibleGalleries).map((gallery, index) => (
              <div key={index} className="card-hover fade-in-up stagger-3">
                <img 
                  src={gallery.picture || "https://images.unsplash.com/photo-1538108149393-fbbd81895907?auto=format&fit=crop&q=80"} 
                  alt={gallery.title} 
                  className="w-full h-64 object-cover"
                />
                <div className="p-6">
                  <h3 className="text-xl font-semibold mb-2">{gallery.title}</h3>
                  <p className="text-gray-600 mb-4">{gallery.details}</p>
                  <div className="flex items-center justify-between text-sm text-gray-500">
                    <span className="flex items-center gap-1">
                      <MapPin size={16} />
                      {gallery.location_name}
                    </span>
                    <span>{formatDate(gallery.date)}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
          {galleries.length > visibleGalleries && (
            <div className="text-center mt-8">
              <button
                onClick={loadMoreGalleries}
                className="bg-primary hover:bg-primary-600 text-white px-6 py-2 rounded-lg font-semibold transition-colors"
              >
                Load More
              </button>
            </div>
          )}
        </div>
      </section>

      {/* News Section */}
      <section id="news" className="py-16 bg-gray-50">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12">Latest News</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {news.map((item, index) => (
              <div 
                key={index} 
                className="card-hover fade-in-up stagger-4"
                onClick={() => handleNewsClick(item.id)}
              >
                <img 
                  src={item.cover_photo || "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&q=80"} 
                  alt={item.title} 
                  className="w-full h-48 object-cover"
                />
                <div className="p-6">
                  <span className="text-sm text-primary mb-2 block">{item.category}</span>
                  <h3 className="text-xl font-semibold mb-3">{item.title}</h3>
                  <p className="text-gray-600">{item.summary}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Map Section */}
      {about && (
        <section id="location" className="py-16 bg-white">
          <div className="container mx-auto px-4">
            <h2 className="text-3xl font-bold text-center mb-12">Our Location</h2>
            <div className="h-[400px] rounded-lg overflow-hidden shadow-lg">
              <MapContainer 
                center={[Number(about.latitude), Number(about.longitude)]} 
                zoom={13} 
                style={{ height: '100%', width: '100%' }}
              >
                <TileLayer
                  url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                  attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                />
                <Marker position={[Number(about.latitude), Number(about.longitude)]}>
                  <Popup>
                    <div className="p-2">
                      <h3 className="font-semibold">{about.name}</h3>
                      <p className="text-sm">{about.location_name}</p>
                    </div>
                  </Popup>
                </Marker>
              </MapContainer>
            </div>
          </div>
        </section>
      )}

      {/* Testimonials Section */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12">What Our Patients Say</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {testimonials.slice(0, 6).map((testimonial, index) => (
              <div key={index} className="testimonial-card">
                <div className="testimonial-profile">
                  <img 
                    src={testimonial.user.profile || "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&q=80"} 
                    alt={testimonial.user.username}
                    className="testimonial-image"
                  />
                  <div className="testimonial-info">
                    <h3 className="testimonial-name">{testimonial.user.first_name} {testimonial.user.last_name}</h3>
                    <div className="testimonial-meta">
                      <span className="testimonial-role">{testimonial.user.role}</span>
                      <span>•</span>
                      <span className="testimonial-date">{formatDate(testimonial.created_at)}</span>
                    </div>
                    <div className="testimonial-rating">
                      <StarRating rating={testimonial.rate} />
                    </div>
                  </div>
                </div>
                <p className="testimonial-message">{testimonial.message}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Subscribe Section */}
      <section className="py-16 bg-primary">
        <div className="container mx-auto px-4">
          <div className="max-w-2xl mx-auto text-center text-white">
            <h2 className="text-3xl font-bold mb-6">Subscribe to Our Newsletter</h2>
            <p className="mb-8">Stay updated with our latest news and updates</p>
            <form onSubmit={handleSubscribe} className="flex flex-col sm:flex-row gap-4 max-w-md mx-auto">
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Enter your email"
                className="flex-1 px-4 py-2 rounded-lg text-gray-900 w-full"
                required
              />
              <button
                type="submit"
                disabled={isSubscribing}
                className="bg-accent hover:bg-accent-600 text-white px-6 py-2 rounded-lg font-semibold transition-colors flex items-center justify-center gap-2 w-full sm:w-auto disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <Send size={20} />
                <span>{isSubscribing ? 'Subscribing...' : 'Subscribe'}</span>
              </button>
            </form>
          </div>
        </div>
      </section>

      {/* News Modal */}
      {selectedNews && (
        <Suspense fallback={
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
          </div>
        }>
          <NewsModal
            news={selectedNews}
            onClose={() => setSelectedNews(null)}
          />
        </Suspense>
      )}
    </div>
  );
}