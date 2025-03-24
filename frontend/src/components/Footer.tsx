import { Facebook, Twitter, Linkedin, Instagram, Youtube, MapPin, Mail, Phone } from 'lucide-react';
import { useEffect, useState } from 'react';
import type { HospitalAbout } from '../types';

export default function Footer() {
  const [about, setAbout] = useState<HospitalAbout | null>(null);

  useEffect(() => {
    fetch('/api/v1/about')
      .then(res => res.json())
      .then(data => setAbout(data))
      .catch(error => console.error('Error fetching about data:', error));
  }, []);

  return (
    <footer className="bg-primary-800 text-white" id="contact">
      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <h3 className="text-lg font-semibold mb-4">Contact Us</h3>
            <div className="space-y-3">
              {about?.email && (
                <a href={`mailto:${about.email}`} className="text-gray-300 hover:text-white flex items-center gap-2">
                  <Mail size={18} />
                  <span>{about.email}</span>
                </a>
              )}
              <p className="text-gray-300 flex items-center gap-2">
                <MapPin size={18} />
                <span>{about?.location_name || 'Meru - Kenya'}</span>
              </p>
            </div>
          </div>
          <div>
            <h3 className="text-lg font-semibold mb-4">Quick Links</h3>
            <ul className="space-y-2">
              <li><a href="#about" className="text-gray-300 hover:text-white">About Us</a></li>
              <li><a href="#departments" className="text-gray-300 hover:text-white">Departments</a></li>
              <li><a href="#doctors" className="text-gray-300 hover:text-white">Doctors</a></li>
              <li><a href="#gallery" className="text-gray-300 hover:text-white">Gallery</a></li>
              <li><a href="#news" className="text-gray-300 hover:text-white">News</a></li>
            </ul>
          </div>
          <div>
            <h3 className="text-lg font-semibold mb-4">Follow Us</h3>
            <div className="flex space-x-4">
              {about?.facebook && (
                <a href={about.facebook} target="_blank" rel="noopener noreferrer" className="text-gray-300 hover:text-white transform hover:scale-110 transition-transform">
                  <Facebook size={24} />
                </a>
              )}
              {about?.twitter && (
                <a href={about.twitter} target="_blank" rel="noopener noreferrer" className="text-gray-300 hover:text-white transform hover:scale-110 transition-transform">
                  <Twitter size={24} />
                </a>
              )}
              {about?.linkedin && (
                <a href={about.linkedin} target="_blank" rel="noopener noreferrer" className="text-gray-300 hover:text-white transform hover:scale-110 transition-transform">
                  <Linkedin size={24} />
                </a>
              )}
              {about?.instagram && (
                <a href={about.instagram} target="_blank" rel="noopener noreferrer" className="text-gray-300 hover:text-white transform hover:scale-110 transition-transform">
                  <Instagram size={24} />
                </a>
              )}
              {about?.youtube && (
                <a href={about.youtube} target="_blank" rel="noopener noreferrer" className="text-gray-300 hover:text-white transform hover:scale-110 transition-transform">
                  <Youtube size={24} />
                </a>
              )}
            </div>
          </div>
        </div>
        <div className="mt-8 pt-8 border-t border-gray-700 text-center">
          <p className="text-gray-300">&copy; {new Date().getFullYear()} {about?.name || 'Hospital Management System'}. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
}