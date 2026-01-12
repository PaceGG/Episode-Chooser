import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/steam": {
        target: "https://store.steampowered.com",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/steam/, ""),
      },
    },
  },
});
