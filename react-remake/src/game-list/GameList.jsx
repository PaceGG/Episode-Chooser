import { useState, useEffect } from "react";
import axios from "axios";
import GameDetails from "./GameDetails"; // Путь к вашему компоненту GameDetails
import AddGameModal from "../addGameModal"; // Путь к вашему компоненту AddGameModal

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

  return (
    <div>
      <button onClick={() => setModalVisible(true)}>Add Game</button>
      {games.map((game) => (
        <GameDetails
          key={game.id}
          mainGameName={game.mainName}
          additionalGames={game.additionalGames}
        />
      ))}
      {modalVisible && (
        <AddGameModal
          setModalVisible={setModalVisible}
          updateGameData={updateGameData} // Передача функции обновления данных
        />
      )}
    </div>
  );
};

export default GameList;
