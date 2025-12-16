import { Box, Typography } from "@mui/material";
import DiskSpace from "./components/DiskSpace";

export default function Home() {
  return (
    <Box>
      <DiskSpace use={900} total={977} />
    </Box>
  );
}
