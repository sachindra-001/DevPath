import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        "highlight-yellow": "#FDF2B3",
        "ink-primary": "#1A1F2C",
        "border-stroke": "#1A1F2C",
        "paper-bg": "#F9F7F2",
        background: "#fbf9f4",
        "accent-lavender": "#E9E4FF",
        "secondary-fixed": "#d4e3ff",
        "secondary-fixed-dim": "#a5c9fe",
        "tertiary-fixed": "#f5dfc3",
        "tertiary-fixed-dim": "#d8c4a8",
        "success-green": "#D4EDDA",
        "surface-container": "#f0eee9",
        "surface-container-high": "#eae8e3",
        "surface-container-low": "#f5f3ee",
        "surface-container-lowest": "#ffffff",
        "on-surface": "#1b1c19",
        "on-surface-variant": "#45464c",
        outline: "#76777c",
        secondary: "#3b608f",
      },
      fontFamily: {
        headline: ["var(--font-space-grotesk)", "Space Grotesk", "sans-serif"],
        body: ["var(--font-geist)", "Geist", "sans-serif"],
        mono: ["var(--font-geist)", "Geist", "monospace"],
      },
      boxShadow: {
        "editorial-sm": "2px 2px 0px 0px #1A1F2C",
        editorial: "4px 4px 0px 0px #1A1F2C",
        "editorial-lg": "8px 8px 0px 0px #1A1F2C",
      },
      maxWidth: {
        "container-max": "1280px",
      },
      spacing: {
        gutter: "24px",
        "margin-mobile": "16px",
        "margin-desktop": "48px",
      },
    },
  },
  plugins: [],
};

export default config;
