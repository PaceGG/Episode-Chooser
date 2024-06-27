import React, { useEffect, useState, useContext } from "react";
import axios from "axios";
import "./GameDetais.css";
import SetGameModal from "../set-game-modal/SetGameModal";

const GameDetails = ({
  mainGameName,
  additionalGames,
  mainStatus,
  gameData,
  updateGameData,
}) => {
  const [modalVisible, setModalVisible] = useState(false);
  const [modalEditorVisible, setModalEditorVisible] = useState(false);

  const [isOpen, setIsOpen] = useState(false);

  const [selectedGameNames, setSelectedGameNames] = useState([]);

  const [selectedGameID, setSelectedGameID] = useState(null);
  const [selectedGameName, setSelectedGameName] = useState(null);
  const [selectedStatus, setSelectedStatus] = useState(null);
  const [selectedTime, setSelectedTime] = useState(0);

  const [filter, setFilter] = useState({
    statusComplete: false,
    statusBad: false,
    statusWait: false,
  });

  useEffect(() => {
    loadFiltersData();
  }, []);

  const loadFiltersData = async () => {
    try {
      const response = await axios.get("http://localhost:3000/filters"); // URL вашего json-server
      setFilter(response.data);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  const handleRightClick = (e, gameName, gameID, gameTime) => {
    e.preventDefault();
    setSelectedGameID(gameID);
    setSelectedGameName(gameName);

    if (gameData.additionalGames.length === 0) {
      setSelectedStatus(gameData.mainStatus);
    } else {
      setSelectedStatus(
        gameData.additionalGames.find((game) => game.name === gameName).status
      );
    }
    setModalVisible(true);
    setSelectedTime(gameTime);
  };

  const handleRadioChange = (e) => {
    setSelectedStatus(e.target.value);
  };

  const pad = (num) => {
    return num < 10 ? "0" + num : num;
  };
  const convertTime = (selectedTime) => {
    const hours = Math.floor(selectedTime / 3600);
    const minutes = Math.floor((selectedTime % 3600) / 60);
    const seconds = selectedTime % 60;

    const formatedTime = `${pad(hours)}:${pad(minutes)}:${pad(seconds)}`;
    return formatedTime;
  };
  const handleInputChange = (e) => {
    setSelectedTime(e.target.value);
  };

  const handleSaveChanges = async () => {
    try {
      const response = await axios.get(
        `http://localhost:3000/games/${selectedGameID}`
      );
      const game = response.data;

      const updateAdditionalGames = game.additionalGames.map((game) =>
        game.name === selectedGameName
          ? { ...game, status: selectedStatus, time: parseInt(selectedTime) }
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
          mainTime: parseInt(selectedTime),
        });
      }
    } catch (error) {
      console.error("Ошибка при обновлении статуса игры: ", error);
    }

    updateGameData();
    setModalVisible(false);
  };

  const cancelChanges = () => {
    setModalVisible(false);
    setSelectedStatus(null);
  };

  const renderMainGame = () => (
    <li
      onContextMenu={(e) =>
        handleRightClick(e, gameData.mainName, gameData.id, gameData.mainTime)
      }
      className={
        selectedGameName === gameData.mainName && selectedStatus
          ? selectedStatus
          : gameData.mainStatus
      }
      style={
        (gameData.mainStatus === "bad" && filter.statusBad) ||
        (gameData.mainStatus === "complete" && filter.statusComplete) ||
        (gameData.mainStatus === "wait" && filter.statusWait)
          ? { display: "none" }
          : null
      }
    >
      {mainGameName}
      {gameData.mainTime === 0
        ? ""
        : " - (" + convertTime(gameData.mainTime) + ")"}
    </li>
  );

  const handleRightClickDetails = (e, gameID) => {
    e.preventDefault();
    if (e.nativeEvent.which === 3) {
      setIsOpen(true);
    }
    setModalEditorVisible(true);

    const listItems = additionalGames.map((game, index) => ({
      id: `${Date.now()}-${index}`,
      value: game.name,
      status: game.status,
      time: game.time,
    }));

    setSelectedGameNames(listItems);
    setSelectedGameName(mainGameName);
    setSelectedGameID(gameID);
  };

  const renderAdditionalGames = () => (
    <details open={isOpen}>
      <summary onContextMenu={(e) => handleRightClickDetails(e, gameData.id)}>
        {mainGameName}

        {additionalGames.map((game) => game.time).reduce((a, b) => a + b, 0) ===
        0
          ? ""
          : " - (" +
            convertTime(
              additionalGames
                .map((game) => game.time)
                .reduce((a, b) => a + b, 0)
            ) +
            ")"}
      </summary>
      <ul>
        {additionalGames.map((game, index) => (
          <li
            key={index}
            onContextMenu={(e) =>
              handleRightClick(e, game.name, gameData.id, game.time)
            }
            className={
              selectedGameName === game.name && selectedStatus
                ? selectedStatus
                : game.status
            }
            style={
              (game.status === "bad" && filter.statusBad) ||
              (game.status === "complete" && filter.statusComplete) ||
              (game.status === "wait" && filter.statusWait)
                ? { display: "none" }
                : null
            }
          >
            {game.name}
            {game.time > 0 ? ` (${convertTime(game.time)})` : ""}
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
          <div className="modal-content selectStatus">
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
          <div className="modal-content selectTime">
            <input
              type="text"
              name="time"
              value={selectedTime}
              onChange={handleInputChange}
            />
          </div>
        </div>
      )}
      {modalEditorVisible && (
        <SetGameModal
          setModalVisible={setModalEditorVisible}
          selectedGameNames={selectedGameNames}
          mainGameNameToi={selectedGameName}
          selectedGameID={selectedGameID}
          updateGameData={updateGameData}
        />
      )}
    </div>
  );
};

export default GameDetails;
