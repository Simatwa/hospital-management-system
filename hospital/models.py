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


class About(models.Model):
    name = models.CharField(
        max_length=40, help_text="The hospital name", default="Smart Hospital"
    )
    short_name = models.CharField(
        max_length=30, help_text="Hospital abbreviated name", default="SH"
    )
    slogan = models.TextField(
        help_text=_("Hospital's slogan"), default="We treat but God heals."
    )
    details = models.TextField(
        help_text=_("Hospital details"),
        default="Welcome to our hospital. We are committed to providing the best healthcare services.",
        null=False,
        blank=False,
    )
    location_name = models.CharField(
        max_length=200, help_text=_("Hospital location name(s)"), default="Meru - Kenya"
    )
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        default=0.000000,
        help_text=_("Latitude of the hospital location"),
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        default=0.000000,
        help_text=_("Longitude of the hospital location"),
    )
    founded_in = models.DateField(
        help_text=_("Date when the hospital was founded"), default=timezone.now
    )
    founder_name = models.CharField(
        max_length=50, help_text=_("Name of the hospital founder"), default="GoK"
    )
    mission = models.TextField(
        help_text=_("Hospital's mission statement"),
        default="To provide quality healthcare services to all.",
    )
    vision = models.TextField(
        help_text=_("Hospital's vision statement"),
        default="To be the leading healthcare provider in the region.",
    )
    email = models.EmailField(
        max_length=50,
        help_text="Website's admin email",
        null=True,
        blank=True,
        default="admin@hospital.com",
    )
    phone_number = models.CharField(
        max_length=50,
        help_text="Hospital's hotline number",
        null=True,
        blank=True,
        default="0200000000",
    )
    facebook = models.URLField(
        max_length=100,
        help_text=_("Hospital's Facebook profile link"),
        null=True,
        blank=True,
        default="https://www.facebook.com/",
    )
    twitter = models.URLField(
        max_length=100,
        help_text=_("Hospital's X (formerly Twitter) profile link"),
        null=True,
        blank=True,
        default="https://www.x.com/",
    )
    linkedin = models.URLField(
        max_length=100,
        help_text=_("Hospital's Facebook profile link"),
        null=True,
        blank=True,
        default="https://www.linkedin.com/",
    )
    instagram = models.URLField(
        max_length=100,
        help_text=_("Hospital's Instagram profile link"),
        null=True,
        blank=True,
        default="https://www.instagram.com/",
    )
    tiktok = models.URLField(
        max_length=100,
        help_text=_("Hospital's Tiktok profile link"),
        null=True,
        blank=True,
        default="https://www.tiktok.com/",
    )
    youtube = models.URLField(
        max_length=100,
        help_text=_("Hospital's Youtube profile link"),
        null=True,
        blank=True,
        default="https://www.youtube.com/",
    )
    logo = models.ImageField(
        help_text=_("Hospital logo  (preferrably 64*64px png)"),
        upload_to=generate_document_filepath,
        default="/static/hospital/img/logo.png",
    )
    wallpaper = models.ImageField(
        help_text=_("Hospital wallpaper image"),
        upload_to=generate_document_filepath,
        default="default/surgery-1822458_1920.jpg",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated At"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At"),
        help_text=_("The date and time when the treatment was created"),
    )

    def __str__(self):
        return self.name


class AccountDetails(models.Model):
    name = models.CharField(max_length=50, help_text=_("Account name e.g M-PESA"))
    paybill_number = models.CharField(
        max_length=100, help_text=_("Paybill number e.g 247247")
    )
    account_number = models.CharField(
        max_length=100,
        default="%(username)s",
        help_text=_(
            "Any or combination of %(id)d, %(username)s,%(phone_number)s, %(email)s etc"
        ),
    )
    is_active = models.BooleanField(default=True, help_text=_("Account active status"))
    details = models.TextField(
        null=True, blank=True, help_text=_("Information related to this department.")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated At"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At"),
        help_text=_("The date and time when the account was created"),
    )

    class Meta:
        verbose_name_plural = _("Account Details")


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
    profile = models.ImageField(
        upload_to=generate_document_filepath,
        default="default/medical-equipment-4099429_1920.jpg",
        verbose_name=_("Profile"),
        help_text=_("Department's profile picture"),
        blank=True,
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


class ExtraFee(models.Model):
    name = models.CharField(max_length=100, help_text=_("Fee name"))
    details = models.TextField(help_text=_("What is this fee for?"))
    amount = models.DecimalField(
        max_digits=8, decimal_places=2, help_text=_("Fee amount in Ksh")
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
        return f"{self.name} (Ksh.{self.amount})"


class ServiceFeedback(models.Model):
    class FeedbackRate(Enum):
        EXCELLENT = "Excellent"
        GOOD = "Good"
        AVERAGE = "Average"
        POOR = "Poor"
        TERRIBLE = "Terrible"

        @classmethod
        def choices(cls):
            return [(key.value, key.name) for key in cls]

    sender = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, help_text=_("Feedback sender")
    )
    message = models.TextField(help_text=_("Response body"))
    rate = models.CharField(
        max_length=15, choices=FeedbackRate.choices(), help_text=_("Feedback rating")
    )
    show_in_index = models.BooleanField(
        default=True,
        help_text=_("Display this feedback in website's feedback sections."),
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
        return f"{self.rate} feedback from {self.sender}"


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

    extra_fees = models.ManyToManyField(
        ExtraFee, help_text=_("Extra treatment fees"), related_name="treatments"
    )

    treatment_status = models.CharField(
        max_length=20,
        choices=TreatmentStatus.choices(),
        default=TreatmentStatus.INPROGRESS.value,
        help_text=_("Treatment status"),
    )
    feedbacks = models.ManyToManyField(
        ServiceFeedback,
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
    feedbacks = models.ManyToManyField(
        ServiceFeedback,
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


class Gallery(models.Model):
    title = models.CharField(max_length=50, help_text=_("Gallery title"))
    details = models.TextField(help_text=_("What about this gallery?"))
    location_name = models.CharField(
        max_length=100, help_text=_("Event location name"), default="Hospital"
    )
    picture = models.ImageField(
        help_text=_("Gallery photograph"),
        upload_to=generate_document_filepath,
        default="default/surgery-1822458_1920.jpg",
    )
    video_link = models.URLField(
        max_length=100, help_text=_("YouTube video link"), null=True, blank=True
    )
    date = models.DateField(help_text="Gallery date", default=timezone.now)
    show_in_index = models.BooleanField(
        default=True, help_text=_("Display this gallery in website's gallery section.")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated At"),
        help_text=_("The date and time when the gallery was last updated"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At"),
        help_text=_("The date and time when the gallery was created"),
    )

    def __str__(self):
        return f"{self.title} in {self.location_name} on {self.date}"

    class Meta:
        verbose_name_plural = _("Galleries")


class News(models.Model):
    class NewsCategory(Enum):
        GENERAL = "General"
        HEALTH = "Health"
        EVENTS = "Events"
        ANNOUNCEMENTS = "Announcements"

        @classmethod
        def choices(cls):
            return [(key.value, key.name) for key in cls]

    title = models.CharField(max_length=40, help_text=_("News title"))
    category = models.CharField(
        max_length=20,
        choices=NewsCategory.choices(),
        default=NewsCategory.GENERAL.value,
        help_text=_("Select the category of the news"),
    )
    content = models.TextField(help_text=_("News in detail"))
    summary = models.TextField(help_text=_("News in brief"))
    cover_photo = models.ImageField(
        help_text=_("News cover photo"),
        upload_to=generate_document_filepath,
        default="default/news-3584901_66059.jpg",
    )
    document = models.FileField(
        help_text=_("Any relevant file attached to the news"),
        upload_to=generate_document_filepath,
        null=True,
        blank=True,
    )
    video_link = models.URLField(
        max_length=100,
        help_text=_("Youtube video link relatint to the news"),
        null=True,
        blank=True,
    )
    is_published = models.BooleanField(default=True, help_text=_("Publish this news."))
    views = models.IntegerField(
        default=0, help_text=_("Number of times the news has been requested.")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated At"),
        help_text=_("The date and time when the news was last updated"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At"),
        help_text=_("The date and time when the news was created"),
    )

    class Meta:
        verbose_name_plural = _("News")

    def __str__(self):
        return f"'{self.title}' on {self.created_at.strftime('%d-%b-%Y %H:%M:%S')}"

    def save(self, *args, **kwargs):
        if not self.id:  # new entry
            # Consider mailing subscribers
            pass
        super().save(*args, **kwargs)


class Subscriber(models.Model):
    email = models.EmailField(help_text=_("Email address"), unique=True)
    token = models.UUIDField(help_text="Subscription confirmation token", unique=True)
    is_verified = models.BooleanField(default=False, help_text=_("Verification status"))

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated At"),
        help_text=_("The date and time when the gallery was last updated"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At"),
        help_text=_("The date and time when the gallery was created"),
    )

    def __str__(self):
        return self.email
