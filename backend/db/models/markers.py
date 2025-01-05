from sqlalchemy import Column, Integer, String
from db.database import Base

class Marker(Base):
    __tablename__ = 'markers'
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    map_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    type = Column(String, nullable=False)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)
