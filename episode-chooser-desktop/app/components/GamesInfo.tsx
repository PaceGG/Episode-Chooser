import { Box, Paper, Stack, Typography } from "@mui/material";
import Image from "next/image";

interface Game {
  color: string;
  title: string;
  time: number;
  quote: number;
}

interface GameCardProps {
  game: Game;
}

function formatTime(minutes: number): string {
  let isNegative = false;
  if (minutes < 0) {
    minutes *= -1;
    isNegative = true;
  }

  const date = new Date(0);
  date.setMinutes(minutes);

  return `${isNegative ? "-" : ""}${date.toISOString().substring(11, 16)}`;
}

function formatQuote(minutes: number): string {
  return `${minutes > 0 ? "+" : ""}${minutes}`;
}

function GameCard({ game }: GameCardProps) {
  const headerSrc = `/headers/${game.title}.png`;
  const quoteColor =
    game.quote > 0
      ? "success.main"
      : game.quote < 0
      ? "error.main"
      : "text.primary";

  return (
    <Stack>
      <Box sx={{ borderBottom: 2, borderColor: game.color }}>
        <Image src={headerSrc} alt={game.title} width={300} height={100} />
      </Box>
      <Typography sx={{ textAlign: "center" }}>
        {formatTime(game.time)} ({game.time}) | [{" "}
        <Box component={"span"} sx={{ color: quoteColor }}>
          {formatQuote(game.quote)}
        </Box>{" "}
        ]
      </Typography>
    </Stack>
  );
}

export default function GamesInfo() {
  const snowRunner: Game = {
    color: "#fff000",
    title: "SnowRunner",
    time: 109,
    quote: 3,
  };

  return (
    <Paper>
      <GameCard game={snowRunner} />
      {/* <Typography>Game1 card</Typography>
      <Typography>Game2 card</Typography> */}
    </Paper>
  );
}
