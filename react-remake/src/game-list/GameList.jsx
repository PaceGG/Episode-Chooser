import { useState, useEffect } from "react";
import axios from "axios";
import GameDetails from "./GameDetails"; // Путь к вашему компоненту GameDetails
import AddGameModal from "../addGameModal"; // Путь к вашему компоненту AddGameModal
import style from "./GameList.module.css";

const GameList = () => {
  const [games, setGames] = useState([]);
  const [modalVisible, setModalVisible] = useState(false);

  useEffect(() => {
    fetchGames(); // Изначальная загрузка данных при монтировании компонента
  }, []);

  const fetchGames = async () => {
    try {
      const response = await axios.get("http://localhost:3000/games"); // URL вашего json-server
      setGames(response.data);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  const updateGameData = () => {
    fetchGames(); // Обновление данных после подтверждения в AddGameModal
  };

  const countCompleteGames = (data) => {
    let count = 0;

    data.forEach((game) => {
      if (game.additionalGames.length === 0) {
        if (game.mainStatus === "complete") {
          count++;
        }
      } else {
        game.additionalGames.forEach((additionalGame) => {
          if (additionalGame.status === "complete") {
            count++;
          }
        });
      }
    });

    return count;
  };

  const countBadGames = (data) => {
    let count = 0;

    data.forEach((game) => {
      if (game.additionalGames.length === 0) {
        if (game.mainStatus === "bad") {
          count++;
        }
      } else {
        game.additionalGames.forEach((additionalGame) => {
          if (additionalGame.status === "bad") {
            count++;
          }
        });
      }
    });

    return count;
  };

  return (
    <div className="game-list-content">
      <div className="statistic">
        <h2>
          Игр пройдено:{" "}
          <span style={{ color: "white" }}>{countCompleteGames(games)}</span>
          <br />
          <span style={{ color: "#ee204d" }}>Игр брошено:&nbsp;&nbsp; </span>
          <span style={{ color: "#white" }}>{countBadGames(games)}</span>
        </h2>
        <button
          onClick={() => setModalVisible(true)}
          className={style.add__game__button}
        >
          Add Game
        </button>
      </div>
      <div className="game-list">
        <ul>
          {games.map((game) => (
            <GameDetails
              updateGameData={updateGameData}
              gameData={game}
              key={game.id}
              mainGameName={game.mainName}
              mainStatus={game.mainStatus}
              additionalGames={game.additionalGames.map((addGame) => ({
                name: addGame.name,
                status: addGame.status,
                time: addGame.time,
                numberOfEps: addGame.numberOfEps,
              }))}
            />
          ))}
          {modalVisible && (
            <AddGameModal
              setModalVisible={setModalVisible}
              updateGameData={updateGameData} // Передача функции обновления данных
            />
          )}
        </ul>
      </div>
    </div>
  );
};

export default GameList;
