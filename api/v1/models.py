from pydantic import BaseModel, Field, field_validator, FutureDatetime
from typing import Optional, Any
from datetime import datetime, date
from hospital_ms.settings import MEDIA_URL
from users.models import CustomUser
from hospital.models import Treatment, WorkingDay, Doctor, Appointment
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
    detail: str = Field(description="Feedback in details")

    class Config:
        json_schema_extra = {
            "example": {"detail": "This is a detailed feedback message."}
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
    profile: Optional[Any] = None
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
        speciality_treatment_charges: float
        speciality_department_name: str

        class Config:
            json_schema_extra = {
                "example": {
                    "name": "Dr. Smith",
                    "speciality": "Cardiology",
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
                "updated_at": "2023-01-02T00:00:00",
            }
        }


class AvailableDoctor(BaseModel):
    id: int
    fullname: str
    speciality: str
    working_days: list[WorkingDay.DaysOfWeek]
    department_name: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "fullname": "Dr. John Doe",
                "speciality": "Cardiology",
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
    status: Appointment.AppointmentStatus
    appointment_datetime: datetime

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
    amount: float

    class Config:
        json_schema_extra = {
            "example": {"phone_number": "+1234567890", "amount": 100.0}
        }
