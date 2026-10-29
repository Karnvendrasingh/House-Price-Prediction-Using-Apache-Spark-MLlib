import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#0A0F1D",
        foreground: "#DEE2F6",
        surface: {
          lowest: "#090E1C",
          low: "#0E1321",
          DEFAULT: "#111827",
          high: "#1E293B",
          highest: "#252A39",
          border: "rgba(255, 255, 255, 0.08)",
          "border-hover": "rgba(6, 182, 212, 0.3)",
        },
        cyber: {
          cyan: "#06B6D4",
          sky: "#38BDF8",
          violet: "#8B5CF6",
          purple: "#A855F7",
          emerald: "#10B981",
          amber: "#F59E0B",
          rose: "#F43F5E",
        },
      },
      fontFamily: {
        sans: ["var(--font-inter)", "system-ui", "sans-serif"],
        mono: ["var(--font-jetbrains)", "monospace"],
      },
      boxShadow: {
        "cyan-glow": "0 0 20px rgba(6, 182, 212, 0.25)",
        "violet-glow": "0 0 20px rgba(139, 92, 246, 0.25)",
        "card-glow": "0 8px 32px -4px rgba(0, 0, 0, 0.6)",
      },
      animation: {
        "pulse-slow": "pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite",
        "glow-slow": "glow 4s ease-in-out infinite alternate",
      },
      keyframes: {
        glow: {
          "0%": { opacity: "0.4" },
          "100%": { opacity: "0.8" },
        },
      },
    },
  },
  plugins: [],
};

export default config;

