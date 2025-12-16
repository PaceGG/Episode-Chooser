import { createTheme } from "@mui/material";
import { ThemeOptions } from "@mui/material/styles";

const basePalette = {
  primary: {
    main: "#0b79d0",
  },
};

const baseTheme: ThemeOptions = {
  cssVariables: true,
  typography: {
    fontFamily: `var(--font-chalet), "Helvetica", "Arial", sans-serif`,
  },
  palette: {
    primary: {
      main: "#0b79d0",
    },
  },
};

export const lightTheme = createTheme({
  ...baseTheme,
  palette: {
    ...basePalette,
    mode: "light",
    text: {
      primary: "#151515",
    },
  },
});

export const darkTheme = createTheme({
  ...baseTheme,
  palette: {
    ...basePalette,
    mode: "dark",
  },
});
