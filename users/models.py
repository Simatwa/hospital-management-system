from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from uuid import uuid4
from os import path
from django.core.validators import FileExtensionValidator
from enum import Enum
from datetime import datetime
from django.core.validators import RegexValidator

# Create your models here.


def generate_profile_filepath(instance: "CustomUser", filename: str) -> str:
    custom_filename = str(uuid4()) + path.splitext(filename)[1]
    return f"user_profile/{instance.id}{custom_filename}"


class Account(models.Model):
    balance = models.DecimalField(
        max_digits=8, decimal_places=2, help_text=_("Account balance"), default=0
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated At"),
        help_text=_("The date and time when the account was last updated"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At"),
        help_text=_("The date and time when the aaccount was created"),
    )

    def __str__(self):
        return str(self.balance)


class CustomUser(AbstractUser):
    """Both indiduals and organizations"""

    class UserRole(Enum):
        PATIENT = "Patient"
        DOCTOR = "Doctor"
        ADMIN = "Admin"

        @classmethod
        def choices(cls):
            return [(key.value, key.name) for key in cls]

    class UserGender(Enum):
        MALE = "M"
        FEMALE = "F"
        OTHER = "O"

        @classmethod
        def choices(cls) -> list[tuple]:
            return [(key.value, key.name) for key in cls]

    gender = models.CharField(
        verbose_name=_("gender"),
        max_length=10,
        help_text=_("Select one"),
        choices=UserGender.choices(),
        default=UserGender.OTHER.value,
    )
    date_of_birth = models.DateField(
        default=datetime(year=2000, month=1, day=1), help_text=_("Date of birth")
    )

    phone_number = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r"^\+?1?\d{9,15}$",
                message=_(
                    "Phone number must be entered in the format: '+254...' or '07...'. Up to 15 digits allowed."
                ),
            )
        ],
        help_text=_("Contact phone number"),
        blank=True,
        null=True,
    )

    location = models.CharField(
        max_length=50, help_text=_("Current location address"), null=True, blank=True
    )

    profile = models.ImageField(
        _("Profile Picture"),
        default="default/user.png",
        upload_to=generate_profile_filepath,
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"])],
        blank=True,
        null=True,
    )

    role = models.CharField(
        max_length=10,
        choices=UserRole.choices(),
        default=UserRole.PATIENT.value,
        help_text=_("Role of the user in the system"),
    )

    bio = models.TextField(
        null=True, blank=True, help_text=_("Relevant user information.")
    )

    token = models.CharField(
        _("token"),
        help_text=_("Token for validation"),
        null=True,
        blank=True,
        max_length=40,
        unique=True,
    )

    account = models.OneToOneField(
        Account,
        on_delete=models.RESTRICT,
        help_text=_("Finance account"),
        related_name="user",
    )

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def save(self, *args, **kwargs):
        if not self.id:  # new entry
            # self.set_password(self.password)
            new_account = Account.objects.create()
            new_account.save()
            self.account = new_account
        super().save(*args, **kwargs)

    def age(self):
        today = datetime.today().date()
        return (
            today.year
            - self.date_of_birth.year
            - (
                (today.month, today.day)
                < (self.date_of_birth.month, self.date_of_birth.day)
            )
        )

    def __str__(self):
        return self.username


class Payment(models.Model):
    class PaymentMethod(str, Enum):
        CASH = "Cash"
        MPESA = "m-pesa"
        BANK = "Bank"
        OTHER = "Other"

        @classmethod
        def choices(cls):
            return [(key.name, key.value) for key in cls]

    user = models.ForeignKey(
        CustomUser,
        verbose_name=_("Patient"),
        on_delete=models.CASCADE,
        help_text=_("User account to deposit to."),
        related_name="payments",
    )

    amount = models.DecimalField(
        max_digits=10, decimal_places=2, help_text=_("Transaction amount in Ksh")
    )
    method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices(),
        default=PaymentMethod.MPESA.value,
        help_text=_("Select means of payment"),
    )
    reference = models.CharField(
        max_length=100, help_text=_("Transaction ID or -- for cash.")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At"),
        help_text=_("The date and time when the order was created"),
    )

    def __str__(self):
        return f"Amount Ksh.{self.amount} via {self.method} (Ref: {self.reference})"

    def save(self, *args, **kwargs):
        if self.id:
            raise Exception("Payments cannot be edited")
        self.user.account.balance += self.amount
        self.user.account.save()
        super().save(*args, **kwargs)
