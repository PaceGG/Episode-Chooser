import React, { useState, useMemo } from "react";
import {
  Box,
  Container,
  Typography,
  Grid,
  Paper,
  Card,
  CardContent,
  CardHeader,
  Avatar,
  Chip,
  Stack,
  Divider,
  LinearProgress,
  useTheme,
  useMediaQuery,
  IconButton,
  Tooltip,
  Fade,
  Zoom,
  Slide,
} from "@mui/material";
import {
  VideogameAsset as GameIcon,
  AccessTime as TimeIcon,
  CalendarToday as CalendarIcon,
  TrendingUp as TrendingIcon,
  EmojiEvents as TrophyIcon,
  Whatshot as HotIcon,
  Timeline as TimelineIcon,
  BarChart as ChartIcon,
  Psychology as BrainIcon,
  ExpandMore as ExpandMoreIcon,
  ExpandLess as ExpandLessIcon,
  AutoAwesome as SparkleIcon,
} from "@mui/icons-material";
import { keyframes } from "@emotion/react";

// Анимация пульсации
const pulse = keyframes`
  0% {
    box-shadow: 0 0 0 0 rgba(25, 118, 210, 0.4);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(25, 118, 210, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(25, 118, 210, 0);
  }
`;

// Анимация появления
const float = keyframes`
  0% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-10px);
  }
  100% {
    transform: translateY(0px);
  }
`;

const Recap = ({ data }) => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down("md"));
  const [expandedSections, setExpandedSections] = useState({
    games: true,
    daily: true,
    time: true,
    episodes: true,
  });

  const toggleSection = (section) => {
    setExpandedSections((prev) => ({
      ...prev,
      [section]: !prev[section],
    }));
  };

  // Форматирование времени
  const formatDuration = (seconds) => {
    if (seconds < 60) return `${seconds} сек`;
    if (seconds < 3600) return `${Math.floor(seconds / 60)} мин`;
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    return `${hours} ч ${minutes} мин`;
  };

  // Цвета для игр
  const gameColors = useMemo(
    () => ({
      "Assassin’s Creed II": theme.palette.primary.main,
      "Hollow Knight: Silksong": theme.palette.success.main,
      "Assassin’s Creed: Brotherhood": theme.palette.info.main,
      "SnowRunner [ng+]: Таймыр": theme.palette.warning.main,
    }),
    [theme]
  );

  // Данные для графиков
  const gameData = useMemo(
    () =>
      data.game_rankings.by_episodes.map((game) => ({
        ...game,
        color: gameColors[game.game],
        duration: data.games[game.game].total_duration,
      })),
    [data, gameColors]
  );

  // Самый длинный день
  const longestDay = useMemo(() => {
    return data.daily_stats_array.reduce((max, day) =>
      day.duration > max.duration ? day : max
    );
  }, [data]);

  // Расчет прогресса
  const calculateProgress = (value, total) => (value / total) * 100;

  return (
    <Box sx={{ bgcolor: "#eee" }}>
      <Fade in timeout={800}>
        <Container maxWidth="xl" sx={{ py: 4 }}>
          {/* Заголовок */}
          <Zoom in timeout={1000}>
            <Box
              sx={{
                textAlign: "center",
                mb: 6,
                position: "relative",
                "&::after": {
                  content: '""',
                  position: "absolute",
                  bottom: -10,
                  left: "50%",
                  transform: "translateX(-50%)",
                  width: "100px",
                  height: "4px",
                  background: `linear-gradient(90deg, ${theme.palette.primary.main}, ${theme.palette.secondary.main})`,
                  borderRadius: "2px",
                },
              }}
            >
              <Typography
                variant="h2"
                sx={{
                  fontWeight: 800,
                  background: `linear-gradient(45deg, ${theme.palette.primary.main}, ${theme.palette.secondary.main})`,
                  WebkitBackgroundClip: "text",
                  WebkitTextFillColor: "transparent",
                  mb: 1,
                }}
              >
                Итоги месяца
              </Typography>
              <Typography variant="h5" color="text.secondary">
                {data.summary.month} • {data.summary.total_episodes} выпусков •{" "}
                {data.summary.total_duration}
              </Typography>
            </Box>
          </Zoom>

          {/* Основные метрики */}
          <Slide direction="up" in timeout={1200}>
            <Grid container spacing={3} sx={{ mb: 4 }}>
              <Grid item xs={12} sm={6} md={3}>
                <Card
                  sx={{
                    height: "100%",
                    background: `linear-gradient(135deg, ${theme.palette.primary.main}20, ${theme.palette.primary.main}40)`,
                    position: "relative",
                    overflow: "hidden",
                    "&::before": {
                      content: '""',
                      position: "absolute",
                      top: -50,
                      right: -50,
                      width: "100px",
                      height: "100px",
                      background: theme.palette.primary.main,
                      borderRadius: "50%",
                      opacity: 0.1,
                    },
                  }}
                >
                  <CardContent sx={{ position: "relative", zIndex: 1 }}>
                    <Stack direction="row" alignItems="center" spacing={2}>
                      <Avatar
                        sx={{
                          bgcolor: theme.palette.primary.main,
                          animation: `${pulse} 2s infinite`,
                        }}
                      >
                        <GameIcon />
                      </Avatar>
                      <Box>
                        <Typography variant="h3" fontWeight="bold">
                          {data.summary.total_episodes}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          Всего выпусков
                        </Typography>
                      </Box>
                    </Stack>
                  </CardContent>
                </Card>
              </Grid>

              <Grid item xs={12} sm={6} md={3}>
                <Card
                  sx={{
                    height: "100%",
                    background: `linear-gradient(135deg, ${theme.palette.success.main}20, ${theme.palette.success.main}40)`,
                    position: "relative",
                    overflow: "hidden",
                  }}
                >
                  <CardContent sx={{ position: "relative", zIndex: 1 }}>
                    <Stack direction="row" alignItems="center" spacing={2}>
                      <Avatar
                        sx={{
                          bgcolor: theme.palette.success.main,
                          animation: `${float} 3s ease-in-out infinite`,
                        }}
                      >
                        <TimeIcon />
                      </Avatar>
                      <Box>
                        <Typography variant="h3" fontWeight="bold">
                          {data.summary.total_duration.split(" ")[0]}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          Часов контента
                        </Typography>
                      </Box>
                    </Stack>
                  </CardContent>
                </Card>
              </Grid>

              <Grid item xs={12} sm={6} md={3}>
                <Card
                  sx={{
                    height: "100%",
                    background: `linear-gradient(135deg, ${theme.palette.warning.main}20, ${theme.palette.warning.main}40)`,
                    position: "relative",
                    overflow: "hidden",
                  }}
                >
                  <CardContent sx={{ position: "relative", zIndex: 1 }}>
                    <Stack direction="row" alignItems="center" spacing={2}>
                      <Avatar
                        sx={{
                          bgcolor: theme.palette.warning.main,
                          animation: `${float} 3s ease-in-out infinite`,
                          animationDelay: "0.5s",
                        }}
                      >
                        <CalendarIcon />
                      </Avatar>
                      <Box>
                        <Typography variant="h3" fontWeight="bold">
                          {data.progress.days_with_content}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          Активных дней
                        </Typography>
                      </Box>
                    </Stack>
                  </CardContent>
                </Card>
              </Grid>

              <Grid item xs={12} sm={6} md={3}>
                <Card
                  sx={{
                    height: "100%",
                    background: `linear-gradient(135deg, ${theme.palette.info.main}20, ${theme.palette.info.main}40)`,
                    position: "relative",
                    overflow: "hidden",
                  }}
                >
                  <CardContent sx={{ position: "relative", zIndex: 1 }}>
                    <Stack direction="row" alignItems="center" spacing={2}>
                      <Avatar
                        sx={{
                          bgcolor: theme.palette.info.main,
                          animation: `${float} 3s ease-in-out infinite`,
                          animationDelay: "1s",
                        }}
                      >
                        <TrendingIcon />
                      </Avatar>
                      <Box>
                        <Typography variant="h3" fontWeight="bold">
                          {data.progress.streak_days}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          Дней подряд
                        </Typography>
                      </Box>
                    </Stack>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>
          </Slide>

          {/* Статистика по играм */}
          <Paper
            elevation={0}
            sx={{
              p: 3,
              mb: 4,
              borderRadius: 4,
              background: `linear-gradient(145deg, ${theme.palette.background.paper}, ${theme.palette.background.default})`,
              border: `1px solid ${theme.palette.divider}`,
            }}
          >
            <Box
              sx={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                mb: 3,
              }}
            >
              <Stack direction="row" alignItems="center" spacing={2}>
                <TrophyIcon
                  sx={{
                    fontSize: 32,
                    animation: `${float} 2s ease-in-out infinite`,
                  }}
                />
                <Typography variant="h5" fontWeight="bold">
                  Игры месяца
                </Typography>
              </Stack>
              <IconButton onClick={() => toggleSection("games")}>
                {expandedSections.games ? (
                  <ExpandLessIcon />
                ) : (
                  <ExpandMoreIcon />
                )}
              </IconButton>
            </Box>

            <Fade in={expandedSections.games} timeout={500}>
              <Box>
                {gameData.map((game, index) => (
                  <Box key={game.game} sx={{ mb: 3 }}>
                    <Stack
                      direction="row"
                      justifyContent="space-between"
                      alignItems="center"
                      sx={{ mb: 1 }}
                    >
                      <Stack direction="row" alignItems="center" spacing={1}>
                        <Box
                          sx={{
                            width: 12,
                            height: 12,
                            borderRadius: "50%",
                            bgcolor: game.color,
                            animation: `${pulse} 2s infinite`,
                            animationDelay: `${index * 0.2}s`,
                          }}
                        />
                        <Typography variant="h6" fontWeight="600">
                          {game.game}
                        </Typography>
                        <Chip
                          label={`${game.episodes} выпусков`}
                          size="small"
                          sx={{
                            bgcolor: `${game.color}20`,
                            color: game.color,
                          }}
                        />
                      </Stack>
                      <Typography variant="h6" fontWeight="bold">
                        {formatDuration(game.duration)}
                      </Typography>
                    </Stack>
                    <LinearProgress
                      variant="determinate"
                      value={calculateProgress(
                        game.duration,
                        data.summary.total_duration.split("ч")[0] * 3600
                      )}
                      sx={{
                        height: 8,
                        borderRadius: 4,
                        bgcolor: `${game.color}20`,
                        "& .MuiLinearProgress-bar": {
                          bgcolor: game.color,
                          borderRadius: 4,
                          transition: "transform 1.5s ease-in-out",
                        },
                      }}
                    />
                  </Box>
                ))}
              </Box>
            </Fade>
          </Paper>

          {/* Дневная активность */}
          <Grid container spacing={3} sx={{ mb: 4 }}>
            <Grid item xs={12} md={8}>
              <Paper
                elevation={0}
                sx={{
                  p: 3,
                  height: "100%",
                  borderRadius: 4,
                  background: `linear-gradient(145deg, ${theme.palette.background.paper}, ${theme.palette.background.default})`,
                  border: `1px solid ${theme.palette.divider}`,
                }}
              >
                <Box
                  sx={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    mb: 3,
                  }}
                >
                  <Stack direction="row" alignItems="center" spacing={2}>
                    <TimelineIcon
                      sx={{
                        fontSize: 32,
                        color: theme.palette.success.main,
                      }}
                    />
                    <Typography variant="h5" fontWeight="bold">
                      Дневная активность
                    </Typography>
                  </Stack>
                  <IconButton onClick={() => toggleSection("daily")}>
                    {expandedSections.daily ? (
                      <ExpandLessIcon />
                    ) : (
                      <ExpandMoreIcon />
                    )}
                  </IconButton>
                </Box>

                <Fade in={expandedSections.daily} timeout={500}>
                  <Box>
                    <Grid container spacing={2}>
                      {data.daily_stats_array.map((day, index) => (
                        <Grid item xs={6} sm={4} md={3} key={day.date}>
                          <Card
                            sx={{
                              height: "100%",
                              position: "relative",
                              overflow: "hidden",
                              bgcolor:
                                day.date === longestDay.date
                                  ? `${theme.palette.warning.main}15`
                                  : theme.palette.background.paper,
                              border:
                                day.date === longestDay.date
                                  ? `2px solid ${theme.palette.warning.main}`
                                  : `1px solid ${theme.palette.divider}`,
                              transition: "all 0.3s ease",
                              "&:hover": {
                                transform: "translateY(-4px)",
                                boxShadow: theme.shadows[8],
                              },
                            }}
                          >
                            <CardContent>
                              <Typography
                                variant="caption"
                                color="text.secondary"
                              >
                                {new Date(day.date).toLocaleDateString(
                                  "ru-RU",
                                  {
                                    day: "numeric",
                                    month: "short",
                                  }
                                )}
                              </Typography>
                              <Typography
                                variant="h6"
                                fontWeight="bold"
                                sx={{ mt: 1 }}
                              >
                                {day.episodes}
                              </Typography>
                              <Typography
                                variant="caption"
                                color="text.secondary"
                              >
                                выпусков
                              </Typography>
                              <Divider sx={{ my: 1 }} />
                              <Typography variant="body2">
                                {formatDuration(day.duration)}
                              </Typography>
                              {day.date === longestDay.date && (
                                <Tooltip title="Самый активный день">
                                  <HotIcon
                                    sx={{
                                      position: "absolute",
                                      top: 8,
                                      right: 8,
                                      color: theme.palette.warning.main,
                                      fontSize: 16,
                                    }}
                                  />
                                </Tooltip>
                              )}
                            </CardContent>
                          </Card>
                        </Grid>
                      ))}
                    </Grid>
                  </Box>
                </Fade>
              </Paper>
            </Grid>

            <Grid item xs={12} md={4}>
              <Paper
                elevation={0}
                sx={{
                  p: 3,
                  height: "100%",
                  borderRadius: 4,
                  background: `linear-gradient(145deg, ${theme.palette.background.paper}, ${theme.palette.background.default})`,
                  border: `1px solid ${theme.palette.divider}`,
                }}
              >
                <Stack
                  direction="row"
                  alignItems="center"
                  spacing={2}
                  sx={{ mb: 3 }}
                >
                  <BrainIcon
                    sx={{
                      fontSize: 32,
                      color: theme.palette.info.main,
                    }}
                  />
                  <Typography variant="h5" fontWeight="bold">
                    Время суток
                  </Typography>
                </Stack>

                <Box sx={{ position: "relative" }}>
                  {data.time_stats_array.map((time, index) => (
                    <Box key={time.slot} sx={{ mb: 3 }}>
                      <Stack
                        direction="row"
                        justifyContent="space-between"
                        alignItems="center"
                        sx={{ mb: 1 }}
                      >
                        <Typography variant="body1" fontWeight="500">
                          {time.slot}
                        </Typography>
                        <Typography variant="body1" fontWeight="bold">
                          {time.episodes}
                        </Typography>
                      </Stack>
                      <LinearProgress
                        variant="determinate"
                        value={time.percentage_of_total}
                        sx={{
                          height: 12,
                          borderRadius: 6,
                          bgcolor: `${theme.palette.primary.main}20`,
                          "& .MuiLinearProgress-bar": {
                            bgcolor: [
                              theme.palette.primary.main,
                              theme.palette.success.main,
                              theme.palette.warning.main,
                              theme.palette.info.main,
                            ][index],
                            borderRadius: 6,
                            transition: "transform 1.5s ease-in-out",
                            transitionDelay: `${index * 0.2}s`,
                          },
                        }}
                      />
                    </Box>
                  ))}
                </Box>
              </Paper>
            </Grid>
          </Grid>

          {/* Топ выпусков */}
          <Paper
            elevation={0}
            sx={{
              p: 3,
              borderRadius: 4,
              background: `linear-gradient(145deg, ${theme.palette.background.paper}, ${theme.palette.background.default})`,
              border: `1px solid ${theme.palette.divider}`,
            }}
          >
            <Box
              sx={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                mb: 3,
              }}
            >
              <Stack direction="row" alignItems="center" spacing={2}>
                <ChartIcon
                  sx={{
                    fontSize: 32,
                    color: theme.palette.primary.main,
                  }}
                />
                <Typography variant="h5" fontWeight="bold">
                  Топ выпусков
                </Typography>
              </Stack>
              <Stack direction="row" spacing={1}>
                <Chip
                  icon={<SparkleIcon />}
                  label="Самые длинные"
                  color="primary"
                  variant="outlined"
                />
                <Chip
                  label={`Средняя длина: ${data.average_duration_per_episode_readable}`}
                  size="small"
                />
              </Stack>
            </Box>

            <Grid container spacing={3}>
              <Grid item xs={12} md={6}>
                <Typography
                  variant="h6"
                  fontWeight="600"
                  color="success.main"
                  sx={{ mb: 2 }}
                >
                  🏆 Самые длинные
                </Typography>
                <Stack spacing={2}>
                  {data.episode_stats.longest_episodes.map((episode, index) => (
                    <Card
                      key={episode.number}
                      sx={{
                        position: "relative",
                        overflow: "hidden",
                        borderLeft: `4px solid ${theme.palette.success.main}`,
                        transition: "all 0.3s ease",
                        "&:hover": {
                          transform: "translateX(4px)",
                        },
                      }}
                    >
                      <CardContent>
                        <Stack
                          direction="row"
                          justifyContent="space-between"
                          alignItems="flex-start"
                        >
                          <Box>
                            <Typography variant="body2" color="text.secondary">
                              #{episode.number} • {episode.game}
                            </Typography>
                            <Typography variant="h6" fontWeight="600">
                              {episode.title}
                            </Typography>
                          </Box>
                          <Chip
                            label={episode.duration_readable}
                            color="success"
                            size="small"
                            sx={{ fontWeight: "bold" }}
                          />
                        </Stack>
                        <Typography
                          variant="caption"
                          color="text.secondary"
                          sx={{ mt: 1, display: "block" }}
                        >
                          {new Date(episode.published_at).toLocaleDateString(
                            "ru-RU",
                            {
                              day: "numeric",
                              month: "long",
                              hour: "2-digit",
                              minute: "2-digit",
                            }
                          )}
                        </Typography>
                      </CardContent>
                    </Card>
                  ))}
                </Stack>
              </Grid>

              <Grid item xs={12} md={6}>
                <Typography
                  variant="h6"
                  fontWeight="600"
                  color="warning.main"
                  sx={{ mb: 2 }}
                >
                  ⚡ Самые короткие
                </Typography>
                <Stack spacing={2}>
                  {data.episode_stats.shortest_episodes.map(
                    (episode, index) => (
                      <Card
                        key={episode.number}
                        sx={{
                          position: "relative",
                          overflow: "hidden",
                          borderLeft: `4px solid ${theme.palette.warning.main}`,
                          transition: "all 0.3s ease",
                          "&:hover": {
                            transform: "translateX(4px)",
                          },
                        }}
                      >
                        <CardContent>
                          <Stack
                            direction="row"
                            justifyContent="space-between"
                            alignItems="flex-start"
                          >
                            <Box>
                              <Typography
                                variant="body2"
                                color="text.secondary"
                              >
                                #{episode.number} • {episode.game}
                              </Typography>
                              <Typography variant="h6" fontWeight="600">
                                {episode.title}
                              </Typography>
                            </Box>
                            <Chip
                              label={episode.duration_readable}
                              color="warning"
                              size="small"
                              sx={{ fontWeight: "bold" }}
                            />
                          </Stack>
                          <Typography
                            variant="caption"
                            color="text.secondary"
                            sx={{ mt: 1, display: "block" }}
                          >
                            {new Date(episode.published_at).toLocaleDateString(
                              "ru-RU",
                              {
                                day: "numeric",
                                month: "long",
                                hour: "2-digit",
                                minute: "2-digit",
                              }
                            )}
                          </Typography>
                        </CardContent>
                      </Card>
                    )
                  )}
                </Stack>
              </Grid>
            </Grid>
          </Paper>

          {/* Футер */}
          <Box
            sx={{
              mt: 6,
              pt: 3,
              textAlign: "center",
              borderTop: `1px solid ${theme.palette.divider}`,
            }}
          >
            <Typography variant="body2" color="text.secondary">
              📊 Обработано {data.processing_info.total_sessions_processed}{" "}
              сессий за {data.processing_info.duration_seconds} секунд
            </Typography>
            <Typography
              variant="caption"
              color="text.secondary"
              sx={{ display: "block", mt: 1 }}
            >
              Создано с ❤️ • {new Date().getFullYear()}
            </Typography>
          </Box>
        </Container>
      </Fade>
    </Box>
  );
};

export default Recap;
