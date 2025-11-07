from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from utils.database import get_db
from models.user import User
from utils.security import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")

def get_current_user(token: str = Depends(oauth2_scheme), db:  Session = Depends(get_db)):
    token_data = verify_token(token)
    user = db.query(User).filter(User.email == token_data.email).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User does not exist",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user

def get_current_admin(current_user: User = Depends(get_current_user)):
    if current_user.is_admin != 1:
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return current_user