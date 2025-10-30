# app/routes/cards.py
import requests
from fastapi import APIRouter, HTTPException
from app.database import SessionLocal
from app import models

router = APIRouter(prefix="/cards", tags=["Cards"])

@router.get("/{pokemon_name}")
def get_top_cards(pokemon_name: str):
    """
    Fetch top 5 most valuable Pokémon cards for the given Pokémon name.
    Cache them in the local database after first fetch.
    """
    db = SessionLocal()
    pokemon_name = pokemon_name.capitalize().replace("♀", "f").replace("♂", "m").replace("’", "")

    # 1️⃣ Check if cards already cached
    cached_cards = db.query(models.Card).filter(models.Card.pokemon_name == pokemon_name).all()
    if cached_cards:
        print(f"🗂️ Returning cached cards for {pokemon_name}")
        return [
            {
                "name": c.name,
                "set": c.set,
                "rarity": c.rarity,
                "image": c.image,
                "price": c.price,
            }
            for c in cached_cards
        ]

    print(f"🌐 Fetching cards for {pokemon_name} from API...")
    url = f"https://api.pokemontcg.io/v2/cards?q=name:*{pokemon_name}*&orderBy=-set.releaseDate"
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch data from TCG API")

    data = response.json()
    cards = data.get("data", [])

    if not cards:
        # fallback lowercase
        alt_url = f"https://api.pokemontcg.io/v2/cards?q=name:*{pokemon_name.lower()}*"
        alt_response = requests.get(alt_url)
        cards = alt_response.json().get("data", [])
        if not cards:
            raise HTTPException(status_code=404, detail=f"No cards found for {pokemon_name}")

    def get_card_price(card):
        """Safely extract a market price, returning 0 if unavalible"""
        prices = card.get("tcgplayer", {}).get("prices", {})
        for variant in ["holofoil", "normal", "reverseHolofoil", "1stEditionHolofoil"]:
            if variant in prices and prices[variant].get("market") is not None:
                return prices[variant]["market"]
        return 0

    cards.sort(key=lambda c: get_card_price(c) or 0, reverse=True)
    top_cards = cards[:5]

    results = []
    for card in top_cards:
        tcg_prices = card.get("tcgplayer", {}).get("prices", {})
        market_price = None
        for variant in ["holofoil", "normal", "reverseHolofoil", "1stEditionHolofoil"]:
            if variant in tcg_prices:
                market_price = tcg_prices[variant].get("market")
                break

        card_data = {
            "name": card.get("name", "Unknown"),
            "set": card.get("set", {}).get("name", "Unknown Set"),
            "rarity": card.get("rarity", "Unknown"),
            "image": card.get("images", {}).get("small", ""),
            "price": round(market_price, 2) if market_price else None,
        }

        results.append(card_data)

        # 2️⃣ Cache the card
        db_card = models.Card(
            pokemon_name=pokemon_name,
            name=card_data["name"],
            set=card_data["set"],
            rarity=card_data["rarity"],
            image=card_data["image"],
            price=card_data["price"],
        )
        db.add(db_card)

    db.commit()
    db.close()

    print(f"✅ Cached {len(results)} cards for {pokemon_name}")
    return results
