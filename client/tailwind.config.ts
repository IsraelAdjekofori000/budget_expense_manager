import type { Config } from "tailwindcss";

export default {
  content: ["./pages/**/*.{js,ts,jsx,tsx,mdx}", "./components/**/*.{js,ts,jsx,tsx,mdx}", "./app/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
        projOrange: "#ff7b00",
      },
      keyframes: {
        typewriter: {
          "0%": { width: "0%" },
          "100%": { width: "100%" },
        },
        blink: {
          "0%": { color: "black" },
          "100%": { color: "transparent" },
        },
        shake: {
          "0%": { transform: "translateX(0)" },
          " 25%": { transform: "translateX(-5px)" },
          " 50%": { transform: "translateX(5px)" },
          " 75%": { transform: "translateX(-5px)" },
          "100%": { transform: "translateX(0) " },
        },
      },
      animation: {
        typewriter: "typewriter 4s steps(40, end) 1s forwards",
        blink: "blink 0.8s steps(2, start) infinite",
        shake: "shake 0.5s ease-in-out",
      },
    },
  },
  plugins: [],
} satisfies Config;
