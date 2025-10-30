import { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [pokemon, setPokemon] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedPokemon, setSelectedPokemon] = useState(null);
  const [cards, setCards] = useState([]);
  const [loadingCards, setLoadingCards] = useState(false);


  useEffect(() => {
    axios
      .get("http://localhost:8000/pokemon/")
      .then((res) => {
        setPokemon(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching Pokémon:", err);
        setLoading(false);
      });
  }, []);

  const fetchPokemonCards = async (pokemonName) => {
    setLoadingCards(true);
    try{
      const res = await axios.get(`http://localhost:8000/cards/${pokemonName}`);
      setCards(res.data);
    } catch (err) {
      console.error("Error fetching Pokémon cards:", err);
      setCards([]);
    }
    setLoadingCards(false);
  };

  if (loading)
    return <h2 className="text-center text-lg mt-10 text-gray-700">Loading Pokédex...</h2>;

  const typeStyles = {
    grass: { bg: "bg-green-600", glow: "hover:shadow-green-400/50" },
    fire: { bg: "bg-red-600", glow: "hover:shadow-red-400/50" },
    water: { bg: "bg-blue-600", glow: "hover:shadow-blue-400/50" },
    bug: { bg: "bg-lime-600", glow: "hover:shadow-lime-400/50" },
    normal: { bg: "bg-gray-500", glow: "hover:shadow-gray-400/50" },
    poison: { bg: "bg-purple-600", glow: "hover:shadow-purple-400/50" },
    electric: { bg: "bg-yellow-500", glow: "hover:shadow-yellow-300/50" },
    ground: { bg: "bg-amber-700", glow: "hover:shadow-amber-400/50" },
    fairy: { bg: "bg-pink-500", glow: "hover:shadow-pink-400/50" },
    fighting: { bg: "bg-orange-700", glow: "hover:shadow-orange-400/50" },
    psychic: { bg: "bg-fuchsia-600", glow: "hover:shadow-fuchsia-400/50" },
    rock: { bg: "bg-stone-500", glow: "hover:shadow-stone-300/50" },
    ghost: { bg: "bg-indigo-700", glow: "hover:shadow-indigo-400/50" },
    ice: { bg: "bg-cyan-500", glow: "hover:shadow-cyan-300/50" },
    dragon: { bg: "bg-violet-700", glow: "hover:shadow-violet-400/50" },
    dark: { bg: "bg-zinc-700", glow: "hover:shadow-zinc-400/50" },
    steel: { bg: "bg-slate-500", glow: "hover:shadow-slate-300/50" },
    default: { bg: "bg-neutral-700", glow: "hover:shadow-neutral-400/50" },
  };
  
  function getTypeStyle(type) {
    return typeStyles[type] || typeStyles.default;
  }
  
  return (
    <div className="min-h-screen bg-gradient-to-b from-neutral-900 to-neutral-800 text-white flex flex-col items-center py-10">
      <h1 className="text-4xl font-extrabold text-red-500 mb-12 tracking-wide drop-shadow-lg">
        Pokédex
      </h1>
      <div className="w-full px-6 max-w-screen-2xl">
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-8">
        {pokemon.map((p) => {
  const { bg, glow } = getTypeStyle(p.type);
  return (
    <div
      key={p.id}
      onClick={() => {
        setSelectedPokemon(p);
        fetchPokemonCards(p.name);
      }}

      className={`p-4 rounded-2xl text-center text-white transition transform hover:scale-105 shadow-md ${bg} ${glow} hover:shadow-2xl`}
    >
      <img src={p.sprite_url} alt={p.name} className="mx-auto w-16 h-16" />
      <h2 className="text-lg font-bold mt-2 capitalize">{p.name}</h2>
      <p className="text-gray-200 text-sm">Type: {p.type}</p>
      <p className="text-gray-300 text-sm">Region: {p.region}</p>
    </div>
  );
})}
        </div>
      </div>
      {/* 🃏 Modal for showing top 5 valuable cards */}
{selectedPokemon && (
  <div
    className="fixed inset-0 bg-black/70 flex items-center justify-center z-50"
    onClick={() => {
      setSelectedPokemon(null);
      setCards([]);
    }}
  >
    <div
      className="bg-neutral-900 p-6 rounded-xl w-96 text-white relative"
      onClick={(e) => e.stopPropagation()} // prevent closing when clicking inside
    >
      <h2 className="text-2xl font-bold mb-4 text-center capitalize">
        {selectedPokemon.name} — Top 5 Cards
      </h2>

      {loadingCards ? (
        <p className="text-center text-gray-400">Loading cards...</p>
      ) : cards.length > 0 ? (
        <div className="space-y-4">
          {cards.map((card, idx) => (
            <div
              key={idx}
              className="flex items-center gap-3 bg-neutral-800 rounded-lg p-2 shadow"
            >
              <img
                src={card.image}
                alt={card.name}
                className="w-16 h-20 rounded-md"
              />
              <div>
                <p className="font-semibold text-lg">{card.name}</p>
                <p className="text-sm text-gray-400">{card.set}</p>
                <p className="text-xs text-yellow-300">{card.rarity}</p>
                {card.price && (
                  <p className="text-sm text-green-400 font-semibold mt-1">
                    Price 💰 ${card.price.toFixed(2)}
                  </p>
                )}
              </div>
            </div>
          ))}
        </div>
      ) : (
        <p className="text-center text-gray-400">No cards found for this Pokémon.</p>
      )}

      <button
        onClick={() => {
          setSelectedPokemon(null);
          setCards([]);
        }}
        className="absolute top-2 right-3 text-gray-400 hover:text-white text-xl"
      >
        ✕
      </button>
    </div>
  </div>
)}

    </div>
  );
}  
  

export default App;





