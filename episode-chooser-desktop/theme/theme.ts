import { createTheme } from "@mui/material";

const baseTheme = createTheme({
  typography: {
    fontFamily: `var(--font-chalet), "Helvetica", "Arial", sans-serif`,
  },
});

export const lightTheme = createTheme({
  ...baseTheme,
  palette: {
    mode: "light",
  },
});

export const darkTheme = createTheme({
  ...baseTheme,
  palette: {
    mode: "dark",
  },
});
