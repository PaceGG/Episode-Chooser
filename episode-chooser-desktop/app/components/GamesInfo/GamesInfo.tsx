import { Paper, Stack } from "@mui/material";
import GameCard, { Game } from "./GameCard";

export default function GamesInfo() {
  const snowRunner: Game = {
    color: "#fff000",
    title: "SnowRunner",
    time: 120,
    limit: 3,
    quote: 0,
  };

  const asc: Game = {
    color: "#f00",
    title: "Assassin’s Creed Revelations",
    time: 84,
    limit: 5,
    quote: 345,
    // forced: true,
  };

  const silksong: Game = {
    color: "#00f",
    title: "Hollow Knight: Silksong",
    time: 120,
    limit: -53,
    quote: 123,
  };

  return (
    <Stack direction={"row"} gap={2}>
      <GameCard game={snowRunner} />
      <GameCard game={asc} />
      <GameCard game={silksong} />
    </Stack>
  );
}
