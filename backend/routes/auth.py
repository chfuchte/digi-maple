import datetime
import secrets
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Header
from db.models.user import User
from db.models.session import Session as SessionModel
from schemas.auth import UserLogin, UserCreate
from db.database import get_session
from utils.auth import is_authenticated, get_bearer_token_from_header

router = APIRouter()

@router.get("/auth/whoami")
def whoami(authorization: str = Header(default=None), session: Session = Depends(get_session)):
    token = get_bearer_token_from_header(authorization)
    user = is_authenticated(token, session)
    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name
    }

@router.post("/auth/logout")
def logout(authorization: str = Header(default=None), session: Session = Depends(get_session)):
    token = get_bearer_token_from_header(authorization)
    existing_session = session.query(SessionModel).filter_by(token=token).first()
    if not existing_session:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    session.delete(existing_session)
    session.commit()
    return {"detail": "Logged out successfully"}

############################################
# Login and Register
## No need to check authentication here
############################################

@router.post("/auth/login")
def login(user: UserLogin, session: Session = Depends(get_session)):
    existing_user = session.query(User).filter_by(email=user.email).first()
    if not existing_user or existing_user.password != user.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Credentials")
    session_token = secrets.token_hex(32)
    expires = datetime.datetime.now() + datetime.timedelta(days=1)
    new_session = SessionModel(user_id=existing_user.id, token=session_token, expires=expires)
    session.add(new_session)
    session.commit()
    session.refresh(new_session)
    return {"access_token": session_token, "token_type": "Bearer"}

@router.post("/auth/register")
def register(user: UserCreate, session: Session = Depends(get_session)):
    existing_user = session.query(User).filter_by(email=user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="E-Mail already taken")
    
    new_user = User(email=user.email, full_name=user.full_name, password=user.password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {"detail": "User registered successfully"}
