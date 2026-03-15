import { Box, Button, IconButton, Skeleton, TextField } from "@mui/material";
import { useEffect, useState } from "react";
import ReplayIcon from "@mui/icons-material/Replay";

interface InputFormProps {
  label: string;
  value: string;
  isLoading?: boolean;
  onReload: () => void;
  onConfirm: (text: string, regionName: string) => void;
}

export default function InputForm({
  label,
  value,
  isLoading = true,
  onReload,
  onConfirm,
}: InputFormProps) {
  const [text, setText] = useState("");
  const [regionName, setRegionName] = useState("Region Name");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const savedRegion = localStorage.getItem("region");
    if (savedRegion) setRegionName(savedRegion);
  }, []);

  useEffect(() => {
    setText(value);
  }, [value]);

  useEffect(() => {
    setLoading(isLoading);
  }, [isLoading]);

  const confirm = () => {
    localStorage.setItem("region", regionName);
    onConfirm(text, regionName);
  };

  const reload = () => {
    onReload();
  };

  const copy = () => {
    navigator.clipboard.writeText(text);
  };

  return (
    <Box mt={1} display={"flex"} flexDirection={"column"}>
      <Box display={"flex"} flexDirection={"column"} gap={2}>
        <TextField
          label="RegionName"
          value={regionName}
          required
          onChange={(e) => setRegionName(e.target.value)}
        />
        <Box display={"flex"} alignItems={"start"}>
          <IconButton onClick={reload}>
            <ReplayIcon />
          </IconButton>
          {loading ? (
            <Skeleton
              component={Box}
              height={59}
              width={"100%"}
              sx={{ transform: "none" }}
            />
          ) : (
            <Box flex={1}>
              <TextField
                label={label}
                multiline
                fullWidth
                value={text}
                onChange={(e) => setText(e.target.value)}
              />
            </Box>
          )}
        </Box>
      </Box>
      <Box>
        <Button onClick={confirm} variant="contained">
          Конвертировать
        </Button>
        <Button onClick={copy}>Копировать</Button>
      </Box>
    </Box>
  );
}
