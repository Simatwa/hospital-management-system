from fastapi import APIRouter, status, HTTPException, Depends, Query, Path
from fastapi.encoders import jsonable_encoder
from fastapi.security.oauth2 import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from users.models import CustomUser
from pharmacy.models import Medicine, Order
from pharmacy.exceptions import InsufficientBalanceError
from pydantic import PositiveInt

# from django.contrib.auth.hashers import check_password
from api.v1.utils import token_id, generate_token
from api.v1.models import (
    TokenAuth,
    Profile,
    Feedback,
    MedicineAvailable,
    MedicineOrder,
    ClientMedicineOrder,
)
import asyncio
from typing import Annotated

router = APIRouter(prefix="/v1", tags=["v1"])


v1_auth_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/token",
    description="Generated API authentication token",
)


async def get_user(token: Annotated[str, Depends(v1_auth_scheme)]) -> CustomUser:
    """Ensures token passed match the one set"""
    if token:
        try:
            if token.startswith(token_id):

                def fetch_user(token):
                    return CustomUser.objects.get(token=token)

                return await asyncio.to_thread(fetch_user, token)

        except CustomUser.DoesNotExist:
            pass

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing token",
        headers={"WWW-Authenticate": "Bearer"},
    )


@router.post("/token", name="User token")
def fetch_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> TokenAuth:
    """
    - `username` : User username
    - `password` : User password.
    """
    try:
        user = CustomUser.objects.get(
            username=form_data.username
        )  # Temporarily restrict to students only
        if user.check_password(form_data.password):
            if user.token is None:
                user.token = generate_token()
                user.save()
            return TokenAuth(
                access_token=user.token,
                token_type="bearer",
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password."
            )
    except CustomUser.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User does not exist.",
        )


@router.patch("/token", name="Generate new token")
def generate_new_token(user: Annotated[CustomUser, Depends(get_user)]) -> TokenAuth:
    user.token = generate_token()
    user.save()
    return TokenAuth(access_token=user.token)


@router.get("/profile", name="Profile information")
def profile_information(user: Annotated[CustomUser, Depends(get_user)]) -> Profile:
    user_data = jsonable_encoder(user)
    user_data["account_balance"] = user.account.balance
    return Profile(**user_data)


@router.get("/medicine", name="medicine available")
def medicine_available(
    name: Annotated[str, Query(description="Medicine name filter")] = None,
    category: Annotated[
        Medicine.MedicineCategory, Query(description="Medicine category filter")
    ] = None,
    short_name: Annotated[str, Query(description="Medicine abbreviated name")] = None,
    price: Annotated[PositiveInt, Query(description="Medicine price filter")] = None,
    limit: Annotated[
        PositiveInt, Query(description="Total medicines not to exceed", ge=1, le=100)
    ] = 100,
    offset: Annotated[int, Query(description="Medicine id to offset from")] = -1,
) -> list[MedicineAvailable]:
    query = Medicine.objects.order_by("-created_at")

    if name:
        query = query.filter(name__icontains=name)
    if category:
        query = query.filter(category__icontains=category.replace(" ", "_"))
    if short_name:
        query = query.filter(short_name__icontains=short_name)
    if price:
        query = query.filter(price__lt=price)
    if offset >= 0:
        query = query.filter(id__gt=offset)

    query = query.all()[:limit]

    return [MedicineAvailable(**jsonable_encoder(med)) for med in query]


@router.get("/medicine/{medicine_id}", name="Details about a particular medicine")
def get_specific_medicine_details(
    medicine_id: Annotated[int, Path(description="Specific medicine id")]
) -> MedicineAvailable:
    try:
        target_medicine = Medicine.objects.get(id=medicine_id)
        return MedicineAvailable(**jsonable_encoder(target_medicine))
    except Medicine.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Medicine with id {medicine_id} does not exist.",
        )


@router.post("/order/{medicine_id}", name="Place a medicine order")
def make_medicine_order(
    medicine_id: Annotated[int, Path(description="Medicine id")],
    client_medicine_order: ClientMedicineOrder,
    user: Annotated[CustomUser, Depends(get_user)],
) -> MedicineOrder:
    try:
        target_medicine = Medicine.objects.get(id=medicine_id)
        new_order = Order.objects.create(
            customer=user,
            medicine=target_medicine,
            quantity=client_medicine_order.quantity,
            prescription="--",
        )
        new_order.save()
        # order_response = jsonable_encoder(new_order)
        # order_response["medicine_name"] = new_order.medicine.name
        # This approach fails most times with error : RecursionError: maximum recursion depth exceeded
        # return MedicineOrder(**order_response)
        return MedicineOrder(
            id=new_order.id,
            medicine_name=new_order.medicine.name,
            quantity=new_order.quantity,
            prescription=new_order.prescription,
            total_price=new_order.total_price,
            status=new_order.status,
            updated_at=new_order.updated_at,
            created_at=new_order.created_at,
        )
    except Medicine.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Medicine with id {medicine_id} does not exist.",
        )
    except InsufficientBalanceError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                f"You do not have enough funds to place this order. "
                "Recharge your account and retry."
            ),
        )


@router.patch("/order/{order_id}", name="Edit an order")
def edit_an_order(
    order_id: Annotated[int, Path(description="Order id")],
    client_medicine_order: ClientMedicineOrder,
    user: Annotated[CustomUser, Depends(get_user)],
) -> MedicineOrder:
    try:
        target_order = Order.objects.get(id=order_id)
        if target_order.customer == user:
            target_order.quantity = client_medicine_order.quantity
            target_order.save()
            return MedicineOrder(
                id=target_order.id,
                medicine_name=target_order.medicine.name,
                quantity=target_order.quantity,
                prescription=target_order.prescription,
                total_price=target_order.total_price,
                status=target_order.status,
                updated_at=target_order.updated_at,
                created_at=target_order.created_at,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can make changes to your orders only.",
            )
    except Order.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with id {order_id} does not exist.",
        )


@router.delete("/order/{order_id}", name="Delete an order")
def delete_an_order(
    order_id: Annotated[int, Path(description="Order id")],
    user: Annotated[CustomUser, Depends(get_user)],
) -> Feedback:
    try:
        target_order = Order.objects.get(id=order_id)
        if target_order.customer == user:
            target_order.delete()
            return Feedback(detail="Order deleted successfully.")
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can delete your orders only.",
            )
    except Order.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with id {order_id} does not exist.",
        )


@router.get("/orders", name="Orders already placed")
def orders_placed(
    user: Annotated[CustomUser, Depends(get_user)]
) -> list[MedicineOrder]:
    # print(user.orders)
    orders_list = []
    for order in Order.objects.filter(customer=user).order_by("-created_at").all():
        order.medicine_name = order.medicine.name
        orders_list.append(MedicineOrder.model_validate(order))
    return orders_list
