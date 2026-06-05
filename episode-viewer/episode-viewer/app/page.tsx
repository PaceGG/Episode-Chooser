import ContributionGraph from "./components/ContributionGraph";
import Statistics from "./components/Statistics";
import StatisticsCard from "./components/StatisticsCard";
import {
  FilmIcon,
  GamepadIcon,
  TimerIcon,
  TrashIcon,
} from "./components/Icons";
import colors from "@/public/colors.json";
import data from "@/public/db.json";
import sessions from "@/public/sessions.json";
import GamesList from "./components/GamesList";

const countCompleteGames = (data) => {
  let count = 0;

  data.forEach((game) => {
    if (game.additionalGames.length === 0) {
      if (game.mainStatus === "complete") {
        count++;
      }
    } else {
      game.additionalGames.forEach((additionalGame) => {
        if (additionalGame.status === "complete") {
          count++;
        }
      });
    }
  });

  return count;
};

const countBadGames = (data) => {
  let count = 0;

  data.forEach((game) => {
    if (game.additionalGames.length === 0) {
      if (game.mainStatus === "bad") {
        count++;
      }
    } else {
      game.additionalGames.forEach((additionalGame) => {
        if (additionalGame.status === "bad") {
          count++;
        }
      });
    }
  });

  return count;
};

const countTime = (data) => {
  let time = 0;

  data.forEach((game) => {
    time += game.mainTime;
    game.additionalGames.forEach((additionalGame) => {
      time += additionalGame.time;
    });
  });

  return Math.round(time / 60 / 60);
};

const countEpisodes = (data) => {
  let count = 0;

  data.forEach((game) => {
    if (game.mainNumberOfEps !== undefined) {
      count += Number(game.mainNumberOfEps);
    }
    game.additionalGames.forEach((additionalGame) => {
      count += additionalGame.numberOfEps;
    });
  });

  return count;
};

export default function Home() {
  const stats = [
    {
      Icon: GamepadIcon,
      label: "Пройдено",
      count: countCompleteGames(data.games),
      color: colors.green,
    },
    {
      Icon: TrashIcon,
      label: "Дропнуто",
      count: countBadGames(data.games),
      color: colors.red,
    },
    {
      Icon: TimerIcon,
      label: "Часов",
      count: countTime(data.games),
      color: colors.blue,
    },
    {
      Icon: FilmIcon,
      label: "Серий",
      count: countEpisodes(data.games),
      color: colors.yellow,
    },
  ];

  return (
    <div className="flex flex-col gap-2">
      <div style={{ overflow: "auto" }}>
        <ContributionGraph />
      </div>
      <Statistics stats={stats} />
      <GamesList games={data.games} />
    </div>
  );
}
