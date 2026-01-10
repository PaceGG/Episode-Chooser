"use client";

import { Stack, Button, Box } from "@mui/material";
import { useMemo, useRef, useState } from "react";
import GameElement from "./GameElement";
import { Game } from "../GamesInfo/GameCard";
import { GameRoulette } from "@/app/roulette/types";
import { PlayArrow } from "@mui/icons-material";

interface RouletteProps {
  games: Game[];
  elementWidth: number;
}

function rand(min: number, max: number) {
  return Math.random() * (max - min) + min;
}

function createSpinAnimation(from: number, to: number, duration: number) {
  const fastEnd = rand(15, 25);
  const linearEnd = rand(60, 75);

  const name = `spin_${Date.now()}`;

  const style = document.createElement("style");
  style.innerHTML = `
    @keyframes ${name} {
      0% {
        margin-left: -${from}px;
        animation-timing-function: cubic-bezier(0.00,0.84,0.29,0.99)
      }

      ${fastEnd}% {
        margin-left: -${to * 0.4}
        animation-timing-function: cubic-bezier(0.12,0.80,0.76,0.99)
      }

      ${linearEnd}% {
        margin-left: -${to * 0.85}
        animation-timing-function: linear;
      }

      100% {
        margin-left: -${to}px;
        animation-timing-function: cubic-bezier(0.25, 1, 0.1, 1);
      }
    }
  `;

  document.head.appendChild(style);

  return { name, duration };
}

export default function Roulette({ games, elementWidth }: RouletteProps) {
  const [isSpinning, setIsSpinning] = useState(false);
  const [animation, setAnimation] = useState<string | null>(null);

  const roulette = useMemo(() => {
    return new GameRoulette(games, elementWidth);
  }, [games, elementWidth]);

  const handleSpin = () => {
    if (isSpinning) return;

    setIsSpinning(true);

    const target =
      roulette.winnerId * elementWidth + roulette.winnerPosition - 500;

    const duration = rand(10, 20);

    const anim = createSpinAnimation(0, target, duration);

    setAnimation(`${anim.name} ${duration}s forwards`);

    setTimeout(() => {
      setIsSpinning(false);
    }, duration * 1000);
  };

  return (
    <div
      style={{
        height: "100%",
        display: "flex",
        flexDirection: "column",
        overflow: "hidden",
      }}
    >
      <Stack sx={{ alignItems: "center" }}>
        <PlayArrow sx={{ rotate: "90deg" }} />
      </Stack>
      <Stack
        direction={"row"}
        sx={{
          overflow: "hidden",
          height: "100%",
          position: "relative",
          willChange: "margin-left",
          animation,
        }}
      >
        {roulette.elements.map((e, i) => (
          <GameElement key={i} game={e} width={elementWidth} />
        ))}
      </Stack>
      <Stack sx={{ alignItems: "center" }}>
        <PlayArrow sx={{ rotate: "-90deg" }} />
      </Stack>

      <Button
        variant="contained"
        onClick={handleSpin}
        disabled={isSpinning}
        sx={{ mb: 2, alignSelf: "center" }}
      >
        {isSpinning ? "Крутится..." : "Крутить рулетку!"}
      </Button>
    </div>
  );
}
