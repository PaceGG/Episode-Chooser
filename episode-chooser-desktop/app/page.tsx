import { Box, Stack, Typography } from "@mui/material";
import DiskSpace from "./components/DiskSpace";
import VideoInfo from "./components/VideoInfo";
import GamesInfo from "./components/GamesInfo/GamesInfo";

export default function Home() {
  return (
    <Stack>
      <DiskSpace use={970} total={977} />
      {/* <VideoInfo onDisk={4} toDelete={3} /> */}
      <GamesInfo />
    </Stack>
  );
}
