import { createTheme } from "@mui/material";

const basePalette = {
  primary: {
    main: "#0b79d0",
  },
};

const baseTheme = {
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
  },
});

export const darkTheme = createTheme({
  ...baseTheme,
  palette: {
    ...basePalette,
    mode: "dark",
  },
});
