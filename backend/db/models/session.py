from sqlalchemy import Column, Integer, String, DateTime
from db.database import Base

class Session(Base):
    __tablename__ = 'sessions'
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    user_id = Column(Integer, nullable=False)
    token = Column(String, nullable=False)
    expires = Column(DateTime, nullable=False)
