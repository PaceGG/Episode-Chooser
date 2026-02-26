import { Box, Chip, Divider, Stack, styled } from "@mui/material";
import { useEffect, useState } from "react";
import gamesApi from "../api/gamesApi";
import { Draggable, DroppableContainer } from "./Draggable";

function SplitText({ text, T = 3 }) {
  const words = text.split(" ");
  const midIndex = Math.floor(words.length / 2);
  const hasOdd = words.length % 2 === 1;
  const midWord = hasOdd ? words[midIndex] : null;

  // Основные половины
  const firstHalf = words.slice(0, midIndex).join(" ");
  const secondHalf = words.slice(hasOdd ? midIndex + 1 : midIndex).join(" ");

  let variants = [];

  if (hasOdd) {
    // Вариант 1: среднее слово к первой половине
    const top1 = firstHalf + (firstHalf ? " " : "") + midWord;
    const bottom1 = secondHalf;
    variants.push({ top: top1, bottom: bottom1 });

    // Вариант 2: среднее слово ко второй половине
    const top2 = firstHalf;
    const bottom2 = midWord + (secondHalf ? " " : "") + secondHalf;
    variants.push({ top: top2, bottom: bottom2 });
  } else {
    variants.push({ top: firstHalf, bottom: secondHalf });
  }

  // Фильтруем по правилу: первое слово второй строки должно быть >= T
  variants = variants.filter(({ bottom }) => {
    const firstWord = bottom.split(" ")[0] || "";
    return firstWord.length >= T;
  });

  if (variants.length === 0) {
    // Если ни один вариант невалидный, возвращаем исходную строку
    return <>{text}</>;
  }

  // Выбираем вариант, где максимальная длина строки минимальна
  let best = variants[0];
  let minMaxLen = Math.max(best.top.length, best.bottom.length);

  for (let i = 1; i < variants.length; i++) {
    const v = variants[i];
    const vMaxLen = Math.max(v.top.length, v.bottom.length);
    if (vMaxLen < minMaxLen) {
      best = v;
      minMaxLen = vMaxLen;
    }
  }

  return (
    <>
      {best.top}
      <br />
      {best.bottom}
    </>
  );
}

function GameChip({ gameName, ivi, duration }) {
  return (
    <Box
      sx={{
        display: "flex",
        alignItems: "center",
        m: 0.5,
        p: 0.5,
        gap: 1.5,
        bgcolor: "#eee",
        borderRadius: 2,
        cursor: "grab",
        userSelect: "none",
      }}
    >
      <Box maxWidth={250} color={"black"}>
        <SplitText text={gameName} />
      </Box>
      <Divider orientation="vertical" sx={{ bgcolor: "#bbb", height: "70%" }} />
      <Box>
        <Box color={"#0b7bd0"}>5</Box>
        <Box color={"#11c46f"}>12:34:56</Box>
      </Box>
    </Box>
  );
}

export default function Schedule() {
  const [games, setGames] = useState([]);
  const [isDraggableReady, setIsDraggableReady] = useState(false);

  useEffect(() => {
    async function fetchData() {
      const gamesData = await gamesApi.getByStatus("none");
      if (gamesData) {
        setGames(gamesData);
        console.log(gamesData);
      }
    }

    fetchData();
  }, []);

  // Если games пустой, показываем загрузку
  if (games.length === 0) {
    return <div>Loading games...</div>;
  }

  return (
    <Draggable>
      <DroppableContainer
        id="games-column"
        title="Available Games"
        placeholder="Drop games here"
        acceptTypes={["item"]}
        columnProps={{
          sx: {
            border: "1px solid #ccc",
            borderRadius: 1,
            minWidth: 300,
            backgroundColor: "#f5f5f5",
          },
        }}
        listProps={{
          sx: {
            minHeight: 200,
            p: 1,
          },
        }}
        insertIndicatorProps={{
          sx: { bgcolor: "red", width: "100%", height: 2 },
        }}
      >
        {games.map((game) => (
          <Box key={game.id} id={`game-${game.id}`} type="item">
            <GameChip gameName={game.name} />
          </Box>
        ))}
      </DroppableContainer>
      <DroppableContainer
        id="scheduled-column"
        title="Scheduled Games"
        placeholder="Drag games here to schedule"
        insertIndicatorProps={{
          sx: { bgcolor: "red", width: "100%", height: 2 },
        }}
      />
    </Draggable>
  );
}
