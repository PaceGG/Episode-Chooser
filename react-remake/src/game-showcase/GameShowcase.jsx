import { useEffect, useState } from "react";
import axios from "axios";
import style from "./GameShowcase.module.css";

const GameShowcase = () => {
  const [games, setGames] = useState([]);

  useEffect(() => {
    fetchGames(); // Изначальная загрузка данных при монтировании компонента
  }, []);

  const fetchGames = async () => {
    try {
      const response = await axios.get("http://localhost:3000/showcase"); // URL вашего json-server
      setGames(response.data);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  return (
    <div className={style.game__showcase}>
      {games.map((game) => (
        <div
          key={game.id}
          className={style.game__card}
          style={{ borderColor: game.color }}
        >
          <img
            src={game.coverart}
            alt={game.name}
            className={style.coverart}
            style={{
              borderTop: `5px solid ${game.color}`,
              borderBottom: `5px solid ${game.color}`,
            }}
          />
          <h2 className={style.game__name} style={{ color: game.color }}>
            {game.name}
          </h2>
        </div>
      ))}
    </div>
  );
};

export default GameShowcase;
