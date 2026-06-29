"use client";

import { Stack, Button, Box, Typography, Fade } from "@mui/material";
import { useState, useRef, useEffect } from "react";
import GameElement from "./GameElement";
import { Game } from "../GamesInfo/GameCard";
import { PlayArrow } from "@mui/icons-material";

interface RouletteProps {
  games: Game[];
  elementWidth: number;
  elementHeight?: number;
}

function getRandomInt(min: number, max: number) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

const sleep = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

function chooseWinner(games: Game[]): Game {
  const totalWeight = games.reduce((sum, game) => sum + (game.quote || 1), 0);
  let randomNum = Math.random() * totalWeight;

  for (const game of games) {
    const weight = game.quote || 1;
    if (randomNum < weight) return game;
    randomNum -= weight;
  }
  return games[0];
}

export default function Roulette({
  games,
  elementWidth,
  elementHeight = 60,
}: RouletteProps) {
  const [isSpinning, setIsSpinning] = useState(false);
  const [rouletteItems, setRouletteItems] = useState<Game[]>([]);
  const [currentStep, setCurrentStep] = useState(0);
  const [isBlinking, setIsBlinking] = useState(false);
  const [blinkShow, setBlinkShow] = useState(true);
  const [winner, setWinner] = useState<Game | null>(null);
  const [showFinalChance, setShowFinalChance] = useState(false);

  const isMounted = useRef(true);

  useEffect(() => {
    isMounted.current = true;
    return () => {
      isMounted.current = false;
    };
  }, []);

  const TOTAL_LINES = 11;
  const SCREEN_SIZE = TOTAL_LINES + (TOTAL_LINES % 2 === 0 ? 1 : 0);
  const HALF_SCREEN = Math.floor(SCREEN_SIZE / 2);

  const handleSpin = async () => {
    if (isSpinning || games.length === 0) return;

    setIsSpinning(true);
    setIsBlinking(false);
    setBlinkShow(true);
    setWinner(null);
    setShowFinalChance(false);

    const pattern = [
      getRandomInt(30, 50),
      getRandomInt(5, 10),
      getRandomInt(3, 5),
      1,
    ];

    const totalStepsNeeded = 50 + 10 + 5 + 1 + HALF_SCREEN;
    const generatedRoulette: Game[] = Array.from(
      { length: totalStepsNeeded },
      () => chooseWinner(games),
    );

    const winner = chooseWinner(games);
    const winnerIndex = pattern.reduce((a, b) => a + b, 0) - 1;
    generatedRoulette[winnerIndex] = winner;

    setRouletteItems(generatedRoulette);
    setCurrentStep(0);

    const initialSleepTime = 0.05;
    const maxSleepTime = 0.5;

    let stepCounter = 0;

    // ФАЗА 0: Разгон
    const phase0Target = pattern[0] - HALF_SCREEN;
    for (let i = 0; i < phase0Target; i++) {
      if (!isMounted.current) return;
      setCurrentStep(stepCounter);
      const progress = i / pattern[0];
      const sleepTime =
        initialSleepTime +
        (maxSleepTime - initialSleepTime) * Math.pow(progress, 2);
      await sleep(sleepTime * 1000);
      stepCounter++;
    }

    // ФАЗА 1: Медленный ход
    for (let i = 0; i < pattern[1]; i++) {
      if (!isMounted.current) return;
      setCurrentStep(stepCounter);
      await sleep(maxSleepTime * 1000);
      stepCounter++;
    }

    // ФАЗА 2: Предфинальная - здесь проверяем "Финальный шанс"
    for (let i = 0; i < pattern[2]; i++) {
      if (!isMounted.current) return;
      setCurrentStep(stepCounter);

      // Проверяем, будет ли "Финальный шанс"
      const currentWinner = generatedRoulette[stepCounter + HALF_SCREEN - 1];
      const nextWinner = generatedRoulette[stepCounter + HALF_SCREEN];
      const isFinalChance = currentWinner.id !== nextWinner.id;

      // Если это последний шаг фазы 2 и есть финальный шанс
      if (i === pattern[2] - 1 && isFinalChance) {
        setShowFinalChance(true);
        await sleep(maxSleepTime * 2 * 1000);
      } else {
        await sleep(maxSleepTime * 2 * 1000);
      }
      stepCounter++;
    }

    // ФАЗА 3: Финальный докат
    for (let i = 0; i < pattern[3]; i++) {
      if (!isMounted.current) return;
      setCurrentStep(stepCounter);
      await sleep(maxSleepTime * 1000);
      stepCounter++;
    }

    // Скрываем "Финальный шанс" после завершения
    setShowFinalChance(false);

    const finalWinner = generatedRoulette[stepCounter + HALF_SCREEN - 1];
    setCurrentStep(stepCounter);
    setWinner(finalWinner);

    // БЛИНК
    setIsBlinking(true);
    for (let frame = 0; frame < 10; frame++) {
      if (!isMounted.current) return;
      setBlinkShow(frame % 2 !== 0);
      await sleep(500);
    }

    setIsBlinking(false);
    setIsSpinning(false);
  };

  const visibleElements = rouletteItems.slice(
    currentStep,
    currentStep + SCREEN_SIZE,
  );

  // Дополняем элементы если не хватает
  while (visibleElements.length < SCREEN_SIZE) {
    visibleElements.push(chooseWinner(games));
  }

  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        width: "100%",
        gap: 2,
      }}
    >
      {/* Контейнер рулетки */}
      <Stack
        direction="column"
        sx={{
          overflow: "hidden",
          width: elementWidth + 80,
          border: "2px solid #333",
          borderRadius: 2,
          backgroundColor: "#1a1a1a",
          position: "relative",
          justifyContent: "center",
          minHeight: elementHeight * SCREEN_SIZE,
          boxShadow: winner ? "0 0 30px rgba(255, 215, 0, 0.2)" : "none",
          transition: "box-shadow 0.5s ease",
        }}
      >
        {/* Оверлей "Финальный шанс" */}
        <Fade in={showFinalChance} timeout={500}>
          <Box
            sx={{
              position: "absolute",
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              backgroundColor: "rgba(0, 0, 0, 0.7)",
              zIndex: 10,
              borderRadius: 2,
            }}
          >
            <Typography
              sx={{
                color: "#ffd700",
                fontSize: "2.5rem",
                fontWeight: "bold",
                textShadow:
                  "0 0 20px rgba(255, 215, 0, 0.5), 0 0 40px rgba(255, 215, 0, 0.3)",
                animation: "pulse 0.5s ease-in-out infinite",
                "@keyframes pulse": {
                  "0%, 100%": {
                    transform: "scale(1)",
                    opacity: 1,
                  },
                  "50%": {
                    transform: "scale(1.1)",
                    opacity: 0.8,
                  },
                },
              }}
            >
              🎯 ФИНАЛЬНЫЙ ШАНС!
            </Typography>
          </Box>
        </Fade>

        {visibleElements.map((game, i) => {
          const isCenter = i === HALF_SCREEN;
          const isWinner = winner && isCenter && !isSpinning;

          const shouldHide = isBlinking && isCenter && !blinkShow;

          return (
            <Box
              key={`${game.id}-${currentStep + i}`}
              sx={{
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                height: elementHeight,
                width: "100%",
                opacity: shouldHide ? 0 : 1,
                backgroundColor: isWinner
                  ? "rgba(255, 215, 0, 0.1)"
                  : "transparent",
                borderBottom:
                  i < visibleElements.length - 1 ? "1px solid #333" : "none",
                transition: "all 0.3s ease",
                position: "relative",
              }}
            >
              {/* Левый указатель */}
              {isCenter && (
                <PlayArrow
                  sx={{
                    position: "absolute",
                    left: 8,
                    color: isWinner ? "#ffd700" : "#666",
                    transform: "rotate(0deg)",
                    fontSize: 24,
                    transition: "color 0.3s ease",
                  }}
                />
              )}

              <Box sx={{ width: elementWidth }}>
                <GameElement
                  game={game}
                  width={elementWidth}
                  // highlight={isCenter && !isSpinning && !isBlinking}
                />
              </Box>

              {/* Правый указатель */}
              {isCenter && (
                <PlayArrow
                  sx={{
                    position: "absolute",
                    right: 8,
                    color: isWinner ? "#ffd700" : "#666",
                    transform: "rotate(180deg)",
                    fontSize: 24,
                    transition: "color 0.3s ease",
                  }}
                />
              )}
            </Box>
          );
        })}
      </Stack>

      {/* Информация о победителе */}
      {winner && !isSpinning && !isBlinking && (
        <Typography
          sx={{
            color: "#ffd700",
            fontWeight: "bold",
            fontSize: "1.2rem",
            animation: "pulse 1s ease-in-out infinite",
            "@keyframes pulse": {
              "0%, 100%": { opacity: 1 },
              "50%": { opacity: 0.5 },
            },
          }}
        >
          🎉 Победитель: {winner.title}!
        </Typography>
      )}

      <Button
        variant="contained"
        onClick={handleSpin}
        disabled={isSpinning || games.length === 0}
        sx={{
          minWidth: "180px",
          background: isSpinning
            ? "linear-gradient(45deg, #666 30%, #888 90%)"
            : "linear-gradient(45deg, #FE6B8B 30%, #FF8E53 90%)",
          color: "#fff",
          "&:hover": {
            background: isSpinning
              ? "linear-gradient(45deg, #666 30%, #888 90%)"
              : "linear-gradient(45deg, #FF8E53 30%, #FE6B8B 90%)",
          },
        }}
      >
        {isSpinning ? "🎰 Крутится..." : "🎰 Крутить рулетку!"}
      </Button>
    </Box>
  );
}
