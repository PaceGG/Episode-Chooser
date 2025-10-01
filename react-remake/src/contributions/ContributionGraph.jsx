import { useEffect, useRef, useState } from "react";

function formatDateLocal(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

function formatDate(dateStr) {
  const date = new Date(dateStr);
  const options = { day: "numeric", month: "long", year: "numeric" };
  return date.toLocaleDateString("ru-RU", options);
}

const ContributionGraph = () => {
  const [sessions, setSessions] = useState(null);
  const [selectedDay, setSelectedDay] = useState(null);
  const scrollContainerRef = useRef(null);

  useEffect(() => {
    fetch("/sessions.json")
      .then((res) => res.json())
      .then((data) => setSessions(data))
      .catch((err) => console.error("Failed to load sessions.json", err));
  }, []);

  useEffect(() => {
    if (sessions && scrollContainerRef.current) {
      scrollContainerRef.current.scrollLeft =
        scrollContainerRef.current.scrollWidth;
    }
  }, [sessions]);

  if (!sessions) return <div>Loading...</div>;

  const sessionsArray = Object.values(sessions);

  const sessionsByDay = {};
  sessionsArray.forEach((session) => {
    const date = new Date(session.datetime * 1000);
    const dateKey = formatDateLocal(date);
    if (!sessionsByDay[dateKey]) sessionsByDay[dateKey] = [];
    sessionsByDay[dateKey].push(session);
  });

  const allDates = Object.keys(sessionsByDay).sort(
    (a, b) => new Date(a) - new Date(b)
  );

  const startDate = new Date(allDates[0]);
  const endDate = new Date(allDates[allDates.length - 1]);

  const getColor = (count) => {
    switch (count) {
      case 0:
        return "#0b7bd028";
      case 1:
        return "#0b7bd071";
      case 2:
        return "#0b7bd0bb";
      case 3:
        return "#0b7bd0ff";
      case 4:
        return "#ee204d";
      case 5:
        return "#ee20ccff";
      case 6:
      case 7:
        return "#eeff00ff";

      default:
        return "black";
    }
  };

  const days = [];
  const current = new Date(startDate);
  while (current <= endDate) {
    days.push(new Date(current));
    current.setDate(current.getDate() + 1);
  }

  const weeks = [];
  let week = [];
  const firstDayOfWeek = (days[0].getDay() + 6) % 7;
  for (let i = 0; i < firstDayOfWeek; i++) week.push(null);
  days.forEach((day) => {
    week.push(day);
    if (week.length === 7) {
      weeks.push(week);
      week = [];
    }
  });
  if (week.length) {
    while (week.length < 7) week.push(null);
    weeks.push(week);
  }

  const weekDays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

  const monthLabels = [];
  const monthPositions = [];
  weeks.forEach((week, weekIndex) => {
    week.forEach((day) => {
      if (!day) return;
      const month = day.toLocaleString("default", { month: "short" });
      const key = `${month}-${day.getFullYear()}`;
      if (!monthLabels.includes(key)) {
        monthLabels.push(key);
        monthPositions.push(weekIndex);
      }
    });
  });

  return (
    <div
      style={{ fontFamily: "sans-serif", overflowX: "auto" }}
      ref={scrollContainerRef}
    >
      <table style={{ borderSpacing: "2px" }}>
        <thead>
          <tr>
            <th />
            {monthLabels.map((monthKey, index) => {
              const [month] = monthKey.split("-");
              const start = monthPositions[index];
              const end = monthPositions[index + 1] || weeks.length;
              const colSpan = end - start;
              return (
                <th
                  key={monthKey}
                  colSpan={colSpan}
                  style={{ textAlign: "left", fontSize: 12 }}
                >
                  {month}
                </th>
              );
            })}
          </tr>
        </thead>
        <tbody>
          {weekDays.map((dayName, dayIndex) => (
            <tr key={dayName}>
              {weekDays.includes(dayName) ? (
                <td
                  style={{
                    fontSize: 10,
                    color: ["Mon", "Wed", "Fri", "Sun"].includes(dayName)
                      ? "#666"
                      : "transparent",
                    position: "sticky",
                    left: 0,
                    zIndex: 2,
                    backgroundColor: "#222",
                    textAlign: "center",
                  }}
                >
                  {dayName[0]}
                </td>
              ) : (
                <td />
              )}
              {weeks.map((week, weekIndex) => {
                const day = week[dayIndex];
                if (!day) return <td key={weekIndex} />;
                const dateKey = formatDateLocal(day);
                const count = sessionsByDay[dateKey]?.length || 0;
                return (
                  <td
                    key={weekIndex}
                    onClick={() => count > 0 && setSelectedDay(dateKey)}
                    style={{ cursor: count > 0 ? "pointer" : "default" }}
                    title={`${count} sessions on ${formatDate(
                      formatDateLocal(day)
                    )}`}
                  >
                    <div
                      style={{
                        width: 12,
                        height: 12,
                        backgroundColor: getColor(count),
                        borderRadius: 3,
                      }}
                    />
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>

      {selectedDay && (
        <div
          onClick={() => setSelectedDay(null)}
          style={{
            position: "fixed",
            top: 0,
            left: 0,
            width: "100%",
            height: "100%",
            backgroundColor: "rgba(0,0,0,0.5)",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            zIndex: 1000,
          }}
        >
          <div
            onClick={(e) => e.stopPropagation()}
            style={{
              backgroundColor: "#333",
              padding: 20,
              borderRadius: 8,
              minWidth: 300,
              maxHeight: "80%",
              overflowY: "auto",
            }}
          >
            <h3>Sessions on {formatDate(selectedDay)}</h3>
            <ul>
              {sessionsByDay[selectedDay].map((session, i) => (
                <li key={i}>
                  <strong>{session.game}</strong>
                  <ul>
                    {session.episodes.map((ep, j) => (
                      <li key={j} style={{ marginBottom: 8, marker: "none" }}>
                        <details style={{ cursor: "pointer" }}>
                          <summary>
                            {ep.number}.{" "}
                            {ep.title.split("•")[0].trim() || "(No title)"}
                          </summary>
                          <p
                            style={{
                              whiteSpace: "pre-line",
                              marginLeft: 40,
                              marginTop: 0,
                              marginBottom: 0,
                            }}
                          >
                            {ep.description || "(No description)"}
                          </p>
                        </details>
                      </li>
                    ))}
                  </ul>
                </li>
              ))}
            </ul>
            <button
              onClick={() => setSelectedDay(null)}
              style={{ marginTop: 10 }}
            >
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ContributionGraph;
