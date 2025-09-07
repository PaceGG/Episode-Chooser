import { useEffect, useState } from "react";

function formatDateLocal(date) {
  // Дата в формате YYYY-MM-DD с учётом локального времени
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

const ContributionGraph = () => {
  const [sessions, setSessions] = useState(null);

  useEffect(() => {
    fetch("/sessions.json")
      .then((res) => res.json())
      .then((data) => setSessions(data))
      .catch((err) => console.error("Failed to load sessions.json", err));
  }, []);

  if (!sessions) return <div>Loading...</div>;

  // === Приводим к массиву ===
  const sessionsArray = Object.values(sessions);

  // === Группировка по дням ===
  const sessionsByDay = {};
  sessionsArray.forEach((session) => {
    const date = new Date(session.datetime * 1000);
    const dateKey = formatDateLocal(date); // ✅ локальная дата
    if (!sessionsByDay[dateKey]) sessionsByDay[dateKey] = [];
    sessionsByDay[dateKey].push(session);
  });

  // === Определяем диапазон ===
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
      default:
        return "green";
    }
  };

  // === Генерация массива всех дней ===
  const days = [];
  const current = new Date(startDate);
  while (current <= endDate) {
    days.push(new Date(current));
    current.setDate(current.getDate() + 1);
  }

  // === Разбиваем на недели ===
  const weeks = [];
  let week = [];
  const firstDayOfWeek = days[0].getDay(); // 0 = Sunday
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

  const weekDays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

  // === Подписи месяцев (месяц+год) ===
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
    <div style={{ fontFamily: "sans-serif", overflowX: "auto" }}>
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
              {/* Лейблы слева */}
              {["Mon", "Wed", "Fri"].includes(dayName) ? (
                <td style={{ fontSize: 10, color: "#666" }}>{dayName[0]}</td>
              ) : (
                <td />
              )}
              {weeks.map((week, weekIndex) => {
                const day = week[dayIndex];
                if (!day) return <td key={weekIndex} />;
                const dateKey = formatDateLocal(day);
                const count = sessionsByDay[dateKey]?.length || 0;
                const tooltip = `${count} contribution${
                  count !== 1 ? "s" : ""
                } on ${day.toDateString()}`;
                return (
                  <td key={weekIndex} title={tooltip}>
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
    </div>
  );
};

export default ContributionGraph;
