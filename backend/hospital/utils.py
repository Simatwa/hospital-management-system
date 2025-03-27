import re
import requests
import datetime
from os import path
from hospital_ms import settings

headers = {"Accept": "*/*"}

url = "https://developer.safaricom.co.ke/api/v1/APIs/API/Simulate/MpesaExpressSimulate/"


def send_payment_push(phone_number: str, amount: int, account_reference: str):
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
        "timestamp": "20250326114804",  # datetime.datetime.now().strftime("%Y%m%d%H%M%S")
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


if __name__ == "__main__":
    send_payment_push("0748981989", 100, "developer")
