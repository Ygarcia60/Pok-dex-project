# app/routes/cards.py
# app/routes/cards.py
import requests
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/cards", tags=["Cards"])

@router.get("/{pokemon_name}")
def get_top_cards(pokemon_name: str):
    """
    Fetch top 5 most valuable Pokémon cards for the given Pokémon name
    using the Pokémon TCG API.
    """
    # Normalize tricky names
    pokemon_name = pokemon_name.replace("♀", "f").replace("♂", "m").replace("’", "")

    url = f"https://api.pokemontcg.io/v2/cards?q=name:*{pokemon_name}*&orderBy=-set.releaseDate"
    response = requests.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch data from TCG API")

    data = response.json()

    if "data" not in data or not data["data"]:
        # Try lowercase fallback
        alt_url = f"https://api.pokemontcg.io/v2/cards?q=name:*{pokemon_name.lower()}*"
        alt_response = requests.get(alt_url)
        alt_data = alt_response.json()
        if "data" not in alt_data or not alt_data["data"]:
            raise HTTPException(status_code=404, detail=f"No cards found for {pokemon_name}")
        cards = alt_data["data"]
    else:
        cards = data["data"]

    # Sort cards by highest market price if available
    def get_card_price(card):
        prices = card.get("tcgplayer", {}).get("prices", {})
        # Check multiple possible print types
        for variant in ["holofoil", "normal", "reverseHolofoil", "1stEditionHolofoil"]:
            if variant in prices:
                return prices[variant].get("market", 0)
        return 0

    # Sort cards by descending market price
    cards.sort(key=get_card_price, reverse=True)

    # Take top 5
    top_cards = cards[:5]

    # Build clean response
    result = []
    for card in top_cards:
        tcg_prices = card.get("tcgplayer", {}).get("prices", {})
        market_price = None
        for variant in ["holofoil", "normal", "reverseHolofoil", "1stEditionHolofoil"]:
            if variant in tcg_prices:
                market_price = tcg_prices[variant].get("market")
                break

        result.append({
            "name": card.get("name", "Unknown"),
            "set": card.get("set", {}).get("name", "Unknown Set"),
            "rarity": card.get("rarity", "Unknown"),
            "image": card.get("images", {}).get("small", ""),
            "price": round(market_price, 2) if market_price else None,
        })

    return result

