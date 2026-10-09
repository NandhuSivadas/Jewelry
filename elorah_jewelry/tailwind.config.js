module.exports = {
  content: ["./templates/**/*.html", "./apps/**/templates/**/*.html"],
  theme: {
    extend: {
      colors: {
        gold: {
          50: "#FFF9E6", 100: "#FFF0B3", 200: "#FFE066",
          300: "#FFD700", 400: "#DAA520", 500: "#B8860B",
          600: "#996515", 700: "#7A4F0E", 800: "#5C3A08",
          900: "#3D2605",
        },
        ivory: { 50: "#FFFFF0", 100: "#FEFCE8", 200: "#FDF6E3" },
        charcoal: { 800: "#1F1F1F", 900: "#0D0D0D" },
      },
      fontFamily: {
        serif: ["Playfair Display", "Georgia", "serif"],
        sans: ["Inter", "system-ui", "sans-serif"],
      },
    },
  },
  plugins: [require("@tailwindcss/forms"), require("@tailwindcss/typography")],
};
