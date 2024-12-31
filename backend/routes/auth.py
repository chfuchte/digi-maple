from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Response

from db.models.user import User
from schemas.auth import UserLogin, UserCreate
from db.database import get_session

router = APIRouter()

@router.get("/auth/whoami")
def whoami(session: Session = Depends(get_session)):
    # TODO
    # 1. get token from cookie
    # 2. get user from token
    # 3. return user data
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)

@router.post("/auth/login")
def login(user: UserLogin, session: Session = Depends(get_session)):
    # TODO
    # 1. check if user exists
    # 2. check if password is correct
    # 3. create token
    # 4. return token
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)

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
