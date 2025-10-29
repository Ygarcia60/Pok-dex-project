import requests
from app.database import SessionLocal, engine, Base
from app import models

# Ensure the database tables are created
Base.metadata.create_all(bind=engine)
db = SessionLocal()

def fetch_pokemon_data(pokemon_id):
    """Fetch data for a single Pokémon from the PokéAPI."""
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"⚠️ Failed to fetch Pokémon #{pokemon_id}")
        return None

    data = response.json()
    
    # Extract Pokémon info
    name = data["name"]
    # ✅ Ensure we store primary type only (as string, not list)
    type_ = data["types"][0]["type"]["name"] if data["types"] else "unknown"
    region = "Kanto"
    sprite_url = data["sprites"]["front_default"]

    return {
        "name": name,
        "type_": type_,
        "region": region,
        "sprite_url": sprite_url,
    }

def seed_pokemon(limit=50):
    """Populate database with first N Pokémon"""
    print(f"🌟 Seeding the first {limit} Pokémon...")
    for i in range(1, limit + 1):
        pokemon_data = fetch_pokemon_data(i)
        if pokemon_data:
            existing = db.query(models.Pokemon).filter_by(name=pokemon_data["name"]).first()
            if existing:
                print(f"🔹 Skipping {pokemon_data['name']} (already exists)")
                continue

            new_pokemon = models.Pokemon(**pokemon_data)
            db.add(new_pokemon)
            db.commit()
            print(f"✅ Added {pokemon_data['name']} ({pokemon_data['type_']})")
    db.close()
    print("🎉 Seeding complete!")

if __name__ == "__main__":
    seed_pokemon(50)


