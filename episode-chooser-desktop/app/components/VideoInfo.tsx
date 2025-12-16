"use client";

import React from "react";
import {
  Paper,
  Typography,
  Chip,
  Stack,
  Box,
  useTheme,
  alpha,
  keyframes,
} from "@mui/material";
import { styled } from "@mui/material/styles";
import {
  VideoLibrary,
  DeleteOutline,
  CheckCircle,
  Warning,
} from "@mui/icons-material";

// Типы
interface VideoCardProps {
  number: number;
  text: string;
  type: "onDisk" | "toDelete";
  isCritical?: boolean;
}

interface VideoInfoProps {
  onDisk: number;
  toDelete: number;
  isLoading?: boolean;
  criticalThreshold?: number;
}

// Анимации
const fadeIn = keyframes`
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
`;

const pulseSubtle = keyframes`
  0% { box-shadow: 0 0 0 0 ${alpha("#1976d2", 0.4)}; }
  70% { box-shadow: 0 0 0 6px ${alpha("#1976d2", 0)}; }
  100% { box-shadow: 0 0 0 0 ${alpha("#1976d2", 0)}; }
`;

const StyledPaper = styled(Paper, {
  shouldForwardProp: (prop) => prop !== "type" && prop !== "isCritical",
})<{ type: "onDisk" | "toDelete"; isCritical?: boolean }>(
  ({ theme, type, isCritical }) => ({
    position: "relative",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "space-evenly",
    width: "100%",
    height: 240,
    padding: 4,
    borderRadius: 4 * 3,
    overflow: "hidden",
    animation: `${fadeIn} 0.6s ease-out`,
    transition: theme.transitions.create(
      ["transform", "box-shadow", "border-color"],
      {
        duration: theme.transitions.duration.standard,
      }
    ),

    // Градиенты в зависимости от типа
    background:
      type === "onDisk"
        ? `linear-gradient(135deg, 
          ${alpha(theme.palette.primary.light, 0.15)} 0%, 
          ${alpha(theme.palette.primary.main, 0.08)} 100%)`
        : `linear-gradient(135deg, 
          ${alpha(theme.palette.secondary.light, 0.15)} 0%, 
          ${alpha(theme.palette.secondary.main, 0.08)} 100%)`,

    border: `2px solid ${
      type === "onDisk"
        ? alpha(theme.palette.primary.main, 0.2)
        : alpha(theme.palette.secondary.main, 0.2)
    }`,

    // Эффект для критического состояния
    ...(isCritical && {
      borderColor: alpha(theme.palette.error.main, 0.3),
      background: `linear-gradient(135deg, 
        ${alpha(theme.palette.error.light, 0.1)} 0%, 
        ${alpha(theme.palette.error.main, 0.05)} 100%)`,
      animation: `${pulseSubtle} 2s infinite`,
    }),

    "&::before": {
      content: '""',
      position: "absolute",
      top: 0,
      left: 0,
      right: 0,
      height: 4,
      background:
        type === "onDisk"
          ? `linear-gradient(90deg, 
            ${theme.palette.primary.main}, 
            ${theme.palette.primary.light})`
          : `linear-gradient(90deg, 
            ${theme.palette.secondary.main}, 
            ${theme.palette.secondary.light})`,
      ...(isCritical && {
        background: `linear-gradient(90deg, 
          ${theme.palette.error.main}, 
          ${theme.palette.error.light})`,
      }),
    },
  })
);

const NumberContainer = styled(Box)(({ theme }) => ({
  position: "relative",
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  marginBottom: theme.spacing(3),
}));

const StyledNumber = styled(Typography)(({ theme }) => ({
  fontSize: "4.5rem",
  fontWeight: 800,
  lineHeight: 1,
  background: `linear-gradient(135deg, 
    ${theme.palette.text.primary}, 
    ${alpha(theme.palette.text.primary, 0.8)})`,
  backgroundClip: "text",
  WebkitBackgroundClip: "text",
  color: "transparent",
  textShadow: `0 2px 10px ${alpha(theme.palette.common.black, 0.1)}`,
}));

const IconContainer = styled(Box)(({ theme }) => ({
  position: "absolute",
  top: -theme.spacing(2),
  right: -theme.spacing(2),
  width: 48,
  height: 48,
  borderRadius: "50%",
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  backgroundColor: theme.palette.background.paper,
  boxShadow: theme.shadows[3],
  border: `2px solid ${theme.palette.background.paper}`,
}));

const StyledChip = styled(Chip, {
  shouldForwardProp: (prop) => prop !== "type" && prop !== "isCritical",
})<{ type: "onDisk" | "toDelete"; isCritical?: boolean }>(
  ({ theme, type, isCritical }) => ({
    padding: theme.spacing(1, 2),
    height: "auto",
    fontSize: "1rem",
    fontWeight: 600,
    borderRadius: 4 * 2,
    backgroundColor:
      type === "onDisk"
        ? alpha(theme.palette.primary.main, 0.1)
        : alpha(theme.palette.secondary.main, 0.1),
    color:
      type === "onDisk"
        ? theme.palette.primary.dark
        : theme.palette.secondary.dark,
    border: `1px solid ${
      type === "onDisk"
        ? alpha(theme.palette.primary.main, 0.3)
        : alpha(theme.palette.secondary.main, 0.3)
    }`,
    ...(isCritical && {
      backgroundColor: alpha(theme.palette.error.main, 0.1),
      color: theme.palette.error.dark,
      borderColor: alpha(theme.palette.error.main, 0.3),
    }),

    "& .MuiChip-label": {
      padding: theme.spacing(0.5, 1),
    },
  })
);

const StatusIndicator = styled(Box)(({ theme }) => ({
  display: "flex",
  alignItems: "center",
  marginTop: theme.spacing(2),
  padding: theme.spacing(1, 2),
  borderRadius: 4 * 2,
  backgroundColor: alpha(theme.palette.success.main, 0.1),
  border: `1px solid ${alpha(theme.palette.success.main, 0.2)}`,
}));

// Компонент карточки
const VideoCard: React.FC<VideoCardProps> = ({
  number,
  text,
  type,
  isCritical,
}) => {
  const theme = useTheme();

  const getIcon = () => {
    if (type === "onDisk") {
      return (
        <VideoLibrary
          sx={{ color: theme.palette.primary.main, fontSize: 28 }}
        />
      );
    }
    return isCritical ? (
      <Warning sx={{ color: theme.palette.error.main, fontSize: 28 }} />
    ) : (
      <DeleteOutline
        sx={{ color: theme.palette.secondary.main, fontSize: 28 }}
      />
    );
  };

  return (
    <StyledPaper
      type={type}
      isCritical={isCritical}
      elevation={2}
      role="article"
      aria-label={`${text}: ${number} файлов`}
    >
      <NumberContainer>
        <StyledNumber variant="h1">{number.toLocaleString()}</StyledNumber>
      </NumberContainer>
      <IconContainer sx={{ top: 12, left: 10 }}>{getIcon()}</IconContainer>

      <StyledChip
        type={type}
        isCritical={isCritical}
        label={text}
        aria-hidden="true"
      />

      {type === "toDelete" && number > 0 && (
        <StatusIndicator>
          <CheckCircle
            sx={{
              color: theme.palette.success.main,
              fontSize: 16,
              mr: 1,
            }}
          />
          <Typography
            variant="caption"
            sx={{
              color: theme.palette.success.dark,
              fontWeight: 600,
              fontSize: "0.75rem",
            }}
          >
            Требует внимания
          </Typography>
        </StatusIndicator>
      )}
    </StyledPaper>
  );
};

// Основной компонент
const VideoInfo: React.FC<VideoInfoProps> = ({
  onDisk,
  toDelete,
  isLoading = false,
  criticalThreshold = 10,
}) => {
  const theme = useTheme();
  const isCritical = toDelete >= criticalThreshold;

  if (isLoading) {
    return (
      <Stack direction="row" gap={3} minWidth={600}>
        {[1, 2].map((i) => (
          <Paper
            key={i}
            sx={{
              width: "100%",
              height: 240,
              borderRadius: 4 * 3,
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center",
              backgroundColor: alpha(theme.palette.grey[200], 0.5),
            }}
          >
            <Box
              sx={{
                width: 120,
                height: 60,
                borderRadius: 2,
                backgroundColor: alpha(theme.palette.grey[300], 0.8),
                mb: 3,
              }}
            />
            <Box
              sx={{
                width: 160,
                height: 32,
                borderRadius: 16,
                backgroundColor: alpha(theme.palette.grey[300], 0.8),
              }}
            />
          </Paper>
        ))}
      </Stack>
    );
  }

  return (
    <Stack
      direction="row"
      gap={3}
      minWidth={470}
      sx={{
        "& > *": {
          flex: 1,
        },
      }}
    >
      <VideoCard number={onDisk} text="Видео на диске" type="onDisk" />
      <VideoCard
        number={toDelete}
        text="из них к удалению"
        type="toDelete"
        isCritical={isCritical}
      />
    </Stack>
  );
};

export default React.memo(VideoInfo);
