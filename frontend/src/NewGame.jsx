import { useEffect, useState } from "react";

export default function NewGame() {
  const [players, setPlayers] = useState([]);
  const [game, setGame] = useState({
    date: new Date().toISOString().split("T")[0],
    payer: null,
    fetcher: null,
    played: {}
  });

  useEffect(() => {
    fetch("/api/players")
      .then(r => r.json())
      .then(setPlayers);
  }, []);

  const togglePlayed = (id) => {
    setGame((g) => ({
      ...g,
      played: { ...g.played, [id]: !g.played[id] }
    }));
  };

  const submit = () => {
    const payload = {
      date: game.date,
      payer: game.payer,
      fetcher: game.fetcher,
      players: Object.keys(game.played).filter(id => game.played[id])
    };

    fetch("/api/games", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(payload)
    }).then(() => alert("Partie enregistrée !"));
  };

  return (
    <div className="p-4 max-w-xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Nouvelle partie ☕</h1>

      <label className="block mb-2">Date :</label>
      <input
        type="date"
        className="border p-2 mb-4 w-full"
        value={game.date}
        onChange={(e) => setGame({...game, date: e.target.value})}
      />

      <table className="w-full border mb-4">
        <thead>
          <tr className="bg-gray-100">
            <th className="p-2 border">Joueur</th>
            <th className="p-2 border">A joué</th>
            <th className="p-2 border">A payé</th>
            <th className="p-2 border">Est allé chercher</th>
          </tr>
        </thead>
        <tbody>
          {players.map(p => (
            <tr key={p.id}>
              <td className="border p-2">{p.name}</td>

              <td className="border p-2">
                <input
                  type="checkbox"
                  checked={!!game.played[p.id]}
                  onChange={() => togglePlayed(p.id)}
                />
              </td>

              <td className="border p-2">
                <input
                  type="radio"
                  name="payer"
                  onChange={() => setGame({...game, payer: p.id})}
                />
              </td>

              <td className="border p-2">
                <input
                  type="radio"
                  name="fetcher"
                  onChange={() => setGame({...game, fetcher: p.id})}
                />
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <button
        onClick={submit}
        className="bg-blue-500 text-white px-4 py-2 rounded"
      >
        Enregistrer
      </button>
    </div>
  );
}
