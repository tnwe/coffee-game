import { useEffect, useState } from "react";

function App() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    fetch("/stats").then(r => r.json()).then(setStats);
  }, []);

  return (
    <div>
      <h1>Coffee Game ☕</h1>
      {stats && (
        <>
          <p>Total parties : {stats.total_games}</p>
          <p>Doublettes : {stats.doublettes}</p>
        </>
      )}
    </div>
  );
}

export default App;
