import { Box, Stack, Typography } from "@mui/material";
import DiskSpace from "./components/DiskSpace";
import VideoInfo from "./components/VideoInfo";
import GamesInfo from "./components/GamesInfo/GamesInfo";
import GameCard, { Game } from "./components/GamesInfo/GameCard";

const snowRunner: Game = {
  color: "#fff000",
  title: "SnowRunner",
  time: 119,
  limit: 40,
  quote: 0,
  srInfo: {
    days: 0,
    date: new Date(1797402548 * 1000),
  },
};

const asc: Game = {
  color: "#f00",
  title: "Assassin’s Creed Revelations",
  time: 84,
  limit: 5,
  quote: 1,
  // forced: true,
};

const silksong: Game = {
  color: "#00f",
  title: "Hollow Knight: Silksong",
  time: 120,
  limit: -5,
  quote: 0,
};

export default function Home() {
  return (
    <Stack
      flexDirection={"row"}
      gap={2}
      flexWrap={"wrap"}
      justifyContent={"center"}
      maxWidth={800}
    >
      <DiskSpace use={33} total={977} videoOnDisk={1} videoToDel={1} />
      <GameCard game={snowRunner} />
      <GameCard game={asc} />
      <GameCard game={silksong} />
    </Stack>
  );
}
