from django.db import models
from users.models import CustomUser
from django.utils.translation import gettext_lazy as _
from enum import Enum
from hospital.exceptions import InsufficientMedicineStockError
from django.db.models import Sum
from datetime import datetime
from django.utils import timezone
from hospital.utils import generate_document_filepath

# Create your models here.


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
        help_text=_("Photo of the medicine"),
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
        "staffing.Doctor",
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

    extra_fees = models.ManyToManyField(
        "finance.ExtraFee",
        help_text=_("Extra treatment fees"),
        related_name="treatments",
    )

    treatment_status = models.CharField(
        max_length=20,
        choices=TreatmentStatus.choices(),
        default=TreatmentStatus.INPROGRESS.value,
        help_text=_("Treatment status"),
    )
    feedbacks = models.ManyToManyField(
        "external.ServiceFeedback",
        help_text=_("Treatment service feedback"),
        related_name="treatments",
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
            self.doctors.aggregate(
                total_charges=Sum("speciality__treatment_charges")
            ).get("total_charges", 0)
            or 0
        )

    @property
    def total_extra_fees_bill(self) -> float:
        return (
            self.extra_fees.aggregate(total_fees=Sum("amount")).get("total_fees", 0)
            or 0
        )

    @property
    def total_bill(self) -> float:
        return (
            self.total_medicine_bill
            + self.total_treatment_bill
            + self.total_extra_fees_bill
        )

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
        "staffing.Doctor",
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
    feedbacks = models.ManyToManyField(
        "external.ServiceFeedback",
        help_text=_("Appointment service feedback"),
        related_name="appointments",
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

    def delete(self, *args, **kwargs):
        if self.status != self.AppointmentStatus.COMPLETED.value:
            # Debit user account
            self.patient.user.account.balance += (
                self.doctor.speciality.appointment_charges
            )
            self.patient.user.account.save()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.patient} with {self.doctor} on {self.appointment_datetime.strftime("%d-%b-%Y %H:%M:%S")}"
