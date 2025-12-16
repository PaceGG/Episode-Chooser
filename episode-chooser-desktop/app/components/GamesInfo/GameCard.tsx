"use client";

import React, { useMemo, useState } from "react";
import {
  Box,
  Typography,
  Chip,
  Paper,
  alpha,
  keyframes,
  Fade,
} from "@mui/material";
import { styled } from "@mui/material/styles";
import {
  TimerOutlined,
  TrendingUp,
  TrendingDown,
  Remove,
  ArrowUpward,
  ArrowDownward,
} from "@mui/icons-material";
import Image from "next/image";

// Типы
export interface Game {
  color: string;
  title: string;
  time: number;
  limit: number;
  quote: number;
  forced?: boolean;
}

interface GameCardProps {
  game: Game;
}

// Анимации
const pulse = keyframes`
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
`;

const slideIn = keyframes`
  from { transform: translateX(-20px); opacity: 0; }
  to { transform: translateX(0); opacity: 1; }
`;

// Стилизованные компоненты
const CardContainer = styled(Paper, {
  shouldForwardProp: (prop) => prop !== "forced",
})<{ forced?: boolean }>(({ theme, forced }) => ({
  position: "relative",
  overflow: "hidden",
  width: 320,
  borderRadius: 12,

  background: `linear-gradient(145deg,
    ${theme.palette.background.paper} 0%,
    ${alpha(theme.palette.background.default, 0.7)} 100%)`,

  border: forced
    ? `1.5px solid ${alpha(theme.palette.error.main, 0.8)}`
    : `1px solid ${alpha(theme.palette.divider, 0.2)}`,

  boxShadow: forced
    ? `
      0 0 0 1px ${alpha(theme.palette.error.main, 0.4)},
      0 8px 24px ${alpha(theme.palette.error.main, 0.35)}
    `
    : theme.shadows[4],

  transition: theme.transitions.create(["transform", "box-shadow", "border"], {
    duration: theme.transitions.duration.standard,
  }),

  // внутренняя подсветка
  ...(forced && {
    "&::after": {
      content: '""',
      position: "absolute",
      inset: 0,
      borderRadius: 12,
      pointerEvents: "none",
      background: `linear-gradient(
        180deg,
        ${alpha(theme.palette.error.main, 0.12)} 0%,
        transparent 40%
      )`,
    },
  }),
}));

const HeaderSection = styled(Box, {
  shouldForwardProp: (prop) => prop !== "accentColor",
})<{ accentColor: string }>(({ theme, accentColor }) => ({
  position: "relative",
  borderBottom: `3px solid ${accentColor}`,
}));

const InfoSection = styled(Box)(({ theme }) => ({
  paddingTop: 8,
  paddingBottom: 8,
  gap: 16,
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  // height: "calc(100% - 80px)",
  background: `linear-gradient(to bottom, 
    transparent 0%, 
    ${alpha(theme.palette.background.paper, 0.8)} 100%)`,
}));

const TimeContainer = styled(Box)(({ theme }) => ({
  display: "flex",
  alignItems: "center",
  gap: theme.spacing(1),
}));

const TimeText = styled(Typography, {
  shouldForwardProp: (prop) => prop !== "isNegative",
})<{ isNegative: boolean }>(({ theme, isNegative }) => ({
  fontSize: "1.75rem",
  fontWeight: 800,
  background: isNegative
    ? `linear-gradient(135deg, 
        ${theme.palette.error.main} 0%, 
        ${theme.palette.error.light} 100%)`
    : `linear-gradient(135deg, 
        ${theme.palette.success.main} 0%, 
        ${theme.palette.success.light} 100%)`,
  backgroundClip: "text",
  WebkitBackgroundClip: "text",
  textShadow: `0 2px 4px ${alpha(theme.palette.common.black, 0.1)}`,
}));

const QuoteContainer = styled(Box, {
  shouldForwardProp: (prop) => prop !== "value",
})<{ value: number }>(({ theme, value }) => {
  let color;
  let bgColor;

  if (value > 0) {
    color = theme.palette.success.dark;
    bgColor = alpha(theme.palette.success.main, 0.15);
  } else if (value < 0) {
    color = theme.palette.error.dark;
    bgColor = alpha(theme.palette.error.main, 0.15);
  } else {
    color = theme.palette.text.secondary;
    bgColor = alpha(theme.palette.grey[500], 0.1);
  }

  return {
    display: "inline-flex",
    alignItems: "center",
    gap: theme.spacing(0.5),
    padding: theme.spacing(0.75, 2),
    borderRadius: 8 * 5,
    backgroundColor: bgColor,
    border: `1px solid ${alpha(color, 0.3)}`,
    animation: value !== 0 ? `${pulse} 2s ease-in-out infinite` : "none",
  };
});

const QuoteText = styled(Typography)(({ theme }) => ({
  fontSize: "1.125rem",
  fontWeight: 700,
}));

const QuoteIcon = styled(Box)(({ theme }) => ({
  display: "flex",
  alignItems: "center",
  "& svg": {
    fontSize: "1.25rem",
  },
}));

const StatsBadge = styled(Chip)<{ value?: number }>(({ value }) => {
  let bgColor;
  let borderRadius = 20;

  if (value != null) {
    if (value > 0) {
      bgColor = "red";
    } else if (value < 0) {
      bgColor = "error.main";
    }
    borderRadius = 1;
  }

  return {
    fontWeight: 600,
    height: 24,
    borderRadius: borderRadius,
    backgroundColor: bgColor,
  };
});

// Вспомогательные функции
function formatTime(minutes: number): string {
  const isNegative = minutes < 0;
  const absMinutes = Math.abs(minutes);

  const hours = Math.floor(absMinutes / 60);
  const mins = absMinutes % 60;

  return `${isNegative ? "-" : ""}${hours.toString().padStart(2, "0")}:${mins
    .toString()
    .padStart(2, "0")}`;
}

function formatQuote(minutes: number): string {
  return `${minutes > 0 ? "+" : ""}${minutes}`;
}

function formatTitle(title: string) {
  return title.replace(/:/g, "");
}

function getQuoteIcon(quote: number) {
  if (quote > 0) return <ArrowUpward color="success" />;
  if (quote < 0) return <ArrowDownward color="error" />;
  return <Remove color="disabled" />;
}

// Основной компонент
const GameCard: React.FC<GameCardProps> = ({ game }) => {
  const formattedTime = formatTime(game.time);
  const formattedLimit = formatQuote(game.limit);
  const formattedTitle = formatTitle(game.title);
  const isTimeNegative = game.time < 0;

  const [error, setError] = useState(false);

  const headerSrc = `/headers/${formattedTitle}.png`;

  return (
    <Fade in timeout={800}>
      <CardContainer
        elevation={4}
        role="article"
        aria-label={`Статистика игры ${game.title}`}
        forced={game.forced}
      >
        <HeaderSection accentColor={game.color}>
          <Box sx={{ width: "100" }}>
            {!error ? (
              <Image
                src={headerSrc}
                alt={game.title}
                width={600}
                height={100}
                style={{
                  width: "100%",
                }}
                onError={() => setError(true)}
              />
            ) : (
              <Box
                height={100}
                sx={{
                  display: "flex",
                  justifyContent: "center",
                  alignItems: "center",
                }}
              >
                <Typography align="center" variant="h5" color={game.color}>
                  {game.title}
                </Typography>
              </Box>
            )}
          </Box>
        </HeaderSection>

        <InfoSection>
          {/* Блок времени */}
          <TimeContainer>
            <TimerOutlined
              sx={{
                fontSize: "1.5rem",
              }}
              aria-hidden="true"
            />
            <TimeText
              variant="h2"
              isNegative={isTimeNegative}
              aria-label={`Отформатированное время: ${formattedTime}`}
            >
              {formattedTime}
            </TimeText>
            <StatsBadge label={`${Math.abs(game.time)} мин`} />
            <StatsBadge label={formattedLimit} value={game.limit} />
          </TimeContainer>

          {/* Блок цитаты */}
          {game.quote > 1 && (
            <QuoteContainer value={game.quote} role="status">
              <QuoteText sx={{ color: "inherit" }}>x{game.quote}</QuoteText>
            </QuoteContainer>
          )}
        </InfoSection>
      </CardContainer>
    </Fade>
  );
};

export default React.memo(GameCard);
