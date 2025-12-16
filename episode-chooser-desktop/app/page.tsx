import { Box, Typography } from "@mui/material";
import DiskSpace from "./components/DiskSpace";

export default function Home() {
  return (
    <Box>
      <DiskSpace use={970} total={977} />
    </Box>
  );
}
