import localFont from "next/font/local";

export const chalet = localFont({
  src: [
    {
      path: "../../public/fonts/Chalet.otf",
      weight: "400",
      style: "normal",
    },
  ],
  variable: "--font-chalet",
});
