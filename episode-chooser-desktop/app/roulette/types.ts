import { Game } from "../components/GamesInfo/GameCard";

export class GameRoulette {
  games: Game[];
  width: number;

  winner: Game;
  winnerId: number;
  winnerPosition: number;
  elements: Game[];

  constructor(games: Game[], width: number) {
    // === Инициализация базовых полей ===
    this.games = [...games];
    this.width = width;

    // === Инициализация полей элементов рулетки ===
    // Генерация массива элементов
    const elementsNumber = 105;

    const gameX = this.games[0];
    const gameY = this.games[1];

    const totalQuote = gameX.quote + gameY.quote;

    const lengthX = Math.round((gameX.quote / totalQuote) * elementsNumber);
    const lengthY = elementsNumber - lengthX;

    const array: Game[] = [
      ...Array(lengthX).fill(gameX),
      ...Array(lengthY).fill(gameY),
    ];

    for (let i = array.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [array[i], array[j]] = [array[j], array[i]];
    }

    // Выбор победителя
    const randomValue = Math.random() * totalQuote;

    if (randomValue < games[0].quote) {
      this.winner = games[0];
    } else {
      this.winner = games[1];
    }

    const minId = 50;
    const maxId = 100;
    this.winnerId = Math.floor(Math.random() * (maxId - minId + 1)) + minId;

    array[this.winnerId] = this.winner;

    this.elements = array;

    // Выбор финальной позиции
    this.winnerPosition = Math.floor(Math.random() * (this.width + 1));
  }
}
