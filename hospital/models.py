from django.db import models
from users.models import CustomUser
from django.utils.translation import gettext_lazy as _
from enum import Enum
from os import path
from hospital.exceptions import InsufficientMedicineStockError
from django.db.models import Sum
from datetime import datetime
from django.utils import timezone

# Create your models here.


def generate_document_filepath(instance: "Medicine", filename: str) -> str:
    filename, extension = path.splitext(filename)
    return f"{instance.__class__.__name__.lower()}/{filename}_{instance.id}{extension}"


class WorkingDay(models.Model):
    class DaysOfWeek(Enum):
        MONDAY = "Monday"
        TUESDAY = "Tuesday"
        WEDNESDAY = "Wednesday"
        THURSDAY = "Thursday"
        FRIDAY = "Friday"
        SATURDAY = "Saturday"
        SUNDAY = "Sunday"

        @classmethod
        def choices(cls):
            return [(key.value, key.name) for key in cls]

    name = models.CharField(
        max_length=30,
        choices=DaysOfWeek.choices(),
        unique=True,
        help_text=_("Weekday name"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At"),
        help_text=_("The date and time when the treatment was created"),
    )

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=30, unique=True, help_text=_("Department name"))
    lead = models.OneToOneField(
        CustomUser, on_delete=models.RESTRICT, help_text=_("Head of department")
    )
    details = models.TextField(
        null=True, blank=True, help_text=_("Information related to this department.")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At"),
        help_text=_("The date and time when the treatment was created"),
    )

    def __str__(self):
        return self.name


class Speciality(models.Model):
    name = models.CharField(max_length=50, unique=True, help_text=_("Specality name"))
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        help_text=_("Department name"),
        related_name="specialities",
    )
    details = models.TextField(
        null=True, blank=True, help_text=_("Information related to this speciality.")
    )
    appointment_charges = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
        help_text=_("Appointment charges in Ksh"),
    )
    treatment_charges = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
        help_text=_("Treatment charges in Ksh"),
    )
    appointments_limit = models.IntegerField(
        default=20, help_text="Daily appointments limit"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated At"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At"),
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Specialities"


class Medicine(models.Model):

    class MedicineCategory(str, Enum):
        ANTIBIOTICS = "Antibiotics"
        PAIN_RELIEF = "Pain Relief"
        FIRST_AID = "First Aid"
        VITAMINS = "Vitamins"
        SUPPLEMENTS = "Supplements"
        COUGH_SYRUP = "Cough Syrup"
        OTHER = "Other"

        @classmethod
        def choices(cls):
            return [(key.value, key.name) for key in cls]

    name = models.CharField(
        max_length=255,
        verbose_name=_("Medicine Name"),
        help_text=_("Full name of the medicine"),
        unique=True,
    )
    short_name = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name=_("Abbreviated name"),
        help_text=_("Abbreviated name for the medicine"),
        unique=True,
    )
    category = models.CharField(
        max_length=50,
        choices=MedicineCategory.choices(),
        verbose_name=_("Category"),
        default=MedicineCategory.OTHER.value,
        help_text=_("Select the category of the medicine"),
    )
    description = models.TextField(
        verbose_name=_("Description"),
        help_text=_("Provide a detailed description of the medicine"),
    )
    expiry_date = models.DateField(help_text=_("Expiration date"))
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Price in Ksh"),
        help_text=_("Enter the price of the medicine in Kenyan Shillings"),
    )
    stock = models.PositiveIntegerField(
        verbose_name=_("Stock Level"),
        help_text=_("Enter the current stock level of the medicine"),
    )
    picture = models.ImageField(
        upload_to=generate_document_filepath,
        default="default/ai-generated-medicine.jpg",
        verbose_name=_("Photo of the medicine"),
        help_text=_("Upload a photo of the medicine"),
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At"),
        help_text=_("The date and time when the medicine was created"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated At"),
        help_text=_("The date and time when the medicine was last updated"),
    )

    def __str__(self):
        return self.name


class Doctor(models.Model):

    class WorkShift(Enum):
        DAY = "Day"
        NIGHT = "Night"

        @classmethod
        def choices(cls):
            return [(key.value, key.name) for key in cls]

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        help_text=_("The user associated with this doctor"),
    )
    speciality = models.ForeignKey(
        Speciality,
        on_delete=models.RESTRICT,
        help_text=_("The doctor's speciality"),
        related_name="doctors",
    )
    working_days = models.ManyToManyField(
        WorkingDay, help_text=_("Working days"), related_name="doctors"
    )
    shift = models.CharField(
        max_length=40, choices=WorkShift.choices(), default=WorkShift.DAY.value
    )
    salary = models.DecimalField(
        max_digits=8, decimal_places=2, help_text=_("Salary in Ksh")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At"),
    )

    def is_working_time(self, time: datetime) -> bool:
        """Checks if doctor will be available at a given time

        Args:
            time (datetime): Time to check against

        Raises:
            ValueError: Inacse time is not an instance of `datetime`

        Returns:
            bool: Doctor's working status
        """
        if not isinstance(time, datetime):
            raise ValueError(
                f"Time needs to be an instance of " f"{datetime} not {type(time)}"
            )
        day_of_week: str = time.strftime("%A")
        current_shift: str = (
            self.WorkShift.DAY.value
            if 6 <= time.hour < 18
            else self.WorkShift.NIGHT.value
        )
        return (
            self.working_days.filter(name=day_of_week).exists()
            and self.shift == current_shift
        )

    @property
    def is_working_now(self) -> bool:
        return self.is_working_time(timezone.now())

    def accepts_appointment_on(self, time: datetime) -> bool:
        return (
            self.appointments.filter(appointment_datetime__date=time.date()).count()
            < self.speciality.appointments_limit
        )

    def __str__(self):
        return str(self.user)


class Patient(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        help_text=_("The user associated with this patient"),
        related_name="patient",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At"),
        help_text=_("The date and time when the treatment was created"),
    )

    def __str__(self):
        return str(self.user)


class TreatmentMedicine(models.Model):
    medicine = models.ForeignKey(
        Medicine,
        on_delete=models.RESTRICT,
        help_text=_("Medicine given"),
        related_name="treament_medicine",
    )
    quantity = models.IntegerField(help_text=_("Medicine amount"))
    prescription = models.TextField(help_text=_("Medicine prescription"))
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated At"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At"),
    )

    @property
    def bill(self) -> float:
        return self.medicine.price * self.quantity

    def __str__(self):
        return f"{self.medicine} - {self.quantity}"

    def save(self, *args, **kwargs):
        if self.medicine.stock < self.quantity:
            raise InsufficientMedicineStockError(
                f"There is only {self.medicine.stock} units of {self.medicine} remaining "
                f"as opposed to the required {self.quantity} units"
            )
        # Consider changes etc
        self.medicine.stock -= self.quantity
        self.medicine.save()
        super().save(*args, **kwargs)


class Treatment(models.Model):
    class PatientType(Enum):
        OUTPATIENT = "Outpatient"
        INPATIENT = "Inpatient"

        @classmethod
        def choices(cls):
            return [(key.value, key.name) for key in cls]

    class TreatmentStatus(Enum):
        INPROGRESS = "Inprogress"
        HEALED = "Healed"
        REFERRED = "Referred"

        @classmethod
        def choices(cls):
            return [(key.value, key.name) for key in cls]

    patient: Patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        help_text=_("The patient under treatment"),
        related_name="treatments",
    )
    patient_type = models.CharField(
        max_length=20,
        choices=PatientType.choices(),
        default=PatientType.OUTPATIENT.value,
        help_text=_("Select whether the patient is an outpatient or inpatient"),
    )
    doctors = models.ManyToManyField(
        Doctor,
        help_text="Doctors who administered treatment",
        related_name="treatments",
    )
    diagnosis = models.CharField(
        max_length=255, help_text=_("The diagnosis of the patient")
    )
    medicines = models.ManyToManyField(
        TreatmentMedicine,
        help_text=_("Treatment medicines"),
        related_name="treatments",
    )
    details = models.TextField(help_text=_("The treatment given to the patient"))

    treatment_status = models.CharField(
        max_length=20,
        choices=TreatmentStatus.choices(),
        default=TreatmentStatus.INPROGRESS.value,
        help_text=_("Treatment status"),
    )
    bill_settled = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        help_text=_("Amount of bill paid so far"),
        default=0,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated At"),
        help_text=_("The date and time when the treatment was last updated"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At"),
        help_text=_("The date and time when the treatment was created"),
    )

    @property
    def total_medicine_bill(self) -> float:
        treatment_bill = 0
        for treatment_medicine in self.medicines.all():
            treatment_bill += (
                treatment_medicine.medicine.price * treatment_medicine.quantity
            )
        return treatment_bill

    @property
    def total_treatment_bill(self) -> float:
        return (
            self.doctors.aggregate(total_charges=Sum("speciality__treatment_charges"))[
                "total_charges"
            ]
            or 0
        )

    @property
    def total_bill(self) -> float:
        return self.total_medicine_bill + self.total_treatment_bill

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        total_bill = self.total_bill
        if self.bill_settled != total_bill:
            # deduct from user account
            payable_amount = total_bill - self.bill_settled
            self.patient.user.account.balance -= payable_amount
            self.bill_settled = total_bill
            self.patient.user.account.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.patient} - {self.diagnosis} on {self.created_at.strftime("%d-%b-%Y %H:%M:%S") if self.created_at else "now"}"


class Appointment(models.Model):
    class AppointmentStatus(Enum):
        SCHEDULED = "Scheduled"
        COMPLETED = "Completed"
        CANCELLED = "Cancelled"

        @classmethod
        def choices(cls):
            return [(key.value, key.name) for key in cls]

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        help_text=_("The patient for this appointment"),
        related_name="appointments",
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        help_text=_("The doctor for this appointment"),
        related_name="appointments",
    )
    appointment_datetime = models.DateTimeField(
        help_text=_("The date and time of the appointment")
    )
    reason = models.TextField(help_text=_("The reason for the appointment"))
    status = models.CharField(
        max_length=20,
        choices=AppointmentStatus.choices(),
        default=AppointmentStatus.SCHEDULED.value,
        help_text=_("Select appointment status"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated At"),
        help_text=_("The date and time when the appointment was last updated"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At"),
        help_text=_("The date and time when the appointment was created"),
    )

    def save(self, *args, **kwargs):
        if not self.id:
            # New entry
            # Credit user account
            self.patient.user.account.balance -= (
                self.doctor.speciality.appointment_charges
            )
            self.patient.user.account.save()
        elif self.status == self.AppointmentStatus.CANCELLED.value:
            # Debit user account
            self.patient.user.account.balance += (
                self.doctor.speciality.appointment_charges
            )
            self.patient.user.account.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.patient} with {self.doctor} on {self.appointment_datetime.strftime("%d-%b-%Y %H:%M:%S")}"
