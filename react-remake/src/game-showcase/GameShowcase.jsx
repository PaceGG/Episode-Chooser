import { useEffect, useState } from "react";
import axios from "axios";
import style from "./GameShowcase.module.css";
import steamApi from "./steamApi";
import { getMainColors } from "./getMainColors";

const GameShowcase = () => {
  const [games, setGames] = useState([]);
  const [initialGames, setInitialGames] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false);

  useEffect(() => {
    fetchGames();
  }, []);

  const fetchGames = async () => {
    try {
      const response = await axios.get("http://localhost:3000/showcase");
      const enrichedGames = response.data.map((game) => ({
        ...game,
        steamApps: [],
        currentAppIndex: 0,
        appColors: [], // массив цветов для текущего steamApp
        selectedColorIndex: 0, // выбранный цвет из массива
      }));
      setGames(enrichedGames);
      setInitialGames(enrichedGames);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  const handleSteamLinkButton = async (gameId, name) => {
    try {
      const apps = await steamApi.getAppsByName(name);
      if (!apps.length) return;

      const firstAppId = apps[0].id;
      const steamImages = steamApi.getSteamImages(firstAppId);
      const colors = await getMainColors(steamImages.logo);

      setGames((prev) =>
        prev.map((game) =>
          game.id === gameId
            ? {
                ...game,
                steamApps: apps,
                currentAppIndex: 0,
                coverart: steamImages.library600x900_2x,
                appColors: colors,
                selectedColorIndex: 0,
              }
            : game
        )
      );
    } catch (error) {
      console.error("Steam API error:", error);
    }
  };

  const handleAppSwitch = async (gameId, direction) => {
    const updatedGames = await Promise.all(
      games.map(async (game) => {
        if (game.id !== gameId || !game.steamApps?.length) return game;

        let newIndex = game.currentAppIndex + direction;
        if (newIndex < 0) newIndex = game.steamApps.length - 1;
        if (newIndex >= game.steamApps.length) newIndex = 0;

        const newAppId = game.steamApps[newIndex].id;
        const steamImages = await steamApi.getSteamImages(newAppId);
        const colors = await getMainColors(steamImages.logo);

        return {
          ...game,
          currentAppIndex: newIndex,
          coverart: steamImages.library600x900_2x,
          appColors: colors,
          selectedColorIndex: 0,
        };
      })
    );
    setGames(updatedGames);
  };

  const handleInputChange = (id, field, value) => {
    setGames((prevData) =>
      prevData.map((item) =>
        item.id === id ? { ...item, [field]: value } : item
      )
    );
  };

  const handleColorSelect = (gameId, colorIndex) => {
    setGames((prev) =>
      prev.map((game) =>
        game.id === gameId
          ? {
              ...game,
              selectedColorIndex: colorIndex,
              color: game.appColors[colorIndex],
            }
          : game
      )
    );
  };

  const handleConfirm = async () => {
    try {
      await Promise.all(
        games.map((game) => {
          const {
            steamApps,
            currentAppIndex,
            appColors,
            selectedColorIndex,
            ...gameToSend
          } = game;
          axios.put(`http://localhost:3000/showcase/${game.id}`, gameToSend);
        })
      );
      setIsModalOpen(false);
    } catch (error) {
      console.error("Error saving data:", error);
    }
  };

  const handleCancel = () => {
    setIsModalOpen(false);
    setGames(initialGames);
  };

  const renderEditor = () =>
    games.map((game, index) => (
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
        <div className={style.coverart_input}>
          <input
            type="url"
            className={style.h2Input}
            id={`url${index}`}
            placeholder={game.coverart}
            onChange={(e) =>
              handleInputChange(game.id, "coverart", e.target.value)
            }
          />
          {game.steamApps?.length > 1 && (
            <button
              className={style.steam_button}
              onClick={() => handleAppSwitch(game.id, -1)}
            >
              ◀
            </button>
          )}
          <button
            className={style.steam_button}
            onClick={() => handleSteamLinkButton(game.id, game.name)}
          >
            Steam link
          </button>
          {game.steamApps?.length > 1 && (
            <button
              className={style.steam_button}
              onClick={() => handleAppSwitch(game.id, 1)}
            >
              ▶
            </button>
          )}
        </div>

        <div className={style.colorContainer}>
          <input
            type="color"
            id={`color${index}`}
            value={game.color}
            onChange={(e) =>
              handleInputChange(game.id, "color", e.target.value)
            }
            className={style.colorInput}
          />
          {game.appColors?.length > 0 && (
            <div className={style.colorSwitcher}>
              {game.appColors.map((col, i) => (
                <button
                  key={i}
                  className={style.colorButton}
                  style={{
                    backgroundColor: col,
                    border:
                      i === game.selectedColorIndex
                        ? "2px solid #0b79d0"
                        : "1px solid #888",
                  }}
                  onClick={() => handleColorSelect(game.id, i)}
                />
              ))}
            </div>
          )}
        </div>

        <textarea
          id={`textarea${index}`}
          onChange={(e) => handleInputChange(game.id, "name", e.target.value)}
          className={style.h2Input + " " + style.game__name}
          style={{ color: game.color }}
          placeholder={game.name}
        />
      </div>
    ));

  const renderShowcase = () =>
    games.map((game) => (
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
    ));

  return (
    <div className={style.game__showcase}>
      <div className={style.edit_container}>
        <button className={style.edit} onClick={() => setIsModalOpen(true)}>
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
            <path d="M471.6 21.7c-21.9-21.9-57.3-21.9-79.2 0L362.3 51.7l97.9 97.9 30.1-30.1c21.9-21.9 21.9-57.3 0-79.2L471.6 21.7zm-299.2 220c-6.1 6.1-10.8 13.6-13.5 21.9l-29.6 88.8c-2.9 8.6-.6 18.1 5.8 24.6s15.9 8.7 24.6 5.8l88.8-29.6c8.2-2.7 15.7-7.4 21.9-13.5L437.7 172.3 339.7 74.3 172.4 241.7zM96 64C43 64 0 107 0 160V416c0 53 43 96 96 96H352c53 0 96-43 96-96V320c0-17.7-14.3-32-32-32s-32 14.3-32 32v96c0 17.7-14.3 32-32 32H96c-17.7 0-32-14.3-32-32V160c0-17.7 14.3-32 32-32h96c17.7 0 32-14.3 32-32s-14.3-32-32-32H96z" />
          </svg>
        </button>
        {isModalOpen && (
          <>
            <button className={style.confirm} onClick={handleConfirm}>
              Confirm
            </button>
            <button className={style.addInput__button} onClick={handleCancel}>
              Cancel
            </button>
          </>
        )}
      </div>
      {isModalOpen ? renderEditor() : renderShowcase()}
    </div>
  );
};

export default GameShowcase;
