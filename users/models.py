from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from uuid import uuid4
from os import path
from django.core.validators import FileExtensionValidator
from enum import Enum

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

    class Role(Enum):
        PATIENT = "Patient"
        DOCTOR = "Doctor"
        ADMIN = "Admin"

        @classmethod
        def choices(cls):
            return [(key.name, key.value) for key in cls]

    gender = models.CharField(
        verbose_name=_("gender"),
        max_length=10,
        help_text=_("Select one"),
        choices=(
            ["M", "Male"],
            ["F", "Female"],
            ["O", "Other"],
        ),
        blank=True,
        default="O",
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
        choices=Role.choices(),
        default=Role.PATIENT.value,
        help_text=_("Role of the user in the system"),
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
        verbose_name=_("Customer"),
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
