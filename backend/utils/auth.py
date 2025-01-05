
from db.models.user import User
from db.models.session import Session as SessionModel
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import datetime

def is_authenticated(token: str, session: Session) -> User:
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header missing")
    existing_session = session.query(SessionModel).filter_by(token=token).first()
    if not existing_session:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    if existing_session.expires < datetime.datetime.now():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    existing_user = session.query(User).filter_by(id=existing_session.user_id).first()
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return existing_user

def get_bearer_token_from_header(header: str) -> str:
    return header.replace("Bearer ", "") if header else None
