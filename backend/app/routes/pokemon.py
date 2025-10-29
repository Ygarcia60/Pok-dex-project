from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import SessionLocal
from pydantic import BaseModel, Field
from typing import List

router = APIRouter(prefix="/pokemon", tags=["Pokemon"])

# Pydantic schema
class PokemonCreate(BaseModel):
    id: int
    name: str
    type: str = Field(..., alias="type_")
    region: str
    sprite_url: str  # ✅ include this field

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


# DB session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# GET endpoint
@router.get("/", response_model=list[schemas.PokemonBase])
def get_pokemon(db: Session = Depends(get_db)):
    return db.query(models.Pokemon).all()

# POST endpoint using JSON
@router.post("/")
def add_pokemon(pokemon: PokemonCreate, db: Session = Depends(get_db)):
    new_pokemon = models.Pokemon(name=pokemon.name,type_=pokemon.type,region=pokemon.region)
    db.add(new_pokemon)
    db.commit()
    db.refresh(new_pokemon)
    return new_pokemon
