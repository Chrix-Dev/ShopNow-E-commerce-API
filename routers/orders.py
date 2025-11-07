from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.order import Order
from models.cart import CartItem
from schemas.order import OrderResponse
from utils.database import get_db
from utils.dependencies import get_current_user

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=OrderResponse)
def checkout(db: Session = Depends(get_db), user=Depends(get_current_user)):
    cart_items = db.query(CartItem).filter_by(user_id=user.id).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")
    total = sum(item.quantity * item.product.price for item in cart_items)
    order = Order(user_id=user.id, total_amount=total)
    db.add(order)
    db.query(CartItem).filter_by(user_id=user.id).delete()
    db.commit()
    db.refresh(order)
    return order