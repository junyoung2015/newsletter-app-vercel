import { nextui } from "@nextui-org/theme/plugin";
import path from "path";
import type { Config } from "tailwindcss";

const nexUiThemePath = path.dirname(require.resolve("@nextui-org/theme"));

export default {
  content: [
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/styles/**/*.{js,ts,jsx,tsx,mdx}",
    `${nexUiThemePath}/**/*.{js,ts,jsx,tsx}`,
  ],
  theme: {
    extend: {},
  },
  darkMode: "class",
  plugins: [
    nextui({
      addCommonColors: true,
      themes: {
        dark: {
          colors: {
            background: "#2D3034",
          },
        },
      },
    }),
  ],
} satisfies Config;
