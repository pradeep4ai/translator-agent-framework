/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        duo: {
          green: "#58CC02",
          greenDark: "#46A302",
          blue: "#1CB0F6",
          gold: "#FFC800",
          slate: "#3C3C3C",
          bg: "#FFFFFF",
          panel: "#F7F7F7",
        },
      },
      fontFamily: {
        sans: ["Nunito", "system-ui", "sans-serif"],
      },
    },
  },
  plugins: [],
};
