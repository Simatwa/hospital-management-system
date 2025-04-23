from django.db import models
from hospital.utils import generate_document_filepath
from django.utils.translation import gettext_lazy as _
from enum import Enum
from datetime import datetime
from django.utils import timezone

# Create your models here.


class Department(models.Model):
    name = models.CharField(max_length=30, unique=True, help_text=_("Department name"))
    lead = models.OneToOneField(
        "users.CustomUser",
        on_delete=models.SET_NULL,
        help_text=_("Head of department"),
        null=True,
        blank=True,
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


class Doctor(models.Model):

    class WorkShift(Enum):
        DAY = "Day"
        NIGHT = "Night"

        @classmethod
        def choices(cls):
            return [(key.value, key.name) for key in cls]

    user = models.OneToOneField(
        "users.CustomUser",
        on_delete=models.CASCADE,
        help_text=_("The user associated with this doctor"),
    )
    speciality = models.ForeignKey(
        Speciality,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
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
