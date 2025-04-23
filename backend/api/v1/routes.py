from fastapi import APIRouter, status, HTTPException, Depends, Query, Path, Form
from fastapi.encoders import jsonable_encoder
from fastapi.security.oauth2 import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from users.models import CustomUser
from hospital.models import (
    Patient,
    Treatment,
    Appointment,
)
from staffing.models import Doctor, Speciality, Department
from finance.models import Account

from external.models import Gallery, About, News, Subscriber, ServiceFeedback

from hospital.utils import send_payment_push

# from django.contrib.auth.hashers import check_password
from django.db import IntegrityError
from api.v1.utils import token_id, generate_token, get_day_and_shift
from api.v1.models import (
    TokenAuth,
    Profile,
    Feedback,
    PatientTreatment,
    ShallowPatientTreatment,
    EditablePersonalData,
    AvailableDoctor,
    DoctorDetails,
    NewAppointmentWithDoctor,
    UpdateAppointmentWithDoctor,
    AvailableAppointmentWithDoctor,
    DepartmentInfo,
    SpecialityInfo,
    PaymentAccountDetails,
    SendMPESAPopupTo,
    HospitalGallery,
    HospitalAbout,
    ShallowHospitalNews,
    HospitalNews,
    UserFeedback,
    NewFeedbackInfo,
    UpdateFeedbackInfo,
    CompleteFeedbackInfo,
)
from pydantic import PositiveInt, EmailStr
from uuid import uuid4

import asyncio
from typing import Annotated
from datetime import datetime

router = APIRouter(prefix="/v1", tags=["v1"])


v1_auth_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/token",
    description="Generated API authentication token",
)


async def get_patient(token: Annotated[str, Depends(v1_auth_scheme)]) -> Patient:
    """Ensures token passed match the one set"""
    if token:
        try:
            if token.startswith(token_id):

                def fetch_user(token) -> Patient:
                    user = CustomUser.objects.get(token=token)
                    try:
                        return user.patient
                    except CustomUser.patient.RelatedObjectDoesNotExist:
                        new_patient = Patient.objects.create(user=user)
                        new_patient.save()
                        return new_patient

                return await asyncio.to_thread(fetch_user, token)

        except CustomUser.DoesNotExist:
            pass

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing token",
        headers={"WWW-Authenticate": "Bearer"},
    )


@router.post("/token", name="User token")
def fetch_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> TokenAuth:
    """
    - `username` : User username
    - `password` : User password.
    """
    try:
        user = CustomUser.objects.get(
            username=form_data.username
        )  # Temporarily restrict to students only
        if user.check_password(form_data.password):
            if user.token is None:
                user.token = generate_token()
                user.save()
            return TokenAuth(
                access_token=user.token,
                token_type="bearer",
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password."
            )
    except CustomUser.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User does not exist.",
        )


@router.patch("/token", name="Generate new token")
def generate_new_token(patient: Annotated[Patient, Depends(get_patient)]) -> TokenAuth:
    patient.user.token = generate_token()
    patient.user.save()
    return TokenAuth(access_token=patient.user.token)


@router.get("/profile", name="Profile information")
def profile_information(patient: Annotated[Patient, Depends(get_patient)]) -> Profile:
    user = patient.user
    return Profile(
        first_name=user.first_name,
        last_name=user.last_name,
        phone_number=user.phone_number,
        email=user.email,
        location=user.location,
        bio=user.bio,
        username=user.username,
        date_of_birth=user.date_of_birth,
        gender=user.gender,
        account_balance=user.account.balance,
        profile=user.profile.name,
        is_staff=user.is_staff,
        date_joined=user.date_joined,
    )


@router.patch("/profile", name="Update profile")
def update_personal_info(
    patient: Annotated[Patient, Depends(get_patient)],
    updated_personal_data: EditablePersonalData,
) -> EditablePersonalData:
    user = patient.user
    user.first_name = updated_personal_data.first_name or user.first_name
    user.last_name = updated_personal_data.last_name or user.last_name
    user.phone_number = updated_personal_data.phone_number or user.phone_number
    user.email = updated_personal_data.email or user.email
    user.location = updated_personal_data.location or user.location
    user.bio = updated_personal_data.bio or user.bio
    user.save()
    return EditablePersonalData(
        first_name=user.first_name,
        last_name=user.last_name,
        phone_number=user.phone_number,
        email=user.email,
        location=user.location,
        bio=user.bio,
    )


@router.get("/user/exists", name="Check if username exists")
def check_if_username_exists(
    username: Annotated[str, Query(description="Username to check against")]
) -> Feedback:
    """Checks if account with a particular username exists
    - Useful when setting username at account creation
    """
    try:
        CustomUser.objects.get(username=username)
        return Feedback(detail=True)
    except CustomUser.DoesNotExist:
        return Feedback(detail=False)


@router.get("/about", name="Details about hospital")
def get_hospital_details() -> HospitalAbout:
    return HospitalAbout(**jsonable_encoder(About.objects.all().first()))


@router.get("/galleries", name="Hospital galleries")
def get_hospital_galleries() -> list[HospitalGallery]:
    return [
        HospitalGallery(**jsonable_encoder(gallery))
        for gallery in Gallery.objects.filter(show_in_index=True)
        .all()
        .order_by("-created_at")[:30]
    ]


@router.get("/news", name="News published")
def get_published_news() -> list[ShallowHospitalNews]:
    return [
        HospitalNews(**jsonable_encoder(news))
        for news in News.objects.filter(is_published=True).order_by("-created_at")
    ]


@router.get("/news/{id}", name="News in detail")
def get_published_news_details(
    id: Annotated[int, Path(description="News ID")]
) -> HospitalNews:
    try:
        target_news = News.objects.get(pk=id, is_published=True)
        target_news_dict = jsonable_encoder(target_news)
        target_news.views += 1
        target_news_dict["views"] += 1
        target_news.save()
        return HospitalNews(**target_news_dict)
    except News.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"News with id {id} does not exist.",
        )


@router.post("/subscribe", name="Add subscription")
def add_subscription(
    email: Annotated[EmailStr, Form(description="Email address")]
) -> Feedback:
    try:
        new_subscriber = Subscriber.objects.create(
            email=email,
            token=uuid4(),
        )
        new_subscriber.save()
        # TODO: Send confirmation link to email
        return Feedback(detail="Check your email inbox to confirm subscription.")
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A subscription with this email already exists.",
        )


@router.get("/feedbacks", name="Get user's feedbacks")
def get_users_feedbacks() -> list[UserFeedback]:
    feedback_list = []
    for feedback in (
        ServiceFeedback.objects.filter(show_in_index=True).all().order_by("-created_at")
    ):
        user_feedback = jsonable_encoder(feedback)
        user_feedback["user"] = jsonable_encoder(feedback.sender)
        feedback_list.append(user_feedback)
    return feedback_list


@router.get("/specialities", name="Specialities available")
def get_available_specialities() -> list[str]:
    return [speciality.name for speciality in Speciality.objects.all()]


@router.get("/departments", name="Departments available")
def get_available_departments() -> list[DepartmentInfo]:
    department_list = []
    for department in Department.objects.all().order_by("-created_at"):
        department_list.append(
            DepartmentInfo(
                name=department.name,
                details=department.details,
                specialities=[
                    SpecialityInfo(
                        name=speciality.name,
                        details=speciality.details,
                        total_doctors=speciality.doctors.count(),
                    )
                    for speciality in department.specialities.all()
                ],
                profile=department.profile.name,
                created_at=department.created_at,
            )
        )
    return department_list


@router.get("/doctors", name="Doctors available")
def get_doctors_available(
    at: Annotated[datetime, Query(description="Particular time filter")] = None,
    speciality_name: Annotated[str, Query(description="Doctor speciality name")] = None,
    limit: Annotated[
        PositiveInt, Query(description="Doctors amount not to exceed", gt=0, le=100)
    ] = 100,
    offset: Annotated[
        int, Query(description="Return doctors whose IDs are greater than this")
    ] = -1,
) -> list[AvailableDoctor]:
    if at:
        day_of_week, work_shift = get_day_and_shift(at)
        doctors = Doctor.objects.filter(
            working_days__name=day_of_week,
            shift=work_shift,
            id__gt=offset,
            speciality__isnull=False,
        )
    else:
        doctors = Doctor.objects.filter(
            id__gt=offset,
            speciality__isnull=False,
        )
    if speciality_name:
        doctors = doctors.filter(
            speciality__name=speciality_name,
            speciality__isnull=False,
        )
    available_doctors_list: list[AvailableDoctor] = []
    for doctor in doctors[:limit]:
        available_doctors_list.append(
            AvailableDoctor(
                id=doctor.id,
                fullname=doctor.user.get_full_name(),
                speciality=doctor.speciality.name,
                profile=doctor.user.profile.name,
                working_days=[
                    day.name
                    for day in doctor.working_days.all().order_by("-created_at")
                ],
                department_name=doctor.speciality.department.name,
            )
        )
    return available_doctors_list


@router.get("/doctor/{id}", name="Details of specific doctor")
def get_specific_doctor_details(
    id: Annotated[int, Path(description="Doctor ID")]
) -> DoctorDetails:
    try:
        target_doctor = Doctor.objects.get(id=id)
        user = target_doctor.user
        speciality = target_doctor.speciality
        return DoctorDetails(
            id=target_doctor.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            phone_number=user.phone_number,
            working_days=[
                day.name
                for day in target_doctor.working_days.all().order_by("-created_at")
            ],
            shift=target_doctor.shift,
            speciality=DoctorDetails.Speciality(
                name=speciality.name,
                appointment_charges=speciality.appointment_charges,
                treatment_charges=speciality.treatment_charges,
                department_name=speciality.department.name,
            ),
        )
    except Doctor.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            details=f"Doctor with id {id} does not exist.",
        )


@router.get("/treatments", name="Treatments ever administered")
def get_treatments_ever_administered(
    patient: Annotated[Patient, Depends(get_patient)],
    treatment_status: Annotated[
        Treatment.TreatmentStatus, Query(description="Treatment status")
    ] = None,
    patient_type: Annotated[
        Treatment.PatientType, Query(description="Either Outpatient or Inpatient")
    ] = None,
    limit: Annotated[
        PositiveInt, Query(description="Treatments amount not to exceed", gt=0, le=100)
    ] = 100,
    offset: Annotated[
        int, Query(description="Return treatments whose IDs are greater than this")
    ] = -1,
) -> list[ShallowPatientTreatment]:

    treatment_list = []
    query_filter = dict(patient=patient, id__gt=offset)
    if treatment_status:
        query_filter["treatment_status"] = treatment_status.value
    if patient_type:
        query_filter["patient_type"] = patient_type.value
    for treatment in (
        Treatment.objects.filter(**query_filter).all().order_by("-created_at")[:limit]
    ):
        treatment_dict = jsonable_encoder(treatment)
        treatment_dict["total_bill"] = treatment.total_bill
        treatment_list.append(ShallowPatientTreatment(**treatment_dict))
    return treatment_list


@router.get("/treatment/{id}", name="Get specific treatment details")
def get_specific_treatment_details(
    patient: Annotated[Patient, Depends(get_patient)],
    id: Annotated[int, Path(description="Treatment ID")],
) -> PatientTreatment:
    try:
        treatment = Treatment.objects.get(pk=id)
        if treatment.patient == patient:
            treatment_dict: dict = jsonable_encoder(treatment)
            treatment_dict.update(
                dict(
                    total_medicine_bill=treatment.total_medicine_bill,
                    total_treatment_bill=treatment.total_treatment_bill,
                    total_bill=treatment.total_bill,
                )
            )
            treatment_dict["medicines_given"] = [
                PatientTreatment.TreatmentMedicine(
                    medicine_name=treatment_medicine.medicine.name,
                    quantity=treatment_medicine.quantity,
                    prescription=treatment_medicine.prescription,
                    price_per_medicine=treatment_medicine.medicine.price,
                    medicine_bill=treatment_medicine.bill,
                )
                for treatment_medicine in treatment.medicines.all().order_by(
                    "-created_at"
                )
            ]

            treatment_dict["doctors_involved"] = [
                PatientTreatment.DoctorInvolved(
                    name=doctor.user.get_full_name(),
                    speciality=doctor.speciality.name,
                    profile=doctor.user.profile.name,
                    speciality_treatment_charges=doctor.speciality.treatment_charges,
                    speciality_department_name=doctor.speciality.department.name,
                )
                for doctor in treatment.doctors.all().order_by("-created_at")
            ]
            treatment_dict["extra_fees"] = [
                PatientTreatment.ExtraFees(
                    name=fee.name, details=fee.details, amount=fee.amount
                )
                for fee in treatment.extra_fees.all()
            ]
            treatment_dict["feedbacks"] = [
                CompleteFeedbackInfo(**jsonable_encoder(feedback))
                for feedback in treatment.feedbacks.all().order_by("-created_at")
            ]
            return PatientTreatment(**treatment_dict)
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only access your own treatment details.",
            )
    except Treatment.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Treatment with id {id} does not exist.",
        )


@router.post("/treatment/{id}/feedback", name="Add treatment feedback")
def add_treatment_feedback(
    patient: Annotated[Patient, Depends(get_patient)],
    id: Annotated[int, Path(description="Treatment ID")],
    new_feedback: NewFeedbackInfo,
) -> CompleteFeedbackInfo:
    try:
        target_treatment = Treatment.objects.get(pk=id, patient=patient)
        new_feedback = ServiceFeedback(
            sender=patient.user,
            message=new_feedback.message,
            rate=new_feedback.rate.value,
        )
        new_feedback.save()
        target_treatment.feedbacks.add(new_feedback)
        target_treatment.save()
        return CompleteFeedbackInfo.from_model(new_feedback)
    except Treatment.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Treatment with id {id} does not exist.",
        )


@router.patch("/feedback/{id}", name="Update service feedback")
def update_service_feedback(
    patient: Annotated[Patient, Depends(get_patient)],
    id: Annotated[int, Path(description="Feedback ID")],
    updated_feedback: UpdateFeedbackInfo,
) -> CompleteFeedbackInfo:
    try:
        target_feedback = ServiceFeedback.objects.get(pk=id, sender=patient.user)
        target_feedback.message = updated_feedback.message or target_feedback.message
        target_feedback.rate = updated_feedback.rate.value or target_feedback.rate
        target_feedback.save()
        return CompleteFeedbackInfo.from_model(target_feedback)
    except ServiceFeedback.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Service feedback with id {id} does not exist.",
        )


@router.delete("/feedback/{id}", name="Delete service feedback")
def delete_service_feedbak(
    patient: Annotated[Patient, Depends(get_patient)],
    id: Annotated[int, Path(description="Feedback ID")],
) -> Feedback:
    try:
        target_feedback = ServiceFeedback.objects.get(pk=id, sender=patient.user)
        target_feedback.delete(keep_parents=True)
        return Feedback(detail="Feedback deleted successfully")
    except ServiceFeedback.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Service feedback with id {id} does not exist.",
        )


@router.get("/appointments", name="Get appointments ever set")
def get_appointments_ever_set(
    patient: Annotated[Patient, Depends(get_patient)],
    status: Annotated[
        Appointment.AppointmentStatus, Query(description="Appointment status")
    ] = None,
    limit: Annotated[
        PositiveInt,
        Query(description="Appointments amount not to exceed", gt=0, le=100),
    ] = 100,
    offset: Annotated[
        int, Query(description="Return appointments whose IDs are greater than this")
    ] = -1,
) -> list[AvailableAppointmentWithDoctor]:
    query_filters: dict[str, str] = dict(patient=patient, id__gt=offset)
    if status:
        query_filters["status"] = status.value
    appointments = (
        Appointment.objects.filter(**query_filters)
        .all()
        .order_by("-created_at")[:limit]
    )
    return [
        AvailableAppointmentWithDoctor(
            doctor_id=appointment.doctor.id,
            appointment_datetime=appointment.appointment_datetime,
            reason=appointment.reason,
            id=appointment.id,
            appointment_charges=appointment.doctor.speciality.appointment_charges,
            status=appointment.status,
            created_at=appointment.created_at,
            updated_at=appointment.updated_at,
            feedbacks=[
                CompleteFeedbackInfo(**jsonable_encoder(feedback))
                for feedback in appointment.feedbacks.all()
            ],
        )
        for appointment in appointments
    ]


@router.post("/appointment", name="Set new appointment")
def set_new_appointment(
    patient: Annotated[Patient, Depends(get_patient)],
    new_appointment: NewAppointmentWithDoctor,
) -> AvailableAppointmentWithDoctor:
    try:
        target_doctor = Doctor.objects.get(pk=new_appointment.doctor_id)
        if target_doctor.is_working_time(new_appointment.appointment_datetime):
            if target_doctor.accepts_appointment_on(
                new_appointment.appointment_datetime
            ):

                appointment = Appointment.objects.create(
                    patient=patient,
                    doctor=target_doctor,
                    appointment_datetime=new_appointment.appointment_datetime,
                    reason=new_appointment.reason,
                )
                appointment.save()
                return AvailableAppointmentWithDoctor(
                    doctor_id=appointment.doctor.id,
                    appointment_datetime=appointment.appointment_datetime,
                    reason=appointment.reason,
                    id=appointment.id,
                    appointment_charges=appointment.doctor.speciality.appointment_charges,
                    status=appointment.status,
                    created_at=appointment.created_at,
                    updated_at=appointment.updated_at,
                    feedbacks=[
                        CompleteFeedbackInfo(**jsonable_encoder(feedback))
                        for feedback in appointment.feedbacks.all()
                    ],
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(
                        "Doctor has reached the maximum number of appointments for the given date ."
                        "Try other dates."
                    ),
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Doctor is not available at the given time. " "Try other times."
                ),
            )
    except Doctor.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Doctor with id {new_appointment.doctor_id} does not exist.",
        )


@router.patch("/appointment/{id}", name="Update existing appointment")
def update_existing_appointment(
    patient: Annotated[Patient, Depends(get_patient)],
    id: Annotated[int, Path(description="Appointment ID")],
    updated_appointment: UpdateAppointmentWithDoctor,
) -> AvailableAppointmentWithDoctor:
    try:
        appointment = Appointment.objects.get(pk=id, patient=patient)
        target_doctor = Doctor.objects.get(
            pk=(updated_appointment.doctor_id or appointment.doctor.id)
        )
        if updated_appointment.appointment_datetime:
            if not target_doctor.is_working_time(
                updated_appointment.appointment_datetime
            ):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(
                        "Doctor is not available at the given time. " "Try other times."
                    ),
                )
            if not target_doctor.accepts_appointment_on(
                updated_appointment.appointment_datetime
            ):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(
                        "Doctor has reached the maximum number of appointments for the given date. "
                        "Try other dates."
                    ),
                )
        appointment.doctor = target_doctor
        appointment.appointment_datetime = (
            updated_appointment.appointment_datetime or appointment.appointment_datetime
        )
        appointment.reason = updated_appointment.reason or appointment.reason
        appointment.status = updated_appointment.status or appointment.status
        appointment.save()
        return AvailableAppointmentWithDoctor(
            doctor_id=appointment.doctor.id,
            appointment_datetime=appointment.appointment_datetime,
            reason=appointment.reason,
            id=appointment.id,
            appointment_charges=(
                appointment.doctor.speciality.appointment_charges
                if appointment.status != appointment.AppointmentStatus.CANCELLED
                else 0
            ),
            status=appointment.status,
            created_at=appointment.created_at,
            updated_at=appointment.updated_at,
            feedbacks=[
                CompleteFeedbackInfo(**jsonable_encoder(feedback))
                for feedback in appointment.feedbacks.all()
            ],
        )
    except Appointment.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Appointment with id {id} does not exist.",
        )
    except Doctor.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Doctor with id {updated_appointment.doctor_id} does not exist.",
        )


@router.delete("/appointment/{id}", name="Delete an appointment")
def delete_appointment(
    patient: Annotated[Patient, Depends(get_patient)],
    id: Annotated[int, Path(description="Appointment ID")],
) -> Feedback:
    try:
        appointment = Appointment.objects.get(pk=id, patient=patient)
        appointment.delete()
        return Feedback(**{"detail": "Appointment deleted successfully."})
    except Appointment.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Appointment with id {id} does not exist.",
        )


@router.post("/appointment/{id}/feedback", name="Add appointment feedback")
def add_appointment_feedback(
    patient: Annotated[Patient, Depends(get_patient)],
    id: Annotated[int, Path(description="Appointment ID")],
    new_feedback: NewFeedbackInfo,
) -> CompleteFeedbackInfo:
    try:
        target_appointment = Appointment.objects.get(pk=id, patient=patient)
        new_feedback = ServiceFeedback(
            sender=patient.user,
            message=new_feedback.message,
            rate=new_feedback.rate.value,
        )
        new_feedback.save()
        target_appointment.feedbacks.add(new_feedback)
        target_appointment.save()
        return CompleteFeedbackInfo.from_model(new_feedback)
    except Appointment.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Appointment with id {id} does not exist.",
        )


@router.get("/payment-account-details", name="Payment account details")
def get_payment_account_details(
    patient: Annotated[Patient, Depends(get_patient)]
) -> list[PaymentAccountDetails]:
    return [
        PaymentAccountDetails(
            name=account.name,
            paybill_number=account.paybill_number,
            account_number=account.account_number
            % dict(
                id=patient.user.id,
                username=patient.user.username,
                phone_number=patient.user.phone_number,
                email=patient.user.email,
            ),
            details=account.details,
        )
        for account in Account.objects.filter(is_active=True).all()
    ]


@router.post("/send-mpesa-payment-popup", name="Send mpesa payment popup")
def send_mpesa_popup_to(
    patient: Annotated[Patient, Depends(get_patient)], popup_to: SendMPESAPopupTo
) -> Feedback:
    def send_popup(phone_number, amount):
        """TODO: Request payment using Daraja API"""
        mpesa_details = Account.objects.filter(name__icontains="m-pesa").first()
        assert mpesa_details is not None, "M-PESA account details not found"
        account_number = mpesa_details.account_number % dict(
            id=patient.user.id,
            username=patient.user.username,
            phone_number=patient.user.phone_number,
            email=patient.user.email,
        )
        send_payment_push(
            phone_number=popup_to.phone_number,
            amount=popup_to.amount,
            account_reference=account_number,
        )
        # Push send successfully let's SIMULATE account debitting
        # TODO: Implement a real account debition.
        patient.user.account.balance += amount
        patient.user.account.save()

    send_popup(popup_to.phone_number, popup_to.amount)
    return Feedback(detail="M-pesa popup sent successfully.")
