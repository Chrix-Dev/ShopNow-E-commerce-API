from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate, UserLogin, UserResponse, Token
from utils.database import get_db
from utils.security import hash_password, verify_password, create_access_token
import config
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from utils.email_utils import create_email_verification_token, send_verification_email, verify_token

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/Register")
def Register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(
            status_code=404,
            detail="User already created!"
        )

    hashed_password = hash_password(user.password)
    db_user = User(
         email = user.email,
         hashed_password = hashed_password,
         is_verified = False
    )   
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    token = create_email_verification_token(user.email)
    send_verification_email(user.email, token)

    return {"message": "Check your email to verify your account"}

@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    email = verify_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_verified = True
    db.commit()

    return {"message": "Email verified successfully"}

@router.post("/token", response_model= Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session= Depends(get_db)):  #test 1 Test endpoint again
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password!",
        )
    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Verify your email first")
    
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub":user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}