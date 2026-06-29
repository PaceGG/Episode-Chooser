import { Box, Button, Paper, Stack } from "@mui/material";
import { Game } from "../components/GamesInfo/GameCard";
import Roulette from "../components/Roulette/Roulette";

export default function RoulettePage() {
  const asc: Game = {
    id: 0,
    color: "#f00",
    title: "Assassin’s Creed Revelations",
    time: 84,
    limit: 5,
    quote: 1,
    // forced: true,
  };

  const silksong: Game = {
    id: 1,
    color: "#00f",
    title: "Hollow Knight: Silksong",
    time: 120,
    limit: -5,
    quote: 1,
  };

  return (
    <Box>
      <Roulette games={[asc, silksong]} elementWidth={300} />
    </Box>
  );
}
