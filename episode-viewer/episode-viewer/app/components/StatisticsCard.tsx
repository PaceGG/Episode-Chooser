export interface StatisticsCardProps {
  Icon: React.ComponentType<{ color?: string; size?: number }>;
  label: string;
  count: string | number;
  color: string;
}

export default function StatisticsCard({
  Icon,
  label,
  count,
  color,
}: StatisticsCardProps) {
  return (
    <div
      className={`flex flex-col items-center flex-1 gap-3 py-2 border-2 rounded-xl`}
      style={{ borderColor: color, color: color }}
    >
      <Icon color={color} size={50} />
      <div className="text-xs uppercase">{label}</div>
      <div className="text-base font-bold">{count}</div>
    </div>
  );
}
