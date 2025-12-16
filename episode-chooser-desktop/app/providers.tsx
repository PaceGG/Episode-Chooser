"use client";

import { ThemeProvider, CssBaseline } from "@mui/material";
import { lightTheme, darkTheme } from "@/theme/theme";
import { useState, createContext, useContext } from "react";

type ThemeMode = "light" | "dark";

const ThemeContext = createContext({
  mode: "light" as ThemeMode,
  toggleTheme: () => {},
});

export const useThemeContext = () => useContext(ThemeContext);

export default function Providers({ children }: { children: React.ReactNode }) {
  const [mode, setMode] = useState<ThemeMode>("dark");

  const toggleTheme = () => {
    setMode((prevMode) => (prevMode === "light" ? "dark" : "light"));
  };

  const theme = mode === "light" ? lightTheme : darkTheme;

  return (
    <ThemeContext.Provider value={{ mode, toggleTheme }}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        {children}
      </ThemeProvider>
    </ThemeContext.Provider>
  );
}
