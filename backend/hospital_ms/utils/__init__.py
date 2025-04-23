"""Provides common required functions and classes"""

import re
import requests
from os import path
from enum import Enum
from django.core.mail import send_mail
from django.utils import timezone
from datetime import datetime, timedelta
from hospital_ms import settings

headers = {"Accept": "*/*"}

url = "https://developer.safaricom.co.ke/api/v1/APIs/API/Simulate/MpesaExpressSimulate/"


def send_payment_push(phone_number: str, amount: int, account_reference: str):
    if settings.MPESA_AUTHORIZATION is None:
        return
    if re.match(r"(^07|^011)", phone_number):
        phone_number = int(phone_number)
    elif re.match(r"^\+254", phone_number):
        phone_number = int(phone_number[4:])
    else:
        raise ValueError(f"Invalid phone number.")

    phone_number = f"254{phone_number}"
    payload = {
        "token": settings.MPESA_TOKEN,
        "authorization": settings.MPESA_AUTHORIZATION,
        "BusinessShortCode": "174379",
        "password": settings.MPESA_PASSWORD,
        "timestamp": settings.MPESA_TIMESTAMP,  # "20250423102923",  # datetime.now().strftime("%Y%m%d%H%M%S")
        "TransactionType": "CustomerPayBillOnline",
        "amount": amount,
        "PartyA": "254708374149",
        "PartyB": "174379",
        "PhoneNumber": phone_number,
        "CallBackURL": "https://mydomain.com/path",
        "AccountReference": account_reference,
        "TransactionDesc": "Payment of X",
    }
    resp = requests.post(url=url, json=payload, headers=headers)
    resp.raise_for_status()


def generate_document_filepath(instance, filename: str) -> str:
    filename, extension = path.splitext(filename)
    return f"{instance.__class__.__name__.lower()}/{filename}_{instance.id or ''}{extension}"


def send_email(subject: str, message: str, recipient: str, html_message: str = None):
    if settings.EMAIL_HOST_PASSWORD is None:
        return
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[recipient],
        fail_silently=(settings.DEBUG == False),  # Silent in production
        html_message=html_message,
    )


def get_expiry_datetime(minutes: float = 30) -> datetime:
    return timezone.now() + timedelta(minutes=minutes)


class EnumWithChoices(Enum):

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
