from sqlalchemy import Column, Integer, String
from db.database import Base

class Map(Base):
    __tablename__ = 'maps'
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    author_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    img_url = Column(String, nullable=False, unique=True)
    imgWidth = Column(Integer, nullable=False)
    imgHeight = Column(Integer, nullable=False)
