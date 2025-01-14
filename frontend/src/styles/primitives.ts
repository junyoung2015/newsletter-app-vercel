import { tv } from "tailwind-variants";

export const title = tv({
  base: "tracking-tight inline font-semibold",
  variants: {
    size: {
      xs: "text-2xl lg:text-3xl",
      sm: "text-3xl lg:text-4xl",
      md: "text-[2.5rem] lg:text-5xl",
      lg: "text-4xl lg:text-6xl",
      xl: "text-5xl md:text-6xl lg:text-7xl",
    },
    fullWidth: {
      true: "w-full block",
    },
  },
  defaultVariants: {
    size: "md",
  },
});

export const subtitle = tv({
  base: "w-full md:w-1/2 my-2 text-lg lg:text-xl font-normal text-default-500 block max-w-full",
  variants: {
    fullWidth: {
      true: "!w-full",
    },
  },
});
