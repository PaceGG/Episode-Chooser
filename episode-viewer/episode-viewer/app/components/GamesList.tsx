"use client";
import { useState } from "react";
import useFilterStore from "../store/useFilterStore";
import "@/app/globals.css";

export interface AdditionalGame {
  name: string;
  status: string;
  time: number;
  numberOfEps: number;
}

export interface GameData {
  id: string | number;
  mainName: string;
  mainStatus: string;
  mainTime: number;
  mainNumberOfEps?: number;
  additionalGames: AdditionalGame[];
}

interface GamesListProps {
  games: GameData[];
}

type SortOrder = "default" | "asc" | "desc";
type SortField = "time" | "eps";

export default function GamesList({ games }: GamesListProps) {
  const { statusComplete, statusBad, statusWait, toggleFilter } =
    useFilterStore();

  const [sortField, setSortField] = useState<SortField | null>(null);
  const [sortOrder, setSortOrder] = useState<SortOrder>("default");
  // Новое состояние для структуры серий
  const [isStructured, setIsStructured] = useState<boolean>(true);

  const handleFilterChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    toggleFilter(event.target.id);
  };

  const getGameTime = (game: GameData) => {
    if (game.additionalGames.length === 0) return game.mainTime;
    return game.additionalGames.reduce((sum, g) => sum + g.time, 0);
  };

  const getGameEps = (game: GameData) => {
    if (game.additionalGames.length === 0) return game.mainNumberOfEps || 0;
    return game.additionalGames.reduce((sum, g) => sum + g.numberOfEps, 0);
  };

  const handleSortToggle = (field: SortField) => {
    if (sortField !== field) {
      setSortField(field);
      setSortOrder("asc");
    } else {
      if (sortOrder === "default") setSortOrder("asc");
      else if (sortOrder === "asc") setSortOrder("desc");
      else {
        setSortOrder("default");
        setSortField(null);
      }
    }
  };

  const getSortLabel = (field: SortField, label: string) => {
    if (sortField !== field || sortOrder === "default") return `${label} ↕`;
    return sortOrder === "asc" ? `${label} ↑` : `${label} ↓`;
  };

  // 1. Формируем список игр в зависимости от галочки структуризации
  const processedGames = isStructured
    ? games
    : games.flatMap((game) => {
        if (game.additionalGames.length === 0) return [game];

        // Превращаем подигры в плоские элементы GameData
        return game.additionalGames.map((subGame, index) => ({
          id: `${game.id}-${index}`, // Генерируем уникальный ID
          mainName: subGame.name,
          mainStatus: subGame.status,
          mainTime: subGame.time,
          mainNumberOfEps: subGame.numberOfEps,
          additionalGames: [], // Очищаем, чтобы рендерилось через renderMainGame
        }));
      });

  // 2. Сортируем уже обработанный (плоский или структурированный) массив
  const sortedGames = [...processedGames].sort((a, b) => {
    if (!sortField || sortOrder === "default") return 0;

    const valA = sortField === "time" ? getGameTime(a) : getGameEps(a);
    const valB = sortField === "time" ? getGameTime(b) : getGameEps(b);

    // Проверяем на нулевые/отсутствующие значения
    const isAEmpty = valA === 0;
    const isBEmpty = valB === 0;

    // Если оба пустые, они равны между собой
    if (isAEmpty && isBEmpty) return 0;
    // Если только A пустой — отправляем его в конец (возвращаем положительное число)
    if (isAEmpty) return 1;
    // Если только B пустой — отправляем его в конец (возвращаем отрицательное число)
    if (isBEmpty) return -1;

    // Обычная сортировка для непустых значений
    if (sortOrder === "asc") return valA - valB;
    if (sortOrder === "desc") return valB - valA;
    return 0;
  });

  const pad = (num: number): string => (num < 10 ? "0" + num : num.toString());

  const convertTime = (secondsTotal: number): string => {
    const hours = Math.floor(secondsTotal / 3600);
    const minutes = Math.floor((secondsTotal % 3600) / 60);
    const seconds = Math.floor(secondsTotal % 60);
    return `${pad(hours)}:${pad(minutes)}:${pad(seconds)}`;
  };

  const selectStatus = (gamesList: AdditionalGame[]): string => {
    let toReturn = "";
    const counter = { none: 0, inProcess: 0, complete: 0, bad: 0 };
    gamesList.forEach((g) => {
      if (g.status in counter) counter[g.status as keyof typeof counter]++;
    });

    if (counter.none === 0 && counter.complete > 0) toReturn = "complete";
    if (counter.none === 0 && counter.complete === 0 && counter.bad > 0)
      toReturn = "bad";
    if (counter.inProcess > 0) toReturn = "inProcess";
    return toReturn;
  };

  const renderMainGame = (game: GameData) => (
    <li
      key={game.id}
      className={game.mainStatus}
      style={
        (game.mainStatus === "bad" && statusBad) ||
        (game.mainStatus === "complete" && statusComplete) ||
        (game.mainStatus === "wait" && statusWait)
          ? { display: "none" }
          : undefined
      }
    >
      {game.mainName}
      {game.mainTime > 0 &&
        ` - ${game.mainNumberOfEps} (${convertTime(game.mainTime)})`}
    </li>
  );

  const renderAdditionalGames = (game: GameData) => {
    const currentStatus = selectStatus(game.additionalGames);
    const totalTime = getGameTime(game);
    const totalEps = getGameEps(game);

    return (
      <details
        key={game.id}
        style={
          (currentStatus === "bad" && statusBad) ||
          (currentStatus === "complete" && statusComplete) ||
          (currentStatus === "wait" && statusWait)
            ? { display: "none" }
            : undefined
        }
        open={currentStatus === "inProcess"}
      >
        <summary className={currentStatus}>
          {game.mainName}
          {totalTime > 0 && ` - ${totalEps} (${convertTime(totalTime)})`}
        </summary>
        <ul>
          {game.additionalGames.map((subGame, index) => (
            <li
              key={index}
              className={subGame.status}
              style={
                (subGame.status === "bad" && statusBad && subGame.time > 0) ||
                (subGame.status === "complete" &&
                  statusComplete &&
                  subGame.time > 0) ||
                (subGame.status === "wait" && statusWait)
                  ? { display: "none" }
                  : undefined
              }
            >
              {subGame.name}
              {subGame.time > 0 &&
                ` - ${subGame.numberOfEps} (${convertTime(subGame.time)})`}
            </li>
          ))}
        </ul>
      </details>
    );
  };

  return (
    <>
      <div className="flex gap-2 justify-center">
        <label className="filter">
          <input
            type="checkbox"
            name="statusFilter"
            id="statusComplete"
            checked={statusComplete}
            onChange={handleFilterChange}
          />
          <span className="checkmark"></span>
          <span className="complete-checkbox checkbox-text">Complete</span>
        </label>

        <label className="filter">
          <input
            type="checkbox"
            name="statusFilter"
            id="statusBad"
            checked={statusBad}
            onChange={handleFilterChange}
          />
          <span className="checkmark"></span>
          <span className="bad-checkbox checkbox-text">Bad</span>
        </label>
      </div>

      {/* Блок сортировки и структуризации */}
      <div className="flex flex-col items-center gap-2 my-2">
        {/* Новая галочка структуризации */}
        <label className="flex items-center gap-2 cursor-pointer text-sm select-none">
          <input
            type="checkbox"
            checked={isStructured}
            onChange={(e) => setIsStructured(e.target.checked)}
            className="w-4 h-4 accent-blue-500 rounded"
          />
          <span>Структуризовать по сериям</span>
        </label>

        <div className="flex gap-2">
          <button
            onClick={() => handleSortToggle("time")}
            className={`px-3 py-1 text-sm border rounded hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors ${
              sortField === "time" && sortOrder !== "default"
                ? "font-bold border-blue-500"
                : "border-gray-300"
            }`}
          >
            {getSortLabel("time", "По времени")}
          </button>
          <button
            onClick={() => handleSortToggle("eps")}
            className={`px-3 py-1 text-sm border rounded hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors ${
              sortField === "eps" && sortOrder !== "default"
                ? "font-bold border-blue-500"
                : "border-gray-300"
            }`}
          >
            {getSortLabel("eps", "По сериям")}
          </button>
        </div>
      </div>

      <div className="game-list pl-15 overflow-hidden">
        <ul>
          {sortedGames.map((game) =>
            game.additionalGames.length === 0
              ? renderMainGame(game)
              : renderAdditionalGames(game),
          )}
        </ul>
      </div>
    </>
  );
}
