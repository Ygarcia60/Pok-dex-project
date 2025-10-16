from fastapi import FastAPI
from app.routes import pokemon
from app.database import Base, engine

#Create database tables
Base.metadata.create_all(bind=engine)
app = FastAPI(title = "Pokedex API")

#Include pokemone routes
app.include_router(pokemon.router)
