import { Card, Row, Col, ProgressBar, ListGroup, Badge } from "react-bootstrap";
import "./MonthlyStats.css"; // Стили ниже

const MonthlyStats = ({ data }) => {
  // Форматирование секунд в читаемый вид
  const formatSeconds = (seconds) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;

    if (hours > 0) {
      return `${hours}ч ${minutes}м`;
    }
    return `${minutes}м ${secs}с`;
  };

  // Форматирование даты
  const formatDate = (dateStr) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString("ru-RU", {
      day: "numeric",
      month: "long",
      year: "numeric",
    });
  };

  // Форматирование времени публикации
  const formatTime = (dateStr) => {
    const date = new Date(dateStr);
    return date.toLocaleTimeString("ru-RU", {
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  if (!data) {
    return <div>Загрузка данных...</div>;
  }

  return (
    <div className="monthly-stats">
      {/* Заголовок месяца */}
      <Card className="mb-4">
        <Card.Header className="bg-primary text-white">
          <h2 className="mb-0">Статистика за {data.target_month}</h2>
        </Card.Header>
        <Card.Body>
          <Row>
            <Col md={3} sm={6}>
              <div className="stat-card">
                <h3>{data.total_sessions}</h3>
                <p>Сессий</p>
              </div>
            </Col>
            <Col md={3} sm={6}>
              <div className="stat-card">
                <h3>{data.total_episodes}</h3>
                <p>Эпизодов</p>
              </div>
            </Col>
            <Col md={3} sm={6}>
              <div className="stat-card">
                <h3>{data.games_count || Object.keys(data.games).length}</h3>
                <p>Игр</p>
              </div>
            </Col>
            <Col md={3} sm={6}>
              <div className="stat-card">
                <h3>
                  {data.total_duration_readable ||
                    formatSeconds(data.total_duration)}
                </h3>
                <p>Общее время</p>
              </div>
            </Col>
          </Row>
        </Card.Body>
      </Card>

      {/* Статистика по играм */}
      <Card className="mb-4">
        <Card.Header>
          <h4>Статистика по играм</h4>
        </Card.Header>
        <Card.Body>
          <Row>
            {Object.entries(data.games).map(([gameName, game]) => (
              <Col lg={6} key={gameName} className="mb-4">
                <Card className="h-100 game-card">
                  <Card.Header>
                    <h5>{gameName}</h5>
                  </Card.Header>
                  <Card.Body>
                    <div className="game-stats">
                      <div className="d-flex justify-content-between mb-2">
                        <span>Сессии:</span>
                        <Badge bg="info">{game.session_count}</Badge>
                      </div>
                      <div className="d-flex justify-content-between mb-2">
                        <span>Эпизоды:</span>
                        <Badge bg="success">{game.episode_count}</Badge>
                      </div>
                      <div className="d-flex justify-content-between mb-2">
                        <span>Общее время:</span>
                        <Badge bg="primary">
                          {game.total_duration_readable}
                        </Badge>
                      </div>
                      <div className="mb-3">
                        <div className="d-flex justify-content-between mb-1">
                          <small>Процент от общего времени:</small>
                          <small>{game.percentage_of_total_duration}%</small>
                        </div>
                        <ProgressBar
                          now={game.percentage_of_total_duration}
                          label={`${game.percentage_of_total_duration}%`}
                        />
                      </div>
                      <div className="episodes-list">
                        <h6>Последние эпизоды:</h6>
                        <ListGroup variant="flush">
                          {game.episodes.slice(-3).map((episode, index) => (
                            <ListGroup.Item key={index} className="py-2">
                              <div className="d-flex justify-content-between">
                                <strong>#{episode.number}</strong>
                                <small>
                                  {formatDate(episode.published_at)}
                                </small>
                              </div>
                              <div className="text-muted">{episode.title}</div>
                              <div className="d-flex justify-content-between">
                                <small>
                                  {formatTime(episode.published_at)}
                                </small>
                                <small>
                                  {episode.duration_readable ||
                                    formatSeconds(episode.duration)}
                                </small>
                              </div>
                            </ListGroup.Item>
                          ))}
                        </ListGroup>
                      </div>
                    </div>
                  </Card.Body>
                </Card>
              </Col>
            ))}
          </Row>
        </Card.Body>
      </Card>

      {/* Ежедневная статистика */}
      <Card className="mb-4">
        <Card.Header>
          <h4>Ежедневная статистика</h4>
        </Card.Header>
        <Card.Body>
          <div className="daily-stats">
            {data.daily_stats_array.map((day, index) => (
              <Card key={index} className="mb-3">
                <Card.Body>
                  <div className="d-flex justify-content-between align-items-center mb-2">
                    <h5 className="mb-0">{formatDate(day.date)}</h5>
                    <Badge bg="secondary">{day.episodes} эп.</Badge>
                  </div>
                  <div className="d-flex justify-content-between mb-2">
                    <span>Игры:</span>
                    <span>{day.games.join(", ")}</span>
                  </div>
                  <div className="d-flex justify-content-between mb-2">
                    <span>Общее время:</span>
                    <span>{day.duration_readable}</span>
                  </div>
                  <div className="episode-titles">
                    <small className="text-muted d-block mb-1">Эпизоды:</small>
                    {day.episode_titles.map((title, idx) => (
                      <Badge
                        key={idx}
                        bg="light"
                        text="dark"
                        className="me-1 mb-1"
                      >
                        {title}
                      </Badge>
                    ))}
                  </div>
                </Card.Body>
              </Card>
            ))}
          </div>
        </Card.Body>
      </Card>

      {/* Самые короткие и длинные эпизоды */}
      <Row className="mb-4">
        <Col md={6}>
          <Card>
            <Card.Header>
              <h5>Самые короткие эпизоды</h5>
            </Card.Header>
            <Card.Body>
              <ListGroup variant="flush">
                {data.episode_stats.shortest_episodes.map((episode, index) => (
                  <ListGroup.Item key={index}>
                    <div className="d-flex justify-content-between">
                      <strong>
                        #{episode.number} {episode.title}
                      </strong>
                      <Badge bg="warning">
                        {episode.duration_readable ||
                          formatSeconds(episode.duration)}
                      </Badge>
                    </div>
                    <div className="text-muted">
                      <small>{episode.game}</small>
                    </div>
                  </ListGroup.Item>
                ))}
              </ListGroup>
            </Card.Body>
          </Card>
        </Col>
        <Col md={6}>
          <Card>
            <Card.Header>
              <h5>Самые длинные эпизоды</h5>
            </Card.Header>
            <Card.Body>
              <ListGroup variant="flush">
                {data.episode_stats.longest_episodes.map((episode, index) => (
                  <ListGroup.Item key={index}>
                    <div className="d-flex justify-content-between">
                      <strong>
                        #{episode.number} {episode.title}
                      </strong>
                      <Badge bg="danger">
                        {episode.duration_readable ||
                          formatSeconds(episode.duration)}
                      </Badge>
                    </div>
                    <div className="text-muted">
                      <small>{episode.game}</small>
                    </div>
                  </ListGroup.Item>
                ))}
              </ListGroup>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      {/* Рейтинги игр */}
      <Card className="mb-4">
        <Card.Header>
          <h4>Рейтинги игр</h4>
        </Card.Header>
        <Card.Body>
          <Row>
            <Col md={6}>
              <h5>По количеству эпизодов</h5>
              {data.game_rankings.by_episodes.map((game, index) => (
                <div key={index} className="mb-3">
                  <div className="d-flex justify-content-between mb-1">
                    <span>{game.game}</span>
                    <span>
                      {game.episodes} эп. ({game.percentage}%)
                    </span>
                  </div>
                  <ProgressBar
                    now={game.percentage}
                    variant={index === 0 ? "success" : "info"}
                  />
                </div>
              ))}
            </Col>
            <Col md={6}>
              <h5>По времени</h5>
              {data.game_rankings.by_duration.map((game, index) => (
                <div key={index} className="mb-3">
                  <div className="d-flex justify-content-between mb-1">
                    <span>{game.game}</span>
                    <span>{game.duration_readable}</span>
                  </div>
                  <ProgressBar
                    now={(game.duration / data.total_duration) * 100}
                    variant={index === 0 ? "success" : "info"}
                  />
                </div>
              ))}
            </Col>
          </Row>
        </Card.Body>
      </Card>

      {/* Временная статистика */}
      <Card className="mb-4">
        <Card.Header>
          <h4>Время активности</h4>
        </Card.Header>
        <Card.Body>
          <Row>
            {data.time_stats_array.map((timeSlot, index) => (
              <Col md={3} sm={6} key={index} className="mb-3">
                <Card className="time-slot-card">
                  <Card.Body className="text-center">
                    <h5>{timeSlot.slot}</h5>
                    <div className="display-4">{timeSlot.episodes}</div>
                    <p className="text-muted">эпизодов</p>
                    <div>{timeSlot.duration_readable}</div>
                    <Badge bg="secondary" className="mt-2">
                      {timeSlot.percentage_of_total}%
                    </Badge>
                  </Card.Body>
                </Card>
              </Col>
            ))}
          </Row>
        </Card.Body>
      </Card>

      {/* Дополнительная статистика */}
      <Row className="mb-4">
        <Col md={4}>
          <Card className="h-100">
            <Card.Header>
              <h5>Средние значения</h5>
            </Card.Header>
            <Card.Body>
              <ListGroup variant="flush">
                <ListGroup.Item className="d-flex justify-content-between">
                  <span>Эпизодов в сессии:</span>
                  <Badge bg="info">
                    {data.average_episodes_per_session?.toFixed(1)}
                  </Badge>
                </ListGroup.Item>
                <ListGroup.Item className="d-flex justify-content-between">
                  <span>Длительность эпизода:</span>
                  <Badge bg="success">
                    {data.average_duration_per_episode_readable ||
                      formatSeconds(data.average_duration_per_episode)}
                  </Badge>
                </ListGroup.Item>
                <ListGroup.Item className="d-flex justify-content-between">
                  <span>Дней с контентом:</span>
                  <Badge bg="primary">
                    {data.completion_stats.days_with_content}
                  </Badge>
                </ListGroup.Item>
              </ListGroup>
            </Card.Body>
          </Card>
        </Col>
        <Col md={4}>
          <Card className="h-100">
            <Card.Header>
              <h5>Самый активный день</h5>
            </Card.Header>
            <Card.Body>
              <h4>{formatDate(data.completion_stats.busiest_day.date)}</h4>
              <div className="d-flex justify-content-between">
                <span>Эпизодов:</span>
                <Badge bg="danger">
                  {data.completion_stats.busiest_day.episodes}
                </Badge>
              </div>
              <div className="d-flex justify-content-between">
                <span>Время:</span>
                <span>
                  {data.completion_stats.busiest_day.duration_readable}
                </span>
              </div>
              <div className="d-flex justify-content-between">
                <span>Игр:</span>
                <Badge bg="warning">
                  {data.completion_stats.busiest_day.games_count}
                </Badge>
              </div>
            </Card.Body>
          </Card>
        </Col>
        <Col md={4}>
          <Card className="h-100">
            <Card.Header>
              <h5>Обработка данных</h5>
            </Card.Header>
            <Card.Body>
              <ListGroup variant="flush">
                <ListGroup.Item className="d-flex justify-content-between">
                  <span>Обработано сессий:</span>
                  <Badge bg="info">
                    {data.processing_info.total_sessions_processed}
                  </Badge>
                </ListGroup.Item>
                <ListGroup.Item className="d-flex justify-content-between">
                  <span>Пропущено:</span>
                  <Badge bg="secondary">
                    {data.processing_info.sessions_skipped}
                  </Badge>
                </ListGroup.Item>
                <ListGroup.Item className="d-flex justify-content-between">
                  <span>Время обработки:</span>
                  <Badge bg="success">
                    {data.processing_info.duration_seconds.toFixed(3)} с
                  </Badge>
                </ListGroup.Item>
              </ListGroup>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default MonthlyStats;
