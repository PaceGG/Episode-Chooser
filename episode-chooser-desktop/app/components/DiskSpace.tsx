"use client";

import {
  Paper,
  Typography,
  LinearProgress,
  Box,
  IconButton,
  Skeleton,
  useTheme,
  alpha,
  keyframes,
  Stack,
} from "@mui/material";
import { styled } from "@mui/material/styles";
import {
  DeleteOutline,
  InfoOutlined,
  StorageOutlined,
  VideocamOutlined,
  VideoLibrary,
  WarningAmberRounded,
} from "@mui/icons-material";
import React, { useMemo } from "react";
import { CardContainer } from "./GamesInfo/GameCard";

// Типы
interface DiskSpaceProps {
  use: number;
  total: number;
  videoOnDisk: number;
  videoToDel: number;
  averageVideoSize?: number;
  isLoading?: boolean;
  onDetailsClick?: () => void;
}

// Анимации
const pulse = keyframes`
  0% { opacity: 1; }
  50% { opacity: 0.7; }
  100% { opacity: 1; }
`;

const StyledPaper = styled(Paper)(({ theme }) => ({
  position: "relative",
  overflow: "hidden",
  transition: theme.transitions.create(["transform", "box-shadow"], {
    duration: theme.transitions.duration.standard,
  }),

  "&:focus-within": {
    outline: `2px solid ${alpha(theme.palette.primary.main, 0.5)}`,
    outlineOffset: 2,
  },
}));

const ProgressContainer = styled(Box)(({ theme }) => ({
  position: "relative",
  marginTop: theme.spacing(2),
  marginBottom: theme.spacing(2),
}));

const ProgressLabel = styled(Typography)(({ theme }) => ({
  position: "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  color: theme.palette.getContrastText(theme.palette.primary.main),
  fontWeight: 700,
  textShadow: "0 1px 2px rgba(0,0,0,0.3)",
  fontSize: theme.typography.pxToRem(12),
}));

const StorageIcon = styled(StorageOutlined, {
  shouldForwardProp: (prop) => prop !== "status",
})<{ status: "normal" | "warning" | "critical" }>(({ theme, status }) => ({
  color:
    status === "normal"
      ? theme.palette.success.main
      : status === "warning"
      ? theme.palette.warning.main
      : theme.palette.error.main,
  marginRight: theme.spacing(1.5),
  animation: `${pulse} 2s ease-in-out infinite`,
  fontSize: 20,
  [theme.breakpoints.up("sm")]: {
    fontSize: 24,
  },
}));

// Компонент
const DiskSpace: React.FC<DiskSpaceProps> = ({
  use,
  total,
  videoOnDisk,
  videoToDel,
  averageVideoSize = 40,
  isLoading = false,
  onDetailsClick,
}) => {
  const theme = useTheme();

  // Мемоизированные вычисления
  const { value, remaining, videoCount, status, isCritical } = useMemo(() => {
    const computedValue = (use / total) * 100;
    const computedRemaining = total - use;
    const computedVideoCount = Math.floor(computedRemaining / averageVideoSize);

    let computedStatus: "normal" | "warning" | "critical" = "normal";
    if (computedRemaining < 90) computedStatus = "critical";
    else if (computedRemaining < 140) computedStatus = "warning";

    return {
      value: computedValue,
      remaining: computedRemaining,
      videoCount: computedVideoCount,
      status: computedStatus,
      isCritical: computedRemaining < 90,
    };
  }, [use, total, averageVideoSize]);

  // Цвет прогресс-бара в зависимости от статуса
  const progressColor = useMemo(() => {
    if (isCritical) return "error";
    if (status === "warning") return "warning";
    return "primary";
  }, [status, isCritical]);

  // Форматирование чисел
  const formatGB = (gb: number) => {
    if (gb >= 1000) return `${(gb / 1000).toFixed(1)} TB`;
    return `${gb.toFixed(1)} GB`;
  };

  if (isLoading) {
    return (
      <StyledPaper elevation={2} sx={{ p: { xs: 2, sm: 3 } }}>
        <Skeleton variant="text" width="60%" height={28} />
        <Skeleton
          variant="rectangular"
          height={8}
          sx={{ my: 2, borderRadius: 1 }}
        />
        <Skeleton variant="text" width="40%" height={24} sx={{ ml: "auto" }} />
      </StyledPaper>
    );
  }

  return (
    <CardContainer
      sx={{
        p: { xs: 2, sm: 3 },
        background: `linear-gradient(135deg, 
          ${alpha(theme.palette.background.paper, 0.9)} 0%, 
          ${alpha(theme.palette.background.default, 0.7)} 100%
        )`,
        backdropFilter: "blur(10px)",
        width: 420,
      }}
      role="region"
      aria-label="Информация о дисковом пространстве"
    >
      {/* Заголовок */}
      <Box
        sx={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          mb: 2,
        }}
      >
        <Box sx={{ display: "flex", alignItems: "center" }}>
          <StorageIcon status={status} />
          <Typography
            variant="h6"
            component="h2"
            sx={{
              fontWeight: 600,
              fontSize: { xs: "1rem", sm: "1.25rem" },
              color: theme.palette.text.primary,
              mr: 0.5,
            }}
          >
            Место на диске
          </Typography>
        </Box>

        <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
          {isCritical && (
            <WarningAmberRounded
              sx={{
                color: theme.palette.error.main,
                fontSize: { xs: 18, sm: 20 },
                animation: `${pulse} 1s ease-in-out infinite`,
              }}
              aria-label="Предупреждение"
            />
          )}
          {onDetailsClick && (
            <IconButton
              size="small"
              onClick={onDetailsClick}
              aria-label="Подробная информация о дисковом пространстве"
              sx={{
                "&:focus-visible": {
                  outline: `2px solid ${theme.palette.primary.main}`,
                },
                transition: theme.transitions.create([
                  "transform",
                  "background-color",
                ]),
              }}
            >
              <InfoOutlined fontSize="small" />
            </IconButton>
          )}
        </Box>
      </Box>

      {/* Прогресс бар */}
      <ProgressContainer>
        <LinearProgress
          variant="determinate"
          color={progressColor}
          value={value}
          sx={{
            height: 16,
            borderRadius: 12,
            backgroundColor: alpha(theme.palette.grey[300], 0.5),
            "& .MuiLinearProgress-bar": {
              borderRadius: 12,
            },
          }}
          aria-label={`Использовано ${value.toFixed(
            1
          )}% дискового пространства`}
        />
        <ProgressLabel variant="caption">{value.toFixed(1)}%</ProgressLabel>
      </ProgressContainer>

      {/* Информация о свободном месте */}
      <Box
        sx={{
          display: "flex",
          flexDirection: { xs: "column", sm: "row" },
          justifyContent: "space-between",
          alignItems: { xs: "flex-start", sm: "center" },
          gap: 2,
          mt: 3,
        }}
      >
        <Box sx={{ display: "flex", alignItems: "center" }}>
          <VideocamOutlined
            sx={{
              color: theme.palette.secondary.main,
              mr: 1,
              fontSize: { xs: 18, sm: 20 },
            }}
            aria-hidden="true"
          />
          <Typography
            variant="body2"
            sx={{
              color: theme.palette.text.secondary,
              fontWeight: 500,
            }}
          >
            <Box
              component="span"
              sx={{
                color: isCritical
                  ? theme.palette.error.main
                  : theme.palette.success.main,
                fontWeight: 700,
                fontSize: { xs: "1rem", sm: "1.1rem" },
              }}
            >
              {formatGB(remaining)}
            </Box>{" "}
            свободно
          </Typography>
        </Box>

        <Typography
          variant="body2"
          sx={{
            textAlign: { xs: "left", sm: "right" },
            color: theme.palette.text.secondary,
            bgcolor: alpha(theme.palette.primary.main, 0.08),
            px: 2,
            py: 1,
            borderRadius: theme.shape.borderRadius,
            transition: theme.transitions.create("background-color"),
          }}
        >
          ~{" "}
          <Box component="span" sx={{ fontWeight: 700 }}>
            {videoCount}
          </Box>{" "}
          {videoCount === 1
            ? "видео"
            : videoCount >= 2 && videoCount <= 4
            ? "видео"
            : "видео"}{" "}
        </Typography>
      </Box>

      {(videoToDel > 0 || videoOnDisk > 0) && (
        <Stack
          direction={"row"}
          alignItems={"center"}
          justifyContent={"space-between"}
          mt={2}
        >
          <Box>
            <VideoLibrary
              sx={{ color: theme.palette.primary.main, fontSize: 28, mr: 1 }}
            />
            {videoOnDisk} видео на диске
          </Box>
          <Box>
            из них к удалению {videoToDel}
            <DeleteOutline
              sx={{ color: theme.palette.error.main, fontSize: 28, ml: 1 }}
            />
          </Box>
        </Stack>
      )}
    </CardContainer>
  );
};

// Оптимизация ререндеров
export default React.memo(DiskSpace);
