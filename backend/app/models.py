from sqlalchemy import Column, Integer, String
from app.database import Base

class Pokemon(Base):
    __tablename__ = "pokemon"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    type_ = Column(String, nullable=False)
    region = Column(String)
    sprite_url = Column(String) # New field for sprite URL
