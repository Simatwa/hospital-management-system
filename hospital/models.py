from django.db import models
from users.models import CustomUser
from django.utils.translation import gettext_lazy as _
from enum import Enum
from os import path

# Create your models here.


def generate_document_filepath(instance: "Medicine", filename: str) -> str:
    filename, extension = path.splitext(filename)
    return f"{instance.__class__.__name__.lower()}/{filename}_{instance.id}{extension}"


class WorkingDay(models.Model):
    name = models.CharField(max_length=30, unique=True, help_text=_("Weekday name"))
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
        Department, on_delete=models.CASCADE, help_text=_("Department name")
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
            return [(key.name, key.value) for key in cls]

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

    class WorkShifts(Enum):
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
    specialty = models.ForeignKey(
        Speciality, on_delete=models.RESTRICT, help_text=_("The doctor's specialty")
    )
    working_days = models.ManyToManyField(WorkingDay, help_text=_("Working days"))
    shift = models.CharField(max_length=40, choices=WorkShifts.choices())
    salary = models.DecimalField(
        max_digits=8, decimal_places=2, help_text=_("Salary in Ksh")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At"),
    )

    def __str__(self):
        return str(self.user)


class Patient(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        help_text=_("The user associated with this patient"),
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
        Medicine, on_delete=models.RESTRICT, help_text=_("Medicine given")
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

    def __str__(self):
        return f"{self.medicine} - {self.quantity}"


class Treatment(models.Model):
    class PatientType(Enum):
        OUTPATIENT = "Outpatient"
        INPATIENT = "Inpatient"

        @classmethod
        def choices(cls):
            return [(key.value, key.name) for key in cls]

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        help_text=_("The patient under treatment"),
        related_name="treatments",
    )
    type = models.CharField(
        max_length=20,
        choices=PatientType.choices(),
        default=PatientType.OUTPATIENT.value,
        help_text=_("Select whether the patient is an outpatient or inpatient"),
    )
    doctor = models.ManyToManyField(
        Doctor, help_text="Doctors who administered treatment"
    )
    diagnosis = models.CharField(
        max_length=255, help_text=_("The diagnosis of the patient")
    )
    medicines = models.ManyToManyField(
        TreatmentMedicine, help_text=_("Treatment medicines")
    )
    details = models.TextField(help_text=_("The treatment given to the patient"))
    is_complete = models.BooleanField(
        default=False, help_text="Treatment completement status"
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

    def __str__(self):
        return f"{self.patient} - {self.diagnosis} on {self.created_at.strftime("%d-%b-%Y %H:%M:%S")}"


class Appointment(models.Model):
    class Status(Enum):
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
    )
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, help_text=_("The doctor for this appointment")
    )
    appointment_date = models.DateTimeField(
        help_text=_("The date and time of the appointment")
    )
    reason = models.TextField(help_text=_("The reason for the appointment"))
    status = models.CharField(
        max_length=20,
        choices=Status.choices(),
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

    def __str__(self):
        return f"{self.patient} with {self.doctor} on {self.appointment_date}"
