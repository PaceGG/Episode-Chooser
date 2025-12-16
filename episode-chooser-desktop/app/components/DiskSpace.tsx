import { LinearProgress, Paper, Typography } from "@mui/material";

interface DiskSpaceProps {
  use: number;
  total: number;
  averageVideoSize?: number;
}

export default function DiskSpace({
  use,
  total,
  averageVideoSize = 40,
}: DiskSpaceProps) {
  const value = (use / total) * 100;
  const remaining = total - use;
  const videoCount = Math.floor(remaining / averageVideoSize);

  return (
    <Paper sx={{ p: 1 }}>
      <Typography>Место на диске: {remaining} GB</Typography>
      <LinearProgress
        variant="determinate"
        color={remaining > 100 ? "primary" : "error"}
        value={value}
        sx={{
          borderRadius: 1,
        }}
      />
      <Typography sx={{ textAlign: "right" }}>~ {videoCount} видео</Typography>
    </Paper>
  );
}
