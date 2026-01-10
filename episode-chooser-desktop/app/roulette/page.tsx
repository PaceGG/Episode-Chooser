import { Box, Button, Paper, Stack } from "@mui/material";
import { Game } from "../components/GamesInfo/GameCard";
import Roulette from "../components/Roulette/Roulette";

export default function RoulettePage() {
  const asc: Game = {
    color: "#f00",
    title: "Assassin’s Creed Revelations",
    time: 84,
    limit: 5,
    quote: 3,
    // forced: true,
  };

  const silksong: Game = {
    color: "#00f",
    title: "Hollow Knight: Silksong",
    time: 120,
    limit: -5,
    quote: 1,
  };

  return (
    <Box>
      <Paper sx={{ width: 1000, height: 200, overflow: "hidden" }}>
        <Roulette games={[asc, silksong]} elementWidth={300} />
      </Paper>
      <Button>Spin</Button>
    </Box>
  );
}
