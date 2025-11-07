from fastapi import APIRouter, Depends
from utils.paystack_service import initialize_payment, verify_payment
from utils.dependencies import get_current_user

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("/initialize")
def paystack_initialize(email: str, amount: int, user=Depends(get_current_user)):
    return initialize_payment(email, amount, product_name="order_payment")

@router.get("/verify/{reference}")
def paystack_verify(reference: str, user=Depends(get_current_user)):
    return verify_payment(reference)