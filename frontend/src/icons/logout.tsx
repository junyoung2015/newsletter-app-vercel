import { IconSvgProps } from "@/types/icons";

export const LogoutIcon = ({
  size = 24,
  strokeWidth = 1.5,
  width,
  height,
  ...props
}: IconSvgProps) => (
  <svg
    height={size || height}
    width={size || width}
    viewBox="0 0 24 24"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    {...props}
  >
    <path
      d="M8.8999 7.56023C9.2099 3.96023 11.0599 2.49023 15.1099 2.49023H15.2399C19.7099 2.49023 21.4999 4.28023 21.4999 8.75023V15.2702C21.4999 19.7402 19.7099 21.5302 15.2399 21.5302H15.1099C11.0899 21.5302 9.2399 20.0802 8.9099 16.5402"
      stroke="currentColor"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
    <path
      d="M15.0001 12H3.62012"
      stroke="currentColor"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
    <path
      d="M5.85 8.65039L2.5 12.0004L5.85 15.3504"
      stroke="currentColor"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  </svg>
);
