from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.cart import CartItem
from models.product import Product
from schemas.cart import CartItemCreate, CartItemResponse
from utils.database import get_db
from utils.dependencies import get_current_user

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.post("/", response_model=CartItemResponse)
def add_to_cart(item: CartItemCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    product = db.query(Product).filter(Product.id == item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.stock < item.quantity:
        raise HTTPException(status_code=400, detail="Insufficient Stock")
    existing_item = db.query(CartItem).filter_by(user_id=user.id, product_id=item.product_id).first()
    if existing_item:
        existing_item.quantity += item.quantity
        db.commit()
        db.refresh(existing_item)
        return existing_item
    cart_item = CartItem(user_id=user.id, product_id=item.product_id, quantity=item.quantity)
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return cart_item    

@router.get("/", response_model=list[CartItemResponse])
def view_cart(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(CartItem).filter_by(user_id=user.id).all()

@router.delete("/{item_id}")
def remove_cart_item(item_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    item = db.query(CartItem).filter_by(user_id=user.id, id=item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return{"detail": "Item removed"}