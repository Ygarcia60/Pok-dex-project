from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.database import Base

class Pokemon(Base):
    __tablename__ = "pokemon"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    type_ = Column(String, nullable=False)
    region = Column(String)
    sprite_url = Column(String) # New field for sprite URL

class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    pokemon_name = Column(String, index=True)
    name = Column(String)
    set = Column(String)
    rarity = Column(String)
    image = Column(String)
    price = Column(Float) 
