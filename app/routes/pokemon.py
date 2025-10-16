from fastapi import APIRouter, HTTPException
from app.database import SessionLocal
from app.models import Pokemon

router = APIRouter(prefix=" /pokemon", tags=["Pokemon"])

@router.get("/")
def get_all_pokemon():
    db = SessionLocal()
    pokemon = db.query(Pokemon).all()
    db.close()
    return pokemon

@router.get("/")
def get_pokemon(name: str):
    db = SessionLocal()
    p = db.query(Pokemon).filter(Pokemon.name.ilike(name)).first()
    db.close()
    if not p:
        raise HTTPException(status_code=404, detail="Pokemon not found")
    return p
