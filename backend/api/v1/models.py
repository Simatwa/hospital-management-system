from pydantic import BaseModel, Field, field_validator, FutureDatetime, Field, HttpUrl
from typing import Optional, Any
from datetime import datetime, date
from hospital_ms.settings import MEDIA_URL
from users.models import CustomUser
from hospital.models import (
    Treatment,
    Appointment,
)
from staffing.models import WorkingDay, Doctor
from external.models import News, ServiceFeedback
from os import path


class TokenAuth(BaseModel):
    """
    - `access_token` : Token value.
    - `token_type` : bearer
    """

    access_token: str
    token_type: Optional[str] = "bearer"

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "pms_27b9d79erc245r44b9rba2crd2273b5cbb71",
                "token_type": "bearer",
            }
        }


class Feedback(BaseModel):
    detail: Any = Field(description="Feedback in details")

    class Config:
        json_schema_extra = {
            "example": {"detail": "This is a detailed feedback message."}
        }


class NewFeedbackInfo(BaseModel):
    message: str
    rate: ServiceFeedback.FeedbackRate

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Great service!",
                "rate": "Excellent",
            }
        }


class UpdateFeedbackInfo(BaseModel):
    message: Optional[str] = None
    rate: Optional[ServiceFeedback.FeedbackRate] = None

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Good service.",
                "rate": "Good",
            }
        }


class CompleteFeedbackInfo(NewFeedbackInfo):
    id: int
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_model(cls, obj: ServiceFeedback):
        assert isinstance(
            obj, ServiceFeedback
        ), f"Obj must be an instance of {ServiceFeedback} not {type(obj)}"
        cls.id = obj.id
        cls.message = obj.message
        cls.rate = obj.rate
        cls.created_at = obj.created_at
        cls.updated_at = obj.updated_at
        return cls

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "message": "Great service!",
                "rate": "Excellent",
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-02T00:00:00",
            }
        }


class UserFeedback(CompleteFeedbackInfo):
    class UserInfo(BaseModel):
        username: str
        first_name: Optional[str] = None
        last_name: Optional[str] = None
        role: CustomUser.UserRole
        profile: Optional[str]

        @field_validator("profile")
        def validate_cover_photo(value):
            if value and not value.startswith("/"):
                return path.join(MEDIA_URL, value)
            return value

        class Config:
            json_schema_extra = {
                "example": {
                    "username": "johndoe",
                    "first_name": "John",
                    "last_name": "Doe",
                    "role": "Patient",
                    "profile": "/media/custom_user/profile.jpg",
                }
            }

    user: UserInfo

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "message": "Great service!",
                "rate": "Excellent",
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-02T00:00:00",
                "user": {
                    "username": "johndoe",
                    "first_name": "John",
                    "last_name": "Doe",
                    "role": "Patient",
                    "profile": "/media/custom_user/profile.jpg",
                },
            }
        }


class EditablePersonalData(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    location: Optional[str] = None
    bio: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "phone_number": "+1234567890",
                "email": "john.doe@example.com",
                "location": "123 Main St, Anytown, USA",
                "bio": "This is an example of user's description.",
            }
        }


class Profile(EditablePersonalData):
    username: str
    date_of_birth: date
    gender: CustomUser.UserGender
    account_balance: float
    profile: Optional[str] = None
    is_staff: Optional[bool] = False
    date_joined: datetime

    @field_validator("profile")
    def validate_file(value):
        if value:
            return path.join(MEDIA_URL, value)
        return value

    class Config:
        json_schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "phone_number": "+1234567890",
                "email": "john.doe@example.com",
                "location": "123 Main St, Anytown, USA",
                "bio": "This is an example of user's description.",
                "username": "johndoe",
                "date_of_birth": "1990-01-01",
                "gender": "male",
                "account_balance": 100.0,
                "profile": "/media/custom_user/profile.jpg",
                "is_staff": False,
                "date_joined": "2023-01-01T00:00:00",
            }
        }


class ShallowPatientTreatment(BaseModel):
    id: int
    patient_type: Treatment.PatientType
    diagnosis: str
    details: str
    treatment_status: Treatment.TreatmentStatus
    total_bill: float
    created_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "patient_type": "Inpatient",
                "diagnosis": "Flu",
                "details": "Patient has a severe flu.",
                "treatment_status": "Inprogress",
                "total_bill": 200.0,
                "created_at": "2023-01-01T00:00:00",
            }
        }


class PatientTreatment(ShallowPatientTreatment):
    class TreatmentMedicine(BaseModel):
        medicine_name: str
        quantity: int
        prescription: str
        price_per_medicine: float
        medicine_bill: float

        class Config:
            json_schema_extra = {
                "example": {
                    "medicine_name": "Paracetamol",
                    "quantity": 10,
                    "prescription": "Take one tablet every 6 hours",
                    "price_per_medicine": 1.0,
                    "medicine_bill": 10.0,
                }
            }

    class DoctorInvolved(BaseModel):
        name: str
        speciality: str
        profile: Optional[str] = None
        speciality_treatment_charges: float
        speciality_department_name: str

        @field_validator("profile")
        def validate_file(value):
            if value:
                return path.join(MEDIA_URL, value)
            return value

        class Config:
            json_schema_extra = {
                "example": {
                    "name": "Dr. Smith",
                    "speciality": "Cardiology",
                    "profile": "/media/custom_user/dr-smith-001.jpg",
                    "speciality_treatment_charges": 150.0,
                    "speciality_department_name": "Cardiology",
                }
            }

    class ExtraFees(BaseModel):
        name: str
        details: str
        amount: float

        class Config:
            json_schema_extra = {
                "example": {"name": "X-ray", "details": "Chest X-ray", "amount": 50.0}
            }

    doctors_involved: list[DoctorInvolved]
    medicines_given: list[TreatmentMedicine]
    total_medicine_bill: float
    total_treatment_bill: float
    extra_fees: list[ExtraFees]
    feedbacks: list[CompleteFeedbackInfo]
    updated_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "patient_type": "inpatient",
                "diagnosis": "Flu",
                "details": "Patient has a severe flu.",
                "treatment_status": "Inprogress",
                "total_bill": 260.0,
                "created_at": "2023-01-01T00:00:00",
                "doctors_involved": [
                    {
                        "name": "Dr. Smith",
                        "speciality": "Cardiology",
                        "speciality_treatment_charges": 150.0,
                        "speciality_department_name": "Cardiology",
                    }
                ],
                "medicines_given": [
                    {
                        "medicine_name": "Paracetamol",
                        "quantity": 10,
                        "prescription": "Take one tablet every 6 hours",
                        "price_per_medicine": 1.0,
                        "medicine_bill": 10.0,
                    }
                ],
                "total_medicine_bill": 10.0,
                "total_treatment_bill": 200.0,
                "extra_fees": [
                    {"name": "X-ray", "details": "Chest X-ray", "amount": 50.0}
                ],
                "feedbacks": [
                    {
                        "id": 1,
                        "message": "Great service!",
                        "rate": "Excellent",
                        "created_at": "2023-01-01T00:00:00",
                        "updated_at": "2023-01-02T00:00:00",
                    },
                ],
                "updated_at": "2023-01-02T00:00:00",
            }
        }


class AvailableDoctor(BaseModel):
    id: int
    fullname: str
    speciality: Optional[str] = None
    profile: Optional[str] = None
    working_days: list[WorkingDay.DaysOfWeek]
    department_name: str

    @field_validator("profile")
    def validate_file(value):
        if value:
            return path.join(MEDIA_URL, value)
        return value

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "fullname": "Dr. John Doe",
                "speciality": "Cardiology",
                "profile": "/media/custom_user/dr-john-doe.jpg",
                "working_days": ["Monday", "Wednesday", "Friday"],
                "department_name": "Cardiology",
            }
        }


class DoctorDetails(BaseModel):
    class Speciality(BaseModel):
        name: str
        appointment_charges: float
        treatment_charges: float
        department_name: str

        class Config:
            json_schema_extra = {
                "example": {
                    "name": "Cardiology",
                    "appointment_charges": 100.0,
                    "treatment_charges": 150.0,
                    "department_name": "Cardiology",
                }
            }

    id: int
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    phone_number: Optional[str]
    working_days: list[WorkingDay.DaysOfWeek]
    shift: Doctor.WorkShift
    speciality: Speciality

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "phone_number": "+1234567890",
                "working_days": ["Monday", "Wednesday", "Friday"],
                "shift": "Night",
                "speciality": {
                    "name": "Cardiology",
                    "appointment_charges": 100.0,
                    "treatment_charges": 150.0,
                    "department_name": "Cardiology",
                },
            }
        }


class NewAppointmentWithDoctor(BaseModel):
    doctor_id: int
    appointment_datetime: FutureDatetime
    reason: str

    class Config:
        json_schema_extra = {
            "example": {
                "doctor_id": 1,
                "appointment_datetime": "2023-01-01T10:00:00",
                "reason": "Regular check-up",
            }
        }


class UpdateAppointmentWithDoctor(NewAppointmentWithDoctor):
    status: Optional[Appointment.AppointmentStatus] = None
    appointment_datetime: Optional[datetime] = None

    class Config:
        json_schema_extra = {
            "example": {
                "doctor_id": 1,
                "appointment_datetime": "2023-01-01T10:00:00",
                "reason": "Regular check-up",
                "status": "Scheduled",
            }
        }


class AppointmentDetails(UpdateAppointmentWithDoctor):
    appointment_charges: float
    created_at: datetime
    updated_at: datetime
    appointment_datetime: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "doctor_id": 1,
                "appointment_datetime": "2023-01-01T10:00:00",
                "reason": "Regular check-up",
                "status": "Scheduled",
                "appointment_charges": 100.0,
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-02T00:00:00",
            }
        }


class AvailableAppointmentWithDoctor(AppointmentDetails):
    id: int
    appointment_datetime: datetime
    feedbacks: list[CompleteFeedbackInfo]

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "doctor_id": 1,
                "appointment_datetime": "2023-01-01T10:00:00",
                "reason": "Regular check-up",
                "status": "Scheduled",
                "appointment_charges": 100.0,
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-02T00:00:00",
                "feedbacks": [
                    {
                        "id": 1,
                        "message": "Great service!",
                        "rate": "Excellent",
                        "created_at": "2023-01-01T00:00:00",
                        "updated_at": "2023-01-02T00:00:00",
                    }
                ],
            }
        }


class SpecialityInfo(BaseModel):
    name: str
    details: Optional[str] = None
    total_doctors: int

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Cardiology",
                "details": "Heart related treatments",
                "total_doctors": 10,
            }
        }


class DepartmentInfo(BaseModel):
    name: str
    details: Optional[str] = None
    specialities: list[SpecialityInfo]
    profile: Optional[str] = None
    created_at: datetime

    @field_validator("profile")
    def validate_file(value):
        if value:
            return path.join(MEDIA_URL, value)
        return value

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Cardiology Department",
                "details": "Department for heart related treatments",
                "specialities": [
                    {
                        "name": "Cardiology",
                        "details": "Heart related treatments",
                        "total_doctors": 10,
                    }
                ],
                "profile": "/media/department/cardiology-profile.jpg",
                "created_at": "2023-01-01T00:00:00",
            }
        }


class PaymentAccountDetails(BaseModel):
    name: str
    paybill_number: str
    account_number: str
    details: Optional[str]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "M-PESA",
                "paybill_number": "123456",
                "account_number": "78901234",
                "details": "Main hospital account",
            }
        }


class SendMPESAPopupTo(BaseModel):
    phone_number: str
    amount: int

    class Config:
        json_schema_extra = {
            "example": {"phone_number": "+1234567890", "amount": 100.0}
        }


class HospitalGallery(BaseModel):
    title: str
    details: str
    location_name: str
    video_link: Optional[HttpUrl] = Field(None, description="Youtube video link")
    picture: Optional[str] = None
    date: date

    @field_validator("picture")
    def validate_file(value):
        if value and not value.startswith("/"):
            return path.join(MEDIA_URL, value)
        return value

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Hospital Tour",
                "details": "A virtual tour of our hospital facilities.",
                "location_name": "Main Hospital",
                "video_link": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "picture": "/media/gallery/hospital-tour.jpg",
                "date": "2023-01-01",
            }
        }


class HospitalAbout(BaseModel):
    name: str
    short_name: str
    details: str
    slogan: str
    location_name: str
    latitude: float
    longitude: float
    founded_in: date
    founder_name: str
    mission: str
    vision: str
    email: Optional[str] = None
    facebook: Optional[str] = None
    twitter: Optional[str] = None
    linkedin: Optional[str] = None
    instagram: Optional[str] = None
    tiktok: Optional[str] = None
    youtube: Optional[str] = None
    logo: Optional[str] = None
    wallpaper: Optional[str] = None

    @field_validator("logo", "wallpaper")
    def validate_file(value):
        if value and not value.startswith("/"):
            return path.join(MEDIA_URL, value)
        return value

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Smart Hospital",
                "short_name": "SH",
                "details": "Welcome to our hospital. We are committed to providing the best healthcare services.",
                "slogan": "We treat but God heals.",
                "location_name": "Meru - Kenya",
                "latitude": 0.000000,
                "longitude": 0.000000,
                "founded_in": "2023-01-01",
                "founder_name": "GoK",
                "mission": "To provide quality healthcare services to all.",
                "vision": "To be the leading healthcare provider in the region.",
                "email": "admin@hospital.com",
                "facebook": "https://www.facebook.com/",
                "twitter": "https://www.x.com/",
                "linkedin": "https://www.linkedin.com/",
                "instagram": "https://www.instagram.com/",
                "tiktok": "https://www.tiktok.com/",
                "youtube": "https://www.youtube.com/",
                "logo": "/media/hospital/logo.png",
                "wallpaper": "/media/hospital/wallpaper.jpg",
            }
        }


class ShallowHospitalNews(BaseModel):
    id: int
    title: str
    category: News.NewsCategory
    summary: str
    cover_photo: Optional[str]
    created_at: datetime
    views: int

    @field_validator("cover_photo")
    def validate_cover_photo(value):
        if value and not value.startswith("/"):
            return path.join(MEDIA_URL, value)
        return value

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "New Wing Inauguration",
                "category": "Announcement",
                "summary": "We are excited to announce the inauguration of our new wing.",
                "cover_photo": "/media/news/new-wing.jpg",
                "created_at": "2023-01-01T00:00:00",
                "views": 100,
            }
        }


class HospitalNews(ShallowHospitalNews):
    content: str
    document: Optional[str] = None
    video_link: Optional[HttpUrl] = Field(None, description="Youtube video link")
    updated_at: datetime

    @field_validator("document")
    def validate_document(value):
        if value and not value.startswith("/"):
            return path.join(MEDIA_URL, value)
        return value

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "New Wing Inauguration",
                "category": "Announcement",
                "summary": "We are excited to announce the inauguration of our new wing.",
                "cover_photo": "/media/news/new-wing.jpg",
                "created_at": "2023-01-01T00:00:00",
                "views": 100,
                "content": "The new wing includes state-of-the-art facilities...",
                "document": "/media/news/new-wing-doc.pdf",
                "video_link": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "updated_at": "2023-01-02T00:00:00",
            }
        }
