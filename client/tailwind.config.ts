import type { Config } from "tailwindcss";

export default {
  content: ["./pages/**/*.{js,ts,jsx,tsx,mdx}", "./components/**/*.{js,ts,jsx,tsx,mdx}", "./app/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
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
      },
      animation: {
        typewriter: "typewriter 4s steps(40, end) 1s forwards",
        blink: "blink 0.8s steps(2, start) infinite",
      },
    },
  },
  plugins: [],
} satisfies Config;
