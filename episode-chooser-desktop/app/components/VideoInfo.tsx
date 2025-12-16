import { Chip, Paper, Stack, Typography } from "@mui/material";

interface VideoCardProps {
  number: number;
  text: string;
}

function VideoCard({ number, text }: VideoCardProps) {
  return (
    <Paper
      sx={{
        display: "flex",
        alignItems: "center",
        justifyContent: "space-evenly",
        flexDirection: "column",
        flex: 1,
        width: "50%",
        height: 200,
        p: 1,
      }}
    >
      <Typography variant="h2">{number}</Typography>
      <Chip label={text} />
    </Paper>
  );
}

interface VideoInfoProps {
  onDisk: number;
  toDelete: number;
}

export default function VideoInfo({ onDisk, toDelete }: VideoInfoProps) {
  return (
    <Stack direction={"row"} minWidth={350} gap={1}>
      <VideoCard number={onDisk} text="Видео на диске" />
      <VideoCard number={toDelete} text="из них к удалению" />
    </Stack>
  );
}
