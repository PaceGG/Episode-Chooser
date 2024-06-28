import { useEffect, useState } from "react";
import axios from "axios";
import "./GameDetais.css";
import SetGameModal from "../set-game-modal/SetGameModal";

const GameDetails = ({
  mainGameName,
  additionalGames,
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
    console.log(convertTimeString(selectedTime));
  };

  function convertTimeString(inputString) {
    // Проверяем, что inputString не является undefined или null
    if (!inputString || typeof inputString !== "string") {
      return 0; // Возвращаем пустую строку или другое значение по умолчанию
    }

    // Извлекаем часть строки, содержащую время
    const timePartIndex = inputString.indexOf(":");
    if (timePartIndex === -1) {
      return 0; // Возвращаем пустую строку или другое значение по умолчанию
    }

    const timePart = inputString.substring(timePartIndex + 1).trim();

    // Разбиваем время на компоненты (дни, часы, минуты, секунды)
    const components = timePart.split(",");

    // Инициализируем переменные для компонентов времени
    let days = 0,
      hours = 0,
      minutes = 0,
      seconds = 0;

    // Обрабатываем каждый компонент времени
    for (let component of components) {
      const trimmedComponent = component.trim();
      if (trimmedComponent.includes("day")) {
        days = parseInt(trimmedComponent.split(" ")[0]);
      } else if (trimmedComponent.includes("hour")) {
        hours = parseInt(trimmedComponent.split(" ")[0]);
      } else if (trimmedComponent.includes("minute")) {
        minutes = parseInt(trimmedComponent.split(" ")[0]);
      } else if (trimmedComponent.includes("second")) {
        seconds = parseInt(trimmedComponent.split(" ")[0]);
      }
    }

    // Преобразуем дни в часы
    hours += days * 24;

    // Форматируем результат в формат HH:mm:ss
    const formattedTime = [
      hours.toString().padStart(2, "0"),
      minutes.toString().padStart(2, "0"),
      seconds.toString().padStart(2, "0"),
    ].join(":");

    return formattedTime;
  }

  function convertTimeStringToSeconds(inputString) {
    // Проверяем, что inputString не является undefined или null
    if (!inputString || typeof inputString !== "string") {
      return inputString;
    }

    // Извлекаем часть строки, содержащую время
    const timePartIndex = inputString.indexOf(":");
    if (timePartIndex === -1) {
      return inputString;
    }

    const timePart = inputString.substring(timePartIndex + 1).trim();
    const timeParts = inputString.split(":");

    if (timeParts.length === 3) {
      const hours = parseInt(timeParts[0], 10);
      const minutes = parseInt(timeParts[1], 10);
      const seconds = parseInt(timeParts[2], 10);

      if (isNaN(hours) || isNaN(minutes) || isNaN(seconds)) {
        return inputString;
      }
      let totalSeconds = hours * 3600 + minutes * 60 + seconds;
      return totalSeconds;
    }

    // Разбиваем время на компоненты (дни, часы, минуты, секунды)
    const components = timePart.split(",");

    // Инициализируем переменные для компонентов времени
    let days = 0,
      hours = 0,
      minutes = 0,
      seconds = 0;

    // Обрабатываем каждый компонент времени
    for (let component of components) {
      const trimmedComponent = component.trim();
      if (trimmedComponent.includes("day")) {
        days = parseInt(trimmedComponent.split(" ")[0]);
      } else if (trimmedComponent.includes("hour")) {
        hours = parseInt(trimmedComponent.split(" ")[0]);
      } else if (trimmedComponent.includes("minute")) {
        minutes = parseInt(trimmedComponent.split(" ")[0]);
      } else if (trimmedComponent.includes("second")) {
        seconds = parseInt(trimmedComponent.split(" ")[0]);
      }
    }

    // Преобразуем дни и часы в секунды
    let totalSeconds = days * 24 * 3600 + hours * 3600 + minutes * 60 + seconds;

    return totalSeconds;
  }

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
          ? {
              ...game,
              status: selectedStatus,
              time: convertTimeStringToSeconds(selectedTime),
            }
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
          mainTime: convertTimeStringToSeconds(selectedTime),
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

  const selectStatus = (game) => {
    let toReturn = "";
    let counter = { none: 0, inProcess: 0, complete: 0, bad: 0 };

    game.forEach((game) => {
      if (game.status === "none") counter.none++;
      if (game.status === "inProcess") counter.inProcess++;
      if (game.status === "complete") counter.complete++;
      if (game.status === "bad") counter.bad++;
    });

    if (counter.none === 0 && counter.complete > 0) toReturn = "complete";
    if (counter.none === 0 && counter.complete === 0 && counter.bad > 0)
      toReturn = "bad";
    if (counter.inProcess > 0) toReturn = "inProcess";

    return toReturn;
  };

  const renderAdditionalGames = () => (
    <details
      open={isOpen || selectStatus(gameData.additionalGames) === "inProcess"}
    >
      <summary
        onContextMenu={(e) => handleRightClickDetails(e, gameData.id)}
        className={selectStatus(gameData.additionalGames)}
      >
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
    <>
      {additionalGames.length === 0
        ? renderMainGame()
        : renderAdditionalGames()}
      {modalVisible && (
        <div className="modal">
          {/* <h2>{selectedGameName}</h2> */}
          <div className="modal-content selectStatus">
            <label
              className={
                selectedStatus === "complete"
                  ? "completeActive"
                  : "completeCheckmark"
              }
            >
              <input
                type="radio"
                name="status"
                value="complete"
                checked={selectedStatus === "complete"}
                onChange={handleRadioChange}
              />
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512">
                <path d="M438.6 105.4c12.5 12.5 12.5 32.8 0 45.3l-256 256c-12.5 12.5-32.8 12.5-45.3 0l-128-128c-12.5-12.5-12.5-32.8 0-45.3s32.8-12.5 45.3 0L160 338.7 393.4 105.4c12.5-12.5 32.8-12.5 45.3 0z" />
              </svg>
            </label>
            <label
              className={
                selectedStatus === "bad" ? "badActive" : "badCheckmark"
              }
            >
              <input
                type="radio"
                name="status"
                value="bad"
                checked={selectedStatus === "bad"}
                onChange={handleRadioChange}
              />
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512">
                <path d="M342.6 150.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L192 210.7 86.6 105.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L146.7 256 41.4 361.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0L192 301.3 297.4 406.6c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L237.3 256 342.6 150.6z" />
              </svg>
            </label>
            <label
              className={
                selectedStatus === "inProcess"
                  ? "inProcessActive"
                  : "inProcessCheckmark"
              }
            >
              <input
                type="radio"
                name="status"
                value="inProcess"
                checked={selectedStatus === "inProcess"}
                onChange={handleRadioChange}
              />
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 512">
                <path d="M192 64C86 64 0 150 0 256S86 448 192 448H448c106 0 192-86 192-192s-86-192-192-192H192zM496 168a40 40 0 1 1 0 80 40 40 0 1 1 0-80zM392 304a40 40 0 1 1 80 0 40 40 0 1 1 -80 0zM168 200c0-13.3 10.7-24 24-24s24 10.7 24 24v32h32c13.3 0 24 10.7 24 24s-10.7 24-24 24H216v32c0 13.3-10.7 24-24 24s-24-10.7-24-24V280H136c-13.3 0-24-10.7-24-24s10.7-24 24-24h32V200z" />
              </svg>
            </label>
          </div>
          <div className="modal-content selectTime">
            Время:
            <input
              type="text"
              name="time"
              value={selectedTime}
              onChange={handleInputChange}
            />
          </div>
          <div className="modal-buttons">
            <button
              onClick={handleSaveChanges}
              className="modalButton confirmButton"
            >
              Confirm
            </button>
            <button
              onClick={cancelChanges}
              className="modalButton cancelButton"
            >
              Cancel
            </button>
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
    </>
  );
};

export default GameDetails;
