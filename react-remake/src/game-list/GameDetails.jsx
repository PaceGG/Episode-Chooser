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
  const [selectedEps, setSelectedEps] = useState(0);

  const [filter, setFilter] = useState({
    statusComplete: false,
    statusBad: false,
    statusWait: false,
  });

  useEffect(() => {
    loadFiltersData();
  }, []);

  // Добавьте эту функцию в компонент GameDetails
  const loadSessionData = async (gameName) => {
    try {
      const response = await fetch("/sessions.json");
      const sessions = await response.json();

      // Ищем записи для указанной игры
      const gameEntries = Object.values(sessions).filter(
        (entry) => entry.gameGroup === gameName,
      );

      if (gameEntries.length === 0) {
        console.log(
          `Поиск по gameGroup не дал результатов, ищем по game: "${gameName}"`,
        );
        const fallbackEntries = Object.values(sessions).filter(
          (entry) => entry.game === gameName,
        );

        if (fallbackEntries.length === 0) {
          return { totalDuration: 0, episodeCount: 0 };
        }

        // Используем fallbackEntries
        let totalDuration = 0;
        let episodeCount = 0;

        fallbackEntries.forEach((entry) => {
          entry.episodes.forEach((episode) => {
            totalDuration += episode.duration;
            episodeCount++;
          });
        });

        return { totalDuration, episodeCount };
      }

      // Суммируем продолжительность всех эпизодов
      let totalDuration = 0;
      let episodeCount = 0;

      gameEntries.forEach((entry) => {
        entry.episodes.forEach((episode) => {
          totalDuration += episode.duration;
          episodeCount++;
        });
      });

      return { totalDuration, episodeCount };
    } catch (error) {
      console.error("Error loading session data:", error);
      return { totalDuration: 0, episodeCount: 0 };
    }
  };

  const loadFiltersData = async () => {
    try {
      const response = await axios.get("http://localhost:3000/filters"); // URL вашего json-server
      setFilter(response.data);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  const handleRightClick = (e, gameName, gameID, gameTime, gameEps) => {
    e.preventDefault();
    setSelectedGameID(gameID);
    setSelectedGameName(gameName);

    if (gameData.additionalGames.length === 0) {
      setSelectedStatus(gameData.mainStatus);
    } else {
      setSelectedStatus(
        gameData.additionalGames.find((game) => game.name === gameName).status,
      );
    }
    setModalVisible(true);
    setSelectedTime(gameTime);
    setSelectedEps(gameEps);
  };

  const handleRadioChange = (e) => {
    setSelectedStatus(e.target.value);
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
      return parseInt(0);
    }

    // Извлекаем часть строки, содержащую время
    const timePartIndex = inputString.indexOf(":");
    if (timePartIndex === -1) {
      return parseInt(inputString);
    }

    const timePart = inputString.substring(timePartIndex + 1).trim();
    const timeParts = inputString.split(":");

    if (timeParts.length === 3) {
      const hours = parseInt(timeParts[0], 10);
      const minutes = parseInt(timeParts[1], 10);
      const seconds = parseInt(timeParts[2], 10);

      if (isNaN(hours) || isNaN(minutes) || isNaN(seconds)) {
        return parseInt(inputString);
      }
      let totalSeconds = hours * 3600 + minutes * 60 + seconds;
      return parseInt(totalSeconds);
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
    const seconds = Math.floor(selectedTime % 60);

    const formatedTime = `${pad(hours)}:${pad(minutes)}:${pad(seconds)}`;
    return formatedTime;
  };

  const handleInputChange = (e) => {
    setSelectedTime(e.target.value);
  };
  const handleEpsInputChange = (e) => {
    setSelectedEps(e.target.value);
  };

  const handleSaveChanges = async () => {
    try {
      const response = await axios.get(
        `http://localhost:3000/games/${selectedGameID}`,
      );
      const game = response.data;

      let timeToSave = convertTimeStringToSeconds(selectedTime);
      let epsToSave = parseInt(selectedEps);

      if (
        selectedStatus === "complete" &&
        (!selectedTime || selectedTime == 0)
      ) {
        // Загружаем данные из sessions.json для этой игры
        const sessionData = await loadSessionData(selectedGameName);

        // Используем данные из sessions.json только если они есть
        if (sessionData.totalDuration > 0) {
          timeToSave = sessionData.totalDuration;
          epsToSave = sessionData.episodeCount;

          // Обновляем локальное состояние для отображения в UI
          setSelectedTime(timeToSave);
          setSelectedEps(sessionData.episodeCount);
        }
      }

      const updateAdditionalGames = game.additionalGames.map((game) =>
        game.name === selectedGameName
          ? {
              ...game,
              status: selectedStatus,
              time: timeToSave,
              numberOfEps: epsToSave,
            }
          : game,
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
          mainTime: timeToSave,
          mainNumberOfEps: epsToSave,
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
        handleRightClick(
          e,
          gameData.mainName,
          gameData.id,
          gameData.mainTime,
          gameData.mainNumberOfEps,
        )
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
        : " - " +
          gameData.mainNumberOfEps +
          " (" +
          convertTime(gameData.mainTime) +
          ")"}
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
      numberOfEps: game.numberOfEps,
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
      style={
        (selectStatus(gameData.additionalGames) === "bad" &&
          filter.statusBad) ||
        (selectStatus(gameData.additionalGames) === "complete" &&
          filter.statusComplete) ||
        (selectStatus(gameData.additionalGames) === "wait" && filter.statusWait)
          ? { display: "none" }
          : null
      }
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
          : " - " +
            additionalGames
              .map((game) => game.numberOfEps)
              .reduce((a, b) => a + b, 0) +
            " (" +
            convertTime(
              additionalGames
                .map((game) => game.time)
                .reduce((a, b) => a + b, 0),
            ) +
            ")"}
      </summary>
      <ul>
        {additionalGames.map((game, index) => (
          <li
            key={index}
            onContextMenu={(e) =>
              handleRightClick(
                e,
                game.name,
                gameData.id,
                game.time,
                game.numberOfEps,
              )
            }
            className={
              selectedGameName === game.name && selectedStatus
                ? selectedStatus
                : game.status
            }
            style={
              (game.status === "bad" && filter.statusBad && game.time > 0) ||
              (game.status === "complete" &&
                filter.statusComplete &&
                game.time > 0) ||
              (game.status === "wait" && filter.statusWait)
                ? { display: "none" }
                : null
            }
          >
            {game.name}
            {game.time > 0
              ? ` - ` + game.numberOfEps + ` (${convertTime(game.time)})`
              : ""}
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
            <label className="reset">
              <button
                className="resetButton"
                onClick={() => {
                  setSelectedStatus("none");
                }}
              >
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
                  <path d="M125.7 160H176c17.7 0 32 14.3 32 32s-14.3 32-32 32H48c-17.7 0-32-14.3-32-32V64c0-17.7 14.3-32 32-32s32 14.3 32 32v51.2L97.6 97.6c87.5-87.5 229.3-87.5 316.8 0s87.5 229.3 0 316.8s-229.3 87.5-316.8 0c-12.5-12.5-12.5-32.8 0-45.3s32.8-12.5 45.3 0c62.5 62.5 163.8 62.5 226.3 0s62.5-163.8 0-226.3s-163.8-62.5-226.3 0L125.7 160z" />
                </svg>
              </button>
            </label>
          </div>
          <div
            className="modal-content selectTime"
            style={{
              display: "flex",
              flexDirection: "column",
              alignItems: "start",
            }}
          >
            <div className="time-line">
              <a href="https://ytplaylist-len.sharats.dev/">
                <img
                  src="https://ytplaylist-len.sharats.dev/static/favicon.png"
                  alt=""
                  width={"35px"}
                />
              </a>
              Время:
              <input
                type="text"
                name="time"
                placeholder={convertTime(selectedTime)}
                onChange={handleInputChange}
                style={{ width: "66px" }}
              />
            </div>
            <div>
              Количество серий:
              <input
                type="text"
                name="episodes"
                placeholder={selectedEps}
                onChange={handleEpsInputChange}
                style={{ width: "22px" }}
              />
            </div>
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
