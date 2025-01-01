import datetime
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie
import secrets

from db.models.user import User
from db.models.session import Session as SessionModel
from schemas.auth import UserLogin, UserCreate
from db.database import get_session

router = APIRouter()

@router.get("/auth/whoami")
def whoami(token: str = Cookie(default=None), session: Session = Depends(get_session)):
    existing_session = session.query(SessionModel).filter_by(token=token).first()
    if not existing_session:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    existing_user = session.query(User).filter_by(id=existing_session.user_id).first()
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    return Response(
        status_code=status.HTTP_200_OK, 
        content=f"""
        {{
            "id": {existing_user.id},
            "email": "{existing_user.email}",
            "full_name": "{existing_user.full_name}"
        }}
        """
    )

@router.post("/auth/login")
def login(user: UserLogin, session: Session = Depends(get_session)):
    existing_user = session.query(User).filter_by(email=user.email).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="Invalid Credentials")
    
    if not existing_user.password == user.password:
        raise HTTPException(status_code=404, detail="Invalid Credentials")
    
    session_token = secrets.token_hex(32)
    expires = datetime.datetime.now() + datetime.timedelta(days=1)
    new_session = SessionModel(user_id=existing_user.id, token=session_token, expires=expires)
    session.add(new_session)
    session.commit()
    session.refresh(new_session)

    response = Response(status_code=status.HTTP_200_OK)
    response.set_cookie("token", session_token, httponly=True)
    return response

@router.post("/auth/logout")
def logout(token: str = Cookie(default=None), session: Session = Depends(get_session)):
    existing_session = session.query(SessionModel).filter_by(token=token).first()
    if not existing_session:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    session.delete(existing_session)
    session.commit()

    response = Response(status_code=status.HTTP_200_OK)
    response.delete_cookie("token")
    return response

@router.post("/auth/register")
def register(user: UserCreate, session: Session = Depends(get_session)):
    existing_user = session.query(User).filter_by(email=user.email).first()
    if existing_user:
        raise HTTPException(status_code=404, detail="E-Mail already taken")
    
    new_user = User(email=user.email, full_name=user.full_name, password=user.password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return Response(status_code=status.HTTP_200_OK)
