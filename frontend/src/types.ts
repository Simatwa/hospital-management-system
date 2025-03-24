import { type ClassValue } from 'clsx';

export interface Doctor {
  id: number;
  fullname: string;
  speciality: string;
  profile: string | null;
  working_days: string[];
  department_name: string;
}

export interface FeedbackFormData {
  message: string;
  rate: 'Excellent' | 'Good' | 'Average' | 'Poor' | 'Terrible';
}

export interface RegisterFormData {
  first_name: string;
  last_name: string;
  username: string;
  email: string;
  phone_number: string;
  location: string;
  password: string;
  date_of_birth: string;
}

export interface LoginFormData {
  username: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export interface Treatment {
  id: number;
  patient_type: 'Inpatient' | 'Outpatient';
  diagnosis: string;
  details: string;
  treatment_status: 'Inprogress' | 'Completed' | 'Cancelled';
  total_bill: number;
  created_at: string;
  updated_at: string;
  doctors_involved: Array<{
    name: string;
    speciality: string;
    profile: string | null;
    speciality_treatment_charges: number;
    speciality_department_name: string;
  }>;
  medicines_given: Array<{
    medicine_name: string;
    quantity: number;
    prescription: string;
    price_per_medicine: number;
    medicine_bill: number;
  }>;
  total_medicine_bill: number;
  total_treatment_bill: number;
  extra_fees: Array<{
    name: string;
    details: string;
    amount: number;
  }>;
  feedbacks: UserFeedback[];
}

export interface Appointment {
  id: number;
  doctor_id: number;
  appointment_datetime: string;
  reason: string;
  status: 'Scheduled' | 'Completed' | 'Cancelled';
  appointment_charges: number;
  created_at: string;
  updated_at: string;
  feedbacks: UserFeedback[];
}

export interface Profile {
  first_name: string;
  last_name: string;
  username: string;
  email: string;
  phone_number: string;
  location: string;
  date_of_birth: string;
  gender: 'male' | 'female' | 'other';
  account_balance: number;
  profile: string | null;
  is_staff: boolean;
  date_joined: string;
  bio: string | null;
}

export interface HospitalAbout {
  name: string;
  short_name: string;
  details: string;
  slogan: string;
  location_name: string;
  latitude: number;
  longitude: number;
  founded_in: string;
  founder_name: string;
  mission: string;
  vision: string;
  email: string | null;
  facebook: string | null;
  twitter: string | null;
  linkedin: string | null;
  instagram: string | null;
  tiktok: string | null;
  youtube: string | null;
  logo: string | null;
  wallpaper: string | null;
}

export interface DepartmentInfo {
  name: string;
  details: string | null;
  profile: string | null;
  specialities: Array<{
    name: string;
    details: string | null;
    total_doctors: number;
  }>;
  created_at: string;
}

export interface AvailableDoctor {
  id: number;
  fullname: string;
  speciality: string;
  profile: string | null;
  working_days: string[];
  department_name: string;
}

export interface HospitalGallery {
  title: string;
  details: string;
  location_name: string;
  video_link: string | null;
  picture: string | null;
  date: string;
}

export interface ShallowHospitalNews {
  id: number;
  title: string;
  category: string;
  summary: string;
  cover_photo: string | null;
  created_at: string;
  views: number;
}

export interface NewsDetail extends ShallowHospitalNews {
  content: string;
  document: string | null;
  video_link: string | null;
  updated_at: string;
  author: {
    first_name: string;
    last_name: string;
    profile: string;
  };
  tags: string[];
  related_news: ShallowHospitalNews[];
}

export interface UserFeedback {
  id: number;
  message: string;
  rate: 'Excellent' | 'Good' | 'Average' | 'Poor' | 'Terrible';
  created_at: string;
  updated_at: string;
  user: {
    username: string;
    first_name: string | null;
    last_name: string | null;
    role: string;
    profile: string | null;
  };
}