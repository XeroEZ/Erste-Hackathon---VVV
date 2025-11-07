/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/**/*.{js,jsx,ts,tsx}", "./components/**/*.{js,jsx,ts,tsx}"],
  presets: [require("nativewind/preset")],
  theme: {
    extend: {
      colors: {
        primary: "#1E40AF",
        secondary: "#FBBF24",
        textSecondary: "#8D8D8D",
        iconTint: "#E3E3E3",
        warning: "#EE1212",
        box: "#5E5E5E",
        stroke: "#898989",
        card:{
          blue:"#4761E4",
          red:"#F06161",
          green:"#35B980",
          pink:"#C53CC3"
        }
      },
    },
  },
  plugins: [],
}

