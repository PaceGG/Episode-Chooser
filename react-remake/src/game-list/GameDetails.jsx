import React, { useState } from "react";
import axios from "axios";
import "./GameDetais.css";

const GameDetails = ({
  mainGameName,
  additionalGames,
  mainStatus,
  gameData,
}) => {
  const [modalVisible, setModalVisible] = useState(false);

  const [selectedGameID, setSelectedGameID] = useState(null);
  const [selectedGameName, setSelectedGameName] = useState(null);
  const [selectedStatus, setSelectedStatus] = useState(null);

  const handleRightClick = (e, gameName, gameID) => {
    e.preventDefault(); // Prevent default context menu
    setSelectedGameID(gameID);
    setSelectedGameName(gameName);
    setSelectedStatus(null);
    setModalVisible(true);
  };

  const handleRadioChange = (e) => {
    setSelectedStatus(e.target.value);
  };

  const handleSaveChanges = async () => {
    try {
      const response = await axios.get(
        `http://localhost:3000/games/${selectedGameID}`
      );
      const game = response.data;

      const updateAdditionalGames = game.additionalGames.map((game) =>
        game.name === selectedGameName
          ? { ...game, status: selectedStatus }
          : game
      );

      if (updateAdditionalGames.length !== 0) {
        await axios.put(`http://localhost:3000/games/${selectedGameID}`, {
          ...game,
          additionalGames: updateAdditionalGames,
        });
      } else {
        await axios.put(`http://localhost:3000/games/${selectedGameID}`, {
          ...game,
          mainStatus: selectedStatus,
        });
      }
    } catch (error) {
      console.log("Ошибка при обновлении статуса игры: ", error);
    }

    setModalVisible(false);
  };

  const cancelChanges = () => {
    setModalVisible(false);
    setSelectedStatus(null);
  };

  const renderMainGame = () => (
    <li
      onContextMenu={(e) => handleRightClick(e, gameData.mainName, gameData.id)}
      className={
        selectedGameName === gameData.mainName && selectedStatus
          ? selectedStatus
          : gameData.mainStatus
      }
    >
      {mainGameName}
    </li>
  );

  const renderAdditionalGames = () => (
    <details>
      <summary>{mainGameName}</summary>
      <ul>
        {additionalGames.map((game, index) => (
          <li
            key={index}
            onContextMenu={(e) => handleRightClick(e, game.name, gameData.id)}
            className={
              selectedGameName === game.name && selectedStatus
                ? selectedStatus
                : game.status
            }
          >
            {game.name}
          </li>
        ))}
      </ul>
    </details>
  );

  return (
    <div>
      {additionalGames.length === 0
        ? renderMainGame()
        : renderAdditionalGames()}
      {modalVisible && (
        <div className="modal">
          <h2>{selectedGameName}</h2>
          <div className="modal-content">
            <label>
              <input
                type="radio"
                name="status"
                value="bad"
                checked={selectedStatus === "bad"}
                onChange={handleRadioChange}
              />
              Крестик
            </label>
            <label>
              <input
                type="radio"
                name="status"
                value="complete"
                checked={selectedStatus === "complete"}
                onChange={handleRadioChange}
              />
              Галочка
            </label>
            <label>
              <input
                type="radio"
                name="status"
                value="inProcess"
                checked={selectedStatus === "inProcess"}
                onChange={handleRadioChange}
              />
              Кружок
            </label>
            <button onClick={handleSaveChanges}>Сохранить</button>
            <button onClick={cancelChanges}>Отмена</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default GameDetails;
