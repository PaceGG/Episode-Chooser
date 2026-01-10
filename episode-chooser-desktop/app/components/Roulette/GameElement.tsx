import { Box, Divider } from "@mui/material";
import { Game } from "../GamesInfo/GameCard";

interface GameElementProps {
  game: Game;
  width: number;

  isWinner?: boolean;
}

export default function GameElement({
  game,
  width,
  isWinner = false,
}: GameElementProps) {
  return (
    <>
      <Box
        sx={{
          width: width,
          bgcolor: isWinner ? "green" : game.color,
          height: "100%",
          flexShrink: 0,
        }}
      >
        {game.title}
      </Box>
      {/* <Divider orientation="vertical" /> */}
    </>
  );
}
