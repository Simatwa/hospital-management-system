from pydantic import (
    BaseModel,
    Field,
    PositiveInt,
    field_validator,
    PositiveFloat,
)
from typing import Optional, Any
from datetime import datetime
from hospital_ms.settings import MEDIA_URL
from hospital.models import Medicine, Order
from os import path


class TokenAuth(BaseModel):
    """
    - `access_token` : Token value.
    - `token_type` : bearer
    """

    access_token: str
    token_type: Optional[str] = "bearer"

    model_config = {
        "json_schema_extras": {
            "example": {
                "access_token": "pms_27b9d79erc245r44b9rba2crd2273b5cbb71",
                "token_type": "bearer",
            }
        }
    }


class Feedback(BaseModel):
    detail: str = Field(description="Feedback in details")

    model_config = {
        "json_schema_extra": {
            "example": {"detail": "This is a detailed feedback message."}
        }
    }


class Profile(BaseModel):
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    location: Optional[str] = None
    account_balance: float
    profile: Optional[Any] = None
    is_staff: Optional[bool] = False

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "johndoe",
                "first_name": "John",
                "last_name": "Doe",
                "email": "johndoe@example.com",
                "location": "Nairobi",
                "account_balance": 1200.15,
                "profile": "/media/profiles/johndoe.jpg",
                "is_staff": False,
            }
        }
    }

    @field_validator("profile")
    def validate_file(value):
        if value:
            return path.join(MEDIA_URL, value)
        return value


class MedicineAvailable(BaseModel):
    id: int
    name: str
    short_name: str | None = None
    category: Medicine.MedicineCategory | str
    description: str
    price: PositiveFloat
    stock: PositiveInt
    picture: str
    updated_at: datetime

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "Aspirin",
                "short_name": "ASP",
                "category": "Pain Relief",
                "description": "Used to reduce pain, fever, or inflammation.",
                "price": 5.99,
                "stock": 100,
                "picture": "/media/medicines/aspirin.jpg",
                "updated_at": "2023-10-01T12:00:00",
            }
        }
    }

    @field_validator("picture")
    def validate_file(value):
        if value:
            return path.join(MEDIA_URL, value)
        return value


class ClientMedicineOrder(BaseModel):
    quantity: PositiveInt

    model_config = {
        "json_schema_extra": {
            "example": {
                "quantity": 2,
            }
        }
    }


class MedicineOrder(BaseModel):
    id: int
    medicine_name: str
    quantity: PositiveInt
    prescription: str | None = None
    total_price: PositiveFloat
    status: Order.OrderStatus | str
    updated_at: datetime
    created_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "medicine_name": "Paracetamol",
                "quantity": 2,
                "prescription": "/media/prescriptions/prescription1.jpg",
                "total_price": 19.99,
                "status": "pending",
                "updated_at": "2023-10-01T12:00:00",
                "created_at": "2023-09-30T12:00:00",
            }
        }
        from_attributes = True
