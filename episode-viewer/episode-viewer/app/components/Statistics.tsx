import StatisticsCard, { StatisticsCardProps } from "./StatisticsCard";

interface StatisticsProps {
  stats: StatisticsCardProps[];
}

export default function Statistics({ stats }: StatisticsProps) {
  return (
    <div className="flex gap-2">
      {stats.map((stat, i) => (
        <StatisticsCard
          key={i}
          Icon={stat.Icon}
          color={stat.color}
          count={stat.count}
          label={stat.label}
        />
      ))}
    </div>
  );
}
