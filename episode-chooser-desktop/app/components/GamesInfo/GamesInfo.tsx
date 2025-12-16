import { Paper, Stack } from "@mui/material";
import GameCard, { Game } from "./GameCard";

export default function GamesInfo() {
  const snowRunner: Game = {
    color: "#fff000",
    title: "SnowRunner",
    time: 120,
    quote: 0,
  };

  const asc: Game = {
    color: "#f00",
    title: "Assassin’s Creed Revelations",
    time: 84,
    quote: 5,
    // forced: true,
  };

  const silksong: Game = {
    color: "#00f",
    title: "Hollow Knight: Silksong",
    time: 120,
    quote: 0,
  };

  return (
    <Stack direction={"row"} sx={{ p: 3 }} gap={2}>
      <GameCard game={snowRunner} />
      <GameCard game={asc} />
      <GameCard game={silksong} />
    </Stack>
  );
}
