# app/main.py
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.database import Base, engine
from app.routes import pokemon, cards

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Pokédex API")
# ✅ Allow frontend (localhost:5173) to access backend (localhost:8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # your React app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ✅ Register the router
app.include_router(pokemon.router)
app.include_router(cards.router)
print("✅ Pokemon router loaded successfully")



@app.get("/")
def read_root():
    return RedirectResponse(url="/docs")

print("✅ Pokemon router loaded:", app.routes)


